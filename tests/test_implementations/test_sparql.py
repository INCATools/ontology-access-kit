import logging
import shutil
import unittest

from oaklib.datamodels import obograph
from oaklib.datamodels.search_datamodel import SearchTermSyntax, SearchProperty
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.datamodels.search import SearchConfiguration
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import index_graph_nodes, index_graph_edges_by_subject, \
    index_graph_edges_by_object, index_graph_edges_by_predicate, graph_as_dict

from tests import OUTPUT_DIR, INPUT_DIR, VACUOLE, DIGIT, CELLULAR_COMPONENT, SHAPE, NUCLEUS, CATALYTIC_ACTIVITY, \
    NUCLEAR_ENVELOPE, CYTOPLASM, FAKE_ID, FAKE_PREDICATE

TEST_RDF = INPUT_DIR / 'go-nucleus.owl.ttl'
TEST_MUTABLE_RDF = OUTPUT_DIR / 'go-nucleus.owl.ttl'


class TestSparqlImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_RDF)))
        self.oi = oi

    def test_relationships(self):
        oi = self.oi
        self.assertIsNotNone(oi.graph)
        rels = oi.get_outgoing_relationships_by_curie(VACUOLE)
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn('GO:0005737', rels[PART_OF])

    def test_parents(self):
        parents = self.oi.get_parents_by_curie(VACUOLE)
        #print(parents)
        assert 'GO:0043231' in parents

    def test_labels(self):
        label = self.oi.get_label_by_curie(NUCLEUS)
        logging.info(label)
        self.assertEqual(label, 'nucleus')
        self.assertEqual(self.oi.get_curies_by_label(label), [NUCLEUS])

    @unittest.skip('TODO')
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
        assert 'cellular_component' in syns
        syns = self.oi.aliases_by_curie(NUCLEUS)
        logging.info(syns)
        self.assertCountEqual(syns, ['nucleus', 'cell nucleus', 'horsetail nucleus'])
        syn_pairs = list(self.oi.alias_map_by_curie(NUCLEUS).items())
        self.assertCountEqual(syn_pairs,
                              [('oio:hasExactSynonym', ['cell nucleus']),
                               ('oio:hasNarrowSynonym', ['horsetail nucleus']),
                               ('rdfs:label', ['nucleus'])])

    def test_all_entity_curies(self):
        curies = list(self.oi.all_entity_curies())
        self.assertGreater(len(curies), 100)
        self.assertIn(NUCLEUS, curies)

    def test_definition(self):
        defn = self.oi.get_definition_by_curie(CELLULAR_COMPONENT)
        assert defn.startswith('A location, relative to cellular compartments')

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search('nucleus', config=config))
        #print(curies)
        assert NUCLEUS in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.LABEL])
        curies = list(self.oi.basic_search('nucleus', config=config))
        assert NUCLEUS in curies
        curies = list(self.oi.basic_search('enzyme activity', config=config))
        assert curies == []
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search('enzyme activity', config=config))
        assert CATALYTIC_ACTIVITY in curies

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        # non-exact matches across all ontobee are slow: restrict to pato
        curies = list(self.oi.basic_search('ucl', config=config))
        #print(curies)
        self.assertGreater(len(curies), 1)
        assert NUCLEUS in curies

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

    @unittest.skip('TODO')
    def test_obograph_todo(self):
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A, PART_OF]))
        assert VACUOLE in descs
        assert CYTOPLASM in descs
        g = self.oi.ancestor_graph(CYTOPLASM)
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == CYTOPLASM]))

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search('nucl', config=config))
        #print(curies)
        #self.assertGreater(len(curie), 1)
        assert NUCLEUS in curies

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.oi.basic_search('nucl.* envelope$', config=config))
        print(curies)
        #self.assertGreater(len(curie), 1)
        assert NUCLEAR_ENVELOPE in curies

    def test_mutable(self):
        """
        Tests the SPARQL store can be modified

        Currently only tests
        """
        shutil.copyfile(TEST_RDF, TEST_MUTABLE_RDF)
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_MUTABLE_RDF)))
        label = oi.get_label_by_curie(NUCLEUS)
        preds = [IS_A, PART_OF]
        preds2 = [IS_A, FAKE_PREDICATE]
        ancestors = list(oi.ancestors(NUCLEUS, predicates=preds))
        descendants = list(oi.descendants(NUCLEUS, predicates=preds))
        def non_reflexive(l):
            return [a for a in ancestors if a != NUCLEUS and a != PART_OF and a != FAKE_PREDICATE]
        expected_ancs = non_reflexive(ancestors)
        descendants_ancs = non_reflexive(descendants)
        oi.migrate_curies({NUCLEUS: FAKE_ID,
                           PART_OF: FAKE_PREDICATE})
        self.assertEqual(label, oi.get_label_by_curie(FAKE_ID))
        self.assertIsNone(oi.get_label_by_curie(NUCLEUS))
        self.assertCountEqual(expected_ancs, non_reflexive(oi.ancestors(FAKE_ID, predicates=preds2)))
        self.assertCountEqual([], list(oi.ancestors(NUCLEUS, predicates=preds)))
        self.assertCountEqual(descendants_ancs, non_reflexive(oi.descendants(FAKE_ID, predicates=preds2)))
        self.assertCountEqual([], list(oi.descendants(NUCLEUS, predicates=preds)))
        oi.save()

