"""Test Ontobee Implementation."""
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
    """Test Ontobee Implementation."""

    def setUp(self) -> None:
        """Set up."""
        oi = OntobeeImplementation(OntologyResource())
        self.oi = oi
        cl_graph_oi = OntobeeImplementation(OntologyResource("cl"))
        self.cl_graph_oi = cl_graph_oi
        pato_graph_oi = OntobeeImplementation(OntologyResource("pato"))
        self.pato_graph_oi = pato_graph_oi

    def test_relationships(self):
        """Test relationships."""
        ont = self.oi
        rels = ont.get_outgoing_relationship_map_by_curie(VACUOLE)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertIn("GO:0043231", rels[IS_A])
        self.assertIn("GO:0005737", rels[PART_OF])

    def test_parents(self):
        """Test parents."""
        parents = self.oi.get_hierararchical_parents_by_curie(VACUOLE)
        # print(parents)
        assert "GO:0043231" in parents

    def test_labels(self):
        """Test labels."""
        label = self.oi.get_label_by_curie(DIGIT)
        logging.info(label)
        self.assertEqual(label, "digit")

    def test_subontology(self):
        """Test subontology."""
        oi = self.pato_graph_oi
        self.assertIsNotNone(oi.named_graph)
        label = oi.get_label_by_curie(DIGIT)
        self.assertIsNone(label)
        # logging.info(label)
        # self.assertEqual(label, 'digit')
        self.assertEqual("shape", oi.get_label_by_curie(SHAPE))

    def test_synonyms(self):
        """Test synonyms."""
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        logging.info(syns)
        assert "cellular component" in syns

    def test_definition(self):
        """Test definition."""
        defn = self.oi.get_definition_by_curie(CELLULAR_COMPONENT)
        logging.info(defn)
        assert defn

    def test_search_exact(self):
        """Test 'search exact' feature."""
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("limb", config=config))
        # print(curies)
        assert "UBERON:0002101" in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.LABEL])
        curies = list(self.oi.basic_search("limb", config=config))
        # print(curies)
        assert "UBERON:0002101" in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("limb", config=config))
        # print(curies)
        assert "UBERON:0002101" in curies
        assert len(curies) > 1

    def test_search_partial(self):
        """Test 'search partial' feature."""
        config = SearchConfiguration(is_partial=True)
        # non-exact matches across all ontobee are slow: restrict to pato
        curies = list(self.pato_graph_oi.basic_search("diameter", config=config))
        # print(curies)
        self.assertGreater(len(curies), 1)
        assert "PATO:0001334" in curies

    def test_search_starts_with(self):
        """Test 'search starts with' feature."""
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.pato_graph_oi.basic_search("diamet", config=config))
        # print(curies)
        # self.assertGreater(len(curie), 1)
        assert "PATO:0001334" in curies

    def test_search_regex(self):
        """Test search regex."""
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.pato_graph_oi.basic_search("ed diameter$", config=config))
        print(curies)
        # self.assertGreater(len(curie), 1)
        assert "PATO:0001714" in curies
