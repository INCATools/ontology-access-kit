from dataclasses import dataclass
from typing import Optional

from oaklib.datamodels.obograph import Graph
from oaklib.transformers.graph_transformer import GraphTransformer


@dataclass
class NodeFilterTransformer(GraphTransformer):
    """
    An ontology graph transformer that filters nodes
    """

    filter_function: Optional[callable] = None
    """A function that takes an Node and returns True if it should be included"""

    remove_dangling_edges: bool = False
    """If true, removes edges that point to nodes that are not in the graph"""

    def transform(self, source_ontology: Graph, **kwargs) -> Graph:
        """
        Filters Nodes from a graph.

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> from oaklib.transformers.node_filter_transformer import NodeFilterTransformer
        >>> from oaklib.datamodels.vocabulary import IS_A
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> graph = adapter.as_obograph()
        >>> transformer = NodeFilterTransformer(
        ...                 filter_function=lambda node: node.lbl.startswith("nuclear"),
        ...                 remove_dangling_edges=True)
        >>> filtered_graph = transformer.transform(graph)
        >>> sorted([n.lbl for n in filtered_graph.nodes])
        ['nuclear envelope', 'nuclear membrane', 'nuclear particle']

        :param graph:
        :return:

        """
        new_nodes = []
        for node in source_ontology.nodes:
            if self.filter_function is not None:
                if not self.filter_function(node):
                    continue
            new_nodes.append(node)
        new_graph = Graph(id=source_ontology.id, nodes=new_nodes, edges=source_ontology.edges)
        return self._post_process(new_graph)
