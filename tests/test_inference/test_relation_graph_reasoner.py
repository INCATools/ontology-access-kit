import unittest

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.inference.relation_graph_reasoner import RelationGraphReasoner
from tests import CELL, IMBO, INPUT_DIR, NUCLEAR_MEMBRANE, NUCLEUS, ORGANELLE, VACUOLE

ONT = INPUT_DIR / "go-nucleus.obo"
ONT_OBO = INPUT_DIR / "go-nucleus.obo"
ONT_OBO_SIMPLE = f"simpleobo:{ONT_OBO}"
ONT_JSON = INPUT_DIR / "go-nucleus.json"
ONT_DB = INPUT_DIR / "go-nucleus.db"


EXPECTED = [
    (NUCLEUS, PART_OF, CELL),
    (NUCLEUS, IS_A, IMBO),
    (NUCLEUS, IS_A, ORGANELLE),
    (NUCLEAR_MEMBRANE, PART_OF, CELL),
    (VACUOLE, IS_A, ORGANELLE),
    (VACUOLE, PART_OF, CELL),
    (NUCLEUS, IS_A, NUCLEUS),
]


class TestRelationGraphReasoner(unittest.TestCase):
    def setUp(self) -> None:
        adapter = get_adapter(ONT)
        self.reasoner = RelationGraphReasoner(adapter)

    def test_reason(self):
        # TODO: ONT_JSON once transitive properties are handled properly
        for handle in [ONT_OBO_SIMPLE, ONT_DB]:
            adapter = get_adapter(handle)
            self.reasoner = RelationGraphReasoner(adapter)
            if self.reasoner.is_available():
                edges = list(self.reasoner.entailed_edges())
                for e in EXPECTED:
                    self.assertIn(e, edges)
