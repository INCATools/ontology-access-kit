import logging
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

import sssom_schema as sssom
from kgcl_schema.datamodel import kgcl

from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import Edge, Graph
from oaklib.datamodels.vocabulary import (
    HAS_DBXREF,
    IS_A,
    LABEL_PREDICATE,
    SEMAPV,
    SKOS_CLOSE_MATCH,
)
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_COMMENT,
    TAG_DEFINITION,
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
from oaklib.interfaces.basic_ontology_interface import ALIAS_MAP, RELATIONSHIP_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.basic_utils import pairs_as_dict


@dataclass
class SimpleOboImplementation(
    ValidatorInterface,
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

    def __post_init__(self):
        if self.obo_document is None:
            resource = self.resource
            self.obo_document = parse_obo_document(resource.local_path)

    def store(self, resource: OntologyResource = None) -> None:
        if resource is None:
            resource = self.resource
        od = self.obo_document
        if resource.local:
            if resource.slug:
                with open(str(resource.local_path), "wb") as f:
                    od.dump(f)
            else:
                od.dump(sys.stdout.buffer)
        else:
            raise NotImplementedError(f"Cannot dump to {resource}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas:
            yield s.id

    def obsoletes(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas:
            if s.get_boolean_value(TAG_OBSOLETE):
                yield s.id

    def subsets(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.header.simple_values(TAG_SUBSETDEF):
            yield s

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas:
            if subset in s.simple_values(TAG_SUBSET):
                yield s.id

    def _stanza(self, curie: CURIE, strict=True) -> Optional[Stanza]:
        stanzas = [s for s in self.obo_document.stanzas if s.id == curie]
        if len(stanzas) > 1:
            raise ValueError(f"Duplicate id: {curie}")
        if stanzas:
            return stanzas[0]
        else:
            if strict:
                raise ValueError(f"No such stanza {curie}")

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
            s.id for s in self.obo_document.stanzas if s.singular_value(TAG_NAME, False) == label
        ]

    def create_entity(
        self,
        curie: CURIE,
        label: Optional[str] = None,
        relationships: Optional[RELATIONSHIP_MAP] = None,
        type: Optional[str] = None,
    ) -> CURIE:
        stanza = Stanza(curie, type)
        stanza.add_tag_value(TAG_NAME, label)
        # TODO
        return curie

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

    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        t = self._stanza(curie)
        for v in t.simple_values(TAG_IS_A):
            yield IS_A, v
        for pred, v in t.pair_values(TAG_RELATIONSHIP):
            # TODO: this is inefficient as it performs a lookup each time
            yield self._get_relationship_type_curie(pred), v

    def outgoing_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.outgoing_relationships(*args, **kwargs))

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        t = self._stanza(curie, strict=True)
        for v in t.simple_values(TAG_XREF):
            yield HAS_DBXREF, v

    def clone(self, resource: OntologyResource) -> "SimpleOboImplementation":
        shutil.copyfile(self.resource.slug, resource.slug)
        return type(self)(resource)

    def dump(self, path: str = None, syntax: str = "obo"):
        if isinstance(path, str):
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
        t = self._stanza(curie)
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

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
        else:
            raise NotImplementedError(f"cannot handle KGCL type {type(patch)}")
