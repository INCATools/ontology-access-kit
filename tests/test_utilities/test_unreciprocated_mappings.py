import unittest
from typing import Dict, List, Tuple

from sssom import Mapping

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.types import CURIE
from oaklib.utilities.mapping.cross_ontology_diffs import group_mappings_by_source_pairs
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

    def test_pronto_mapping_groups(self):
        groups: Dict[Tuple[str, str], List[Mapping]] = group_mappings_by_source_pairs(
            self.pronto_oi, self.pronto_oi
        )
        expected_keys = [("X", "Y"), ("Y", "X"), ("Y", "Z")]
        self.assertEqual(set(groups.keys()), set(expected_keys))

    def test_pronto_mappings_by_source(self):
        map_list: List[Mapping] = list(self.pronto_oi.sssom_mappings_by_source())
        self.assertEqual(len(map_list), 19)

    # SOMETIMES PAIRS iS COMING BACK AS {('X:5', 'Y:5'), ('Y:2', 'X:1')}
    def test_unreciprocated_pronto(self):
        oi = self.pronto_oi
        unrec_maps: list[Mapping] = list(
            unreciprocated_mappings(subject_oi=oi, object_oi=oi, both_directions=True)
        )
        self.assertEqual(len(unrec_maps), 6)
        # Unrec_maps swaps between 4 and 5 members
        pairs: list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4")]
        self.assertEqual(set(pairs), set(expected_pairs))

    def test_unreciprocated_owl(self):
        oi = self.owl_oi
        unrec_maps: list[Mapping] = list(unreciprocated_mappings(oi, oi))
        self.assertEqual(len(unrec_maps), 6)
        pairs: list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4")]
        self.assertEqual(set(pairs), set(expected_pairs))

    def test_unreciprocated_pronto_with_unidirectional(self):
        oi = self.pronto_oi
        unrec_maps: list[Mapping] = list(
            unreciprocated_mappings(oi, oi, filter_unidirectional=False)
        )
        self.assertEqual(len(unrec_maps), 7)
        pairs: list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4"), ("Y:4", "Z:4")]
        self.assertEqual(set(pairs), set(expected_pairs))

    def test_unreciprocated_owl_with_unidirectional(self):
        oi = self.owl_oi
        unrec_maps: list[Mapping] = list(
            unreciprocated_mappings(oi, oi, filter_unidirectional=False)
        )
        self.assertEqual(len(unrec_maps), 7)
        pairs: list[Tuple[CURIE, CURIE]] = mappings_to_pairs(unrec_maps)
        expected_pairs = [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4"), ("Y:4", "Z:4")]
        self.assertEqual(set(pairs), set(expected_pairs))
