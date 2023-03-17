import logging
import unittest
from itertools import chain, combinations

from oaklib import OntologyResource
from oaklib.datamodels.association import Association
from oaklib.datamodels.vocabulary import IS_A, LOCATED_IN, PART_OF
from oaklib.implementations import ProntoImplementation
from oaklib.utilities.associations.association_differ import AssociationDiffer
from tests import INPUT_DIR, NUCLEAR_MEMBRANE, NUCLEUS, PROTEIN1, PROTEIN2, VACUOLE

GAF = INPUT_DIR / "test-uniprot.gaf"

ASSOC_DATA = [
    (PROTEIN1, LOCATED_IN, NUCLEUS),
    (PROTEIN1, LOCATED_IN, VACUOLE),
    (PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),
]

PREDS = [IS_A, PART_OF]


# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def _powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class AssociationDiffsTest(unittest.TestCase):
    """Tests diffs."""

    def setUp(self) -> None:
        self.assocs = [Association(*a) for a in ASSOC_DATA]
        self.oi = ProntoImplementation(
            OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        )
        self.differ = AssociationDiffer(self.oi)

    def test_diffs_powerset(self):
        # TODO: turn this into a test
        for assocs1 in _powerset(self.assocs):
            for assocs2 in _powerset(self.assocs):
                changes = list(self.differ.changes(assocs1, assocs2, PREDS))
                logging.info(f"## DIFF {assocs1} -VS- {assocs2} == {len(changes)}")
                for change in changes:
                    logging.info(change)

    def test_diffs(self):
        assocs1 = [Association(PROTEIN1, LOCATED_IN, NUCLEUS)]
        assocs2 = [Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE)]
        diff = self.differ.compare(assocs1, assocs2, PREDS)
        self.assertCountEqual([(PROTEIN1, "set2", NUCLEAR_MEMBRANE)], diff.changes)
        assocs1 = [Association(PROTEIN1, LOCATED_IN, VACUOLE)]
        assocs2 = [Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE)]
        diff = self.differ.compare(assocs1, assocs2, PREDS)
        self.assertCountEqual(
            [(PROTEIN1, "set2", NUCLEAR_MEMBRANE), (PROTEIN1, "set1", VACUOLE)], diff.changes
        )
