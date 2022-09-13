import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.utilities.ontology_builder import OntologyBuilder


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
