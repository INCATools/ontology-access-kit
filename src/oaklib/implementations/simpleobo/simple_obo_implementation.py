import logging
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import sssom_schema as sssom
from kgcl_schema.datamodel import kgcl

from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import (
    Edge,
    ExistentialRestrictionExpression,
    Graph,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    IS_A,
    LABEL_PREDICATE,
    SEMAPV,
    SKOS_CLOSE_MATCH,
)
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_COMMENT,
    TAG_DEFINITION,
    TAG_EQUIVALENT_TO,
    TAG_IS_A,
    TAG_NAME,
    TAG_OBSOLETE,
    TAG_RELATIONSHIP,
    TAG_SUBSET,
    TAG_SUBSETDEF,
    TAG_SYNONYM,
    TAG_XREF,
    OboDocument,
    Stanza,
    _synonym_scope_pred,
    parse_obo_document,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.basic_utils import pairs_as_dict


def _is_isa(x: str):
    return x == IS_A or x.lower() == "is_a" or x.lower() == "isa"


@dataclass
class SimpleOboImplementation(
    ValidatorInterface,
    DifferInterface,
    RdfInterface,
    OboGraphInterface,
    SearchInterface,
    MappingProviderInterface,
    PatcherInterface,
):
    """
    Simple OBO-file backed implementation

    This implementation is incomplete and is intended primarily as a Patcher implementation

    This can be abandoned when pronto is less strict
    """

    obo_document: OboDocument = None
    _relationship_index_cache: Dict[CURIE, List[RELATIONSHIP]] = None

    def __post_init__(self):
        if self.obo_document is None:
            resource = self.resource
            if resource and resource.local_path:
                self.obo_document = parse_obo_document(resource.local_path)
            else:
                self.obo_document = OboDocument()

    def store(self, resource: OntologyResource = None) -> None:
        if resource is None:
            resource = self.resource
        od = self.obo_document
        if resource.local:
            if resource.slug:
                with open(str(resource.local_path), "w", encoding="UTF-8") as f:
                    od.dump(f)
            else:
                od.dump(sys.stdout.buffer)
        else:
            raise NotImplementedError(f"Cannot dump to {resource}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        logging.info("Commencing indexing")
        n = 0
        for s in self.entities(filter_obsoletes=False):
            t = self._stanza(s)
            for v in t.simple_values(TAG_IS_A):
                n += 1
                yield s, IS_A, v
            for v in t.simple_values(TAG_EQUIVALENT_TO):
                n += 1
                yield s, EQUIVALENT_CLASS, v
                yield v, EQUIVALENT_CLASS, s
            for p, v in t.pair_values(TAG_RELATIONSHIP):
                yield s, self._get_relationship_type_curie(p), v
            # for p, v in t.intersection_of_tuples():
            #    n += 1
            #    yield s, self._get_relationship_type_curie(p), v
        logging.info(f"Indexed {n} relationships")

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        od = self.obo_document
        for s_id in od.stanzas.keys():
            yield s_id

    def obsoletes(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas.values():
            if s.get_boolean_value(TAG_OBSOLETE):
                yield s.id

    def subsets(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.header.simple_values(TAG_SUBSETDEF):
            yield s

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas.values():
            if subset in s.simple_values(TAG_SUBSET):
                yield s.id

    def _stanza(self, curie: CURIE, strict=True) -> Optional[Stanza]:
        stanza = self.obo_document.stanzas.get(curie, None)
        if strict and not stanza:
            raise ValueError(f"No such stanza {curie}")
        return stanza

    def label(self, curie: CURIE) -> Optional[str]:
        s = self._stanza(curie, False)
        if s:
            return s.singular_value(TAG_NAME)
        else:
            if curie == IS_A:
                return "subClassOf"
            else:
                return None

    def set_label(self, curie: CURIE, label: str) -> bool:
        s = self._stanza(curie, False)
        s.set_singular_tag(TAG_NAME, label)

    def curies_by_label(self, label: str) -> List[CURIE]:
        return [
            s.id
            for s in self.obo_document.stanzas.values()
            if s.singular_value(TAG_NAME, False) == label
        ]

    def _lookup(self, label_or_curie: str) -> CURIE:
        if ":" in label_or_curie and " " not in label_or_curie:
            return label_or_curie
        else:
            candidates = self.curies_by_label(label_or_curie)
            if len(candidates) != 1:
                raise ValueError(f"{label_or_curie} => {candidates}")
            return candidates[0]

    def create_entity(
        self,
        curie: CURIE,
        label: Optional[str] = None,
        relationships: Optional[RELATIONSHIP_MAP] = None,
        type: Optional[str] = None,
    ) -> CURIE:
        stanza = Stanza(id=curie, type=type)
        stanza.add_tag_value(TAG_NAME, label)
        self.obo_document.add_stanza(stanza)

    def definition(self, curie: CURIE) -> Optional[str]:
        s = self._stanza(curie)
        return s.quoted_value(TAG_DEFINITION)

    def comments(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        for curie in curies:
            s = self._stanza(curie)
            if s:
                yield curie, s.singular_value(TAG_COMMENT)

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        s = self._stanza(curie)
        if s is None:
            return {}
        m = defaultdict(list)
        lbl = self.label(curie)
        if lbl:
            m[LABEL_PREDICATE] = [lbl]
        for st in s.synonyms():
            syn, pred, _type, _xrefs = st
            pred = _synonym_scope_pred(pred)
            m[pred].append(syn)
        return m

    def _get_relationship_type_curie(self, rel_type: str) -> PRED_CURIE:
        for _, x in self.simple_mappings_by_curie(rel_type):
            if x.startswith("BFO:") or x.startswith("RO:"):
                return x
        return rel_type

    def _get_relationship_type_shorthand(self, rel_type: PRED_CURIE) -> str:
        for _, x in self.simple_mappings_by_curie(rel_type):
            return x
        return rel_type

    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        for s in self._relationship_index.keys():
            if subjects is not None and s not in subjects:
                continue
            for s2, p, o in self._relationship_index[s]:
                if s2 == s:
                    if predicates is not None and p not in predicates:
                        continue
                    if objects is not None and o not in objects:
                        continue
                    yield s, p, o

    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for s, p, o in self.relationships([curie], predicates, include_entailed=entailed):
            if s == curie:
                yield p, o

    def outgoing_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.outgoing_relationships(*args, **kwargs))

    def incoming_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for s, p, o in self.relationships(None, predicates, [curie], include_entailed=entailed):
            if o == curie:
                yield p, s

    def incoming_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.incoming_relationships(*args, **kwargs))

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        # TODO: move up
        if config is None:
            config = SearchConfiguration()
        matches = []
        mfunc = None
        if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
            mfunc = lambda label: str(label).startswith(search_term)
        elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
            prog = re.compile(search_term)
            mfunc = lambda label: prog.search(label)
        elif config.is_partial:
            mfunc = lambda label: search_term in str(label)
        else:
            mfunc = lambda label: label == search_term
        search_all = SearchProperty(SearchProperty.ANYTHING) in config.properties
        logging.info(f"SEARCH={search_term}")
        for t in self.entities():
            lbl = self.label(t)
            logging.debug(f"T={t} // {config}")
            if (
                search_all
                or SearchProperty(SearchProperty.LABEL)
                or config.properties not in config.properties
            ):
                if lbl and mfunc(lbl):
                    matches.append(t)
                    logging.info(f"Name match to {t}")
                    continue
            if search_all or SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
                if mfunc(t):
                    matches.append(t)
                    logging.info(f"identifier match to {t}")
                    continue
            if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
                for syn in self.entity_aliases(t):
                    if mfunc(syn):
                        logging.info(f"Syn match to {t}")
                        matches.append(t)
                        continue
        for m in matches:
            yield m

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        t = self._stanza(curie, strict=False)
        if t:
            for v in t.simple_values(TAG_XREF):
                yield HAS_DBXREF, v

    def clone(self, resource: OntologyResource) -> "SimpleOboImplementation":
        shutil.copyfile(self.resource.slug, resource.slug)
        return type(self)(resource)

    def dump(self, path: str = None, syntax: str = "obo"):
        if isinstance(path, str) or isinstance(path, Path):
            logging.info(f"Saving to {path}")
            with open(path, "w", encoding="UTF-8") as file:
                self.obo_document.dump(file)
        else:
            self.obo_document.dump(path)

    def save(
        self,
    ):
        logging.info("Committing and flushing changes")
        self.dump(self.resource.slug)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[sssom.Mapping]:
        s = self._stanza(curie)
        if s:
            for x in s.simple_values(TAG_XREF):
                yield sssom.Mapping(
                    subject_id=curie,
                    predicate_id=SKOS_CLOSE_MATCH,
                    object_id=x,
                    mapping_justification=SEMAPV.UnspecifiedMatching.value,
                )
        # TODO: use a cache to avoid re-calculating
        for s in self.obo_document.stanzas:
            if s:
                for x in s.simple_values(TAG_XREF):
                    if x == curie:
                        yield sssom.Mapping(
                            subject_id=s.id,
                            predicate_id=SKOS_CLOSE_MATCH,
                            object_id=curie,
                            mapping_justification=SEMAPV.UnspecifiedMatching.value,
                        )

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False, include_metadata=False) -> obograph.Node:
        t = self._stanza(curie, strict=False)
        if t is None:
            return obograph.Node(id=curie)
        else:
            meta = obograph.Meta()
            # TODO
            return obograph.Node(id=curie, lbl=self.label(curie), meta=meta)

    def as_obograph(self) -> Graph:
        nodes = [self.node(curie) for curie in self.entities()]
        edges = [Edge(sub=r[0], pred=r[1], obj=r[2]) for r in self.all_relationships()]
        return Graph(id="TODO", nodes=nodes, edges=edges)

    def logical_definitions(self, subjects: Iterable[CURIE]) -> Iterable[LogicalDefinitionAxiom]:
        for s in subjects:
            t = self._stanza(s, strict=False)
            ldef_tuples = t.intersection_of_tuples()
            if ldef_tuples:
                ldef = LogicalDefinitionAxiom(definedClassId=s)
                for m1, m2 in ldef_tuples:
                    if m2:
                        ldef.restrictions.append(ExistentialRestrictionExpression(m1, m2))
                    else:
                        ldef.genusIds.append(m1)
                yield ldef

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def different_from(self, entity: CURIE, other_ontology: DifferInterface) -> bool:
        t1 = self._stanza(entity, strict=False)
        if t1:
            t2 = other_ontology._stanza(entity, strict=False)
            if t2:
                return str(t1) != str(t2)
        return True

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        raise NotImplementedError

    def apply_patch(self, patch: kgcl.Change) -> None:
        od = self.obo_document

        def _clean(v: str) -> str:
            # TODO: remove this when this is fixed: https://github.com/INCATools/kgcl-rdflib/issues/43
            if v.startswith("'"):
                return v.replace("'", "")
            else:
                return v

        if isinstance(patch, kgcl.NodeRename):
            self.set_label(patch.about_node, _clean(patch.new_value))
        elif isinstance(patch, kgcl.NodeObsoletion):
            t = self._stanza(patch.about_node, strict=True)
            t.set_singular_tag(TAG_OBSOLETE, "true")
        elif isinstance(patch, kgcl.NodeDeletion):
            t = self._stanza(patch.about_node, strict=True)
            od.stanzas = [s for s in od.stanzas if s.id != patch.about_node]
        elif isinstance(patch, kgcl.NodeCreation):
            self.create_entity(patch.about_node, patch.name)
        elif isinstance(patch, kgcl.SynonymReplacement):
            t = self._stanza(patch.about_node, strict=True)
            n = 0
            for tv in t.tag_values:
                if tv.tag == TAG_SYNONYM:
                    syn = tv.as_synonym()
                    if syn[0] == patch.old_value:
                        tv.replace_quoted_part(patch.new_value)
                        n += 1
            if not n:
                raise ValueError(f"Failed to find synonym {patch.old_value} for {t.id}")
        elif isinstance(patch, kgcl.NodeTextDefinitionChange):
            t = self._stanza(patch.about_node, strict=True)
            for tv in t.tag_values:
                if tv == TAG_DEFINITION:
                    tv.replace_quoted_part(patch.new_value)
        elif isinstance(patch, kgcl.NewSynonym):
            t = self._stanza(patch.about_node, strict=True)
            # Get scope from patch.qualifier
            # rather than forcing all synonyms to be related.
            scope = str(patch.qualifier.value).upper() if patch.qualifier else "RELATED"
            v = patch.new_value.replace('"', '\\"')
            t.add_tag_value(TAG_SYNONYM, f'"{v}" {scope} []')
        elif isinstance(patch, kgcl.RemoveSynonym):
            t = self._stanza(patch.about_node, strict=True)
            # scope = str(patch.qualifier.value).upper() if patch.qualifier else "RELATED"
            v = patch.old_value.replace('"', '\\"')
            t.remove_simple_tag_value(TAG_SYNONYM, f'"{v}"')
        elif isinstance(patch, kgcl.NodeMove):
            logging.warning(f"Cannot handle {patch}")
        elif isinstance(patch, kgcl.PredicateChange):
            e = patch.about_edge
            subject = self._lookup(e.subject)
            object = self._lookup(e.object)
            t = self._stanza(subject, strict=True)
            if _is_isa(patch.old_value):
                t.remove_simple_tag_value(TAG_IS_A, object)
            else:
                pred = self._get_relationship_type_shorthand(patch.old_value)
                t.remove_pairwise_tag_value(TAG_RELATIONSHIP, pred, object)
            if _is_isa(patch.new_value):
                t.add_tag_value(TAG_IS_A, object)
            else:
                t.add_tag_value(TAG_RELATIONSHIP, f"{patch.new_value} {object}")
        else:
            raise NotImplementedError(f"cannot handle KGCL type {type(patch)}")
