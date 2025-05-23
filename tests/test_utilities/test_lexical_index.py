import unittest

from oaklib.datamodels.lexical_index import (
    LexicalTransformation,
    LexicalTransformationPipeline,
    TransformationType,
)
from oaklib.datamodels.synonymizer_datamodel import Synonymizer
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
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
        builder.add_class("X:6", "Other foo bar")
        builder.add_class("X:7", "Other  (FOO) [bar] foo bar")
        builder.build()
        syn_param = [
            Synonymizer(
                description="Remove parentheses bound info from the label.",
                match=r"\([^)]*\)",  # noqa W605
                match_scope="*",
                replacement="",
            ),
            Synonymizer(
                description="Remove box brackets bound info from the label.",
                match=r"\[[^)]*\]",  # noqa W605
                match_scope="*",
                replacement="",
            ),
            Synonymizer(
                description="Broad match terms with the term 'other' in them.",
                match=r"(?i)^Other ",  # noqa W605
                match_scope="*",
                replacement="",
                qualifier="broad",
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
                    "other foo bar": ["X:6"],
                    "other (foo) [bar] foo bar": ["X:7"],
                },
            ),
            (
                [case_norm],
                {
                    "foo bar": ["X:1", "X:2"],
                    "foo  bar": ["X:3"],
                    "foo bar (foo bar)": ["X:4"],
                    "foo bar [foo bar]": ["X:5"],
                    "other foo bar": ["X:6"],
                    "other  (foo) [bar] foo bar": ["X:7"],
                },
            ),
            (
                [whitespace_norm],
                {
                    "foo bar": ["X:1", "X:3"],
                    "FOO BAR": ["X:2"],
                    "foo bar (foo bar)": ["X:4"],
                    "foo bar [foo bar]": ["X:5"],
                    "Other foo bar": ["X:6"],
                    "Other (FOO) [bar] foo bar": ["X:7"],
                },
            ),
            (
                [synonymization],
                {
                    "FOO BAR": ["X:2"],
                    "foo  bar": ["X:3"],
                    "foo bar": ["X:1", "X:4", "X:5", "X:6", "X:7"],
                },
            ),
            (
                [case_norm, whitespace_norm, synonymization],
                {"foo bar": ["X:1", "X:2", "X:3", "X:4", "X:5", "X:6", "X:7"]},
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
                self.assertCountEqual(expected[k], groupings[k])
            self.assertEqual(expected.keys(), groupings.keys())

    def test_save(self):
        save_lexical_index(self.lexical_index, TEST_OUT)

    def test_synonymizer_with_other(self):
        """Test synonymizer with 'other' in label."""
        resource = OntologyResource(slug="foo_bar.obo", directory=INPUT_DIR, local=True)
        oi = SimpleOboImplementation(resource)
        syn_param = [
            Synonymizer(
                description="Broad match terms with the term 'other' in them.",
                match="(?i)^Other ",  # noqa W605
                match_scope="*",
                replacement="",
                qualifier="broad",
            ),
        ]
        synonymization = LexicalTransformation(TransformationType.Synonymization, params=syn_param)
        pipelines = [
            LexicalTransformationPipeline(name="test_other", transformations=synonymization)
        ]
        lexical_index = create_lexical_index(oi, pipelines=pipelines, synonym_rules=syn_param)

        for _, v in lexical_index.groupings.items():
            relation = [x for x in v.relationships if x.synonymized is True]
            self.assertTrue(len(relation), 1)
            self.assertEqual(relation[0].predicate, "oio:hasBroadSynonym")
