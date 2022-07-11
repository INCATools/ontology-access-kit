import unittest

import yaml
from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.cross_ontology_diff import RelationalDiff
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

    def test_structural_diff(self):
        expected_results = yaml.safe_load(open(EXPECTED))
        expected_results = [RelationalDiff(**obj) for obj in expected_results]
        for oi in [self.oi, self.owl_oi]:
            results = list(calculate_pairwise_relational_diff(oi, oi, ["X", "Y", "Z"]))
            yaml_dumper.dump(results, str(TEST_OUT))
            self.assertCountEqual(expected_results, results)
