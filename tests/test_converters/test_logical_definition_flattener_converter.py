import unittest

from linkml_runtime.loaders import json_loader

from oaklib import get_adapter
from oaklib.converters.logical_definition_flattener import LogicalDefinitionFlattener
from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import GraphDocument
from oaklib.datamodels.vocabulary import HAS_PART, PART_OF
from tests import INPUT_DIR, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

ONT = INPUT_DIR / "go-nucleus.json"
OUT = OUTPUT_DIR / "go-nucleus.ttl"


class LogicalDefinitionFlattenerTest(unittest.TestCase):
    """Tests turning logical definition axioms into tuples."""

    def setUp(self):
        self.oi = get_adapter(f"obograph:{ONT}")
        self.converter = LogicalDefinitionFlattener(
            labeler=lambda x: self.oi.label(x), curie_converter=self.oi.converter
        )
        self.compliance_tester = ComplianceTester(self)

    def test_convert_file(self):
        """Tests parsing then converting to tuples."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        objs = self.converter.convert(gd)
        cases = [
            {
                "defined_class": "GO:0008047",
                "genus_class": "GO:0003674",
                "positively_regulates": "GO:0003824",
            },
            {
                "defined_class": "GO:0006793",
                "genus_class": "GO:0008152",
                "has_primary_input_or_output": "CHEBI:26082",
            },
            {"defined_class": "GO:0051338", "genus_class": "GO:0065007", "regulates": "GO:0016740"},
            {"defined_class": "GO:0043231", "genus_class": "GO:0043227", "part_of": "GO:0005622"},
            {"defined_class": "GO:0005938", "genus_class": "GO:0005737", "part_of": "GO:0071944"},
        ]
        for case in cases:
            self.assertIn(case, objs)

    def test_convert_objects(self):
        """Tests parsing then converting to tuples."""
        restrictions = []
        restrictions.append(
            obograph.ExistentialRestrictionExpression(propertyId=PART_OF, fillerId="Y:1")
        )
        restrictions.append(
            obograph.ExistentialRestrictionExpression(propertyId=PART_OF, fillerId="Y:2")
        )
        restrictions.append(
            obograph.ExistentialRestrictionExpression(propertyId=HAS_PART, fillerId="Y:3")
        )
        ldef = obograph.LogicalDefinitionAxiom(
            definedClassId="X:1", genusIds=["X:2"], restrictions=restrictions
        )
        obj = self.converter.convert(ldef)
        self.assertEqual(
            obj,
            {
                "defined_class": "X:1",
                "genus_class": "X:2",
                "part_of_1": "Y:1",
                "part_of_2": "Y:2",
                "has_part": "Y:3",
            },
        )
