import unittest

from obolib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from obolib.vocabulary.vocabulary import IS_A

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestOntobeeProvider(unittest.TestCase):
    """tests pronto """

    def setUp(self) -> None:
        oi = OntobeeImplementation.create()
        self.basic_ont = oi

    @unittest.skip('TODO')
    def test_relationships(self):
        ont = self.basic_ont
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0005773', 'GO:0043231'])
        self.assertCountEqual(rels['part_of'], ['GO:0005737'])

    def test_parents(self):
        parents = self.basic_ont.get_parents_by_curie('GO:0005773')
        print(parents)

    def test_labels(self):
        label = self.basic_ont.get_label_by_curie('UBERON:0002544')
        print(label)
        self.assertEqual(label, 'digit')

    def test_synonyms(self):
        syns = self.basic_ont.aliases_by_curie('GO:0005575')
        print(syns)
        assert 'cellular component' in syns

