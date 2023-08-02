import logging
import re
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

import sssom_schema as sssom
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import json_loader

from oaklib.converters.obo_graph_to_rdf_owl_converter import SCOPE_MAP
from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import (
    Edge,
    Graph,
    GraphDocument,
    LogicalDefinitionAxiom,
    Meta,
    Node,
)
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    INVERSE_OF,
    IS_A,
    LABEL_PREDICATE,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    SUBPROPERTY_OF,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    LANGUAGE_TAG,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE, URI
from oaklib.utilities.axioms.logical_definition_utilities import (
    logical_definition_matches,
)
from oaklib.utilities.basic_utils import pairs_as_dict

RDFLIB_FORMAT_MAP = {
    "ttl": "ttl",
    "n3": "n3",
    "rdfxml": "xml",
    "xml": "xml",
    "owl": "xml",
}


@dataclass
class OboGraphImplementation(
    ValidatorInterface,
    DifferInterface,
    RdfInterface,
    OboGraphInterface,
    SearchInterface,
    PatcherInterface,
    DumperInterface,
    MergeInterface,
):
    """
    OBO Graphs JSON backed implementation.

    This implementation works off of an in-memory GraphDocument object.

    To use:

    .. packages :: python

    >>> from oaklib import get_adapter
    >>> oi = get_adapter('obograph:tests/input/go-nucleus.json')
    >>> for node_id in oi.entities():
    ...     print(node_id, oi.label(node_id))
    <BLANKLINE>
    ...
    GO:0043226 organelle
    ...
    """

    obograph_document: GraphDocument = None
    _relationship_index_cache: Dict[CURIE, List[RELATIONSHIP]] = None

    def __post_init__(self):
        if self.obograph_document is None:
            resource = self.resource
            if resource and resource.local_path:
                gd = json_loader.load(str(resource.local_path), target_class=GraphDocument)
            else:
                gd = GraphDocument()
            self.obograph_document = gd

    def uri_to_curie(
        self, uri: URI, strict: bool = False, use_uri_fallback=True
    ) -> Optional[CURIE]:
        # TODO: use a map
        if uri == "is_a":
            return IS_A
        elif uri == "subPropertyOf":
            return SUBPROPERTY_OF
        elif uri == "inverseOf":
            return INVERSE_OF
        elif uri == EQUIVALENT_CLASS:
            return EQUIVALENT_CLASS
        else:
            return super().uri_to_curie(uri, strict=strict, use_uri_fallback=use_uri_fallback)

    def store(self, resource: OntologyResource = None) -> None:
        if resource is None:
            resource = self.resource
        od = self.obograph_document
        if resource.local:
            if resource.slug:
                json_dumper.dump(od, resource.slug)
            else:
                print(json_dumper.dumps(od))
        else:
            raise NotImplementedError(f"Cannot dump to {resource}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _tuple_to_curies(self, t: Tuple) -> Tuple:
        return tuple([self.uri_to_curie(x) for x in t])

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        logging.info("Commencing indexing")
        od = self.obograph_document
        for g in od.graphs:
            for e in g.edges:
                yield self._tuple_to_curies((e.sub, e.pred, e.obj))
            for ens in g.equivalentNodesSets:
                for n1 in ens.nodeIds:
                    for n2 in ens.nodeIds:
                        if n1 != n2:
                            # directionality is lost in OboGraph representation
                            yield self._tuple_to_curies((n1, EQUIVALENT_CLASS, n2))

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        od = self.obograph_document
        for g in od.graphs:
            for n in g.nodes:
                if filter_obsoletes and n.meta and n.meta.deprecated:
                    continue
                if owl_type:
                    t = n.type
                    if t:
                        if t == "CLASS" and owl_type != OWL_CLASS:
                            continue
                        if t == "PROPERTY" and owl_type != OWL_OBJECT_PROPERTY:
                            continue
                yield self.uri_to_curie(n.id)

    def obsoletes(self) -> Iterable[CURIE]:
        od = self.obograph_document
        for g in od.graphs:
            for n in g.nodes:
                if n.meta.deprecated:
                    yield n.id

    # TODO: abstract into separate standalone package
    def _get_subset_curie(self, curie: str) -> str:
        if "#" in curie:
            return curie.split("#")[-1]
        else:
            return curie

    def _node_subsets(self, node: Node) -> List[SUBSET_CURIE]:
        if node.meta:
            return [self._get_subset_curie(s) for s in node.meta.subsets]
        else:
            return []

    def _entire_graph(self) -> Graph:
        if len(self.obograph_document.graphs) > 1:
            raise ValueError("Multiple graphs")
        return self.obograph_document.graphs[0]

    def _nodes(self) -> Iterator[Node]:
        for g in self.obograph_document.graphs:
            for n in g.nodes:
                yield n

    def _node(self, curie: CURIE, strict=False) -> Optional[Node]:
        node: Optional[Node] = None
        for g in self.obograph_document.graphs:
            for n in g.nodes:
                # TODO: make this more efficient
                if self.uri_to_curie(n.id) == curie:
                    # handle duplicates
                    if node:
                        if node.lbl:
                            if strict:
                                raise ValueError(f"Multiple nodes with id {curie}")
                        else:
                            # previously encountered node was dangling/stub;
                            # replace
                            node = n
                    else:
                        node = n
        if node:
            node = deepcopy(node)
            node.id = self.uri_to_curie(node.id)
            return node
        else:
            if strict:
                raise ValueError(f"No such node {curie}")

    def _meta(self, curie: CURIE, strict=False) -> Optional[Meta]:
        n = self._node(curie, strict=strict)
        if n:
            return n.meta

    def ontologies(self) -> Iterable[CURIE]:
        return [g.id for g in self.obograph_document.graphs]

    def subsets(self) -> Iterable[CURIE]:
        raise NotImplementedError

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        od = self.obograph_document
        for g in od.graphs:
            for n in g.nodes:
                if subset in self._node_subsets(n):
                    yield n

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError("Language tags not supported")
        if curie == IS_A:
            return "subClassOf"
        n = self._node(curie)
        if n:
            return n.lbl

    def set_label(self, curie: CURIE, label: str, lang: Optional[LANGUAGE_TAG] = None) -> bool:
        if lang:
            raise NotImplementedError("Language tags not supported")
        n = self._node(curie, True)
        n.lbl = label
        return True

    def curies_by_label(self, label: str) -> List[CURIE]:
        return [self.uri_to_curie(n.id) for n in self._nodes() if n.lbl == label]

    def create_entity(
        self,
        curie: CURIE,
        label: Optional[str] = None,
        relationships: Optional[RELATIONSHIP_MAP] = None,
        type: Optional[str] = None,
        **kwargs,
    ) -> CURIE:
        g = self._entire_graph()
        g.nodes.append(Node(curie, lbl=label, type=type))
        for p, objs in relationships:
            for obj in objs:
                g.edges.append(Edge(curie, p, obj))
        return curie

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError("Language tags not supported")
        m = self._meta(curie)
        if m:
            return m.definition.val

    def comments(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        for curie in curies:
            m = self._meta(curie)
            if m:
                for v in m.comments:
                    yield curie, v

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        meta = self._meta(curie)
        m = defaultdict(list)
        lbl = self.label(curie)
        if lbl:
            m[LABEL_PREDICATE] = [lbl]
        if meta is not None:
            for syn in meta.synonyms:
                pred = SCOPE_MAP.get(syn.pred, None)
                m[pred].append(syn.val)
        return m

    # TODO: DRY
    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        ei = self.edge_index
        if include_entailed:
            raise NotImplementedError("Entailment not supported for pronto")
        yield from ei.edges(
            subjects=subjects,
            predicates=predicates,
            objects=objects,
        )

    # TODO: DRY
    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for s, p, o in self.relationships([curie], predicates, include_entailed=entailed):
            if s == curie:
                yield p, o

    # TODO: DRY
    def outgoing_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.outgoing_relationships(*args, **kwargs))

    # TODO: DRY
    def incoming_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for s, p, o in self.relationships(None, predicates, [curie], include_entailed=entailed):
            if o == curie:
                yield p, s

    # TODO: DRY
    def incoming_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.incoming_relationships(*args, **kwargs))

    # TODO: DRY
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
        meta = self._meta(curie, strict=False)
        if meta:
            # TODO: SKOS
            for x in meta.xrefs:
                yield HAS_DBXREF, x.val

    def dump(self, path: str = None, syntax: str = "json", **kwargs):
        logging.info(f"Dumping graph to {path} syntax: {syntax}")
        if syntax == "json" or syntax == "obojson":
            if path is None:
                print(json_dumper.dumps(self.obograph_document))
            else:
                json_dumper.dump(self.obograph_document, to_file=str(path))
        else:
            super().dump(path, syntax, **kwargs)

    def save(
        self,
    ):
        logging.info("Committing and flushing changes")
        self.dump(self.resource.slug)

    def load_graph(self, graph: Graph, replace: True) -> None:
        if not replace:
            raise NotImplementedError
        self.obograph_document = GraphDocument(graphs=[graph])

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[sssom.Mapping]:
        raise NotImplementedError()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> obograph.Node:
        return self._node(curie)

    def as_obograph(self) -> Graph:
        return self._entire_graph()

    def logical_definitions(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        **kwargs,
    ) -> Iterable[LogicalDefinitionAxiom]:
        if subjects:
            subjects = list(subjects)
        for g in self.obograph_document.graphs:
            for ldef in g.logicalDefinitionAxioms:
                if logical_definition_matches(
                    ldef, subjects=subjects, predicates=predicates, objects=objects
                ):
                    yield ldef

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def different_from(self, entity: CURIE, other_ontology: DifferInterface) -> bool:
        raise NotImplementedError

    def migrate_curies(self, curie_map: Mapping[CURIE, CURIE]) -> None:
        raise NotImplementedError

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: kgcl.Configuration = None,
    ) -> kgcl.Change:
        raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OwlInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def transitive_object_properties(self) -> Iterable[CURIE]:
        # TODO: obographs datamodel needs to be expanded to support this
        pass

    def simple_subproperty_of_chains(self) -> Iterable[Tuple[CURIE, List[CURIE]]]:
        for g in self.obograph_document.graphs:
            for pca in g.propertyChainAxioms:
                yield self.uri_to_curie(pca.predicateId), [
                    self.uri_to_curie(p) for p in pca.chainPredicateIds
                ]
