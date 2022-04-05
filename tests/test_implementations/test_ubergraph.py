import logging
import unittest

from oaklib.implementations.ubergraph.ubergraph_implementation import UbergraphImplementation
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.vocabulary.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


DIGIT = 'UBERON:0002544'

class TestUbergraphImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = UbergraphImplementation()
        self.oi = oi

    def test_relationships(self):
        ont = self.oi
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn('GO:0005737', rels[PART_OF])

    def test_labels(self):
        label = self.oi.get_label_by_curie(DIGIT)
        self.assertEqual(label, 'digit')
        self.assertIn(DIGIT, self.oi.get_curies_by_label(label))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie('GO:0005575')
        logging.info(syns)
        assert 'cellular component' in syns

    def test_definition(self):
        defn = self.oi.get_definition_by_curie('GO:0005575')
        logging.info(defn)
        assert defn

    @unittest.skip('Too slow')
    def test_search(self):
        config = SearchConfiguration(complete=True).use_label_only()
        curies = list(self.oi.basic_search('limb', config=config))
        print(curies)
        assert 'UBERON:0002101' in curies


