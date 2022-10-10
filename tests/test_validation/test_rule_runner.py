import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.validation.rule_runner import RuleRunner
from tests import INPUT_DIR, OUTPUT_DIR

TEST_OUT = OUTPUT_DIR / "lint-test-output.obo"
TERM_X1 = "X:1"


class TestRuleRunner(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.rule_runner = RuleRunner()

    def test_rule_runner(self):
        self.rule_runner.run(self.oi)
