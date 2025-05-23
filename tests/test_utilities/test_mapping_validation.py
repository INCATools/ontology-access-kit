import unittest

from sssom_schema import Mapping

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A, PART_OF, SEMAPV, SKOS_EXACT_MATCH
from oaklib.utilities.mapping.mapping_validation import validate_mappings
from tests import CYTOPLASM, FUNGI, INPUT_DIR, NUCLEUS, OUTPUT_DIR, VACUOLE

DB = INPUT_DIR / "go-nucleus.db"
TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"

PREDS = [IS_A, PART_OF]

# these are biologically nonsensical, the purpose
# is purely to test structural properties
cases = [
    (
        [
            (NUCLEUS, SKOS_EXACT_MATCH, CYTOPLASM),
            (NUCLEUS, SKOS_EXACT_MATCH, VACUOLE),
        ],
        2,
    ),
    (
        [
            (NUCLEUS, SKOS_EXACT_MATCH, CYTOPLASM),
            (FUNGI, SKOS_EXACT_MATCH, VACUOLE),
        ],
        0,
    ),
]


class TestMappingValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.adaptor = get_adapter(DB)
        self.adapters = {
            "go": self.adaptor,
        }

    def test_mapping_validation(self):
        for case in cases:
            tuples, expected_n = case
            mappings = [
                Mapping(
                    subject_id=t[0],
                    predicate_id=t[1],
                    object_id=t[2],
                    mapping_justification=SEMAPV.LexicalMatching.value,
                )
                for t in tuples
            ]
            results = list(validate_mappings(mappings, self.adapters))
            self.assertEqual(case[1], len(results))
