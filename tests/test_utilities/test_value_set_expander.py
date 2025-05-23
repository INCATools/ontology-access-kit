import unittest

from linkml_runtime.linkml_model import EnumDefinition, SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from oaklib.datamodels.value_set_configuration import ValueSetConfiguration
from oaklib.utilities.subsets.value_set_expander import ValueSetExpander
from tests import (
    BACTERIA,
    EXAMPLE_ONTOLOGY_DB,
    FUNGI,
    INPUT_DIR,
    MEMBRANE,
    NUCLEAR_MEMBRANE,
    OUTPUT_DIR,
    PLASMA_MEMBRANE,
    VACUOLE,
)

SCHEMA = str(INPUT_DIR / "value_set_example.yaml")
SCHEMA_OUT = str(OUTPUT_DIR / "value_set_example-expanded.yaml")

CONF = f"""
resource_resolvers:
  obo:go:
    shorthand: {EXAMPLE_ONTOLOGY_DB}
"""

cases = [
    ("GoMembrane", [MEMBRANE, NUCLEAR_MEMBRANE, PLASMA_MEMBRANE], [VACUOLE]),
    ("OnlyInEukaryotes", [NUCLEAR_MEMBRANE, FUNGI], [MEMBRANE, BACTERIA]),
    ("MembraneExcludingEukaryotes", [MEMBRANE], [NUCLEAR_MEMBRANE, FUNGI]),
]


class TestValueSetExpander(unittest.TestCase):
    def setUp(self) -> None:
        self.expander = ValueSetExpander()
        self.expander.configuration = yaml_loader.loads(CONF, ValueSetConfiguration)

    def test_trivial(self):
        expander = self.expander
        vset = yaml_loader.loads(
            """
        name: test
        permissible_values:
          a:
          b:
          c:
        """,
            EnumDefinition,
        )
        pvs = list(expander.expand_value_set(vset))
        for pv in pvs:
            print(pv)
        self.assertEqual(3, len(pvs))
        self.assertCountEqual(["a", "b", "c"], [pv.text for pv in pvs])

    def test_descendants(self):
        expander = self.expander
        vset: EnumDefinition = yaml_loader.loads(
            f"""
        name: test
        reachable_from:
          source_ontology: obo:go
          source_nodes: {MEMBRANE}
        """,
            EnumDefinition,
        )
        pvs = list(expander.expand_value_set(vset))
        for pv in pvs:
            print(pv)
        self.assertEqual(len(pvs), 4)
        texts = [pv.text for pv in pvs]
        self.assertIn(PLASMA_MEMBRANE, texts)
        self.assertNotIn(MEMBRANE, texts)
        vset.reachable_from.include_self = True
        pvs = list(expander.expand_value_set(vset))
        self.assertEqual(len(pvs), len(texts) + 1)
        texts = [pv.text for pv in pvs]
        self.assertIn(PLASMA_MEMBRANE, texts)
        self.assertIn(MEMBRANE, texts)

    def test_identifier(self):
        expander = self.expander
        vset = yaml_loader.loads(
            """
        name: test
        matches:
          source_ontology: obo:go
          identifier_pattern: "GO:003196.*"
        """,
            EnumDefinition,
        )
        pvs = list(expander.expand_value_set(vset))
        # for pv in pvs:
        #    print(pv)
        self.assertEqual(len(pvs), 2)
        self.assertIn(NUCLEAR_MEMBRANE, [pv.text for pv in pvs])

    def test_complex(self):
        schema = yaml_loader.load(SCHEMA, SchemaDefinition)
        enums = schema.enums
        for case in cases:
            vset_name, expected, unexpected = case
            vset = enums[vset_name]
            pvs = list(self.expander.expand_value_set(vset, schema=schema))
            texts = [pv.text for pv in pvs]
            for ex in expected:
                self.assertIn(ex, texts, f"Expected {ex} in {vset_name}")
            for un in unexpected:
                self.assertNotIn(un, texts, f"Unexpected {un} in {vset_name}")

    def test_expand_in_place(self):
        self.expander.expand_in_place(
            SCHEMA,
            # value_set_names=[case[0] for case in cases],
            value_set_names=["GoMembrane"],
            output_path=SCHEMA_OUT,
        )
