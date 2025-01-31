import logging
import unittest

from kgcl_schema.datamodel import kgcl
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
    PHOTOSYNTHETIC_MEMBRANE,
    PMID1,
    PMID2,
    PROTEIN1,
    PROTEIN2,
    PROTEIN3,
    THYLAKOID,
    VACUOLE,
)

GAF = INPUT_DIR / "test-uniprot.gaf"

ASSOC_DATA = [
    (PROTEIN1, LOCATED_IN, NUCLEUS),
    (PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE),
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
        self.oi.apply_patch(
            kgcl.NodeObsoletionWithDirectReplacement(
                id="TMP", about_node=PHOTOSYNTHETIC_MEMBRANE, has_direct_replacement=THYLAKOID
            )
        )
        self.differ = AssociationDiffer(self.oi)

    def test_diffs_powerset(self):
        # TODO: turn this into a test
        for assocs1 in powerset(self.assocs):
            for assocs2 in powerset(self.assocs):
                changes = list(self.differ.calculate_change_objects(assocs1, assocs2, PREDS))
                logging.info(f"## DIFF {assocs1} -VS- {assocs2} == {len(changes)}")
                len1 = len(assocs1)
                len2 = len(assocs2)
                print(f"## DIFF {len1} <=> {len2} // {assocs1} -VS- {assocs2} == {len(changes)}")
                if len1 == 0 and len2 == 0:
                    self.assertEqual([], changes)
                    continue
                if assocs1 == assocs2:
                    self.assertEqual([], changes)
                    continue
                if len1 == 0:
                    for change in changes:
                        self.assertTrue(change.is_creation)
                if len2 == 0:
                    for change in changes:
                        self.assertTrue(change.is_deletion)
                self.assertNotEqual([], changes)
                for change in changes:
                    logging.info(change)
                    print(yaml_dumper.dumps(change))
                    self.assertIsNotNone(change.subject)
                    if not change.is_creation and not change.is_deletion:
                        self.assertIsNotNone(change.old_object)
                        self.assertIsNotNone(change.new_object)
                    if change.is_generalization:
                        self.assertLess(change.closure_delta, 0)
                    if change.is_specialization:
                        self.assertGreater(change.closure_delta, 0)
                reverse_changes = list(
                    self.differ.calculate_change_objects(assocs2, assocs1, PREDS)
                )
                self.assertEqual(len(changes), len(reverse_changes))
                # specializations = [change for change in changes if change.is_specialization]
                # generalizations = [change for change in changes if change.is_generalization]
                # self.assertEqual(len(specializations), len(generalizations))

    def test_diffs_creation(self):
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEUS),  # obsoleted and replaced
        ]
        changes = self.differ.calculate_change_objects(assocs1, [], PREDS)
        for change in changes:
            print(yaml_dumper.dumps(change))
            self.assertTrue(change.is_deletion)
            self.assertEqual(-16, change.closure_delta)
        changes = self.differ.calculate_change_objects([], assocs1, PREDS)
        for change in changes:
            print(yaml_dumper.dumps(change))
            self.assertTrue(change.is_creation)
            self.assertEqual(16, change.closure_delta)

    def test_diffs_with_obsoletion(self):
        # old set
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, PHOTOSYNTHETIC_MEMBRANE),  # obsoleted and replaced
            Association(PROTEIN2, LOCATED_IN, PHOTOSYNTHETIC_MEMBRANE),  # obsoleted
        ]
        # new set
        assocs2 = [
            Association(PROTEIN1, LOCATED_IN, THYLAKOID),
            # Association(PROTEIN2, LOCATED_IN, IMBO),
        ]
        changes = self.differ.calculate_change_objects(assocs1, assocs2, PREDS)
        for change in changes:
            print(yaml_dumper.dumps(change))

    def test_diffs(self):
        # old set
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEUS),  # will be refined
            Association(PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),  # will be generalized
            Association(PROTEIN3, LOCATED_IN, VACUOLE),  # will be lost
        ]
        # new set
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

    def test_diffs_by_term(self):
        # old set
        assocs1 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEUS),  # will be refined
            Association(PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),  # will be generalized
            Association(PROTEIN3, LOCATED_IN, VACUOLE),  # will be lost
        ]
        # new set
        assocs2 = [
            Association(PROTEIN1, LOCATED_IN, NUCLEAR_MEMBRANE),
            Association(PROTEIN2, LOCATED_IN, IMBO),
        ]

        # by terms
        by_term = self.differ.changes_by_terms(
            assocs1,
            assocs2,
            min_num_entities_changes=1,
        )
        for t, exp1, exp2 in [
            (NUCLEAR_MEMBRANE, [PROTEIN2], [PROTEIN1]),
            (IMBO, [PROTEIN1, PROTEIN2, PROTEIN3], [PROTEIN2, PROTEIN1]),
        ]:
            bt = by_term[t]
            self.assertCountEqual(exp1, bt.old_entities, f"For term {t}")
            self.assertCountEqual(exp2, bt.new_entities, f"For term {t}")

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
