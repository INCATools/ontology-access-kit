import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib import OntologyResource
from oaklib.datamodels.association import Association
from oaklib.datamodels.vocabulary import IS_A, LOCATED_IN, PART_OF
from oaklib.implementations import ProntoImplementation
from oaklib.utilities.associations.association_differ import AssociationDiffer
from oaklib.utilities.basic_utils import powerset
from tests import (
    IMBO,
    INPUT_DIR,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    PMID1,
    PMID2,
    PROTEIN1,
    PROTEIN2,
    PROTEIN3,
    VACUOLE,
)

GAF = INPUT_DIR / "test-uniprot.gaf"

ASSOC_DATA = [
    (PROTEIN1, LOCATED_IN, NUCLEUS),
    (PROTEIN1, LOCATED_IN, VACUOLE),
    (PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),
]

PREDS = [IS_A, PART_OF]


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
        for assocs1 in powerset(self.assocs):
            for assocs2 in powerset(self.assocs):
                changes = list(self.differ.calculate_change_tuples(assocs1, assocs2, PREDS))
                logging.info(f"## DIFF {assocs1} -VS- {assocs2} == {len(changes)}")
                for change in changes:
                    logging.info(change)

    def test_diffs(self):
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEUS),  # will be refined
            Association(PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),  # will be generalized
            Association(PROTEIN3, LOCATED_IN, VACUOLE),  # will be lost
        ]
        assocs2 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE),
            Association(PROTEIN2, LOCATED_IN, IMBO),
        ]
        diff = self.differ.compare(assocs1, assocs2, PREDS)
        self.assertCountEqual(
            [
                (PROTEIN1, "set2", NUCLEAR_MEMBRANE),
                (PROTEIN2, "set1", NUCLEAR_MEMBRANE),
                (PROTEIN3, "set1", VACUOLE),
            ],
            diff.changes,
        )
        changes = list(self.differ.calculate_change_objects(assocs1, assocs2, PREDS))
        for change in changes:
            if change.subject == PROTEIN1:
                self.assertTrue(change.is_specialization)
                self.assertEqual(NUCLEUS, change.old_object)
                self.assertEqual(NUCLEAR_MEMBRANE, change.new_object)
            if change.subject == PROTEIN2:
                self.assertTrue(change.is_generalization)
                self.assertEqual(NUCLEAR_MEMBRANE, change.old_object)
                self.assertEqual(IMBO, change.new_object)
            if change.subject == PROTEIN3:
                self.assertTrue(change.is_deletion)
                self.assertEqual(VACUOLE, change.old_object)
        self.assertEqual(3, len(changes))
        self.assertCountEqual([PROTEIN1, PROTEIN2, PROTEIN3], [c.subject for c in changes])
        # reverse
        changes = list(self.differ.calculate_change_objects(assocs2, assocs1, PREDS))
        for change in changes:
            if change.subject == PROTEIN1:
                self.assertTrue(change.is_generalization)
                self.assertEqual(NUCLEUS, change.new_object)
                self.assertEqual(NUCLEAR_MEMBRANE, change.old_object)
            if change.subject == PROTEIN2:
                self.assertTrue(change.is_specialization)
                self.assertEqual(NUCLEAR_MEMBRANE, change.new_object)
                self.assertEqual(IMBO, change.old_object)
            if change.subject == PROTEIN3:
                self.assertTrue(change.is_creation)
                self.assertEqual(VACUOLE, change.new_object)
        self.assertEqual(3, len(changes))
        self.assertCountEqual([PROTEIN1, PROTEIN2, PROTEIN3], [c.subject for c in changes])

        # again with no closure
        diff = self.differ.compare(assocs1, assocs2, [])
        self.assertCountEqual(
            [
                (PROTEIN1, "set1", NUCLEUS),
                (PROTEIN1, "set2", NUCLEAR_MEMBRANE),
                (PROTEIN2, "set1", NUCLEAR_MEMBRANE),
                (PROTEIN2, "set2", IMBO),
                (PROTEIN3, "set1", VACUOLE),
            ],
            diff.changes,
        )
        assocs1 = [Association(PROTEIN1, LOCATED_IN, VACUOLE)]
        assocs2 = [Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE)]
        diff = self.differ.compare(assocs1, assocs2, PREDS)
        self.assertCountEqual(
            [
                (PROTEIN1, "set2", NUCLEAR_MEMBRANE),
                (PROTEIN1, "set1", VACUOLE),
            ],
            diff.changes,
        )
        diff = self.differ.compare(assocs1, assocs2, [])
        self.assertCountEqual(
            [(PROTEIN1, "set2", NUCLEAR_MEMBRANE), (PROTEIN1, "set1", VACUOLE)], diff.changes
        )

    def test_diffs_by_publications(self):
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEUS, publications=[PMID1]),
            Association(PROTEIN1, LOCATED_IN, NUCLEUS, publications=[PMID2]),
            Association(PROTEIN1, LOCATED_IN, VACUOLE, publications=[PMID2]),
        ]
        assocs2 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE, publications=[PMID1]),
            Association(PROTEIN1, LOCATED_IN, NUCLEUS, publications=[PMID2]),
            Association(PROTEIN1, LOCATED_IN, VACUOLE, publications=[PMID2]),
        ]
        diffs = self.differ.changes_by_publication(assocs1, assocs2, PREDS)
        for diff in diffs:
            print(yaml_dumper.dumps(diff))
