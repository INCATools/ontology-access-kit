import unittest
from dataclasses import dataclass

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import EQUIVALENT_CLASS, IS_A, ONLY_IN_TAXON, PART_OF
from tests import (
    CELL,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    EUKARYOTA,
    HUMAN,
    IMBO,
    MAMMALIA,
    NUCLEUS,
    SUBATOMIC_PARTICLE,
    VACUOLE,
)


@dataclass
class ComplianceTester:
    """
    Tests for compliance against expected behavior
    """

    test: unittest.TestCase
    """Link back to the calling test"""

    def test_relationships(self, oi: BasicOntologyInterface = None):
        """
        Tests relationship methods for compliance

        :param oi:
        :return:
        """
        test = self.test
        if oi is None:
            oi = test.oi
        cases = [
            (NUCLEUS, False, [(NUCLEUS, IS_A, IMBO), (NUCLEUS, ONLY_IN_TAXON, EUKARYOTA)]),
            (VACUOLE, True, [(VACUOLE, IS_A, IMBO), (VACUOLE, PART_OF, CYTOPLASM)]),
            (SUBATOMIC_PARTICLE, True, []),
            (HUMAN, True, [(HUMAN, IS_A, MAMMALIA)]),
            (CELL, True, [(CELL, IS_A, "CARO:0000003"), (CELL, ONLY_IN_TAXON, CELLULAR_ORGANISMS)]),
            (CELLULAR_COMPONENT, True, [(CELLULAR_COMPONENT, IS_A, "BFO:0000040")]),
        ]
        for curie, complete, expected_rels in cases:
            rels = list(oi.relationships([curie]))
            preds = set()
            for rv in expected_rels:
                test.assertIn(rv, rels)
                preds.add(rv[1])
            if complete:
                test.assertCountEqual(expected_rels, rels)
            rels = list(oi.relationships([curie], predicates=list(preds)))
            test.assertCountEqual(expected_rels, rels)
            for p in preds:
                for rel in oi.relationships([curie], predicates=[p]):
                    test.assertIn(rel, expected_rels)
                for r, o in oi.outgoing_relationships(curie, predicates=[p]):
                    test.assertIn((curie, r, o), expected_rels)
            # test reverse
            for s, p, o in expected_rels:
                expected_rel = s, p, o
                rels = list(oi.relationships(None, None, [o]))
                test.assertIn(expected_rel, rels)
                rels = list(oi.relationships(None, [p], [o]))
                test.assertIn(expected_rel, rels)
                rels = list(oi.relationships([s], [p], [o]))
                test.assertEqual([expected_rel], rels)
                irels = list(oi.incoming_relationships(o, predicates=[p]))
                test.assertIn((p, s), irels)

    def test_equiv_relationships(self, oi: BasicOntologyInterface = None):
        """
        Tests equivalence relationship methods for compliance

        :param oi:
        :return:
        """
        test = self.test
        if oi is None:
            oi = test.oi
        oi = test.oi
        pairs = [("BFO:0000023", "CHEBI:50906")]
        for c1, c2 in pairs:
            for s1, s2 in [(c1, c2), (c2, c1)]:
                rels = oi.outgoing_relationship_map(s1)
                # print(rels)
                test.assertCountEqual(rels[EQUIVALENT_CLASS], [s2])
