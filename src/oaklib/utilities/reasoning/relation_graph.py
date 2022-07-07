from collections import Iterator
from dataclasses import dataclass

import oaklib.datamodels.obograph as og

# from oaklib.utilities.obograph_utils import (
#     index_graph_edges_by_subject,
#     index_graph_edges_by_subject_object,
# )


@dataclass
class RelationGraphReasoner:
    ontology: og.Graph = None

    def get_non_redundant_edges(self) -> Iterator[og.Edge]:
        ont = self.ontology
        # six = index_graph_edges_by_subject(ont.edges)
        # soix = index_graph_edges_by_subject_object(ont.edges)
        for e in ont.edges:
            yield e
