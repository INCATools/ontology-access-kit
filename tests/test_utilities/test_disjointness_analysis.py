import unittest

from oaklib import get_adapter
from oaklib.datamodels.obograph import (
    DisjointClassExpressionsAxiom,
    ExistentialRestrictionExpression,
)
from oaklib.datamodels.vocabulary import PART_OF
from oaklib.utilities.axioms.disjointness_axiom_analyzer import (
    generate_disjoint_class_expressions_axioms,
    subsumed_by,
)
from tests import (
    FUNGI,
    INPUT_DIR,
    MEMBRANE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    ORGANELLE,
    VACUOLE,
)


class TestDisjointnessAnalyzer(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = get_adapter(INPUT_DIR / "go-nucleus.db")

    def test_generate_axioms(self):
        found = False
        for ax in generate_disjoint_class_expressions_axioms(self.adapter):
            if len(ax.classIds) > 1:
                assert ax.classIds[0] != ax.classIds[1]
            if set(ax.classIds) == {ORGANELLE, MEMBRANE}:
                found = True
        assert found

    def test_subsumed_by(self):
        cases = [
            ((ORGANELLE, MEMBRANE), [], 0, "edge case, no existing axioms"),
            ((ORGANELLE, MEMBRANE), [(ORGANELLE, MEMBRANE)], 1, "simple case, identical axioms"),
            (
                (ORGANELLE, MEMBRANE),
                [(MEMBRANE, ORGANELLE)],
                1,
                "simple case, identical axioms, different structure",
            ),
            ((ORGANELLE, MEMBRANE), [(ORGANELLE, FUNGI)], 0, "simple case, different axioms"),
            ((ORGANELLE, NUCLEAR_MEMBRANE), [(ORGANELLE, MEMBRANE)], 1, "subsumption on one side"),
            ((NUCLEUS, NUCLEAR_MEMBRANE), [(ORGANELLE, MEMBRANE)], 1, "subsumption on both sides"),
            ((ORGANELLE, MEMBRANE), [(NUCLEUS, NUCLEAR_MEMBRANE)], 0, "inverted"),
        ]
        for asserted_pair, existing_pairs, expected, _info in cases:
            asserted_ax = DisjointClassExpressionsAxiom(classIds=list(asserted_pair))
            existing_axioms = [
                DisjointClassExpressionsAxiom(classIds=list(x)) for x in existing_pairs
            ]
            subsumers = list(subsumed_by(self.adapter, asserted_ax, existing_axioms))
            assert len(subsumers) == expected

    def test_subsumed_by_expr(self):
        cases = [
            ((ORGANELLE, MEMBRANE), [], 0, "edge case, no existing axioms"),
            ((ORGANELLE, MEMBRANE), [(ORGANELLE, MEMBRANE)], 1, "simple case, identical axioms"),
            (
                (ORGANELLE, MEMBRANE),
                [(MEMBRANE, ORGANELLE)],
                1,
                "simple case, identical axioms, different structure",
            ),
            ((ORGANELLE, MEMBRANE), [(ORGANELLE, FUNGI)], 0, "simple case, different axioms"),
            ((ORGANELLE, NUCLEAR_MEMBRANE), [(ORGANELLE, MEMBRANE)], 1, "subsumption on one side"),
            (
                (NUCLEAR_MEMBRANE, VACUOLE),
                [(NUCLEUS, VACUOLE)],
                1,
                "part subsumption on both sides",
            ),
            ((NUCLEUS, VACUOLE), [(NUCLEAR_MEMBRANE, VACUOLE)], 0, "inverted"),
        ]

        def _as_expr(c: str) -> ExistentialRestrictionExpression:
            return ExistentialRestrictionExpression(propertyId=PART_OF, fillerId=c)

        for asserted_pair, existing_pairs, expected, info in cases:
            asserted_ax = DisjointClassExpressionsAxiom(
                classExpressions=[_as_expr(x) for x in asserted_pair]
            )
            existing_axioms = []
            for pair in existing_pairs:
                existing_axioms.append(
                    DisjointClassExpressionsAxiom(classExpressions=[_as_expr(x) for x in pair])
                )
            subsumers = list(subsumed_by(self.adapter, asserted_ax, existing_axioms))
            self.assertEqual(expected, len(subsumers), info)
