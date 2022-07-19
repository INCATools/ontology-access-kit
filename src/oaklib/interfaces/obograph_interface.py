import logging
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, List, Optional, Union

from oaklib.datamodels.obograph import Edge, Graph, Node, SynonymPropertyValue
from oaklib.interfaces.basic_ontology_interface import (
    RELATIONSHIP,
    BasicOntologyInterface,
)
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.relationship_walker import walk_down, walk_up


class Distance(Enum):
    """
    Specifies how many hops to walk in any given direction
    """

    ZERO = "zero"
    DIRECT = "direct"
    TRANSITIVE = "transitive"


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

    def nodes(self) -> Iterator[Node]:
        """
        Iterator over all nodes in all graphs

        :return:
        """
        raise NotImplementedError

    def edges(self) -> Iterator[Edge]:
        """
        Iterator over all edges in all graphs

        :return:
        """
        raise NotImplementedError

    def node(self, curie: CURIE, strict=False, include_metadata=False) -> Node:
        """
        Look up a node object by CURIE

        :param curie: identifier of node
        :param strict: raise exception if node not found
        :param include_metadata: include detailed metadata
        :return:
        """
        raise NotImplementedError

    def synonym_property_values(self, subject: CURIE) -> List[SynonymPropertyValue]:
        return self.synonym_map_for_curies(subject)[subject]

    def synonym_map_for_curies(
        self, subject: Union[CURIE, List[CURIE]]
    ) -> Dict[CURIE, List[SynonymPropertyValue]]:
        """
        Get a map of SynonymPropertyValue objects keyed by curie

        :param subject: curie or list of curies
        :return:
        """
        raise NotImplementedError

    def _graph(self, triples: Iterable[RELATIONSHIP]) -> Graph:
        node_map: Dict[str, Node] = {}
        edges = []
        for s, p, o in triples:
            if s not in node_map:
                node_map[s] = self.node(s)
            if p not in node_map:
                node_map[p] = self.node(p)
            if o not in node_map:
                node_map[o] = self.node(o)
            edges.append(Edge(sub=s, pred=p, obj=o))
        graph_id = "test"
        return Graph(id=graph_id, nodes=list(node_map.values()), edges=edges)

    def ancestor_graph(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Graph:
        """
        Return a graph object that consists of all the nodes specified in the start_curies list,
        extended with an interactive walk up the graph following all relationships (optionally filtered by the predicate
        list)

        :param start_curies:
        :param predicates: if supplied then only follow edges with these predicates
        :return: ancestor graph
        """
        key = (
            "ancestor_graph",
            tuple(start_curies),
            tuple(predicates if predicates is not None else ()),
        )
        if self.transitive_query_cache is not None:
            if key in self.transitive_query_cache:
                return self.transitive_query_cache[key]
        g = self._graph(walk_up(self, start_curies, predicates=predicates))
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

    def ancestors(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
    ) -> Iterable[CURIE]:
        """
        Ancestors obtained from a walk starting from start_curies ending in roots, following only the specified
        predicates.

        .. note::

           This operation is reflexive: self is included

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include self
        :return: all ancestor CURIEs
        """
        return _edges_to_nodes(
            start_curies, self.ancestor_graph(start_curies, predicates).edges, reflexive
        )

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
    ) -> Iterable[CURIE]:
        """
        Descendants obtained from a walk downwards starting from start_curies
        ending in roots, following only the specified predicates.

        .. note::

           This operation is reflexive: self is included

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include self
        :return: all descendant CURIEs
        """
        return _edges_to_nodes(
            start_curies, self.descendant_graph(start_curies, predicates).edges, reflexive
        )

    def subgraph(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        traversal: TraversalConfiguration = None,
    ) -> Graph:
        """
        Combines ancestors and descendants according to a traversal configuration

        :param start_curies:
        :param predicates:
        :param traversal:
        :return:
        """
        if traversal is None:
            traversal = TraversalConfiguration()
        if traversal.up_distance == Distance.TRANSITIVE:
            logging.info(f"Getting ancestor graph from {type(self)}, start={start_curies}")
            up_graph = self.ancestor_graph(start_curies, predicates=predicates)
        else:
            up_graph = None
        if traversal.down_distance == Distance.TRANSITIVE:
            down_graph = self.descendant_graph(start_curies, predicates=predicates)
        else:
            down_graph = None
        g = self._merge_graphs([up_graph, down_graph])
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

    def add_metadata(self, graph: Graph) -> None:
        """
        Decorates the graph with meta objects on all nodes
        :param graph:
        :return:
        """
        graph.nodes = [self.node(n.id, include_metadata=True) for n in graph.nodes]

    def as_obograph(self) -> Graph:
        """
        Convert entire resource to an OBO Graph object

        .. warning ::

           some remote resources may choose to throw a NotImplementedError if it is impractical
           to download the entire ontology as a graph
        :return:
        """
        raise NotImplementedError

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
