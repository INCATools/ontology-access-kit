import logging
import unittest

import yaml
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.vocabulary.vocabulary import IS_A, PART_OF, HAS_PART

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'

CYTOPLASM = 'GO:0005737'

class TestProntoImplementation(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationships_by_curie('GO:0005773')
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0043231'])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])

    def test_incoming_relationships(self):
        oi = self.oi
        rels = oi.get_incoming_relationships_by_curie(CYTOPLASM)
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0005938', 'GO:0099568'])
        self.assertCountEqual(rels[PART_OF], ['GO:0005773', 'GO:0099568'])

    def test_all_terms(self):
        assert any(curie for curie in self.oi.all_entity_curies() if curie == 'GO:0008152')

    def test_relations(self):
        oi = self.oi
        label = oi.get_label_by_curie(PART_OF)
        assert label.startswith('part')
        t = self.oi.node(PART_OF)
        assert t.id == PART_OF
        assert t.label.startswith('part')

    def test_metadata(self):
        for curie in self.oi.all_entity_curies():
            m = self.oi.metadata_map_by_curie(curie)
            print(f'{curie} {m}')
        m = self.oi.metadata_map_by_curie('GO:0005622')
        assert 'term_tracker_item' in m.keys()
        assert 'https://github.com/geneontology/go-ontology/issues/17776' in m['term_tracker_item']

    def test_labels(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        :return:
        """
        oi = self.oi
        label = oi.get_label_by_curie('GO:0005773')
        self.assertEqual(str,  type(label))
        self.assertEqual(label, 'vacuole')
        label = oi.get_label_by_curie('FOOBAR:123')
        self.assertIsNone(label)
        # TODO: test strict mode
        label = oi.get_label_by_curie(IS_A)
        self.assertIsNotNone(label)

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie('GO:0005575')
        #print(syns)
        self.assertCountEqual(syns, ['cellular_component',
                                    'cellular component',
                                    'cell or subcellular entity',
                                    'subcellular entity'])

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.all_subset_curies())
        self.assertIn('goslim_aspergillus', subsets)
        self.assertIn('GO:0003674', oi.curies_by_subset('goslim_generic'))
        self.assertNotIn('GO:0003674', oi.curies_by_subset('gocheck_do_not_manually_annotate'))

    def test_save(self):
        oi = ProntoImplementation.create()
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.create_entity('FOO:1', label='foo', relationships={IS_A: ['FOO:2'], 'part_of': ['FOO:3']})
        oi.store(OntologyResource(slug='go-nucleus.saved.obo', directory=OUTPUT_DIR, local=True, format='obo'))

    def test_from_obo_library(self):
        oi = ProntoImplementation.create(OntologyResource(local=False, slug='pato.obo'))
        curies = oi.get_curies_by_label('shape')
        self.assertEqual(['PATO:0000052'], curies)

    @unittest.skip('Hide warnings')
    def test_from_owl(self):
        r = OntologyResource(local=True, slug='go-nucleus.owl', directory=INPUT_DIR)
        oi = ProntoImplementation.create(r)
        rels = list(oi.walk_up_relationship_graph('GO:0005773'))
        for rel in rels:
            print(rel)

    def test_subontology(self):
        subont = self.oi.create_subontology(['GO:0005575', 'GO:0005773'])
        subont.store(OntologyResource(slug='go-nucleus.filtered.obo', directory=OUTPUT_DIR, local=True, format='obo'))

    def test_qc(self):
        oi = self.oi
        for t in oi.term_curies_without_definitions():
            print(t)
        self.assertIn('CARO:0000003', oi.term_curies_without_definitions())

    def test_walk_up(self):
        oi = self.oi
        rels = list(oi.walk_up_relationship_graph('GO:0005773'))
        print('ALL')
        for rel in rels:
            logging.info(rel)
        assert ('GO:0043227', HAS_PART, 'GO:0016020') in rels
        print('**IS_A')
        rels = list(oi.walk_up_relationship_graph('GO:0005773', predicates=[IS_A]))
        for rel in rels:
            logging.info(rel)
            self.assertEqual(rel[1], IS_A)
        assert ('GO:0043227', HAS_PART, 'GO:0016020') not in rels
        assert ('GO:0110165', IS_A, 'CARO:0000000') in rels

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors('GO:0005773'))
        for a in ancs:
            logging.info(a)
        assert 'NCBITaxon:1' in ancs
        assert 'GO:0005773' in ancs  # reflexive
        ancs = list(oi.ancestors('GO:0005773', predicates=[IS_A]))
        for a in ancs:
            print(a)
        assert 'NCBITaxon:1' not in ancs
        assert 'GO:0005773' in ancs  # reflexive
        assert 'GO:0043231' in ancs  # reflexive

    def test_obograph(self):
        g = self.oi.ancestor_graph('GO:0005773')
        obj = graph_as_dict(g)
        print(yaml.dump(obj))





