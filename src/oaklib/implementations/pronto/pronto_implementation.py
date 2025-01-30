import logging
import re
import shutil
import sys
import tempfile

# https://github.com/althonos/pronto/issues/173
import warnings
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

import pronto
import sssom_schema as sssom
from deprecated import deprecated
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import json_dumper
from pronto import LiteralPropertyValue, Ontology, ResourcePropertyValue, Term

from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    CONSIDER_REPLACEMENT,
    DEPRECATED_PREDICATE,
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    HAS_OBO_NAMESPACE,
    HAS_OBSOLESCENCE_REASON,
    IS_A,
    LABEL_PREDICATE,
    OIO_SUBSET_PROPERTY,
    OIO_SYNONYM_TYPE_PROPERTY,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    OWL_VERSION_INFO,
    SCOPE_TO_SYNONYM_PRED_MAP,
    SEMAPV,
    SKOS_MATCH_PREDICATES,
    TERM_REPLACED_BY,
    TERMS_MERGED,
)
from oaklib.inference.relation_graph_reasoner import RelationGraphReasoner
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    DEFINITION,
    LANGUAGE_TAG,
    METADATA_MAP,
    PRED_CURIE,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.obolegacy_interface import OboLegacyInterface
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, SUBSET_CURIE
from oaklib.utilities.axioms.logical_definition_utilities import (
    logical_definition_matches,
)
from oaklib.utilities.kgcl_utilities import tidy_change_object
from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

warnings.filterwarnings("ignore", category=pronto.warnings.SyntaxWarning, module="pronto")


def _synonym_scope_pred(s: pronto.Synonym) -> str:
    scope = s.scope.upper()
    if scope in SCOPE_TO_SYNONYM_PRED_MAP:
        return SCOPE_TO_SYNONYM_PRED_MAP[scope]
    else:
        raise ValueError(f"Unknown scope: {scope}")


@dataclass
class ProntoImplementation(
    ValidatorInterface,
    RdfInterface,
    OboGraphInterface,
    OboLegacyInterface,
    SearchInterface,
    MappingProviderInterface,
    PatcherInterface,
    DifferInterface,
    # AssociationProviderInterface,
    ClassEnrichmentCalculationInterface,
    SemanticSimilarityInterface,
    TextAnnotatorInterface,
    SummaryStatisticsInterface,
    TaxonConstraintInterface,
    DumperInterface,
    MergeInterface,
    OwlInterface,
):
    """
    An adapter that standardizes access to OBO Format files by wrapping the Pronto library.

    `Pronto <https://github.com/althonos/pronto/>`_ is a high-performance parsing library
    for parsing obo format 1.4 and other formats.

    Input Selector
    --------------

    This adapter uses the ``pronto:`` :term:`Input Selector`; e.g.

    - ``pronto:path/to/my/file``
    - ``pronto:https://example.com/my/file``
    - ``prontolib:go`

    Examples
    --------
    >>> from oaklib.implementations import ProntoImplementation
    >>> resource = OntologyResource(slug='go-nucleus.obo', directory='tests/input', local=True)
    >>> adapter = ProntoImplementation(resource)

    Or use a selector:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("pronto:tests/input/go-nucleus.obo")

    Then you can use any of the methods implemented by pronto

    >>> rels = adapter.relationships(['GO:0005773'])
    >>> for _s, p, o in rels:
    ...    print(f'  {p} {o} ! {adapter.label(o)}')
    rdfs:subClassOf GO:0043231 ! intracellular membrane-bounded organelle
    BFO:0000050 GO:0005737 ! cytoplasm

    .. warning::

       pronto uses the fastobo library for loading ontologies. This follows a strict
       interpretation of obo format, and some ontologies may fail to load.
       In these cases, consider an alternative implementation

    Alternatives:

    - use the :ref:`simple_obo_implementation`
    - convert to an OWL representation using ROBOT
    - convert to a JSON representation using ROBOT and use :ref:`obograph_implementation`

    """

    wrapped_ontology: Ontology = None
    _relationship_index_cache: Dict[CURIE, List[RELATIONSHIP]] = None
    _alt_id_to_replacement_map: Dict[CURIE, List[CURIE]] = None

    def __post_init__(self):
        if self.wrapped_ontology is None:
            resource = self.resource
            logging.info(f"Pronto using resource: {resource}")
            kwargs = {}
            if resource and resource.import_depth is not None:
                kwargs["import_depth"] = resource.import_depth
            if resource is None:
                ontology = Ontology()
            elif resource.local:
                if resource.local_path:
                    ontology = Ontology(str(resource.local_path), **kwargs)
                else:
                    ontology = Ontology()
            else:
                ontology = Ontology.from_obo_library(resource.slug, **kwargs)
            self.wrapped_ontology = ontology
            for prefix, expansion in ontology.metadata.idspaces.items():
                self.prefix_map()[prefix] = expansion[0]

    @classmethod
    @deprecated("old style")
    def create(cls, resource: OntologyResource = None) -> "ProntoImplementation":
        return ProntoImplementation(resource=resource)

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        for s in self.entities(filter_obsoletes=False):
            term = self._entity(s)
            if isinstance(term, Term):
                # only "Terms" in pronto have relationships
                for o in term.superclasses(distance=1):
                    if o.id != s:
                        yield s, IS_A, o.id
                for rel_type, parents in term.relationships.items():
                    p = self._get_pronto_relationship_type_curie(rel_type)
                    try:
                        for o in parents:
                            yield s, p, o.id
                    except KeyError:
                        pass
                if term.equivalent_to:
                    for o in term.equivalent_to.ids:
                        # symmetric
                        yield s, EQUIVALENT_CLASS, o
                        yield o, EQUIVALENT_CLASS, s

    def _all_entailed_relationships(self):
        reasoner = RelationGraphReasoner(self)
        yield from reasoner.entailed_edges()

    def store(self, resource: OntologyResource = None) -> None:
        if resource is None:
            resource = self.resource
        ontology = self.wrapped_ontology
        if resource.local:
            if resource.slug:
                with open(str(resource.local_path), "wb") as f:
                    ontology.dump(f, format=resource.format)
            else:
                ontology.dump(sys.stdout.buffer, format=resource.format)
        else:
            raise NotImplementedError(f"Cannot dump to {resource}")

    def load_graph(self, graph: Graph, replace: True) -> None:
        if replace:
            converter = OboGraphToOboFormatConverter()
            gd = GraphDocument(graphs=[graph])
            io = converter.as_bytes_io(gd)
            ont = Ontology(io)
            self.wrapped_ontology = ont
            self._relationship_index_cache = None
            self._alt_id_to_replacement_map = None
            return
        for n in graph.nodes:
            if n.id == IS_A:
                pass
            else:
                self.create_entity(n.id, n.lbl, type=n.type)
        for e in graph.edges:
            self.add_relationship(e.sub, e.pred, e.obj)

    @deprecated("Use this when we fix https://github.com/fastobo/fastobo/issues/42")
    def load_graph_using_jsondoc(self, graph: Graph, replace: True) -> None:
        tf = tempfile.NamedTemporaryFile()
        tf_name = "/tmp/tf.json"  # noqa
        gd = GraphDocument(graphs=[graph])
        json_dumper.dump(gd, to_file=tf_name)
        tf.flush()
        ont = Ontology(tf_name)
        if replace:
            self.wrapped_ontology = ont
        else:
            raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _entity(self, curie: CURIE, strict=False):
        for r in self.wrapped_ontology.relationships():
            # TODO: use OboLegacyInterface
            # see https://owlcollab.github.io/oboformat/doc/obo-syntax.html#4.4.1
            # pronto gives relations shorthand IDs for RO and BFO, as it is providing
            # oboformat as a level of abstraction. We want to map these back to the CURIEs
            if r.id == curie:
                return r
            if curie.startswith("RO:") or curie.startswith("BFO:"):
                if any(x for x in r.xrefs if x.id == curie):
                    return r
        if curie in self.wrapped_ontology:
            return self.wrapped_ontology[curie]
        else:
            if strict:
                raise ValueError(f"No such CURIE: {curie}")
            return None

    def _create(self, curie: CURIE, exist_ok=True):
        if curie in self.wrapped_ontology:
            return self.wrapped_ontology[curie]
        else:
            return self.wrapped_ontology.create_term(curie)

    def _create_pred(self, curie: CURIE, exist_ok=True):
        if curie in self.wrapped_ontology.relationships():
            return self.wrapped_ontology.get_relationship(curie)
        else:
            return self.wrapped_ontology.create_relationship(curie)

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.terms():
            if filter_obsoletes and t.obsolete:
                continue
            if owl_type and owl_type != OWL_CLASS:
                continue
            yield t.id
        # note what Pronto calls "relationship" is actually "relationship type"
        for t in self.wrapped_ontology.relationships():
            if filter_obsoletes and t.obsolete:
                continue
            if owl_type and owl_type != OWL_OBJECT_PROPERTY:
                continue
            curie = self._get_pronto_relationship_type_curie(t)
            yield curie
        for t in self.wrapped_ontology.synonym_types():
            if owl_type and owl_type != OIO_SYNONYM_TYPE_PROPERTY:
                continue
            yield t.id
        for t in self.wrapped_ontology.metadata.subsetdefs:
            if owl_type and owl_type != OIO_SUBSET_PROPERTY:
                continue
            yield t.name
        if not owl_type or owl_type == OWL_CLASS:
            # note that in the case of alt_ids, metadata such as
            # original owl_type is lost. We assume that the original
            # owl_type was OWL_CLASS
            if not filter_obsoletes:
                for s in self._get_alt_id_to_replacement_map().keys():
                    yield s

    def ontologies(self) -> Iterable[CURIE]:
        yield self.wrapped_ontology.metadata.ontology

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
        m = {}
        meta = self.wrapped_ontology.metadata
        ont_id = meta.ontology
        if meta.data_version:
            m[OWL_VERSION_INFO] = [f"obo:{ont_id}/{meta.data_version}{ont_id}.owl"]
        return m

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CURIE]]:
        subset_names = [s.name for s in self.wrapped_ontology.metadata.subsetdefs]
        syntype_ids = [s.id for s in self.wrapped_ontology.synonym_types()]
        for curie in entities:
            if curie in self.wrapped_ontology.terms():
                yield curie, OWL_CLASS
            elif curie in self.wrapped_ontology.relationships():
                yield curie, OWL_OBJECT_PROPERTY
            elif curie in syntype_ids:
                yield curie, OIO_SYNONYM_TYPE_PROPERTY
            elif curie in subset_names:
                yield curie, OIO_SUBSET_PROPERTY
            else:
                yield curie, None

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.terms():
            if t.obsolete:
                yield t.id
        # note what Pronto calls "relationship" is actually "relationship type"
        for t in self.wrapped_ontology.relationships():
            if t.obsolete:
                yield t.id
        if include_merged:
            for a in self._get_alt_id_to_replacement_map().keys():
                yield a

    def subsets(self) -> Iterable[CURIE]:
        reported = set()
        for s in self.wrapped_ontology.metadata.subsetdefs:
            reported.add(s.name)
            yield s.name
        # also yield implicit subsets
        subsets = set()
        for t in self.wrapped_ontology.terms():
            subsets.update(t.subsets)
        for subset in subsets:
            if subset not in reported:
                yield subset

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.terms():
            if subset in t.subsets:
                yield t.id

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> str:
        t = self._entity(curie)
        if t:
            return t.name
        else:
            if curie == IS_A:
                return "subClassOf"
            else:
                return None

    def set_label(self, curie: CURIE, label: str, lang: Optional[LANGUAGE_TAG] = None) -> bool:
        t = self._entity(curie)
        if t:
            curr = t.name
            if curr != label:
                t.name = label
                return True
            else:
                return False
        else:
            raise ValueError(f"No such ID: {curie}")

    def curies_by_label(self, label: str) -> List[CURIE]:
        return [t.id for t in self.wrapped_ontology.terms() if t.name == label]

    def _get_pronto_relationship_type_curie(self, rel_type: pronto.Relationship) -> CURIE:
        for x in rel_type.xrefs:
            if x.id.startswith("BFO:") or x.id.startswith("RO:"):
                return x.id
        for x in rel_type.xrefs:
            if x.id.startswith("http"):
                compacted = self.uri_to_curie(x.id)
                return compacted
        return rel_type.id

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

    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for _s, p, o in self.relationships([curie], predicates, include_entailed=entailed):
            yield p, o

    def create_entity(
        self,
        curie: CURIE,
        label: Optional[str] = None,
        relationships: Optional[RELATIONSHIP_MAP] = None,
        type: Optional[str] = None,
        replace=False,
    ) -> CURIE:
        ont = self.wrapped_ontology
        t = self._entity(curie, False)
        if t:
            if replace:
                t = None
        if not t:
            if not type or type == "CLASS":
                t = ont.create_term(curie)
            elif type == "PROPERTY":
                t = ont.create_relationship(curie)
            else:
                raise ValueError(f"Pronto cannot handle type of {type} for {curie}")
        t.name = label
        if relationships:
            for pred, fillers in relationships.items():
                for filler in fillers:
                    self.add_relationship(curie, pred, filler)
        logging.info(f"Created: {curie}")
        return curie

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE):
        t = self._entity(curie)
        filler_term = self._create(filler)
        if predicate == IS_A:
            t.superclasses().add(filler_term)
        else:
            predicate_term = self._create_pred(predicate)
            if predicate_term not in t.relationships.keys():
                t.relationships[predicate_term] = []
            t.relationships[predicate_term].add(filler_term)
        self._clear_relationship_index()

    def remove_relationship(self, curie: CURIE, predicate: Optional[PRED_CURIE], filler: CURIE):
        t = self._entity(curie)
        filler_term = self._entity(filler)
        if not predicate or predicate == IS_A:
            t.superclasses().remove(filler_term)
        else:
            predicate_term = self._create_pred(predicate)
            t.relationships[predicate_term].remove(filler_term)
        self._clear_relationship_index()

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        e = self._entity(curie)
        return str(e.definition) if e and e.definition else None

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[DEFINITION]:
        for curie in curies:
            e = self._entity(curie)
            if not e:
                continue
            defn = e.definition
            if not defn and not include_missing:
                continue
            metadata = {}
            if include_metadata:
                metadata[HAS_DBXREF] = []
                for x in defn.xrefs:
                    metadata[HAS_DBXREF].append(x.id)
            yield curie, defn, metadata

    def comments(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        for curie in curies:
            e = self._entity(curie)
            if e:
                yield curie, e.comment

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        t = self._entity(curie)
        if t is None:
            return {}
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [t.name]
        for s in t.synonyms:
            pred = _synonym_scope_pred(s)
            m[pred].append(s.description)
        return m

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        t = self._entity(curie)
        if t is None:
            return
        for s in t.xrefs:
            yield HAS_DBXREF, s.id
        for s in t.annotations:
            rel = self._entity(s.property)
            if ":" in s.property:
                pred = s.property
            else:
                pred = self._get_pronto_relationship_type_curie(rel)
            if pred in SKOS_MATCH_PREDICATES:
                if isinstance(s, LiteralPropertyValue):
                    v = s.literal
                    yield pred, v
                elif isinstance(s, ResourcePropertyValue):
                    yield pred, s.resource
        if isinstance(t, Term):
            for rel_type, parents in t.relationships.items():
                pred = self._get_pronto_relationship_type_curie(rel_type)
                if pred in SKOS_MATCH_PREDICATES:
                    for parent in parents:
                        yield pred, parent.id

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        t = self._entity(curie)
        m = defaultdict(list)
        _alt_id_map = self._get_alt_id_to_replacement_map()
        if t:
            for ann in t.annotations:
                if isinstance(ann, LiteralPropertyValue):
                    m[ann.property].append(ann.literal)
                elif isinstance(ann, ResourcePropertyValue):
                    m[ann.property].append(ann.resource)
            if t.replaced_by:
                for x in t.replaced_by:
                    m[TERM_REPLACED_BY].append(x.id)
            if t.consider:
                for x in t.consider:
                    m[CONSIDER_REPLACEMENT].append(x.id)
            if t.obsolete:
                m[DEPRECATED_PREDICATE].append(True)
            if t.namespace:
                m[HAS_OBO_NAMESPACE].append(t.namespace)
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
                t = self._entity(e)
                if t and t.alternate_ids:
                    for a in t.alternate_ids:
                        self._alt_id_to_replacement_map[a].append(e)
        return self._alt_id_to_replacement_map

    def create_subontology(self, curies: List[CURIE]) -> "ProntoImplementation":
        subontology = Ontology()
        for curie in curies:
            t = self._entity(curie)
            subontology.create_term(curie)
            t2 = subontology[curie]
            t2.name = t.name
            # TODO - complete object
        return ProntoImplementation(wrapped_ontology=subontology)

    def clone(self, resource: Any) -> None:
        shutil.copyfile(self.resource.slug, resource.slug)
        return type(self)(resource)

    def dump(
        self, path: str = None, syntax: str = "obo", enforce_canonical_ordering=False, **kwargs
    ):
        if syntax is None:
            syntax = "obo"
        if syntax in ["obo", "json"]:
            if enforce_canonical_ordering:
                raise NotImplementedError("enforce_canonical_ordering not implemented for pronto")
            # TODO: simplify the logic here; not clear why pronto wants a binary file
            if isinstance(path, str):
                with open(path, "wb") as file:
                    self.wrapped_ontology.dump(file, format=syntax)
            else:
                if path == sys.stdout:
                    print(self.wrapped_ontology.dumps(format=syntax))
                else:
                    self.wrapped_ontology.dump(path, format=syntax)
        else:
            super().dump(path, syntax, **kwargs)

    def save(
        self,
    ):
        logging.info("Committing and flushing changes")
        self.dump(self.resource.slug)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[sssom.Mapping]:
        if isinstance(curies, CURIE):
            curies = [curies]
        elif curies is None:
            curies = list(self.entities())
        else:
            curies = list(curies)
        # mappings where curie is the subject:
        for curie in curies:
            for pred, obj in self.simple_mappings_by_curie(curie):
                m = sssom.Mapping(
                    subject_id=curie,
                    predicate_id=pred,
                    object_id=obj,
                    mapping_justification=sssom.EntityReference(SEMAPV.UnspecifiedMatching.value),
                )
                inject_mapping_sources(m)
                if source and m.object_source != source and m.subject_source != source:
                    continue
                yield m
        # mappings where curie is the object:
        # TODO: use a cache to avoid re-calculating
        for e in self.entities():
            t = self._entity(e)
            if t:
                for x in t.xrefs:
                    if x.id in curies:
                        m = sssom.Mapping(
                            subject_id=e,
                            predicate_id=HAS_DBXREF,
                            object_id=x.id,
                            mapping_justification=sssom.EntityReference(
                                SEMAPV.UnspecifiedMatching.value
                            ),
                        )
                        inject_mapping_sources(m)
                        if source and m.object_source != source and m.subject_source != source:
                            continue
                        yield m

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False, include_metadata=False) -> obograph.Node:
        t = self._entity(curie)
        if t is None:
            return obograph.Node(id=curie)
        else:
            meta = obograph.Meta()
            if isinstance(t, pronto.Relationship):
                t_id = self._get_pronto_relationship_type_curie(t)
                typ = "PROPERTY"
            else:
                t_id = t.id
                typ = "CLASS"
            if include_metadata:
                if t.definition:
                    defn_xrefs = [x.id for x in t.definition.xrefs]
                    meta.definition = obograph.DefinitionPropertyValue(
                        val=t.definition, xrefs=defn_xrefs
                    )
                if t.xrefs:
                    meta.xrefs = [obograph.XrefPropertyValue(val=x.id) for x in t.xrefs]
                if t.subsets:
                    meta.subsets = [x for x in t.subsets]
                if isinstance(t, pronto.Relationship):
                    for x in t.xrefs:
                        if x.id.startswith("RO:") or x.id.startswith("BFO:"):
                            t_id = x.id
                for s in t.synonyms:
                    pred = SCOPE_TO_SYNONYM_PRED_MAP[s.scope].replace("oio:", "")
                    synonym_type = s.type.id if s.type else None
                    meta.synonyms.append(
                        obograph.SynonymPropertyValue(
                            val=s.description,
                            pred=pred,
                            synonymType=synonym_type,
                            xrefs=[x.id for x in s.xrefs],
                        )
                    )
            return obograph.Node(id=t_id, lbl=t.name, type=typ, meta=meta)

    def as_obograph(self, expand_curies=False) -> Graph:
        om = self.wrapped_ontology.metadata
        entities = set(self.entities(filter_obsoletes=False, owl_type=OWL_CLASS))
        # entities.extend(self.entities(filter_obsoletes=False, owl_type=OWL_OBJECT_PROPERTY))
        nodes = [self.node(curie) for curie in entities]
        nodes = [n for n in nodes if n.lbl or n.meta]
        edges = [
            Edge(sub=r[0], pred="is_a" if r[1] == IS_A else r[1], obj=r[2])
            for r in self.relationships()
        ]
        ldefs = list(self.logical_definitions(entities))
        graph_id = om.ontology
        if not graph_id:
            graph_id = self.resource.slug
        return Graph(id=graph_id, nodes=nodes, edges=edges, logicalDefinitionAxioms=ldefs)

    def synonym_property_values(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Iterator[Tuple[CURIE, obograph.SynonymPropertyValue]]:
        if isinstance(subject, CURIE):
            subject = [subject]
        for curie in subject:
            e = self._entity(curie)
            if e:
                for s in e.synonyms:
                    pred = _synonym_scope_pred(s).replace("oio:", "")
                    xrefs = [x.id for x in s.xrefs]
                    t = s.type.id if s.type else None
                    spv = obograph.SynonymPropertyValue(
                        pred=pred, val=s.description, xrefs=xrefs, synonymType=t
                    )
                    yield curie, spv

    def logical_definitions(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        **kwargs,
    ) -> Iterable[obograph.LogicalDefinitionAxiom]:
        if not subjects:
            subjects = self.entities()
        for s in subjects:
            term = self._entity(s)
            if term and term.intersection_of:
                ldef = obograph.LogicalDefinitionAxiom(definedClassId=s)
                for ix in term.intersection_of:
                    if isinstance(ix, Term):
                        ldef.genusIds.append(ix.id)
                    else:
                        (rel, filler) = ix
                        rel = self._get_pronto_relationship_type_curie(rel)
                        er = obograph.ExistentialRestrictionExpression(
                            propertyId=rel, fillerId=filler.id
                        )
                        ldef.restrictions.append(er)
                if logical_definition_matches(ldef, predicates=predicates, objects=objects):
                    yield ldef

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
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
        for t in self.wrapped_ontology.terms():
            logging.debug(f"T={t} // {config}")
            if (
                search_all
                or SearchProperty(SearchProperty.LABEL)
                or config.properties not in config.properties
            ):
                if t.name and mfunc(t.name):
                    matches.append(t.id)
                    logging.info(f"Name match to {t.id}")
                    continue
            if search_all or SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
                if mfunc(t.id):
                    matches.append(t.id)
                    logging.info(f"identifier match to {t.id}")
                    continue
            if (
                search_all
                or SearchProperty(SearchProperty.REPLACEMENT_IDENTIFIER) in config.properties
            ):
                if t.replaced_by:
                    for r in t.replaced_by:
                        if mfunc(t.id):
                            matches.append(r.id)
                            logging.info(f"replaced_by match to {t.id}")
                            continue
                if t.alternate_ids:
                    for a in t.alternate_ids:
                        if mfunc(a):
                            matches.append(t.id)
                            logging.info(f"alternate_id match to {t.id}")
                            continue
            if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
                for syn in t.synonyms:
                    if mfunc(syn.description):
                        logging.info(f"Syn match to {t.id}")
                        matches.append(t.id)
                        continue
            if search_all or SearchProperty(SearchProperty.MAPPED_IDENTIFIER) in config.properties:
                for x in t.xrefs:
                    if mfunc(x.id):
                        logging.info(f"Mapping match to {t.id}")
                        matches.append(t.id)
                        continue
        # if search_all or SearchProperty(SearchProperty.REPLACEMENT_IDENTIFIER) in config.properties:
        #    if search_term in self._get_alt_id_to_replacement_map():
        #        matches.append(self._get_alt_id_to_replacement_map()[search_term])
        for m in matches:
            yield m

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        pass

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: kgcl.Configuration = None,
        strict=False,
    ) -> Optional[kgcl.Change]:
        tidy_change_object(patch)
        if isinstance(patch, kgcl.NodeRename):
            self.set_label(patch.about_node, patch.new_value)
        elif isinstance(patch, kgcl.NodeObsoletion):
            t = self._entity(patch.about_node, strict=True)
            t.obsolete = True
            if isinstance(patch, kgcl.NodeObsoletionWithDirectReplacement):
                t.replaced_by = [self._entity(patch.has_direct_replacement)]
        elif isinstance(patch, kgcl.NodeDeletion):
            t = self._entity(patch.about_node, strict=True)
            raise NotImplementedError
        elif isinstance(patch, kgcl.NodeCreation):
            # TODO: decide which field to use in KGCL
            if patch.about_node:
                self.create_entity(patch.about_node, patch.name)
            else:
                self.create_entity(patch.node_id, patch.name)
        elif isinstance(patch, kgcl.SynonymReplacement):
            t = self._entity(patch.about_node, strict=True)
            for syn in t.synonyms:
                if syn.description == patch.old_value:
                    syn.description = patch.new_value
        elif isinstance(patch, kgcl.NewTextDefinition):
            t = self._entity(patch.about_node, strict=True)
            xrefs = t.definition.xrefs if t.definition else []
            t.definition = pronto.Definition(patch.new_value, xrefs=xrefs)
        elif isinstance(patch, kgcl.NodeTextDefinitionChange):
            t = self._entity(patch.about_node, strict=True)
            current = t.definition
            if patch.old_value and current != patch.old_value:
                msg = f"Definition mismatch: {current} != {patch.old_value}"
                if strict:
                    raise ValueError(msg)
                else:
                    logging.error(msg)
            else:
                xrefs = t.definition.xrefs if t.definition else []
                t.definition = pronto.Definition(patch.new_value, xrefs=xrefs)
        elif isinstance(patch, kgcl.NewSynonym):
            t = self._entity(patch.about_node, strict=True)
            # Get scope from patch.qualifier
            # rather than forcing all synonyms to be related.
            scope = str(patch.qualifier.value).upper() if patch.qualifier else "RELATED"
            t.add_synonym(description=patch.new_value, scope=scope)
        elif isinstance(patch, kgcl.AddNodeToSubset):
            t = self._entity(patch.about_node, strict=True)
            t.subsets = t.subsets.union({patch.in_subset})
        elif isinstance(patch, kgcl.RemoveNodeFromSubset):
            t = self._entity(patch.about_node, strict=True)
            t.subsets = t.subsets.difference({patch.in_subset})
        elif isinstance(patch, kgcl.EdgeCreation):
            self.add_relationship(patch.subject, patch.predicate, patch.object)
        elif isinstance(patch, kgcl.EdgeDeletion):
            self.remove_relationship(patch.subject, patch.predicate, patch.object)
        elif isinstance(patch, kgcl.RemoveSynonym):
            t = self._entity(patch.about_node, strict=True)
            synonym_to_remove = [
                syn for syn in t._data().synonyms if syn.description == patch.old_value
            ][0]
            t._data().synonyms.discard(synonym_to_remove)
        else:
            raise NotImplementedError(f"cannot handle KGCL type {type(patch)}")
        return patch

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OwlInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def transitive_object_properties(self) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.relationships():
            if t.transitive:
                yield self._get_pronto_relationship_type_curie(t)

    def simple_subproperty_of_chains(self) -> Iterable[Tuple[CURIE, List[CURIE]]]:
        for t in self.wrapped_ontology.relationships():
            try:
                if t.holds_over_chain:
                    subp = self._get_pronto_relationship_type_curie(t)
                    r1, r2 = t.holds_over_chain
                    p1 = self._get_pronto_relationship_type_curie(r1)
                    p2 = self._get_pronto_relationship_type_curie(r2)
                    yield subp, [p1, p2]
            except KeyError as e:
                logging.warning(f"could not find chain relationships for {t}: {e}")
