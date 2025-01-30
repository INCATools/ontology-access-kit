from typing import List

from sssom_schema import Mapping

import oaklib.datamodels.obograph as og
from oaklib.types import CURIE


def mappings_to_obograph(
    mappings: List[Mapping],
    graph_id="tmp",
) -> og.Graph:
    """
    Convert a list of mappings to an OboGraph.

    :param mappings: List of mappings
    :param source: Source ontology
    :param target: Target ontology
    :return: OboGraph
    """
    graph = og.Graph(graph_id)
    lbls = {}

    def _xref(curie: CURIE):
        return og.XrefPropertyValue(val=curie)

    for mapping in mappings:
        lbls[mapping.subject_id] = mapping.subject_label
        lbls[mapping.object_id] = mapping.object_label
        graph.edges.append(
            og.Edge(
                sub=mapping.subject_id,
                pred=mapping.predicate_id,
                obj=mapping.object_id,
                meta=og.Meta(
                    xrefs=[_xref(mapping.mapping_source)],
                ),
            )
        )
    for curie, lbl in lbls.items():
        graph.nodes.append(
            og.Node(
                id=curie,
                lbl=lbl,
            )
        )
    return graph
