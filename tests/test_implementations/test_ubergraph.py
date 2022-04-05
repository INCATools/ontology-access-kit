import logging
import unittest

from oaklib.implementations.ubergraph.ubergraph_implementation import UbergraphImplementation
from oaklib.vocabulary.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestUbergraphImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = UbergraphImplementation()
        self.basic_ont = oi

    def test_relationships(self):
        ont = self.basic_ont
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn('GO:0005737', rels[PART_OF])

    def test_labels(self):
        label = self.basic_ont.get_label_by_curie('UBERON:0002544')
        self.assertEqual(label, 'digit')

    def test_synonyms(self):
        syns = self.basic_ont.aliases_by_curie('GO:0005575')
        logging.info(syns)
        assert 'cellular component' in syns

    def test_definition(self):
        defn = self.basic_ont.get_definition_by_curie('GO:0005575')
        logging.info(defn)
        assert defn


