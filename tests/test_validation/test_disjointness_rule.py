import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib import get_adapter
from oaklib.utilities.validation.disjointness_rule import DisjointnessRule
from oaklib.utilities.validation.rule_runner import RuleRunner
from tests import INPUT_DIR, OUTPUT_DIR, SUBATOMIC_PARTICLE

TEST_OUT = OUTPUT_DIR / "lint-test-output.obo"
TERM_X1 = "X:1"


class TestDisjointnessRule(unittest.TestCase):
    def setUp(self) -> None:
        oi = get_adapter(f"{INPUT_DIR}/go-nucleus.db")
        self.oi = oi
        self.rule_runner = RuleRunner()
        self.rule = DisjointnessRule()

    def test_rule(self):
        oi = self.oi
        rule = self.rule
        rule.labelled_only = False
        rule.min_descendants = 10
        results = list(rule.evaluate(self.oi))
        expected = [("OBI:0100026", SUBATOMIC_PARTICLE), ("BFO:0000002", SUBATOMIC_PARTICLE)]
        for result in results:
            print(f"{oi.label(result.subject)} -VS- {oi.label(result.object)}")
            print(yaml_dumper.dumps(result))
            print("---")
            for c1, c2 in expected:
                if (result.subject == c1 and result.object == c2) or (
                    result.subject == c2 and result.object == c1
                ):
                    expected.remove((c1, c2))
        self.assertEqual(len(expected), 0, f"Did not find: {expected}")
        self.assertEqual(6, len(results))
