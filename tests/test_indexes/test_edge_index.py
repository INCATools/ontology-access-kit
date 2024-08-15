import unittest

from oaklib.datamodels.vocabulary import HAS_PART, IS_A, PART_OF
from oaklib.indexes.edge_index import EdgeIndex
from tests import CELL, IMBO, NUCLEUS, VACUOLE

RELS = [
    (NUCLEUS, IS_A, IMBO),
    (NUCLEUS, PART_OF, CELL),
    (VACUOLE, PART_OF, CELL),
]

EXPECTED = [
    # by subject
    ([NUCLEUS], [IS_A], None, [(NUCLEUS, IS_A, IMBO)]),
    ([NUCLEUS], [PART_OF], None, [(NUCLEUS, PART_OF, CELL)]),
    ([NUCLEUS], [IS_A, PART_OF], None, [(NUCLEUS, IS_A, IMBO), (NUCLEUS, PART_OF, CELL)]),
    ([NUCLEUS], None, None, [(NUCLEUS, IS_A, IMBO), (NUCLEUS, PART_OF, CELL)]),
    ([NUCLEUS], [IS_A], [IMBO], [(NUCLEUS, IS_A, IMBO)]),
    ([NUCLEUS], [], None, []),
    # by predicate
    (None, [IS_A], [IMBO], [(NUCLEUS, IS_A, IMBO)]),
    (None, None, [IMBO], [(NUCLEUS, IS_A, IMBO)]),
    (None, None, [CELL], [(NUCLEUS, PART_OF, CELL), (VACUOLE, PART_OF, CELL)]),
    (None, [PART_OF], [CELL], [(NUCLEUS, PART_OF, CELL), (VACUOLE, PART_OF, CELL)]),
    (None, [IS_A], [CELL], []),
    ([CELL], None, None, []),
    # additional nodes with no relationships have no effect
    ([NUCLEUS, CELL], [IS_A], None, [(NUCLEUS, IS_A, IMBO)]),
    ([NUCLEUS], [PART_OF, HAS_PART], None, [(NUCLEUS, PART_OF, CELL)]),
    # empty
    ([], [], [], []),
    ([], [IS_A], [], []),
    ([], None, None, []),
    (None, [], None, []),
    (None, None, [], []),
]


class TestEdgeIndex(unittest.TestCase):
    def setUp(self) -> None:
        rel_func = lambda: RELS
        self.index = EdgeIndex(rel_func)

    def test_edge_index(self):
        for rel in RELS:
            s, p, o = rel
            self.assertIn(rel, list(self.index.edges(None, None, None)))
            self.assertIn(rel, list(self.index.edges([s], None, None)))
            self.assertIn(rel, list(self.index.edges(None, [p], None)))
            self.assertIn(rel, list(self.index.edges(None, None, [o])))
            self.assertIn(rel, list(self.index.edges([s], [p], None)))
            self.assertIn(rel, list(self.index.edges([s], None, [o])))
            self.assertIn(rel, list(self.index.edges(None, [p], [o])))
            self.assertIn(rel, list(self.index.edges([s], [p], [o])))
        for sl, pl, ol, expected in EXPECTED:
            self.assertCountEqual(expected, list(self.index.edges(sl, pl, ol)))
