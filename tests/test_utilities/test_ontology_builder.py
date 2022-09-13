import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.lexical_index import (
    LexicalTransformation,
    LexicalTransformationPipeline,
    TransformationType,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import (
    create_lexical_index,
    save_lexical_index,
)
from oaklib.utilities.ontology_builder import OntologyBuilder
from tests import INPUT_DIR, OUTPUT_DIR


class TestOntologyBuilder(unittest.TestCase):
    def test_builder(self):
        """
        Tests simple ontology building operations
        """
        oi = ProntoImplementation()
        builder = OntologyBuilder(oi)
        builder.add_class("X:1", "x1")
        builder.add_class("X:2", "x2", is_as=["X:1"])
        builder.build()
        labels = list(oi.labels(oi.entities()))
        self.assertCountEqual([("X:1", "x1"), ("X:2", "x2")], labels)
        rels = list(oi.relationships())
        self.assertCountEqual([("X:2", "rdfs:subClassOf", "X:1")], rels)
