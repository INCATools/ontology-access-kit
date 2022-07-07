"""Test OBOGraph Utilities."""
import json
import logging
import unittest

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import (
    as_multi_digraph,
    filter_by_predicates,
    graph_as_dict,
    graph_to_tree,
    trim_graph,
)
from tests import CELLULAR_ORGANISMS, HUMAN, IMBO, INPUT_DIR, OUTPUT_DIR, VACUOLE
from tests.test_cli import NUCLEUS

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"


class TestOboGraphUtils(unittest.TestCase):
    """Test OBOGraph Utilities."""

    def setUp(self) -> None:
        """Set up."""
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.graph = oi.as_obograph()

    def test_as_json(self):
        """Test as JSON."""
        obj = graph_as_dict(self.graph)
        json_obj = json.dumps(obj)
        self.assertIn('{"id": "GO:0003674"', json_obj)
        # https://github.com/althonos/pronto/issues/163
        # self.assertIn('{"sub": "CL:0000000", "pred": "BFO:0000051", "obj": "GO:0005634"}', json_obj)

    def test_as_networkx(self):
        """Test as networkx"""
        mdg = as_multi_digraph(self.graph)
        self.assertIn(NUCLEUS, mdg.nodes)
        for e in mdg.edges(data=True):
            logging.info(f"SU={e}")
        self.assertIn(
            ("GO:0005634", "GO:0031965", {"predicate": "BFO:0000050"}), mdg.edges(data=True)
        )

    def test_filter_by_predicates(self):
        """Test filter by predicates."""
        g = self.graph
        g2 = filter_by_predicates(g, predicates=[IS_A, PART_OF])
        self.assertCountEqual(g.nodes, g2.nodes)
        self.assertGreater(len(g.edges), len(g2.edges))
        self.assertGreater(len(g2.edges), 100)

    def test_as_tree(self):
        """Test as tree."""
        t = graph_to_tree(self.graph, predicates=[IS_A])
        lines = t.split("\n")
        self.assertIn("[i] BFO:0000015 ! process", t)
        self.assertNotIn("[p]", t)
        self.assertNotIn(PART_OF, t)
        self.assertGreater(len(lines), 100)
        t = graph_to_tree(self.graph, predicates=[IS_A, PART_OF])
        lines = t.split("\n")
        self.assertIn("[i] BFO:0000015 ! process", t)
        self.assertIn("* [p] GO:0019209 ! kinase activator activity", t)
        self.assertGreater(len(lines), 100)

    def test_trim_ancestors(self):
        """Test trim ancestors."""
        oi = self.oi
        both = [IS_A, PART_OF]
        expected_list = [
            ([], 0, True, both, 0),
            ([NUCLEUS], 0, True, both, 0),
            ([NUCLEUS], 1, True, both, 1),
            ([NUCLEUS, IMBO], 0, True, both, 1),
            ([NUCLEUS, IMBO], 1, True, both, 5),
            ([NUCLEUS, VACUOLE], 0, True, both, 0),
            ([NUCLEUS, VACUOLE], 1, True, both, 3),
            ([NUCLEUS, VACUOLE, IMBO], 1, True, both, 8),
            ([NUCLEUS, VACUOLE, IMBO], 1, False, [IS_A], 4),
            ([HUMAN, CELLULAR_ORGANISMS], 1, True, [IS_A], 8),
            ([HUMAN, CELLULAR_ORGANISMS], 1, False, [IS_A], 2),
        ]
        if isinstance(oi, OboGraphInterface):
            for ex in expected_list:
                seeds, dist, include_intermediates, predicates, expected_len = ex
                g = oi.ancestor_graph(seeds, predicates=predicates)
                trimmed = trim_graph(
                    g, seeds, distance=dist, include_intermediates=include_intermediates
                )
                if expected_len is not None:
                    self.assertEqual(expected_len, len(trimmed.edges))
                node_ids = [n.id for n in trimmed.nodes]
                for seed in seeds:
                    self.assertIn(seed, node_ids)
        else:
            raise NotImplementedError
