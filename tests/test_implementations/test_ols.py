"""Test OLS Implementation."""
import itertools
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.search import SearchConfiguration, SearchProperty
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, CYTOPLASM, DIGIT, VACUOLE


class TestOlsImplementation(unittest.TestCase):
    """Test OLS Implementation."""

    def setUp(self) -> None:
        """Set up."""
        oi = OlsImplementation(OntologyResource("go"))
        self.oi = oi

    def test_mappings(self):
        """Test mappings."""
        oi = self.oi
        mappings = list(oi.get_sssom_mappings_by_curie(DIGIT))
        for m in mappings:
            print(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == "EMAPA:32725")

    def test_ancestors(self):
        """Test ancestors."""
        oi = self.oi
        ancs = list(oi.ancestors([VACUOLE]))
        # for a in ancs:
        #    print(a)
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A]))
        # for a in ancs:
        #    print(a)
        assert CYTOPLASM not in ancs
        assert CELLULAR_COMPONENT in ancs

    def test_basic_search(self):
        """Test basic search."""
        self.oi.focus_ontology = None
        results = list(itertools.islice(self.oi.basic_search("epilepsy"), 20))
        self.assertIn("MONDO:0005027", results)

    def test_focus_ontology_search(self):
        """Test focus ontology search."""
        self.oi.focus_ontology = "MONDO"
        results = list(itertools.islice(self.oi.basic_search("epilepsy"), 20))
        for result in results:
            self.assertRegex(result, "^MONDO:")

    def test_search_configuration(self):
        """Test search configuration."""
        self.oi.focus_ontology = None

        config = SearchConfiguration(properties=[SearchProperty.LABEL])
        results = list(itertools.islice(self.oi.basic_search("swimming", config), 20))
        self.assertIn("GO:0036268", results)  # GO:0036268 == swimming
        self.assertNotIn("NBO:0000371", results)  # NBO:0000371 == aquatic locomotion

        config = SearchConfiguration(is_complete=True)
        results = list(itertools.islice(self.oi.basic_search("swimming", config), 20))
        self.assertIn("OMIT:0014415", results)  # OMIT:0014415 == Swimming
        self.assertNotIn("OMIT:0014416", results)  # OMIT:0014416 == Swimming Pools
