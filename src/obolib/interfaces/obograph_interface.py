from abc import ABC
from typing import Dict, List, Tuple, Iterable, Union, Iterator

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, RELATIONSHIP
from obolib.types import CURIE, LABEL, URI, PRED_CURIE
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.vocabulary.obograph import Node, Graph, Edge


class OboGraphInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides an Object Oriented view of an ontology, following the OBO Graph Datamodel

    See `OBOGraphs <https://github.com/geneontology/obographs>_`

    Key datamodel concepts:

    - :class:`.Node` - any named ontology element
    - :class:`.Edge` - any relationship between elements; for example between "finger" and "hand"
    - :class:`.Graph` - a collection of nodes, edges, and other ontology components

    This datamodel conceives of an ontology as a graph
    """

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

    def node(self, curie: CURIE, strict=False) -> Node:
        """
        Look up a node object by CURIE

        :param curie:
        :param strict:
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
        graph_id = 'test'
        return Graph(id=graph_id,
                     nodes=list(node_map.values()),
                     edges=edges)

    def ancestor_graph(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Graph:
        """
        Return a graph object that consists of all the nodes specified in the start_curies list,
        extended with an interactive walk up the graph following all relationships (optionally filtered by the predicate
        list)

        :param start_curies:
        :param predicates: if supplied then only follow edges with these predicates
        :return: ancestor graph
        """
        return self._graph(walk_up(self, start_curies, predicates=predicates))

    def as_obograph(self) -> Graph:
        """
        Convert entire resource to an OBO Graph object

        .. warning ::

           some remote resources may choose to throw a NotImplementedError if it is impractical
           to download the entire ontology as a graph
        :return:
        """
        raise NotImplementedError








