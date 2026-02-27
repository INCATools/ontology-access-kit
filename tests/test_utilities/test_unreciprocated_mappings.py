import logging
from typing import Tuple
import unittest

from sssom import Mapping

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.types import CURIE
from oaklib.utilities.mapping.mapping_validation import unreciprocated_mappings
from oaklib.utilities.mapping.sssom_utils import mappings_to_pairs
from tests import INPUT_DIR

TEST_ONT = INPUT_DIR / "unreciprocated-mapping-test.obo"
TEST_OWL = INPUT_DIR / "unreciprocated-mapping-test.owl"
# TEST_DB = INPUT_DIR / 'unreciprocated-mapping-test.db'


class TestUnreciprocated(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug=str(TEST_ONT), local=True)
        self.pronto_oi = ProntoImplementation(resource)
        self.owl_oi = SparqlImplementation(OntologyResource(str(TEST_OWL)))

    def test_unreciprocated_pronto_with_unidirectional(self):
        oi = self.pronto_oi
        unrec_maps:list[Mapping] = list(unreciprocated_mappings(oi, oi,filter_unidirectional=False))
        pairs:list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4"), ("Y:4", "Z:4")]
        self.assertEqual(set(pairs),set(expected_pairs))

    def test_unreciprocated_pronto(self):
        oi = self.pronto_oi
        unrec_maps:list[Mapping] = list(unreciprocated_mappings(oi, oi))
        pairs:list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        for p in pairs:
            logging.warning(str(p))
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4")]
        self.assertEqual(set(pairs),set(expected_pairs))

    def test_unreciprocated_owl(self):
        oi = self.owl_oi
        unrec_maps:list[Mapping] = list(unreciprocated_mappings(oi, oi))
        pairs:list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4")]
        self.assertEqual(set(pairs),set(expected_pairs))


    def test_unreciprocated_owl_with_unidirectional(self):
        oi = self.owl_oi
        unrec_maps:list[Mapping] = list(unreciprocated_mappings(oi, oi,filter_unidirectional=False))
        pairs:list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4"), ("Y:4", "Z:4")]
        self.assertEqual(set(pairs),set(expected_pairs))