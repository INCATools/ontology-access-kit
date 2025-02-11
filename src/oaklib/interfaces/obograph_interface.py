import logging
from abc import ABC
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from sssom.constants import RDFS_SUBCLASS_OF, RDFS_SUBPROPERTY_OF

from oaklib.datamodels.obograph import (
    DisjointClassExpressionsAxiom,
    Edge,
    Graph,
    LogicalDefinitionAxiom,
    Node,
    SynonymPropertyValue,
)
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.basic_ontology_interface import (
    RELATIONSHIP,
    BasicOntologyInterface,
)
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.relationship_walker import walk_down, walk_up
from oaklib.utilities.obograph_utils import shortest_paths

GRAPH_PATH = Tuple[CURIE, CURIE, CURIE]


class Distance(Enum):
    """
    Specifies how many hops to walk in any given direction.
    """

    ZERO = "zero"
    DIRECT = "direct"
    TRANSITIVE = "transitive"


class GraphTraversalMethod(Enum):
    """
    Specifies a strategy for computing graph relationships.
    """

    HOP = "HOP"
    ENTAILMENT = "ENTAILMENT"


def _edges_to_nodes(
    start_curies: Union[CURIE, List[CURIE]], edges: List[Edge], reflexive=True
) -> Iterable[CURIE]:
    node_ids = set()
    for edge in edges:
        node_ids.update([edge.sub, edge.obj])
    if not isinstance(start_curies, list):
        start_curies = [start_curies]
    node_ids.update(start_curies)
    for node_id in node_ids:
        if not reflexive and node_id in start_curies:
            continue
        yield node_id


@dataclass
class TraversalConfiguration:
    """
    Specifies how to walk up and down a graph
    """

    predicates: List[PRED_CURIE] = None
    up_distance: Distance = field(default_factory=lambda: Distance.TRANSITIVE)
    down_distance: Distance = field(default_factory=lambda: Distance.TRANSITIVE)


@dataclass
class EdgeTemplate:
    subject_nodes: Optional[List[CURIE]] = None
    predicates: Optional[List[PRED_CURIE]] = None
    object_nodes: Optional[List[CURIE]] = None
    inverted: bool = field(default=False)
    entailed: bool = field(default=False)


class OboGraphInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides an Object Oriented view of an ontology, following the OBO Graph Datamodel

    See `OBOGraphs <https://github.com/geneontology/obographs>`_

    Key datamodel concepts:

    - :class:`obograph.Node` - any named ontology element
    - :class:`obograph.Edge` - any relationship between elements; for example between "finger" and "hand"
    - :class:`obograph.Graph` - a collection of nodes, edges, and other ontology components

    This datamodel conceives of an ontology as a graph
    """

    transitive_query_cache: Dict[Any, Any] = None

    def enable_transitive_query_cache(self):
        """
        Cache transitive queries
        """
        self.transitive_query_cache = {}

    def disable_transitive_query_cache(self):
        """
        Do not cache transitive queries (default)
        """
        self.transitive_query_cache = None

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[Node]:
        """
        Look up a node object by CURIE

        :param curie: identifier of node
        :param strict: raise exception if node not found
        :param include_metadata: include detailed metadata
        :param expand_curies: if True expand CURIEs to URIs
        :return:
        """
        raise NotImplementedError

    def nodes(self, expand_curies=False) -> Iterator[Node]:
        """
        Yields all nodes in all graphs

        :param expand_curies: if True expand CURIEs to URIs
        :return:
        """
        for e in self.entities():
            yield self.node(e, include_metadata=True, expand_curies=expand_curies)

    def edges(self, expand_curies=False) -> Iterator[Edge]:
        """
        Yields all edges in all graphs.

        :param expand_curies: if True expand CURIEs to URIs
        :return:
        """
        for e in self.relationships():
            s, p, o = e
            is_isa = p == IS_A
            if expand_curies:
                s = self.curie_to_uri(s)
                p = self.curie_to_uri(p)
                o = self.curie_to_uri(o)
            if s is None or o is None:
                # skip any blank nodes
                logging.debug(f"Skipping: {e}")
            else:
                if is_isa:
                    p = "is_a"
                yield Edge(sub=s, pred=p, obj=o)

    def synonym_property_values(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Iterator[Tuple[CURIE, SynonymPropertyValue]]:
        raise NotImplementedError

    def synonym_map_for_curies(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Dict[CURIE, List[SynonymPropertyValue]]:
        """
        Get a map of SynonymPropertyValue objects keyed by curie

        :param subject: curie or list of curies
        :return:
        """
        d = defaultdict(list)
        for curie, spv in self.synonym_property_values(subject):
            d[curie].append(spv)
        return d

    def _graph(self, triples: Iterable[RELATIONSHIP]) -> Graph:
        node_map: Dict[str, Node] = {}
        edges = []
        for s, p, o in triples:
            if s not in node_map:
                node_map[s] = self.node(s)
            if p not in node_map:
                p_node = self.node(p)
                if not p_node:
                    p_node = Node(p)
                p_node.type = "PROPERTY"
                node_map[p] = p_node
            if o not in node_map:
                node_map[o] = self.node(o)
            edges.append(Edge(sub=s, pred=p, obj=o))
        graph_id = "test"
        return Graph(id=graph_id, nodes=list(node_map.values()), edges=edges)

    def direct_graph(
        self,
        curies: Union[CURIE, List[CURIE]],
        **kwargs,
    ) -> Graph:
        """
        Return a graph object that consists of all the nodes specified in the curies list,
        extended with all direct relationships

        :param curies:
        :return: direct graph
        """
        if not isinstance(curies, list):
            curies = [curies]
        g = self._graph(self.relationships(subjects=curies))
        for curie in curies:
            n = self.node(curie, include_metadata=True)
            if n:
                g.nodes.append(n)
        ldefs = list(self.logical_definitions(curies))
        g.logicalDefinitionAxioms = ldefs
        return g

    def ancestor_graph(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        method: Optional[GraphTraversalMethod] = None,
        **kwargs,
    ) -> Graph:
        """
        Return a graph object that consists of all the nodes specified in the start_curies list,
        extended with an interactive walk up the graph following all relationships (optionally filtered by the predicate
        list)

        :param start_curies:
        :param predicates: if supplied then only follow edges with these predicates
        :return: ancestor graph
        """
        if method and method == GraphTraversalMethod.ENTAILMENT:
            ancs = self.ancestors(
                start_curies,
                predicates=predicates,
                method=method,
            )
            node_map = {}
            edges = []
            for s, p, o in self.relationships(
                subjects=ancs,
                predicates=predicates,
            ):
                node_map[s] = None
                node_map[o] = None
                edges.append(Edge(sub=s, pred=p, obj=o))
            labels = {k: v for k, v in self.labels(list(node_map.keys()))}
            for n in node_map.keys():
                node_map[n] = Node(n, lbl=labels.get(n), type="CLASS")
            g = Graph(id="ancestor_graph")
            g.nodes = list(node_map.values())
            g.edges = edges
            return g
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        key = (
            "ancestor_graph",
            tuple(start_curies),
            tuple(predicates if predicates is not None else ()),
        )
        if self.transitive_query_cache is not None:
            if key in self.transitive_query_cache:
                return self.transitive_query_cache[key]
        # this implements a traversal approach that iteratively walks up the graph;
        # this may be inefficient. It is recommended that different implementations
        # override this with a more efficient method that leverages cached tables
        logging.info(
            f"Computing ancestor graph for {start_curies} / {predicates} using graph walking"
        )
        logging.info(f"Walking up from {len(start_curies)} over {predicates}")
        g = self._graph(walk_up(self, start_curies, predicates=predicates, **kwargs))
        if self.transitive_query_cache is not None:
            self.transitive_query_cache[key] = g
        return g

    def descendant_graph(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Graph:
        """
        As ancestor graph, but in opposite direction

        :param start_curies:
        :param predicates: if supplied then only follow edges with these predicates
        :return: ancestor graph
        """
        key = (
            "descendant_graph",
            tuple(start_curies),
            tuple(predicates if predicates is not None else ()),
        )
        if self.transitive_query_cache is not None:
            if key in self.transitive_query_cache:
                return self.transitive_query_cache[key]
        g = self._graph(walk_down(self, start_curies, predicates=predicates))
        if self.transitive_query_cache is not None:
            self.transitive_query_cache[key] = g
        return g

    def non_redundant_entailed_relationships(
        self,
        predicates: List[PRED_CURIE] = None,
        **kwargs,
    ) -> Iterator[RELATIONSHIP]:
        """
        Yields all relationships that are directly entailed.

        See https://github.com/INCATools/ontology-access-kit/issues/739

        :param kwargs: same as relationships
        :return:
        """
        if "include_entailed" in kwargs:
            kwargs.pop("include_entailed")
        relationships = list(
            self.relationships(predicates=predicates, include_entailed=True, **kwargs)
        )
        rel_by_sp = defaultdict(list)
        for s, p, o in relationships:
            if s == o:
                continue
            rel_by_sp[(s, p)].append(o)
        for (s, p), objs in rel_by_sp.items():
            redundant_set = set()
            predicates_plus_isa = ([IS_A] + predicates) if predicates else None
            for o in objs:
                ancs = list(self.ancestors(o, predicates=predicates_plus_isa, reflexive=False))
                redundant_set.update(ancs)
            for o in objs:
                if o not in redundant_set:
                    yield s, p, o

    def ancestors(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Ancestors obtained from a walk starting from start_curies ending in roots, following only the specified
        predicates.

        .. note::

           This operation is reflexive: self is included

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include self
        :param method: HOP or ENTAILMENT
        :return: all ancestor CURIEs
        """
        if method and method == GraphTraversalMethod.ENTAILMENT:
            if isinstance(start_curies, str):
                start_curies = [start_curies]
            yielded = set()
            for rel in self.relationships(
                start_curies, predicates=predicates, include_entailed=True
            ):
                o = rel[2]
                if o not in yielded:
                    yield o
                    yielded.add(o)
        else:
            g = self.ancestor_graph(start_curies, predicates).edges
            yield from _edges_to_nodes(start_curies, g, reflexive)

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Descendants obtained from a walk downwards starting from start_curies
        ending in roots, following only the specified predicates.

        .. note::

           This operation is reflexive: self is included

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include self
        :param method:
        :return: all descendant CURIEs
        """
        if method and method == GraphTraversalMethod.ENTAILMENT:
            if isinstance(start_curies, str):
                start_curies = [start_curies]
            yielded = set()
            for rel in self.relationships(
                objects=start_curies, predicates=predicates, include_entailed=True
            ):
                s = rel[0]
                if s not in yielded:
                    yield s
                    yielded.add(s)
        else:
            g = self.descendant_graph(start_curies, predicates).edges
            yield from _edges_to_nodes(start_curies, g, reflexive)

    def descendant_count(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
    ) -> int:
        """
        Count of descendants.

        See :ref:`descendants` for more details.

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include self
        :return: count of distinct CURIEs
        """
        return len(set(self.descendants(start_curies, predicates, reflexive)))

    def subgraph_from_traversal(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        traversal: TraversalConfiguration = None,
    ) -> Graph:
        """
        Combines ancestors and descendants according to a traversal configuration.

        >>> from oaklib import get_adapter
        >>> from oaklib.interfaces.obograph_interface import TraversalConfiguration, Distance
        >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
        >>> # use an adapter to talk to an endpoint (here, sqlite)
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> # get a subgraph centered around these nodes
        >>> seeds = ["GO:0005634", "GO:0005773"] # nucleus, vacuole
        >>> # walk up the graph to get ancestors, and also get direct children
        >>> traversal = TraversalConfiguration(up_distance=Distance.TRANSITIVE, down_distance=Distance.DIRECT)
        >>> graph = adapter.subgraph_from_traversal(seeds, predicates=[IS_A, PART_OF], traversal=traversal)
        >>> len(graph.nodes)
        22
        >>> len(graph.edges)
        27

        :param start_curies:
        :param predicates:
        :param traversal:
        :return:
        """
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        if traversal is None:
            traversal = TraversalConfiguration()
        if traversal.up_distance == Distance.TRANSITIVE:
            logging.info(f"Getting ancestor graph from {type(self)}, start={start_curies}")
            up_graph = self.ancestor_graph(start_curies, predicates=predicates)
        elif traversal.up_distance == Distance.DIRECT:
            up_graph = self._graph(self.relationships(start_curies, predicates=predicates))
        else:
            up_graph = None
        if traversal.down_distance == Distance.TRANSITIVE:
            down_graph = self.descendant_graph(start_curies, predicates=predicates)
        elif traversal.down_distance == Distance.DIRECT:
            down_graph = self._graph(
                self.relationships(objects=start_curies, predicates=predicates)
            )
        else:
            down_graph = None
        g = self._merge_graphs([up_graph, down_graph])
        return g

    def extract_graph(
        self,
        entities: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        dangling=True,
        include_metadata=True,
    ) -> Graph:
        """
        Extract a subgraph from the graph that contains the specified entities and predicates.

        :param entities: entities to extract
        :param predicates: predicates to extract
        :param dangling: if true, include dangling nodes
        :return: subgraph
        """
        logging.info(f"Extracting using seed of {len(entities)} entities")
        nodes = [self.node(e, include_metadata=include_metadata) for e in entities]
        edges = []
        logging.info(f"extracting rels for {len(entities)} p={predicates} dangling={dangling}")
        used_predicates = set()
        for s, p, o in self.relationships(subjects=entities, predicates=predicates):
            if dangling or o in entities:
                edges.append(Edge(sub=s, pred=p, obj=o))
                if p not in [RDFS_SUBCLASS_OF, RDFS_SUBPROPERTY_OF]:
                    used_predicates.add(p)
        ontologies = list(self.ontologies())
        curr_id = ontologies[0]
        g = Graph(id=f"{curr_id}-transformed", nodes=nodes, edges=edges)
        for lda in self.logical_definitions(entities):
            if predicates:
                if any(r for r in lda.restrictions if r.propertyId not in predicates):
                    continue
            if not dangling:
                signature = set(lda.genusIds + [r.fillerId for r in lda.restrictions])
                if signature.difference(entities):
                    continue
            g.logicalDefinitionAxioms.append(lda)
            for r in lda.restrictions:
                used_predicates.add(r.propertyId)
        logging.info(f"Used predicates = {used_predicates}")
        pred_nodes = [self.node(e, include_metadata=include_metadata) for e in used_predicates]
        g.nodes.extend([n for n in pred_nodes if n])
        return g

    def relationships_to_graph(self, relationships: Iterable[RELATIONSHIP]) -> Graph:
        """
        Generates an OboGraph from a list of relationships

        :param relationships:
        :return:
        """
        relationships = list(relationships)
        node_ids = set()
        for rel in relationships:
            node_ids.update(list(rel))
        edges = [Edge(sub=s, pred=p, obj=o) for s, p, o in relationships]
        nodes = [self.node(id) for id in node_ids]
        return Graph(id="query", nodes=list(nodes), edges=edges)

    def walk_up_relationship_graph(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[RELATIONSHIP]:
        """
        Walks up the relation graph from a seed set of curies or individual curie, returning the full ancestry graph

        Note: this may be inefficient for remote endpoints, in future a graph walking endpoint will implement this

        :param start_curies:
        :param predicates:
        :return:
        """
        return walk_up(self, start_curies, predicates=predicates)

    def paths(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        target_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        predicate_weights: Dict[PRED_CURIE, float] = None,
        shortest=True,
        directed=False,
    ) -> Iterator[GRAPH_PATH]:
        """
        Returns all paths between sources and targets.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db", implements=OboGraphInterface)
        >>> for path in sorted(list(adapter.paths(["GO:0005634"], ["GO:0005773"]))):
        ...   print(path)
        ('GO:0005634', 'GO:0005773', 'GO:0005634')
        ('GO:0005634', 'GO:0005773', 'GO:0005773')
        ('GO:0005634', 'GO:0005773', 'GO:0043231')

        :param start_curies:
        :param start_curies:
        :param predicates:
        :param predicate_weights:
        :param shortest:
        :return:
        """
        if not shortest:
            raise NotImplementedError("Only shortest paths are supported")
        if isinstance(start_curies, CURIE):
            start_curies = [start_curies]
        if isinstance(target_curies, CURIE):
            target_curies = [target_curies]
        if target_curies is None:
            all_curies = start_curies
        else:
            all_curies = list(set(start_curies).union(set(target_curies)))
        graph = self.ancestor_graph(all_curies, predicates=predicates)
        logging.info("Calculating graph stats")
        for s, o, intermediates in shortest_paths(
            graph,
            start_curies,
            end_curies=target_curies,
            predicate_weights=predicate_weights,
            directed=directed,
        ):
            for intermediate in intermediates:
                yield s, o, intermediate

    def chains(
        self,
        edge_templates: List[EdgeTemplate],
        start_nodes: Optional[List[CURIE]] = None,
        exclude_nodes: Optional[List[CURIE]] = None,
        allow_cycles=False,
        **kwargs,
    ) -> Iterator[List[Edge]]:
        if not edge_templates:
            yield []
            return
        et = edge_templates[0]
        rest = edge_templates[1:]
        subjects = et.subject_nodes
        predicates = et.predicates
        objects = et.object_nodes
        # print(f"-- SN={start_nodes} SUBJS={subjects} PRED={predicates} OBJS={objects}")
        if start_nodes:
            if subjects:
                subjects = list(set(subjects).intersection(start_nodes))
            else:
                subjects = start_nodes
        if rest:
            if rest[0].subject_nodes:
                objects = list(set(objects).intersection(rest[0].subject_nodes))
        # print(f"ZZ {subjects} {predicates} {objects} // x={exclude_nodes}")
        for rel in self.relationships(
            subjects=subjects,
            predicates=predicates,
            objects=objects,
            include_entailed=et.entailed,
            invert=et.inverted,
        ):
            if exclude_nodes and rel[2] in exclude_nodes:
                continue
            new_exclude_nodes = None
            if not allow_cycles:
                if exclude_nodes is None:
                    new_exclude_nodes = []
                else:
                    new_exclude_nodes = copy(exclude_nodes)
                new_exclude_nodes.append(rel[0])
            e = Edge(*rel)
            # print(f".. Rest={rest} exclude={exclude_nodes} start={e.obj} // {rel}")
            for chain in self.chains(rest, start_nodes=[e.obj], exclude_nodes=new_exclude_nodes):
                yield [e] + chain

    def logical_definitions(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        **kwargs,
    ) -> Iterable[LogicalDefinitionAxiom]:
        """
        Yields all logical definitions for input subjects.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db", implements=OboGraphInterface)
        >>> for ldef in adapter.logical_definitions(["GO:0009892"]):
        ...     print(f"Genus: {adapter.label(ldef.genusIds[0])}")
        ...     for r in ldef.restrictions:
        ...         print(f"  Differentia: {adapter.label(r.propertyId)} SOME {adapter.label(r.fillerId)}")
        Genus: biological regulation
          Differentia: negatively regulates SOME metabolic process

        Leaving the subjects parameter as None will yield all logical definitions in the ontology.

        >>> len(list(adapter.logical_definitions()))
        50

        :param subjects: If specified, defined class must be in this set
        :param predicates: If specified, only yields logical definitions with these predicates
        :param objects: If specified, only yields logical definitions with genus or filler in this list

        :return:
        """
        return iter(())

    def disjoint_class_expressions_axioms(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Iterable[PRED_CURIE] = None,
        group=False,
        **kwargs,
    ) -> Iterable[DisjointClassExpressionsAxiom]:
        """
        Yields all disjoint class expressions.

        :param subjects: if present, filter to only those that reference these subjects
        :param predicates: if present, filter to only those that reference these predicates
        :param group: if True, group into cliques
        :param kwargs:
        :return:
        """
        return iter(())

    def add_metadata(self, graph: Graph) -> None:
        """
        Decorates the graph with meta objects on all nodes
        :param graph:
        :return:
        """
        graph.nodes = [self.node(n.id, include_metadata=True) for n in graph.nodes]

    def as_obograph(self, expand_curies=False) -> Graph:
        """
        Convert entire resource to an OBO Graph object

        .. warning ::

           some remote resources may choose to throw a NotImplementedError if it is impractical
           to download the entire ontology as a graph

        :param expand_curies:
        :return:
        """
        ontologies = list(self.ontologies())
        if len(ontologies) != 1:
            logging.warning(f"Could not determine a single ontology for: {ontologies}")
            ont_id = "TEMP"
        else:
            ont_id = list(ontologies)[0]
        ldefs = list(self.logical_definitions())
        logging.info(f"Found {len(ldefs)} logical definitions")
        g = Graph(
            id=ont_id,
            nodes=list(self.nodes(expand_curies=expand_curies)),
            edges=list(self.edges(expand_curies=expand_curies)),
            logicalDefinitionAxioms=ldefs,
        )
        return g

    def load_graph(self, graph: Graph, replace: True) -> None:
        """
        Loads a graph into the repository

        :param graph:
        :param replace:
        :return:
        """
        raise NotImplementedError

    def _merge_graphs(self, graphs: List[Optional[Graph]]) -> Graph:
        g = Graph(id="merged")
        node_ids = [n.id for n in g.nodes]
        for src in graphs:
            if src is not None:
                for n in src.nodes:
                    if n.id not in node_ids:
                        g.nodes.append(n)
                        node_ids.append(n.id)
        for src in graphs:
            if src is not None:
                g.edges += src.edges
        return g
