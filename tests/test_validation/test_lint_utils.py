import unittest

from oaklib import get_adapter
from oaklib.datamodels.obograph import SynonymPropertyValue
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.resource import OntologyResource
from oaklib.utilities.validation.lint_utils import lint_ontology
from tests import INPUT_DIR, OUTPUT_DIR

TEST_OUT = OUTPUT_DIR / "lint-test-output.obo"
TERM_X1 = "X:1"


class TestLintUtils(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="lint-test.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_lint(self):
        issues = list(lint_ontology(self.oi))
        self.assertEqual(4, len(issues))
        # for issue in issues:
        #    print(issue)
        self.oi.dump(path=str(TEST_OUT))
        oi_repaired = get_adapter(str(TEST_OUT))
        self.assertEqual(oi_repaired.label(TERM_X1), "test 1")
        self.assertEqual(oi_repaired.definition(TERM_X1), "foo bar")
        if not isinstance(oi_repaired, OboGraphInterface):
            raise AssertionError("Expected OboGraphInterface")
        pvs = list(oi_repaired.synonym_property_values(TERM_X1))
        self.assertCountEqual(
            [
                (
                    TERM_X1,
                    SynonymPropertyValue(pred="hasExactSynonym", val="syn 1", xrefs=["PMID:1"]),
                ),
                (TERM_X1, SynonymPropertyValue(pred="hasBroadSynonym", val="syn 2", xrefs=[])),
            ],
            pvs,
        )
