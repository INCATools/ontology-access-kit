import logging
import unittest

from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, DIGIT, INPUT_DIR, OUTPUT_DIR, SHAPE, VACUOLE

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"


@unittest.skip("Ontobee times out too often")
class TestOntobeeImplementation(unittest.TestCase):
    def setUp(self) -> None:
        oi = OntobeeImplementation(OntologyResource())
        self.oi = oi
        cl_graph_oi = OntobeeImplementation(OntologyResource("cl"))
        self.cl_graph_oi = cl_graph_oi
        pato_graph_oi = OntobeeImplementation(OntologyResource("pato"))
        self.pato_graph_oi = pato_graph_oi

    def test_relationships(self):
        ont = self.oi
        rels = ont.outgoing_relationship_map(VACUOLE)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertIn("GO:0043231", rels[IS_A])
        self.assertIn("GO:0005737", rels[PART_OF])

    def test_parents(self):
        parents = self.oi.hierarchical_parents(VACUOLE)
        # logging.info(parents)
        assert "GO:0043231" in parents

    def test_labels(self):
        label = self.oi.label(DIGIT)
        logging.info(label)
        self.assertEqual(label, "digit")

    def test_subontology(self):
        oi = self.pato_graph_oi
        self.assertIsNotNone(oi.named_graph)
        label = oi.label(DIGIT)
        self.assertIsNone(label)
        # logging.info(label)
        # self.assertEqual(label, 'digit')
        self.assertEqual("shape", oi.label(SHAPE))

    def test_synonyms(self):
        syns = self.oi.entity_aliases(CELLULAR_COMPONENT)
        logging.info(syns)
        assert "cellular component" in syns

    def test_definition(self):
        defn = self.oi.definition(CELLULAR_COMPONENT)
        logging.info(defn)
        assert defn

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("limb", config=config))
        # logging.info(curies)
        assert "UBERON:0002101" in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.LABEL])
        curies = list(self.oi.basic_search("limb", config=config))
        # logging.info(curies)
        assert "UBERON:0002101" in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("limb", config=config))
        # logging.info(curies)
        assert "UBERON:0002101" in curies
        assert len(curies) > 1

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        # non-exact matches across all ontobee are slow: restrict to pato
        curies = list(self.pato_graph_oi.basic_search("diameter", config=config))
        # logging.info(curies)
        self.assertGreater(len(curies), 1)
        assert "PATO:0001334" in curies

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.pato_graph_oi.basic_search("diamet", config=config))
        # logging.info(curies)
        # self.assertGreater(len(curie), 1)
        assert "PATO:0001334" in curies

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.pato_graph_oi.basic_search("ed diameter$", config=config))
        logging.info(curies)
        # self.assertGreater(len(curie), 1)
        assert "PATO:0001714" in curies
