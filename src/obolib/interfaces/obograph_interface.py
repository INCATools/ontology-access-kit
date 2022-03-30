from abc import ABC
from typing import Dict, List, Tuple, Iterable, Union, Iterator

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, RELATIONSHIP
from obolib.types import CURIE, LABEL, URI, PRED_CURIE
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.vocabulary.obograph import Node, Graph, Edge


class OboGraphInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides an Object Oriented view of an ontology, following the OBO Graph Datamodel
    """

    def nodes(self) -> Iterator[Node]:
        raise NotImplementedError

    def edges(self) -> Iterator[Edge]:
        raise NotImplementedError

    def node(self, curie: CURIE) -> Node:
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
        graph_id = 'test'
        return Graph(id=graph_id,
                     nodes=list(node_map.values()),
                     edges=edges)

    def ancestor_graph(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Graph:
        return self._graph(walk_up(self, start_curies, predicates=predicates))








