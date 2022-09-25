import unittest

from oaklib.datamodels.lexical_index import (
    LexicalTransformation,
    LexicalTransformationPipeline,
    TransformationType,
)
from oaklib.datamodels.mapping_rules_datamodel import Synonymizer
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import (
    create_lexical_index,
    save_lexical_index,
)
from oaklib.utilities.ontology_builder import OntologyBuilder
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.lexical.yaml"


class TestLexicalIndex(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.lexical_index = create_lexical_index(oi)

    def test_index_contents(self):
        groupings = self.lexical_index.groupings["cell periphery"]
        self.assertEqual(len(groupings.relationships), 2)
        self.assertCountEqual(
            ["GO:0005938", "GO:0071944"], [r.element for r in groupings.relationships]
        )

    def test_pipelines(self):
        """
        Tests customization of pipelines to apply for lexical indexing

        This creates a fake ontology and performs lexical indexing with various combinations
        of pipelines
        """
        oi = ProntoImplementation()
        builder = OntologyBuilder(oi)
        builder.add_class("X:1", "foo bar")
        builder.add_class("X:2", "FOO BAR")
        builder.add_class("X:3", "foo  bar")
        builder.add_class("X:4", "foo bar (foo bar)")
        builder.add_class("X:5", "foo bar [foo bar]")
        builder.build()
        syn_param = [
            Synonymizer(
                the_rule="Remove parentheses bound info from the label.",
                match="r'\([^)]*\)'",  # noqa W605
                match_scope="*",
                replacement="",
            ),
            Synonymizer(
                the_rule="Remove parentheses bound info from the label.",
                match="r'\[[^)]*\]'",  # noqa W605
                match_scope="*",
                replacement="",
            ),
        ]

        case_norm = LexicalTransformation(TransformationType.CaseNormalization)
        whitespace_norm = LexicalTransformation(TransformationType.WhitespaceNormalization)
        synonymization = LexicalTransformation(TransformationType.Synonymization, params=syn_param)

        cases = [
            (
                None,
                {
                    "foo bar": ["X:1", "X:2", "X:3"],
                    "foo bar (foo bar)": ["X:4"],
                    "foo bar [foo bar]": ["X:5"],
                },
            ),
            (
                [case_norm],
                {
                    "foo bar": ["X:1", "X:2"],
                    "foo  bar": ["X:3"],
                    "foo bar (foo bar)": ["X:4"],
                    "foo bar [foo bar]": ["X:5"],
                },
            ),
            (
                [whitespace_norm],
                {
                    "foo bar": ["X:1", "X:3"],
                    "FOO BAR": ["X:2"],
                    "foo bar (foo bar)": ["X:4"],
                    "foo bar [foo bar]": ["X:5"],
                },
            ),
            (
                [synonymization],
                {"FOO BAR": ["X:2"], "foo  bar": ["X:3"], "foo bar": ["X:1", "X:4", "X:5"]},
            ),
            (
                [case_norm, whitespace_norm, synonymization],
                {"foo bar": ["X:1", "X:2", "X:3", "X:4", "X:5"]},
            ),
        ]

        include_syn_rules = False

        for trs, expected in cases:
            if trs:
                pipelines = [LexicalTransformationPipeline(name="default", transformations=trs)]
                if trs[0].type.code.text == "Synonymization":
                    include_syn_rules = True
            else:
                pipelines = None

            if include_syn_rules:
                lexical_index = create_lexical_index(
                    oi, pipelines=pipelines, synonym_rules=syn_param
                )
            else:
                lexical_index = create_lexical_index(oi, pipelines=pipelines)

            groupings = {}
            for k, v in lexical_index.groupings.items():
                groupings[k] = [x.element for x in v.relationships]
            self.assertEqual(expected, groupings)

    def test_save(self):
        save_lexical_index(self.lexical_index, TEST_OUT)
