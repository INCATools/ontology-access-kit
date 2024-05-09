from dataclasses import dataclass

from oaklib.datamodels.obograph import Graph
from oaklib.transformers.ontology_transformer import OntologyTransformer


@dataclass
class GraphTransformer(OntologyTransformer):
    """
    An ontology transformer that operates on a graph
    """

    remove_dangling_edges: bool = False
    """If true, removes edges that point to nodes that are not in the graph"""

    def transform(self, source_ontology: Graph, **kwargs) -> Graph:
        """
        Transforms a graph into an ontology

        :param graph:
        :return:
        """
        raise NotImplementedError

    def apply_remove_dangling_edges(self, graph: Graph):
        """
        Removes edges that point to nodes that are not in the graph.

        :param graph:
        :return:
        """
        node_ids = {n.id for n in graph.nodes}
        new_edges = []
        for edge in graph.edges:
            if edge.sub in node_ids and edge.obj in node_ids:
                new_edges.append(edge)
        return Graph(id=graph.id, nodes=graph.nodes, edges=new_edges)

    def _post_process(self, graph: Graph):
        if self.remove_dangling_edges:
            return self.apply_remove_dangling_edges(graph)
        else:
            return graph
