import logging
import unittest

from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestOntobeeImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = OntobeeImplementation()
        self.basic_ont = oi

    def test_relationships(self):
        ont = self.basic_ont
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn('GO:0005737', rels[PART_OF])

    def test_parents(self):
        parents = self.basic_ont.get_parents_by_curie('GO:0005773')
        #print(parents)
        assert 'GO:0043231' in parents

    def test_labels(self):
        label = self.basic_ont.get_label_by_curie('UBERON:0002544')
        logging.info(label)
        self.assertEqual(label, 'digit')

    def test_synonyms(self):
        syns = self.basic_ont.aliases_by_curie('GO:0005575')
        logging.info(syns)
        assert 'cellular component' in syns

    def test_definition(self):
        defn = self.basic_ont.get_definition_by_curie('GO:0005575')
        logging.info(defn)
        assert defn

