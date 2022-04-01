import logging
import unittest

from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.vocabulary.vocabulary import IS_A
from pronto import Ontology

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestRelationshipWalker(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_walk_up(self):
        oi = self.oi
        rels = list(walk_up(oi, 'GO:0005773'))
        print('ALL')
        for rel in rels:
            logging.info(rel)
        assert ('GO:0043227', 'has_part', 'GO:0016020') in rels
        print('**IS_A')
        rels = list(walk_up(oi, 'GO:0005773', predicates=[IS_A]))
        for rel in rels:
            logging.info(rel)
            self.assertEqual(rel[1], IS_A)
        assert ('GO:0043227', 'has_part', 'GO:0016020') not in rels
        assert ('GO:0110165', 'rdfs:subClassOf', 'CARO:0000000') in rels






