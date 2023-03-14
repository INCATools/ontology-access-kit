import json
import sys
from dataclasses import dataclass
from typing import Dict


from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.obograph import GraphDocument
from oaklib.types import CURIE


@dataclass
class OboGraphToCXConverter(DataModelConverter):
    """Converts from OboGraph to OBO Format."""

    def dump(self, source: GraphDocument, target: str = None, **kwargs) -> None:
        """
        Dump an OBO Graph Document to CX

        :param source:
        :param target:
        :return:
        """
        obj = self.convert(source)
        if target is None:
            file = sys.stdout
        else:
            file = open(target, "w", encoding="UTF-8")
        json.dump(obj, file, indent=2, sort_keys=False)

    def convert(self, source: GraphDocument, target: Dict = None, **kwargs) -> Dict:
        """
        Convert an OBO Graph Document to a CX Dictionary.

        :param source:
        :param target: if None, one will be created
        :return:
        """
        cx_nodes = []
        cx_edges = []
        cx_metadata = {
            "metadata": [],
        }
        node_id_map = {}
        next_id = 0
        for g in source.graphs:
            for n in g.nodes:
                node_id_map[n.id] = next_id
                node = {
                    "@id": next_id,
                    "n": n.lbl,
                    "r": self._id(n.id)
                }
                next_id += 1
                cx_nodes.append(node)
            for e in g.edges:
                s = node_id_map.get(e.sub, None)
                t = node_id_map.get(e.obj, None)
                if not s or not t:
                    continue
                edge = {
                   "@id": next_id,
                    "s": s,
                    "t": t,
                    "i": self._id(e.pred)
                }
                next_id += 1
                cx_edges.append(edge)
        doc = [
            cx_metadata,
            {"nodes": cx_nodes},
            {"edges": cx_edges}
        ]
        return doc

    def _id(self, uri: CURIE) -> CURIE:
        if not self.curie_converter:
            return uri
        curie = self.curie_converter.compress(uri)
        if curie is None:
            return uri
        else:
            return curie