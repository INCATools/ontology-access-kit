import unittest

from oaklib.implementations.cx.cx_implementation import CXImplementation
from oaklib.resource import OntologyResource
from tests import INPUT_DIR
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.cx"
TEST_PATHWAY = INPUT_DIR / "AMPK-Signaling.cx"


class TestCXImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = CXImplementation(resource)
        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

    def test_labels(self):
        self.compliance_tester.test_labels(self.oi)

    def test_pathway(self):
        """Tests converting CX to OBO Graph."""
        resource = OntologyResource(slug=TEST_PATHWAY, local=True)
        oi = CXImplementation(resource)
        og = oi.as_obograph()
        self.assertGreater(len(og.nodes), 0)
        self.assertGreater(len(og.edges), 0)
