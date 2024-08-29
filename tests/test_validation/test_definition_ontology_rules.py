import unittest

from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.vocabulary import PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.validation.definition_ontology_rule import (
    DefinitionOntologyRule,
)
from oaklib.utilities.validation.rule_runner import RuleRunner
from tests import INPUT_DIR, MEMBRANE, NUCLEAR_MEMBRANE, NUCLEUS, OUTPUT_DIR

TEST_OUT = OUTPUT_DIR / "lint-test-output.obo"
TERM_X1 = "X:1"


class TestDefinitionOntologyRules(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.rule_runner = RuleRunner()
        self.rule = DefinitionOntologyRule()

    def test_rule(self):
        """
        Checks logical definitions and text definitions are aligned.
        """
        rule = self.rule
        cases = [
            (
                "A membrane that is part of a nucleus. Blah.",
                "membrane",
                "is part of a nucleus",
                "Blah.",
                0,
            ),
            (
                "A membrane which is part of a nucleus. Blah.",
                "membrane",
                "is part of a nucleus",
                "Blah.",
                0,
            ),
            ("A membrane that is part of a nucleus", "membrane", "is part of a nucleus", None, 0),
            ("A foo or a bar", None, None, None, 2),
            ("A membranXX that is part of a nucleXX", "membranXX", "is part of a nucleXX", None, 2),
            (
                "A foo membrane that is part of a nucleus",
                "foo membrane",
                "is part of a nucleus",
                None,
                1,
            ),
        ]
        ldef = LogicalDefinitionAxiom(
            definedClassId=NUCLEAR_MEMBRANE,
            genusIds=[MEMBRANE],
            restrictions=[ExistentialRestrictionExpression(propertyId=PART_OF, fillerId=NUCLEUS)],
        )
        for case in cases:
            tdef, genus, differentia, gloss, expected_results = case
            pdef = rule.process_text_definition(tdef)
            self.assertEqual(genus, pdef.genus_text)
            self.assertEqual(differentia, pdef.differentia_text)
            self.assertEqual(gloss, pdef.gloss)
            anns = list(self.oi.annotate_text(tdef))
            anns_by_object = {ann.object_id: ann for ann in anns}
            results = list(
                rule.check_against_logical_definition(self.oi, pdef, ldef, anns_by_object)
            )
            self.assertEqual(
                expected_results,
                len(results),
                f"check_against_logical_definition unexpected; Case: {case}",
            )
            for r in results:
                print(f"{tdef} :: {r.type} :: {r.info}")
        _results = list(rule.evaluate(self.oi))
