from dataclasses import dataclass
from typing import Collection, Optional

from oaklib.datamodels.obograph import Graph
from oaklib.datamodels.vocabulary import IS_A
from oaklib.transformers.graph_transformer import GraphTransformer
from oaklib.types import PRED_CURIE


@dataclass
class EdgeFilterTransformer(GraphTransformer):
    """
    An ontology graph transformer that filters edges
    """

    include_predicates: Optional[Collection[PRED_CURIE]] = None
    """A collection of predicates to include"""

    exclude_predicates: Optional[Collection[PRED_CURIE]] = None
    """A collection of predicates to exclude"""

    filter_function: Optional[callable] = None
    """A function that takes an edge and returns True if it should be included"""

    def transform(self, source_ontology: Graph, **kwargs) -> Graph:
        """
        Filters edges from a graph.

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> from oaklib.transformers.transformers_factory import get_ontology_transformer
        >>> from oaklib.datamodels.vocabulary import IS_A
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> graph = adapter.as_obograph()
        >>> transformer = get_ontology_transformer("EdgeFilterTransformer", include_predicates=[IS_A])
        >>> filtered_graph = transformer.transform(graph)
        >>> set([e.pred for e in filtered_graph.edges])
        {'is_a'}

        :param graph:
        :return:

        """
        include_predicates = self.include_predicates
        exclude_predicates = self.exclude_predicates

        if include_predicates is None and exclude_predicates is None:
            return source_ontology

        def _normalize_id(pred: PRED_CURIE) -> PRED_CURIE:
            if pred == IS_A:
                return "is_a"
            else:
                return pred

        if include_predicates is not None:
            include_predicates = {_normalize_id(pred) for pred in include_predicates}

        if exclude_predicates is not None:
            exclude_predicates = {_normalize_id(pred) for pred in exclude_predicates}

        new_edges = []
        for edge in source_ontology.edges:
            if include_predicates is not None:
                if edge.pred not in include_predicates:
                    continue
            if exclude_predicates is not None:
                if edge.pred in exclude_predicates:
                    continue
            if self.filter_function is not None:
                if not self.filter_function(edge):
                    continue
            new_edges.append(edge)
        new_graph = Graph(id=source_ontology.id, nodes=source_ontology.nodes, edges=new_edges)
        return self._post_process(new_graph)
