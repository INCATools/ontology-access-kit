import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import ndex2

from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.implementations.obograph.obograph_implementation import (
    OboGraphImplementation,
)

__all__ = [
    "CXImplementation",
]


def from_cx(net_cx: ndex2.NiceCXNetwork) -> GraphDocument:
    gd = GraphDocument()
    graph = Graph(net_cx.get_name())
    node_index = {}
    for nid, obj in net_cx.get_nodes():
        att_n = obj.get("n")
        logging.debug(f"Node: {nid} {obj}")
        node = Node(id=obj.get("r", att_n), lbl=att_n, type="CLASS")
        node_index[nid] = node
        graph.nodes.append(node)
    for _edge_id, edge_obj in net_cx.get_edges():
        s = node_index[edge_obj.get("s")]
        t = node_index[edge_obj.get("t")]
        graph.edges.append(Edge(sub=s.id, obj=t.id, pred=edge_obj.get("i")))
    gd.graphs = [graph]
    return gd


@dataclass
class CXImplementation(OboGraphImplementation):
    """
    A :class:`OntologyInterface` implementation that wraps the NDexBio database or CX document.

    Status: Experimental

    This currently ignores node and edge attributes, and is read only.

    In future it will be possible to edit graphs you own, e.g. via KGCL commands.

    Command Line:

    .. code-block:: bash

        runoak -i ndexbio:0f019be9-1e5f-11e8-b939-0ac135e8bacf terms

        runoak -i ndexbio:0f019be9-1e5f-11e8-b939-0ac135e8bacf viz .all

        runoak -i ndexbio:0f019be9-1e5f-11e8-b939-0ac135e8bacf dump -O obo

    """

    engine: Any = None

    def __post_init__(self):
        locator = str(self.resource.slug)
        logging.info(f"Locator: {locator}")
        cx = None
        if locator.startswith("ndexbio:") or self.resource.scheme == "ndexbio":
            uuid = locator.replace("ndexbio:", "")
            if uuid:
                cx = ndex2.create_nice_cx_from_server(server="public.ndexbio.org", uuid=uuid)
        else:
            path = Path(locator.replace("cx:", "")).absolute()
            if not path.exists():
                raise FileNotFoundError(f"File does not exist: {path}")
            locator = path
            cx = ndex2.create_nice_cx_from_file(path)
        self.obograph_document = from_cx(cx)
