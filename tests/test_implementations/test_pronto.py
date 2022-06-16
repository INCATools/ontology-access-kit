import logging
import unittest

from kgcl_schema.datamodel import kgcl
from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchTermSyntax, SearchProperty
from oaklib.implementations import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from oaklib.utilities.obograph_utils import graph_as_dict, index_graph_nodes, index_graph_edges_by_subject, \
    index_graph_edges_by_object, index_graph_edges_by_predicate
from oaklib.datamodels.vocabulary import IS_A, PART_OF, HAS_PART, ONLY_IN_TAXON, IN_TAXON

from tests import OUTPUT_DIR, INPUT_DIR, VACUOLE, CYTOPLASM, CELL, CELLULAR_ORGANISMS, NUCLEUS

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_SIMPLE_ONT = INPUT_DIR / 'go-nucleus-simple.obo'
TEST_ONT_COPY = OUTPUT_DIR / 'go-nucleus.copy.obo'
TEST_SUBGRAPH_OUT = OUTPUT_DIR / 'vacuole.obo'


class TestProntoImplementation(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_obo_json(self) -> None:
        resource = OntologyResource(slug='go-nucleus.json', directory=INPUT_DIR, local=True)
        json_oi = ProntoImplementation(resource)
        oi_src = self.oi
        curies = list(json_oi.all_entity_curies())
        #for e in curies:
        #    print(e)
        self.assertIn(NUCLEUS, curies)
        #for e in oi_src.all_entity_curies():
        #    self.assertIn(e, curies)
        #    assert e in list(oi_src.all_entity_curies())
        # TODO: pronto obo parsing excludes alt_ids
        #self.assertCountEqual(list(json_oi.all_entity_curies()), list(oi_src.all_entity_curies()))
        # TODO: workaround for https://github.com/althonos/pronto/issues/164
        #json_oi.store(OntologyResource(slug='go-nucleus.from-json.obo', directory=OUTPUT_DIR, local=True, format='obo'))

    def test_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationship_map_by_curie('GO:0005773')
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0043231'])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])

    @unittest.skip('https://github.com/althonos/pronto/issues/163')
    def test_gci_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationship_map_by_curie(CELL)
        self.assertCountEqual(rels[IS_A], ['CARO:0000003'])
        self.assertCountEqual(rels[ONLY_IN_TAXON], [CELLULAR_ORGANISMS])
        self.assertNotIn(NUCLEUS, rels[PART_OF])

    def test_incoming_relationships(self):
        oi = self.oi
        rels = oi.get_incoming_relationship_map_by_curie(CYTOPLASM)
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
        assert t.lbl.startswith('part')

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
        syns = self.oi.aliases_by_curie(NUCLEUS)
        logging.info(syns)
        self.assertCountEqual(syns, ['nucleus', 'cell nucleus', 'horsetail nucleus'])
        syn_pairs = list(self.oi.alias_map_by_curie(NUCLEUS).items())
        self.assertCountEqual(syn_pairs,
                              [('oio:hasExactSynonym', ['cell nucleus']),
                               ('oio:hasNarrowSynonym', ['horsetail nucleus']),
                               ('rdfs:label', ['nucleus'])])

    def test_mappings(self):
        oi = self.oi
        mappings = list(oi.get_sssom_mappings_by_curie(NUCLEUS))
        #for m in mappings:
        #    print(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == 'Wikipedia:Cell_nucleus')
        self.assertEqual(len(mappings), 2)
        for m in mappings:
            print(f'GETTING {m.object_id}')
            reverse_mappings = list(oi.get_sssom_mappings_by_curie(m.object_id))
            reverse_subject_ids = [m.subject_id for m in reverse_mappings]
            self.assertEqual(reverse_subject_ids, [NUCLEUS])

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
        g = self.oi.ancestor_graph(VACUOLE)
        nix = index_graph_nodes(g)
        self.assertEqual(nix[VACUOLE].lbl, 'vacuole')
        v2c = obograph.Edge(sub=VACUOLE, pred=PART_OF, obj=CYTOPLASM)
        six = index_graph_edges_by_subject(g)
        self.assertIn(v2c, six[VACUOLE])
        self.assertNotIn(v2c, six[CYTOPLASM])
        oix = index_graph_edges_by_object(g)
        self.assertIn(v2c, oix[CYTOPLASM])
        self.assertNotIn(v2c, oix[VACUOLE])
        pix = index_graph_edges_by_predicate(g)
        self.assertIn(v2c, pix[PART_OF])
        self.assertNotIn(v2c, pix[IS_A])
        obj = graph_as_dict(g)
        assert 'nodes' in g
        assert 'edges' in g
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == VACUOLE]))
        ancs = list(self.oi.ancestors(VACUOLE, predicates=[IS_A, PART_OF]))
        assert VACUOLE in ancs
        assert CYTOPLASM in ancs
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A, PART_OF]))
        assert VACUOLE in descs
        assert CYTOPLASM in descs
        g = self.oi.ancestor_graph(CYTOPLASM)
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == CYTOPLASM]))

    def test_save_extract(self):
        g = self.oi.ancestor_graph(VACUOLE)
        oi = ProntoImplementation()
        oi.load_graph(g, replace=True)
        r = OntologyResource(slug=str(TEST_SUBGRAPH_OUT), format='obo', local=True)
        oi.store(r)

    def test_search_aliases(self):
        config = SearchConfiguration(properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, ['GO:0003824'])
        config = SearchConfiguration()
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, [])

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("cytoplasm", config=config))
        #print(curies)
        assert CYTOPLASM in curies

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        curies = list(self.oi.basic_search("nucl", config=config))
        #print(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search("nucl", config=config))
        #print(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.oi.basic_search("^nucl", config=config))
        print(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    @unittest.skip('https://github.com/althonos/pronto/issues/175')
    def test_dump(self):
        COPY = 'go-nucleus.copy.obo'
        OUTPUT_DIR.mkdir(exist_ok=True)
        resource = OntologyResource(slug=COPY, directory=OUTPUT_DIR, local=True, format='obo')
        self.oi.dump(str(OUTPUT_DIR / COPY), syntax='obo')

    def test_patcher(self):
        resource = OntologyResource(slug=TEST_SIMPLE_ONT, local=True)
        oi = ProntoImplementation(resource)
        oi.apply_patch(kgcl.NodeObsoletion(id=generate_change_id(), about_node=NUCLEUS))
        with self.assertRaises(ValueError) as e:
            oi.apply_patch(kgcl.NodeObsoletion(id='x', about_node='NO SUCH TERM'))
        oi.dump(str(OUTPUT_DIR / 'post-kgcl.obo'), syntax='obo')












