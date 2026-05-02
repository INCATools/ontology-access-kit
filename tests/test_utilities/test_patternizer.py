import unittest

import yaml

from oaklib.datamodels.vocabulary import (
    NEGATIVELY_REGULATES,
    PART_OF,
    POSITIVELY_REGULATES,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.patternizer import (
    Differentia,
    LexicalPattern,
    LexicalPatternCollection,
    LogicalDefinition,
    Term,
    lexical_pattern_instances,
    load_pattern_collection,
)
from tests import INPUT_DIR, MEMBRANE, NUCLEAR_MEMBRANE, NUCLEUS, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_PATTERNS_OUT = OUTPUT_DIR / "go-patterns.yaml"

PATTERNS = [
    LexicalPattern(
        name="nucleus",
        pattern="nuclear",
        description="A nuclear X is an X that is part of the nucleus.",
        curie=NUCLEUS,
        curie_is_genus=False,
        differentia_predicate=PART_OF,
    ),
    LexicalPattern(
        name="negative regulation",
        pattern="negative regulation of",
        curie="GO:0065007",
        differentia_predicate=NEGATIVELY_REGULATES,
    ),
    LexicalPattern(
        name="positive regulation",
        pattern="positive regulation of",
        curie="GO:0065007",
        differentia_predicate=POSITIVELY_REGULATES,
    ),
]


class TestPatternizer(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.pattern_collection = LexicalPatternCollection(patterns=PATTERNS)

    def test_patternizer(self):
        """Test that the patternizer works by extracting nucleus and regulation concepts."""
        expected = [
            Term(
                curie=NUCLEAR_MEMBRANE,
                label="nuclear membrane",
                logical_definition=LogicalDefinition(
                    genus=MEMBRANE, differentia=[Differentia(predicate=PART_OF, filler=NUCLEUS)]
                ),
                pattern="nucleus",
            ),
            Term(
                curie="GO:0009892",
                label="negative regulation of metabolic process",
                logical_definition=LogicalDefinition(
                    genus="GO:0065007",
                    differentia=[Differentia(predicate=NEGATIVELY_REGULATES, filler="GO:0008152")],
                ),
                pattern="negative regulation",
            ),
        ]
        for new_concept_prefix in [None, "TEST"]:
            todo = [yaml.dump(ec.model_dump()) for ec in expected]
            ecs = lexical_pattern_instances(
                self.oi, PATTERNS, new_concept_prefix=new_concept_prefix
            )
            for ec in ecs:
                print(yaml.dump(ec.model_dump()))
                for inst in ec.instances.values():
                    if(inst is None):
                        continue
                    inst_yaml = yaml.dump(inst.model_dump())
                    if inst_yaml in todo:
                        todo.remove(inst_yaml)
            self.assertEqual(todo, [])

    def test_write_patterns(self):
        """Test that the patternizer works by extracting nucleus and regulation concepts."""
        with open(TEST_PATTERNS_OUT, "w") as outf:
            yaml.dump(self.pattern_collection.model_dump(), outf)
        load_pattern_collection(str(TEST_PATTERNS_OUT))
