import logging
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    TextIO,
    Tuple,
    Union,
)

import sssom_schema as sssom
from kgcl_schema.datamodel import kgcl

from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import (
    Edge,
    ExistentialRestrictionExpression,
    Graph,
    GraphDocument,
    LogicalDefinitionAxiom,
    SynonymPropertyValue,
)
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    CONSIDER_REPLACEMENT,
    CONTRIBUTOR,
    CREATED,
    CREATOR,
    DEPRECATED_PREDICATE,
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    HAS_OBO_NAMESPACE,
    HAS_OBSOLESCENCE_REASON,
    INVERSE_OF,
    IS_A,
    LABEL_PREDICATE,
    OIO_CREATED_BY,
    OIO_CREATION_DATE,
    OIO_SUBSET_PROPERTY,
    OIO_SYNONYM_TYPE_PROPERTY,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    OWL_VERSION_IRI,
    RDFS_DOMAIN,
    RDFS_RANGE,
    SCOPE_TO_SYNONYM_PRED_MAP,
    SEMAPV,
    SKOS_MATCH_PREDICATES,
    SUBPROPERTY_OF,
    TERM_REPLACED_BY,
    TERMS_MERGED,
)
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_ALT_ID,
    TAG_COMMENT,
    TAG_CONSIDER,
    TAG_CREATED_BY,
    TAG_CREATION_DATE,
    TAG_DATA_VERSION,
    TAG_DEFINITION,
    TAG_DOMAIN,
    TAG_EQUIVALENT_TO,
    TAG_HOLDS_OVER_CHAIN,
    TAG_ID_SPACE,
    TAG_INVERSE_OF,
    TAG_IS_A,
    TAG_IS_OBSOLETE,
    TAG_IS_TRANSITIVE,
    TAG_NAME,
    TAG_NAMESPACE,
    TAG_ONTOLOGY,
    TAG_PROPERTY_VALUE,
    TAG_RANGE,
    TAG_RELATIONSHIP,
    TAG_REPLACED_BY,
    TAG_SUBSET,
    TAG_SUBSETDEF,
    TAG_SYNONYM,
    TAG_SYNONYMTYPEDEF,
    TAG_XREF,
    OboDocument,
    Stanza,
    _synonym_scope_pred,
    parse_obo_document,
)
from oaklib.inference.relation_graph_reasoner import RelationGraphReasoner
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    DEFINITION,
    LANGUAGE_TAG,
    METADATA_MAP,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
)
from oaklib.interfaces.differ_interface import DiffConfiguration, DifferInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.obolegacy_interface import PRED_CODE, OboLegacyInterface
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.axioms.logical_definition_utilities import (
    logical_definition_matches,
)
from oaklib.utilities.kgcl_utilities import generate_change_id, tidy_change_object
from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources


def _is_isa(x: str):
    return x == IS_A or x.lower() == "is_a" or x.lower() == "isa"


@dataclass
class SimpleOboImplementation(
    ValidatorInterface,
    DifferInterface,
    RdfInterface,
    OboGraphInterface,
    OboLegacyInterface,
    SearchInterface,
    MappingProviderInterface,
    PatcherInterface,
    SummaryStatisticsInterface,
    SemanticSimilarityInterface,
    TaxonConstraintInterface,
    TextAnnotatorInterface,
    DumperInterface,
    MergeInterface,
    OwlInterface,
):
    """
    Simple OBO-file backed implementation

    This implementation is incomplete and is intended primarily as a Patcher implementation

    This can be abandoned when pronto is less strict
    """

    obo_document: OboDocument = None
    _relationship_index_cache: Dict[CURIE, List[RELATIONSHIP]] = None
    _alt_id_to_replacement_map: Dict[CURIE, List[CURIE]] = None
    _uses_legacy_properties: bool = None

    def __post_init__(self):
        if self.obo_document is None:
            resource = self.resource
            if resource and resource.local_path:
                logging.info(f"Creating doc for {resource}")
                self.obo_document = parse_obo_document(resource.local_path)
                if "edit.obo" in str(resource.local_path) and self.auto_relax_axioms is None:
                    # TODO: in future ontology modules should explicitly set this in the metadata
                    logging.info(
                        f"Auto-setting auto_relax_axioms based on name: {resource.local_path}"
                    )
                    self.auto_relax_axioms = True
            else:
                self.obo_document = OboDocument()
        for prefix, expansion in self.obo_document.header.pair_values(TAG_ID_SPACE):
            self.prefix_map()[prefix] = expansion

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

    def load_graph(self, graph: Graph, replace: True) -> None:
        if not replace:
            raise NotImplementedError("Cannot merge obograph")
        converter = OboGraphToOboFormatConverter()
        self.obo_document = OboDocument()
        gd = GraphDocument(graphs=[graph])
        converter.convert(gd, self.obo_document)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        logging.info("Commencing indexing")
        n = 0
        entities = list(self.entities(filter_obsoletes=False))
        for s in entities:
            t = self._stanza(s, strict=False)
            if t is None:
                # alt_ids
                continue
            is_relation = t.type == "Typedef"
            for v in t.simple_values(TAG_IS_A):
                n += 1
                if is_relation:
                    yield s, SUBPROPERTY_OF, self.map_shorthand_to_curie(v)
                else:
                    yield s, IS_A, v
            for tag, prop in [
                (TAG_INVERSE_OF, INVERSE_OF),
                (TAG_DOMAIN, RDFS_DOMAIN),
                (TAG_RANGE, RDFS_RANGE),
            ]:
                for v in t.simple_values(tag):
                    n += 1
                    yield s, prop, self.map_shorthand_to_curie(v)
            for v in t.simple_values(TAG_EQUIVALENT_TO):
                n += 1
                yield s, EQUIVALENT_CLASS, v
                yield v, EQUIVALENT_CLASS, s
            for p, v in t.pair_values(TAG_RELATIONSHIP):
                yield s, self.map_shorthand_to_curie(p), v
            # for p, v in t.intersection_of_tuples():
            #    n += 1
            #    yield s, self._get_relationship_type_curie(p), v
        logging.info(f"Indexed {n} relationships")
        if self.auto_relax_axioms:
            n = 0
            logging.info("Auto-relaxing axioms")
            for ldef in self.logical_definitions(entities):
                for p in ldef.genusIds:
                    yield ldef.definedClassId, IS_A, p
                    n += 1
                for r in ldef.restrictions:
                    yield ldef.definedClassId, r.propertyId, r.fillerId
                    n += 1
            logging.info(f"Relaxed {n} relationships")

    def _all_entailed_relationships(self):
        reasoner = RelationGraphReasoner(self)
        yield from reasoner.entailed_edges()

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        od = self.obo_document
        for s_id, s in od.stanzas.items():
            if filter_obsoletes:
                if s.get_boolean_value(TAG_IS_OBSOLETE):
                    continue
            if (
                owl_type is None
                or (owl_type == OWL_CLASS and s.type == "Term")
                or (owl_type == OWL_OBJECT_PROPERTY and s.type == "Typedef")
            ):
                if s.type == "Typedef":
                    yield self.map_shorthand_to_curie(s_id)
                else:
                    yield s_id
        if not owl_type or owl_type == OWL_CLASS:
            # note that in the case of alt_ids, metadata such as
            # original owl_type is lost. We assume that the original
            # owl_type was OWL_CLASS
            if not filter_obsoletes:
                for s in self._get_alt_id_to_replacement_map().keys():
                    yield s
        if not owl_type or owl_type == OIO_SUBSET_PROPERTY:
            for v in od.header.simple_values(TAG_SUBSETDEF):
                yield v
        if not owl_type or owl_type == OIO_SYNONYM_TYPE_PROPERTY:
            for v in od.header.simple_values(TAG_SYNONYMTYPEDEF):
                yield v

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CURIE]]:
        od = self.obo_document
        for curie in entities:
            s = self._stanza(curie, False)
            if s is None:
                if curie in self.subsets():
                    yield curie, OIO_SUBSET_PROPERTY
                elif curie in od.header.simple_values(TAG_SYNONYMTYPEDEF):
                    yield curie, OIO_SYNONYM_TYPE_PROPERTY
                else:
                    yield curie, None
            else:
                if s.type == "Term":
                    yield curie, OWL_CLASS
                elif s.type == "Typedef":
                    yield curie, OWL_OBJECT_PROPERTY
                else:
                    raise ValueError(f"Unknown stanza type: {s.type}")

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas.values():
            if s.get_boolean_value(TAG_IS_OBSOLETE):
                yield s.id
        if include_merged:
            for s in self._get_alt_id_to_replacement_map().keys():
                yield s

    def subsets(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.header.simple_values(TAG_SUBSETDEF):
            yield s

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        od = self.obo_document
        for s in od.stanzas.values():
            if subset in s.simple_values(TAG_SUBSET):
                yield s.id

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        for curie in curies:
            s = self._stanza(curie, False)
            if s:
                for subset in s.simple_values(TAG_SUBSET):
                    yield curie, subset

    def ontologies(self) -> Iterable[CURIE]:
        od = self.obo_document
        for v in od.header.simple_values(TAG_ONTOLOGY):
            yield v

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
        m = defaultdict(list)
        m["id"] = [ontology]
        omo_map = {
            TAG_DATA_VERSION: OWL_VERSION_IRI,
        }
        header = self.obo_document.header
        for tv in header.tag_values:
            tag = tv.tag
            if tag in omo_map:
                p = omo_map[tag]
                val = tv.value
                if p == OWL_VERSION_IRI:
                    val = f"obo:{ontology}/{val}{ontology}.owl"
                m[p].append(val)
        return dict(m)

    def _stanza(self, curie: CURIE, strict=True) -> Optional[Stanza]:
        stanza = self.obo_document.stanzas.get(curie, None)
        if stanza is None:
            alt_curie = self.map_curie_to_shorthand(curie)
            if alt_curie and alt_curie != curie:
                stanza = self.obo_document.stanzas.get(alt_curie)
        if strict and not stanza:
            raise ValueError(f"No such stanza {curie}")
        return stanza

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError("Language tags not supported")
        s = self._stanza(curie, False)
        if s:
            return s.singular_value(TAG_NAME)
        else:
            if curie == IS_A:
                return "subClassOf"
            else:
                return None

    def set_label(self, curie: CURIE, label: str, lang: Optional[LANGUAGE_TAG] = None) -> bool:
        if lang:
            raise NotImplementedError("Language tags not supported")
        s = self._stanza(curie, False)
        s.set_singular_tag(TAG_NAME, label)
        return True

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
        replace=False,
    ) -> CURIE:
        if type is None or type == OWL_CLASS:
            type = "Term"
        elif type == OWL_OBJECT_PROPERTY:
            type = "Typedef"
        else:
            raise ValueError(f"Cannot handle type: {type}")
        stanza = self._stanza(curie, False)
        if stanza:
            if replace:
                stanza = None
        if not stanza:
            stanza = Stanza(id=curie, type=type)
        stanza.add_tag_value(TAG_NAME, label)
        self.obo_document.add_stanza(stanza)
        if relationships:
            for pred, fillers in relationships.items():
                for filler in fillers:
                    self.add_relationship(curie, pred, filler)

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE, **kwargs):
        t = self._stanza(curie)
        if predicate == IS_A:
            t.add_tag_value(TAG_IS_A, filler, **kwargs)
        else:
            predicate_code = self.map_curie_to_shorthand(predicate)
            t.add_tag_value_pair(TAG_RELATIONSHIP, predicate_code, filler, **kwargs)
        self._clear_relationship_index()

    def remove_relationship(self, curie: CURIE, predicate: Optional[PRED_CURIE], filler: CURIE):
        t = self._stanza(curie)
        if not predicate or predicate == IS_A:
            t.remove_simple_tag_value(TAG_IS_A, filler)
        else:
            predicate_code = self.map_curie_to_shorthand(predicate)
            t.remove_pairwise_tag_value(TAG_RELATIONSHIP, predicate_code, filler)
        self._clear_relationship_index()

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        s = self._stanza(curie, strict=False)
        if s:
            return s.quoted_value(TAG_DEFINITION)

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[DEFINITION]:
        for curie in curies:
            s = self._stanza(curie, strict=False)
            if s:
                d = s.quoted_value(TAG_DEFINITION)
                if d:
                    if include_metadata:
                        defn_tvs = [tv for tv in s.tag_values if tv.tag == TAG_DEFINITION]
                        if defn_tvs:
                            defn_tv = defn_tvs[0]
                            defn, xrefs = defn_tv.as_definition()
                            yield curie, defn, {HAS_DBXREF: xrefs}
                    else:
                        yield curie, d, None
                elif include_missing:
                    yield curie, None, None

    def comments(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        for curie in curies:
            s = self._stanza(curie)
            if s:
                yield curie, s.singular_value(TAG_COMMENT)

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        s = self._stanza(curie, strict=False)
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

    def synonym_property_values(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Iterator[Tuple[CURIE, SynonymPropertyValue]]:
        if isinstance(subject, str):
            subject = [subject]
        for curie in subject:
            s = self._stanza(curie, strict=False)
            if not s:
                continue
            for syn in s.synonyms():
                pred = _synonym_scope_pred(syn[1]).replace("oio:", "")
                yield curie, SynonymPropertyValue(
                    pred=pred, val=syn[0], synonymType=syn[2], xrefs=syn[3]
                )

    def map_shorthand_to_curie(self, rel_code: PRED_CODE) -> PRED_CURIE:
        """
        Maps either a true relationship type CURIE or a shorthand packages to a CURIE.

        See `section 5.9 <https://owlcollab.github.io/oboformat/doc/obo-syntax.html#5.9>`_

        :param rel_code:
        :return:
        """
        for _, x in self.simple_mappings_by_curie(rel_code):
            if x.startswith("BFO:") or x.startswith("RO:"):
                return x
            if ":" not in rel_code and ":" in x:
                return x
        return rel_code

    def map_curie_to_shorthand(self, rel_type: PRED_CURIE) -> PRED_CODE:
        """
        Reciprocal of `_get_relationship_type_curie`

        :param rel_type:
        :return:
        """
        if rel_type:
            is_core = rel_type.startswith("BFO:") or rel_type.startswith("RO:")
            for s in self.obo_document.stanzas.values():
                if s.type == "Typedef":
                    for x in s.simple_values(TAG_XREF):
                        if x == rel_type:
                            if is_core or ":" not in s.id:
                                return s.id
        return rel_type

    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        if invert:
            for s, p, o in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
                exclude_blank=exclude_blank,
            ):
                yield o, p, s
            return
        ei = self.edge_index
        if include_entailed:
            ei = self.entailed_edge_index
        yield from ei.edges(
            subjects=subjects,
            predicates=predicates,
            objects=objects,
        )

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        # TODO: move up, avoid repeating packages
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
        for t in self.entities(filter_obsoletes=False):
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
            if (
                search_all
                or SearchProperty(SearchProperty.REPLACEMENT_IDENTIFIER) in config.properties
            ):
                s = self._stanza(t, strict=False)
                if s:
                    for r in s.simple_values(TAG_REPLACED_BY):
                        if mfunc(t):
                            matches.append(r)
                            logging.info(f"replaced_by match to {t}")
                            continue
                    for a in s.simple_values(TAG_ALT_ID):
                        if mfunc(a):
                            matches.append(t)
                            logging.info(f"alternate_id match to {t}")
                            continue
            if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
                for syn in self.entity_aliases(t):
                    if mfunc(syn):
                        logging.info(f"Syn match to {t}")
                        matches.append(t)
                        continue
            if search_all or SearchProperty(SearchProperty.MAPPED_IDENTIFIER) in config.properties:
                for x in self.simple_mappings_by_curie(t):
                    if mfunc(x):
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

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        t = self._stanza(curie, strict=False)
        _alt_id_map = self._get_alt_id_to_replacement_map()
        m = defaultdict(list)
        if t:
            for tag, mkey in [
                (TAG_REPLACED_BY, TERM_REPLACED_BY),
                (TAG_CONSIDER, CONSIDER_REPLACEMENT),
                (TAG_NAMESPACE, HAS_OBO_NAMESPACE),
                (TAG_IS_OBSOLETE, DEPRECATED_PREDICATE),
                (TAG_CREATION_DATE, OIO_CREATION_DATE),
                (TAG_CREATED_BY, OIO_CREATED_BY),
            ]:
                for v in t.simple_values(tag):
                    if tag == TAG_IS_OBSOLETE:
                        v = True if v == "true" else False
                    m[mkey].append(v)
            for pv in t.property_values():
                m[self.map_shorthand_to_curie(pv[0])].append(pv[1])
        if curie in _alt_id_map:
            m[TERM_REPLACED_BY] += _alt_id_map[curie]
            m[DEPRECATED_PREDICATE].append(True)
            m[HAS_OBSOLESCENCE_REASON].append(TERMS_MERGED)
        self.add_missing_property_values(curie, m)
        return dict(m)

    def _get_alt_id_to_replacement_map(self) -> Dict[CURIE, List[CURIE]]:
        if self._alt_id_to_replacement_map is None:
            self._alt_id_to_replacement_map = defaultdict(list)
            for e in self.entities():
                t = self._stanza(e, False)
                if t:
                    for a in t.simple_values(TAG_ALT_ID):
                        self._alt_id_to_replacement_map[a].append(e)
        return self._alt_id_to_replacement_map

    def clone(self, resource: OntologyResource) -> "SimpleOboImplementation":
        shutil.copyfile(self.resource.slug, resource.slug)
        return type(self)(resource)

    def dump(self, path: Union[str, TextIO] = None, syntax: str = "obo", **kwargs):
        if syntax is None or syntax == "obo":
            if isinstance(path, str) or isinstance(path, Path):
                logging.info(f"Saving to {path}")
                with open(path, "w", encoding="UTF-8") as file:
                    self.obo_document.dump(file)
            else:
                self.obo_document.dump(path)
        else:
            super().dump(path, syntax=syntax)

    def save(
        self,
    ):
        logging.info("Committing and flushing changes")
        self.dump(self.resource.slug)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[sssom.Mapping]:
        s = self._stanza(curie, strict=False)
        if s:
            for x in s.simple_values(TAG_XREF):
                m = sssom.Mapping(
                    subject_id=curie,
                    predicate_id=HAS_DBXREF,
                    object_id=x,
                    mapping_justification=sssom.EntityReference(SEMAPV.UnspecifiedMatching.value),
                )
                inject_mapping_sources(m)
                yield m
            for x in s.property_values():
                p = self.map_shorthand_to_curie(x[0])
                if p in SKOS_MATCH_PREDICATES:
                    m = sssom.Mapping(
                        subject_id=curie,
                        predicate_id=p,
                        object_id=x[1],
                        mapping_justification=sssom.EntityReference(
                            SEMAPV.UnspecifiedMatching.value
                        ),
                    )
                    inject_mapping_sources(m)
                    yield m
            for p, v in s.pair_values(TAG_RELATIONSHIP):
                p = self.map_shorthand_to_curie(p)
                if p in SKOS_MATCH_PREDICATES:
                    m = sssom.Mapping(
                        subject_id=curie,
                        predicate_id=p,
                        object_id=v,
                        mapping_justification=sssom.EntityReference(
                            SEMAPV.UnspecifiedMatching.value
                        ),
                    )
                    inject_mapping_sources(m)
                    yield m
        # TODO: use a cache to avoid re-calculating
        for _, stanza in self.obo_document.stanzas.items():
            if len(stanza.simple_values(TAG_XREF)) > 0:
                for x in stanza.simple_values(TAG_XREF):
                    if x == curie:
                        m = sssom.Mapping(
                            subject_id=stanza.id,
                            predicate_id=HAS_DBXREF,
                            object_id=curie,
                            mapping_justification=SEMAPV.UnspecifiedMatching.value,
                        )
                        inject_mapping_sources(m)
                        yield m

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False, include_metadata=False) -> obograph.Node:
        t = self._stanza(curie, strict=False)
        if t is None:
            return obograph.Node(id=curie)
        else:
            types = self.owl_type(curie)
            if OWL_CLASS in types:
                typ = "CLASS"
            elif OWL_OBJECT_PROPERTY in types:
                typ = "PROPERTY"
            else:
                typ = None
            meta = obograph.Meta()
            if include_metadata:
                for s in t.simple_values(TAG_SUBSET):
                    meta.subsets.append(s)
                defn = self.definition(curie)
                if defn:
                    meta.definition = obograph.DefinitionPropertyValue(val=defn)
                for _, syn in self.synonym_property_values([curie]):
                    meta.synonyms.append(syn)
                for _, subset in self.terms_subsets([curie]):
                    meta.subsets.append(subset)
            return obograph.Node(id=curie, lbl=self.label(curie), type=typ, meta=meta)

    def as_obograph(self, expand_curies=False) -> Graph:
        def expand(curie: CURIE) -> CURIE:
            if expand_curies:
                uri = self.curie_to_uri(curie, strict=False)
                return uri if uri is not None else curie
            else:
                return curie

        entities = list(self.entities())
        nodes = [self.node(expand(curie)) for curie in entities]
        edges = [
            Edge(sub=expand(r[0]), pred=expand(r[1]), obj=expand(r[2]))
            for r in self.relationships()
        ]
        ldefs = list(self.logical_definitions(entities))
        return Graph(id="TODO", nodes=nodes, edges=edges, logicalDefinitionAxioms=ldefs)

    def logical_definitions(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        **kwargs,
    ) -> Iterable[LogicalDefinitionAxiom]:
        if subjects is None:
            subjects = self.entities()
        for s in subjects:
            t = self._stanza(s, strict=False)
            if not t:
                continue
            ldef_tuples = t.intersection_of_tuples()
            if ldef_tuples:
                ldef = LogicalDefinitionAxiom(definedClassId=s)
                for m1, m2 in ldef_tuples:
                    if m2:
                        ldef.restrictions.append(
                            ExistentialRestrictionExpression(
                                propertyId=self.map_shorthand_to_curie(m1), fillerId=m2
                            )
                        )
                    else:
                        ldef.genusIds.append(m1)
                if logical_definition_matches(ldef, predicates=predicates, objects=objects):
                    yield ldef

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: DifferInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def diff(
        self,
        other_ontology: DifferInterface,
        configuration: DiffConfiguration = None,
        **kwargs,
    ) -> Iterator[kgcl.Change]:
        if configuration is None:
            configuration = DiffConfiguration()
        if not isinstance(other_ontology, SimpleOboImplementation):
            raise ValueError("Can only diff SimpleOboImplementation")
        stanzas1 = self.obo_document.stanzas
        stanzas2 = other_ontology.obo_document.stanzas
        all_ids = set(stanzas1.keys()).union(stanzas2.keys())
        for id in all_ids:
            yield from self._diff_stanzas(stanzas1.get(id, None), stanzas2.get(id, None))

    def _diff_stanzas(
        self, stanza1: Optional[Stanza], stanza2: Optional[Stanza]
    ) -> Iterator[kgcl.Change]:
        def _id():
            return generate_change_id()

        node_is_deleted = False
        node_is_created = False
        if stanza1 is None and stanza2 is None:
            raise ValueError("Both stanzas are None")
        if stanza1 is None:
            stanza1 = Stanza(id=stanza2.id, type=stanza2.type)
            if stanza2.type == "Term":
                yield kgcl.ClassCreation(
                    id=_id(), about_node=stanza2.id, name=stanza2.singular_value(TAG_NAME)
                )
            elif stanza2.type == "Typedef":
                yield kgcl.NodeCreation(
                    id=_id(), about_node=stanza2.id, name=stanza2.singular_value(TAG_NAME)
                )
            else:
                raise ValueError(f"Unknown stanza type: {stanza2.type}")
            node_is_created = True
        if stanza2 is None:
            stanza2 = Stanza(id=stanza1.id, type=stanza1.type)
            if stanza1.type == "Term":
                yield kgcl.NodeDeletion(id=_id(), about_node=stanza1.id)
            else:
                yield kgcl.NodeDeletion(id=_id(), about_node=stanza1.id)
            node_is_deleted = True
        if stanza1 == stanza2:
            return
        if stanza1.type != stanza2.type:
            raise ValueError(f"Stanza types differ: {stanza1.type} vs {stanza2.type}")
        t1id = stanza1.id
        t2id = stanza2.id
        logging.info(f"Diffing: {t1id} vs {t2id}")

        def _tv_dict(stanza: Stanza) -> Dict[str, List[str]]:
            d = defaultdict(set)
            for tv in stanza.tag_values:
                d[tv.tag].add(tv.value)
            return d

        tv_dict1 = _tv_dict(stanza1)
        tv_dict2 = _tv_dict(stanza2)
        all_tags = set(tv_dict1.keys()).union(tv_dict2.keys())
        for tag in all_tags:
            vals1 = tv_dict1.get(tag, [])
            vals2 = tv_dict2.get(tag, [])
            vals1list = list(vals1)
            vals2list = list(vals2)
            tvs1 = [tv for tv in stanza1.tag_values if tv.tag == tag]
            tvs2 = [tv for tv in stanza2.tag_values if tv.tag == tag]
            if vals1 == vals2:
                continue
            logging.info(f"Difference in {tag}: {vals1} vs {vals2}")
            if tag == TAG_NAME:
                if node_is_deleted or node_is_created:
                    continue
                if vals1 and vals2:
                    yield kgcl.NodeRename(
                        id=_id(), about_node=t1id, new_value=vals2list[0], old_value=vals1list[0]
                    )
                elif vals2:
                    # Existing node goes from having no name to having a name
                    # In future KGCL may have a NodeNewName. For now we use NodeRename.
                    yield kgcl.NodeRename(
                        id=_id(), about_node=t1id, new_value=vals2list[0], old_value=None
                    )
                else:
                    yield kgcl.NodeDeletion(
                        id=_id(), about_node=t1id, old_value=vals1list[0], new_value=None
                    )
            elif tag == TAG_DEFINITION:
                if node_is_deleted:
                    continue
                # TODO: provenance changes
                td1 = stanza1.quoted_value(TAG_DEFINITION)
                td2 = stanza2.quoted_value(TAG_DEFINITION)
                if vals1 and vals2:
                    yield kgcl.NodeTextDefinitionChange(
                        id=_id(), about_node=t1id, new_value=td2, old_value=td1
                    )
                elif vals1:
                    yield kgcl.RemoveTextDefinition(id=_id(), about_node=t1id, old_value=td1)
                else:
                    yield kgcl.NewTextDefinition(id=_id(), about_node=t2id, new_value=td2)
            elif tag == TAG_IS_OBSOLETE:
                if node_is_deleted:
                    continue
                if vals1 and not vals2:
                    yield kgcl.NodeUnobsoletion(id=_id(), about_node=t1id)
                elif not vals1 and vals2:
                    replaced_by = stanza2.simple_values(TAG_REPLACED_BY)
                    if replaced_by:
                        yield kgcl.NodeObsoletionWithDirectReplacement(
                            id=_id(), about_node=t2id, has_direct_replacement=replaced_by[0]
                        )
                    else:
                        yield kgcl.NodeObsoletion(id=_id(), about_node=t2id)
            elif tag == TAG_SUBSET:
                if node_is_deleted:
                    continue
                xrefs1 = stanza1.simple_values(TAG_SUBSET)
                xrefs2 = stanza2.simple_values(TAG_SUBSET)
                for xref in xrefs1:
                    if xref not in xrefs2:
                        yield kgcl.RemoveNodeFromSubset(id=_id(), about_node=t1id, in_subset=xref)
                for xref in xrefs2:
                    if xref not in xrefs1:
                        yield kgcl.AddNodeToSubset(id=_id(), about_node=t2id, in_subset=xref)
            elif tag == TAG_IS_A:
                isas1 = stanza1.simple_values(TAG_IS_A)
                isas2 = stanza2.simple_values(TAG_IS_A)
                for isa in isas1:
                    if isa not in isas2:
                        yield kgcl.EdgeDeletion(id=_id(), subject=t1id, predicate=IS_A, object=isa)
                for isa in isas2:
                    if isa not in isas1:
                        yield kgcl.EdgeCreation(id=_id(), subject=t2id, predicate=IS_A, object=isa)
            elif tag == TAG_RELATIONSHIP:
                rels1 = stanza1.pair_values(TAG_RELATIONSHIP)
                rels2 = stanza2.pair_values(TAG_RELATIONSHIP)
                for p, v in rels1:
                    p_curie = self.map_shorthand_to_curie(p)
                    if (p, v) not in rels2:
                        yield kgcl.EdgeDeletion(id=_id(), subject=t1id, predicate=p_curie, object=v)
                for p, v in rels2:
                    p_curie = self.map_shorthand_to_curie(p)
                    if (p, v) not in rels1:
                        yield kgcl.EdgeCreation(id=_id(), subject=t2id, predicate=p_curie, object=v)
            elif tag == TAG_SYNONYM:
                if node_is_deleted:
                    continue
                # TODO: make this sensitive to annotation changes; for now we truncate the tuple
                syns1 = [tv.as_synonym()[0:2] for tv in tvs1]
                syns2 = [tv.as_synonym()[0:2] for tv in tvs2]
                for syn in syns1:
                    if syn not in syns2:
                        yield kgcl.RemoveSynonym(id=_id(), about_node=t1id, old_value=syn[0])
                for syn in syns2:
                    if syn not in syns1:
                        pred = SCOPE_TO_SYNONYM_PRED_MAP[syn[1]]
                        yield kgcl.NewSynonym(
                            id=_id(), about_node=t2id, new_value=syn[0], predicate=pred
                        )
            elif tag == TAG_XREF:
                if node_is_deleted:
                    continue
                xrefs1 = stanza1.simple_values(TAG_XREF)
                xrefs2 = stanza2.simple_values(TAG_XREF)
                for xref in xrefs1:
                    if xref not in xrefs2:
                        yield kgcl.RemoveMapping(
                            id=_id(), about_node=t1id, object=xref, predicate=HAS_DBXREF
                        )
                for xref in xrefs2:
                    if xref not in xrefs1:
                        yield kgcl.MappingCreation(
                            id=_id(), subject=t2id, object=xref, predicate=HAS_DBXREF
                        )

    def different_from(self, entity: CURIE, other_ontology: DifferInterface) -> bool:
        t1 = self._stanza(entity, strict=False)
        if t1:
            t2 = other_ontology._stanza(entity, strict=False)
            if t2:
                return str(t1) != str(t2)
        return True

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def migrate_curies(self, curie_map: Mapping[CURIE, CURIE]) -> None:
        od = self.obo_document
        for t in od.stanzas.values():
            t.replace_token(curie_map)
        od.reindex()
        self._rebuild_relationship_index()

    @property
    def uses_legacy_properties(self) -> bool:
        if self._uses_legacy_properties is not None:
            return self._uses_legacy_properties
        for s in self.obo_document.stanzas.values():
            for tv in s.tag_values:
                if tv.tag in [TAG_CREATED_BY, TAG_CREATION_DATE]:
                    self._uses_legacy_properties = True
                    return True
        return False

    def set_uses_legacy_properties(self, value: bool) -> None:
        self._uses_legacy_properties = value

    def add_contributors(self, curie: CURIE, agents: List[CURIE]) -> None:
        t = self._stanza(curie, strict=True)
        for agent in agents:
            t.add_tag_value_pair(TAG_PROPERTY_VALUE, CONTRIBUTOR, agent)

    def set_creator(self, curie: CURIE, agent: CURIE, date: Optional[str] = None) -> None:
        t = self._stanza(curie, strict=True)
        if self._uses_legacy_properties:
            t.set_singular_tag(TAG_CREATED_BY, agent)
        else:
            t.add_tag_value_pair(TAG_PROPERTY_VALUE, CREATOR, agent)
        if date:
            self.set_creation_date(curie, date)

    def set_creation_date(self, curie: CURIE, date: str) -> None:
        t = self._stanza(curie, strict=True)
        if self._uses_legacy_properties:
            t.set_singular_tag(TAG_CREATION_DATE, date)
        else:
            t.add_tag_value_pair(TAG_PROPERTY_VALUE, CREATED, date)

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: kgcl.Configuration = None,
        strict=False,
    ) -> kgcl.Change:
        od = self.obo_document
        tidy_change_object(patch)
        logging.debug(f"Applying {patch}")
        modified_entities = []
        if isinstance(patch, kgcl.NodeRename):
            # self.set_label(patch.about_node, _clean(patch.new_value))
            self.set_label(patch.about_node, patch.new_value)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.NodeObsoletion):
            t = self._stanza(patch.about_node, strict=True)
            t.set_singular_tag(TAG_IS_OBSOLETE, "true")
            if isinstance(patch, kgcl.NodeObsoletionWithDirectReplacement):
                t.set_singular_tag(TAG_REPLACED_BY, patch.has_direct_replacement)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.NodeDeletion):
            try:
                del od.stanzas[patch.about_node]
            except KeyError:
                logging.error(f"CURIE {patch.about_node} does not exist in the OBO file provided.")
        elif isinstance(patch, kgcl.NodeCreation):
            self.create_entity(patch.about_node, patch.name)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.ClassCreation):
            self.create_entity(patch.about_node, patch.name)
            modified_entities.append(patch.about_node)
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
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.AddNodeToSubset):
            t = self._stanza(patch.about_node, strict=True)
            t.add_tag_value(TAG_SUBSET, patch.in_subset)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.RemoveNodeFromSubset):
            t = self._stanza(patch.about_node, strict=True)
            t.remove_simple_tag_value(TAG_SUBSET, patch.in_subset)
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.NewTextDefinition):
            t = self._stanza(patch.about_node, strict=True)
            t.add_quoted_tag_value(TAG_DEFINITION, patch.new_value.strip("'"), xrefs=[])
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.RemoveTextDefinition):
            t = self._stanza(patch.about_node, strict=True)
            for tv in t.tag_values:
                if tv.tag == TAG_DEFINITION:
                    # This is a remove_definition request
                    t.remove_tag_quoted_value(TAG_DEFINITION, t._quoted_value(tv.value))
        elif isinstance(patch, kgcl.NodeTextDefinitionChange):
            t = self._stanza(patch.about_node, strict=True)
            current = t.quoted_value(TAG_DEFINITION)
            if patch.old_value and current != patch.old_value:
                msg = f"Current definition {current} does not match expected {patch.old_value}"
                if strict:
                    raise ValueError(msg)
                else:
                    logging.error(msg)
            else:
                for tv in t.tag_values:
                    if tv.tag == TAG_DEFINITION:
                        tv.replace_quoted_part(patch.new_value.strip("'"))
        elif isinstance(patch, kgcl.NewSynonym):
            t = self._stanza(patch.about_node, strict=True)
            # Get scope from patch.qualifier
            # rather than forcing all synonyms to be related.
            if isinstance(patch.qualifier, str):
                scope = patch.qualifier.upper()
            else:
                scope = str(patch.qualifier.value).upper() if patch.qualifier else "RELATED"
            v = patch.new_value.replace('"', '\\"')
            t.add_tag_value(TAG_SYNONYM, f'"{v}" {scope} []')
            modified_entities.append(patch.about_node)
        elif isinstance(patch, kgcl.RemoveSynonym):
            t = self._stanza(patch.about_node, strict=True)
            # scope = str(patch.qualifier.value).upper() if patch.qualifier else "RELATED"
            v = patch.old_value.strip(
                '"'
            )  # Handling a bug where quotes are accidentally introduced.
            t.remove_tag_quoted_value(TAG_SYNONYM, v)
        elif isinstance(patch, kgcl.EdgeCreation):
            description = patch.change_description
            self.add_relationship(
                patch.subject, patch.predicate, patch.object, description=description
            )
            modified_entities.append(patch.subject)
        elif isinstance(patch, kgcl.EdgeDeletion):
            self.remove_relationship(patch.subject, patch.predicate, patch.object)
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
                pred = self.map_curie_to_shorthand(patch.old_value)
                t.remove_pairwise_tag_value(TAG_RELATIONSHIP, pred, object)
            if _is_isa(patch.new_value):
                t.add_tag_value(TAG_IS_A, object)
            else:
                t.add_tag_value(TAG_RELATIONSHIP, f"{patch.new_value} {object}")
            self._clear_relationship_index()
            modified_entities.append(subject)
        else:
            raise NotImplementedError(f"cannot handle KGCL type {type(patch)}")
        if patch.contributor:
            self.add_contributors(patch.about_node, [patch.contributor])
            modified_entities.append(patch.about_node)
        for e in modified_entities:
            stanza = self._stanza(e, strict=True)
            stanza.normalize_order()
        return patch

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OwlInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def transitive_object_properties(self) -> Iterable[CURIE]:
        od = self.obo_document
        for s_id, s in od.stanzas.items():
            if s.type == "Typedef":
                if s.get_boolean_value(TAG_IS_TRANSITIVE, False):
                    yield self.map_shorthand_to_curie(s_id)

    def simple_subproperty_of_chains(self) -> Iterable[Tuple[CURIE, List[CURIE]]]:
        od = self.obo_document
        for s_id, s in od.stanzas.items():
            if s.type == "Typedef":
                for p1, p2 in s.pair_values(TAG_HOLDS_OVER_CHAIN):
                    curie = self.map_shorthand_to_curie(s_id)
                    yield curie, [self.map_shorthand_to_curie(p1), self.map_shorthand_to_curie(p2)]
