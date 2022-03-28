import unittest

from obolib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from obolib.implementations.sqldb.sql_implementation import SqlImplementation
from obolib.interfaces.basic_ontology_interface import SearchConfiguration
from obolib.resource import OntologyResource
from obolib.vocabulary.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR

DB = INPUT_DIR / 'go-nucleus.db'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestSqlDatabaseProvider(unittest.TestCase):

    def setUp(self) -> None:
        print(f'DB={str(DB)}')
        oi = SqlImplementation.create(OntologyResource(slug=f'sqlite:///{str(DB)}'))
        self.basic_ont = oi

    def test_relationships(self):
        ont = self.basic_ont
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0043231'])
        self.assertCountEqual(rels[PART_OF], ['GO:0005737'])

    def test_all_nodes(self):
        for curie in self.basic_ont.all_entity_curies():
            print(curie)

    def test_labels(self):
        label = self.basic_ont.get_label_by_curie('GO:0005773')
        self.assertEqual(label, 'vacuole')

    def test_search(self):
        oi = self.basic_ont
        for curie in oi.basic_search('intracellular'):
            print(curie)
        self.assertIn('GO:0005622', oi.basic_search('intracellular'))
        c = SearchConfiguration()
        self.assertEqual(list(oi.basic_search('protoplasm')), ['GO:0005622'])
        self.assertEqual(list(oi.basic_search('protoplasm', SearchConfiguration(include_aliases=False))), [])

    @unittest.skip("TODO")
    def test_synonyms(self):
        syns = self.basic_ont.aliases_by_curie('GO:0005575')
        print(syns)
        assert 'cellular component' in syns

