import logging
import unittest

import networkx as nx

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.graph.networkx_bridge import (
    relationships_to_multi_digraph,
    transitive_reduction,
    transitive_reduction_by_predicate,
)
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"

KINASE_ACTIVATOR_ACTIVITY = "GO:0019209"
BIOLOGICAL_PROCESS = "GO:0008152"


class TestNetworkxBridge(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.mdg = relationships_to_multi_digraph(oi.all_relationships())

    def test_all_paths(self):
        paths = list(nx.all_simple_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY))
        for path in paths:
            logging.info(path)
        assert len(paths) > 10
        paths = list(
            nx.all_simple_edge_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY)
        )
        for path in paths:
            logging.info(path)
        assert len(paths) > 10
        # paths = list(nx.shortest_simple_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY))
        # for path in paths:
        #    logging.info(path)
        # assert len(paths) > 10

    def test_reduction(self):
        rels = [("a", IS_A, "b"), ("b", IS_A, "c"), ("a", IS_A, "c")]
        reduced = list(transitive_reduction(rels))
        # for r in reduced:
        #    logging.info(r)
        self.assertEqual(len(reduced), 2)
        self.assertCountEqual(
            reduced, [("a", "rdfs:subClassOf", "b"), ("b", "rdfs:subClassOf", "c")]
        )
        rels = list(self.oi.all_relationships())
        reduced = list(transitive_reduction([rel for rel in rels if rel[1] == IS_A]))
        for r in reduced:
            logging.info(r)
        # reduced = list(transitive_reduction([rel for rel in rels if rel[1] == PART_OF]))

    def test_reduction_by_predicate(self):
        rels = [("a", IS_A, "b"), ("b", IS_A, "c"), ("a", IS_A, "c")]
        reduced = list(transitive_reduction_by_predicate(rels))
        # for r in reduced:
        #    logging.info(r)
        self.assertEqual(len(reduced), 2)
        self.assertCountEqual(
            reduced, [("a", "rdfs:subClassOf", "b"), ("b", "rdfs:subClassOf", "c")]
        )
        rels = [("a", IS_A, "b"), ("b", IS_A, "c"), ("a", PART_OF, "c")]
        reduced = list(transitive_reduction_by_predicate(rels))
        self.assertEqual(len(reduced), 3)
        rels = list(self.oi.all_relationships())
        reduced = list(transitive_reduction_by_predicate(rels))
        for r in reduced:
            logging.info(r)
