import logging
import unittest

from oaklib.datamodels.vocabulary import HAS_PART, IS_A
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.graph.relationship_walker import walk_down, walk_up
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"

CELLULAR_COMPONENT = "GO:0005575"


class TestRelationshipWalker(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_walk_up(self):
        oi = self.oi
        rels = list(walk_up(oi, "GO:0005773"))
        logging.info("ALL")
        for rel in rels:
            logging.info(rel)
        assert ("GO:0043227", HAS_PART, "GO:0016020") in rels
        logging.info("**IS_A")
        rels = list(walk_up(oi, "GO:0005773", predicates=[IS_A]))
        for rel in rels:
            logging.info(rel)
            self.assertEqual(rel[1], IS_A)
        assert ("GO:0043227", HAS_PART, "GO:0016020") not in rels
        assert ("GO:0110165", IS_A, "CARO:0000000") in rels

    def test_walk_down(self):
        oi = self.oi
        rels = list(walk_down(oi, CELLULAR_COMPONENT))
        logging.info("ALL")
        for rel in rels:
            logging.info(rel)
        assert ("GO:0043227", "rdfs:subClassOf", "GO:0043226") in rels
        assert ("GO:0005938", "BFO:0000050", "GO:0071944") in rels
