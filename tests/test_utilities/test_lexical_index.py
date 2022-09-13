import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.lexical_index import LexicalTransformation, TransformationType, LexicalTransformationPipeline
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
        builder.build()
        cases = [
            (None, {"foo bar": ["X:1", "X:2", "X:3"]}),
            ([LexicalTransformation(TransformationType.CaseNormalization)],
             {"foo bar": ["X:1", "X:2"],
              "foo  bar": ["X:3"]}),
            ([LexicalTransformation(TransformationType.WhitespaceNormalization)],
             {"foo bar": ["X:1", "X:3"],
              "FOO BAR": ["X:2"]}),
        ]
        for trs, expected in cases:
            if trs:
                pipelines = [LexicalTransformationPipeline(name="default", transformations=trs)]
            else:
                pipelines = None
            lexical_index = create_lexical_index(oi, pipelines=pipelines)
            groupings = {}
            for k, v in lexical_index.groupings.items():
                groupings[k] = [x.element for x in v.relationships]
            self.assertEqual(expected, groupings)





    def test_save(self):
        save_lexical_index(self.lexical_index, TEST_OUT)
