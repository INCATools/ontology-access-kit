import logging
import unittest

from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.resource import OntologyResource

from tests import OUTPUT_DIR, INPUT_DIR, VACUOLE, DIGIT, CELLULAR_COMPONENT, SHAPE

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestOntobeeImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = OntobeeImplementation(OntologyResource())
        self.oi = oi
        cl_graph_oi = OntobeeImplementation(OntologyResource('cl'))
        self.cl_graph_oi = cl_graph_oi
        pato_graph_oi = OntobeeImplementation(OntologyResource('pato'))
        self.pato_graph_oi = pato_graph_oi

    def test_relationships(self):
        ont = self.oi
        rels = ont.get_outgoing_relationships_by_curie(VACUOLE)
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn('GO:0005737', rels[PART_OF])

    def test_parents(self):
        parents = self.oi.get_parents_by_curie(VACUOLE)
        #print(parents)
        assert 'GO:0043231' in parents

    def test_labels(self):
        label = self.oi.get_label_by_curie(DIGIT)
        logging.info(label)
        self.assertEqual(label, 'digit')

    def test_subontology(self):
        oi = self.pato_graph_oi
        self.assertIsNotNone(oi.named_graph)
        label = oi.get_label_by_curie(DIGIT)
        self.assertIsNone(label)
        #logging.info(label)
        #self.assertEqual(label, 'digit')
        self.assertEqual('shape', oi.get_label_by_curie(SHAPE))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        logging.info(syns)
        assert 'cellular component' in syns

    def test_definition(self):
        defn = self.oi.get_definition_by_curie(CELLULAR_COMPONENT)
        logging.info(defn)
        assert defn

    #@unittest.skip('Too slow')
    def test_search(self):
        config = SearchConfiguration(complete=True).use_label_only()
        curies = list(self.oi.basic_search('limb', config=config))
        print(curies)
        assert 'UBERON:0002101' in curies