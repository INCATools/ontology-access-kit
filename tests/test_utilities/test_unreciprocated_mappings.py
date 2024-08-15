import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.mapping.mapping_validation import unreciprocated_mappings
from oaklib.utilities.mapping.sssom_utils import mappings_to_pairs
from tests import INPUT_DIR

TEST_ONT = INPUT_DIR / "unreciprocated-mapping-test.obo"
TEST_OWL = INPUT_DIR / "unreciprocated-mapping-test.owl"
# TEST_DB = INPUT_DIR / 'unreciprocated-mapping-test.db'


class TestUnreciprocated(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug=str(TEST_ONT), local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.owl_oi = SparqlImplementation(OntologyResource(str(TEST_OWL)))

    def test_unreciprocated(self):
        # temporarily restricting tests: see https://github.com/INCATools/ontology-access-kit/pull/715
        for oi in [self.oi]:
            # for oi in [self.oi, self.owl_oi]:
            pairs = mappings_to_pairs(unreciprocated_mappings(oi, oi))
            # for p in pairs:
            #    logging.info(p)
            self.assertCountEqual(pairs, [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4")])
            pairs = mappings_to_pairs(unreciprocated_mappings(oi, oi, filter_unidirectional=False))
            # for p in pairs:
            #    logging.info(p)
            self.assertCountEqual(
                pairs, [("X:5", "Y:5"), ("Y:2", "X:1"), ("Y:4", "X:4"), ("Y:4", "Z:4")]
            )
