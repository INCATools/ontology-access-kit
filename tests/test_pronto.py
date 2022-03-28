import unittest

from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.vocabulary.vocabulary import IS_A
from pronto import Ontology

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestProntoProvider(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        ont = ProntoImplementation.create(resource)
        self.basic_ont = ont

    def test_relationships(self):
        ont = self.basic_ont
        rels = ont.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0005773', 'GO:0043231'])
        self.assertCountEqual(rels['part_of'], ['GO:0005737'])

    def test_all_terms(self):
        assert any(curie for curie in self.basic_ont.all_entity_curies() if curie == 'GO:0008152')

    def test_metadata(self):
        for curie in self.basic_ont.all_entity_curies():
            m = self.basic_ont.metadata_map_by_curie(curie)
            print(f'{curie} {m}')
        m = self.basic_ont.metadata_map_by_curie('GO:0005622')
        assert 'term_tracker_item' in m.keys()
        assert 'https://github.com/geneontology/go-ontology/issues/17776' in m['term_tracker_item']


    def test_labels(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        :return:
        """
        ont = self.basic_ont
        label = ont.get_label_by_curie('GO:0005773')
        self.assertEqual(label, 'vacuole')
        label = ont.get_label_by_curie('FOOBAR:123')
        self.assertIsNone(label)
        # TODO: test strict mode
        label = ont.get_label_by_curie(IS_A)
        self.assertIsNotNone(label)


    def test_synonyms(self):
        syns = self.basic_ont.aliases_by_curie('GO:0005575')
        #print(syns)
        self.assertCountEqual(syns, ['cellular_component',
                                    'cellular component',
                                    'cell or subcellular entity',
                                    'subcellular entity'])

    def test_save(self):
        ont = ProntoImplementation.create()
        OUTPUT_DIR.mkdir(exist_ok=True)
        ont.create_entity('FOO:1', label='foo', relationships = {IS_A: ['FOO:2'], 'part_of': ['FOO:3']})
        ont.store(OntologyResource(slug='go-nucleus.saved.obo', directory=OUTPUT_DIR, local=True, format='obo'))

    def test_from_obo_library(self):
        ont = ProntoImplementation.create(OntologyResource(local=False, slug='pato.obo'))
        curies = ont.get_curies_by_label('shape')
        self.assertEqual(['PATO:0000052'], curies)

    def test_subontology(self):
        subont = self.basic_ont.create_subontology(['GO:0005575', 'GO:0005773'])
        subont.store(OntologyResource(slug='go-nucleus.filtered.obo', directory=OUTPUT_DIR, local=True, format='obo'))

    def test_qc(self):
        ont = self.basic_ont
        for t in ont.term_curies_without_definitions():
            print(t)
        self.assertIn('CARO:0000003', ont.term_curies_without_definitions())



