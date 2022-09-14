import unittest

import yaml
from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.cross_ontology_diff import RelationalDiff
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.mapping.cross_ontology_diffs import (
    calculate_pairwise_relational_diff,
)
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "unreciprocated-mapping-test.obo"
TEST_OWL = INPUT_DIR / "unreciprocated-mapping-test.owl"
SSSOM = INPUT_DIR / "unreciprocated-mapping-test.sssom.tsv"
EXPECTED = INPUT_DIR / "unreciprocated-mapping-test.expected.diff.yaml"
TEST_OUT = OUTPUT_DIR / "unreciprocated-mapping-test.diff.yaml"


class TestStructuralDiff(unittest.TestCase):
    def setUp(self) -> None:
        """
        Creates handles for all implementations to be tested
        """
        resource = OntologyResource(slug=str(TEST_ONT), local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.owl_oi = SparqlImplementation(OntologyResource(str(TEST_OWL)))

    def test_initial_check(self):
        cases = [
            ("Y:5", [IS_A], ["Y:5"]),
            ("Y:5", [IS_A, IS_A], ["Y:5"]),
        ]
        for oi in [self.oi, self.owl_oi]:
            for subject, preds, ancs in cases:
                self.assertEqual(ancs, list(oi.ancestors([subject], predicates=preds)))

    def test_structural_diff(self):
        with open(EXPECTED) as f:
            expected_results = yaml.safe_load(f)
        expected_results = [RelationalDiff(**obj) for obj in expected_results]
        for oi in [self.oi, self.owl_oi]:
            results = list(calculate_pairwise_relational_diff(oi, oi, ["X", "Y", "Z"]))
            yaml_dumper.dump(results, str(TEST_OUT))
            self.assertCountEqual(expected_results, results)

    def test_structural_diff_with_preds(self):
        with open(EXPECTED) as f:
            expected_results = yaml.safe_load(f)
        expected_results = [RelationalDiff(**obj) for obj in expected_results]
        for oi in [self.oi, self.owl_oi]:
            results = list(
                calculate_pairwise_relational_diff(
                    oi, oi, ["X", "Y", "Z"], predicates=[IS_A, PART_OF]
                )
            )
            yaml_dumper.dump(results, str(TEST_OUT))
            self.assertCountEqual(expected_results, results)
            results = list(
                calculate_pairwise_relational_diff(oi, oi, ["X", "Y", "Z"], predicates=[PART_OF])
            )
            # logging.info(yaml_dumper.dumps(results))
            self.assertEqual(2, len(results))

    def test_restrict_to_sources(self):
        for oi in [self.oi, self.owl_oi]:
            results = list(calculate_pairwise_relational_diff(oi, oi, ["Z"]))
            self.assertEqual([], results)
