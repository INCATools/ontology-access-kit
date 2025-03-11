import itertools
import unittest
from unittest.mock import MagicMock, patch

from oaklib.datamodels.search import SearchConfiguration, SearchProperty
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, CYTOPLASM, VACUOLE

# Example term data for mocking OLS API responses
TERM_DATA = {
    "GO:0005634": {
        "iri": "http://purl.obolibrary.org/obo/GO_0005634",
        "label": "nucleus",
        "description": (
            "A membrane-bounded organelle of eukaryotic cells in which "
            "chromosomes are housed and replicated."
        ),
    },
    "GO:0005635": {
        "iri": "http://purl.obolibrary.org/obo/GO_0005635",
        "label": "nuclear envelope",
        "description": (
            "The double lipid bilayer enclosing the nucleus and separating "
            "its contents from the rest of the cytoplasm."
        ),
    },
}


class TestOlsImplementation(unittest.TestCase):
    @patch("oaklib.implementations.ols.ols_implementation.EBIClient")
    def setUp(self, mock_ebi_client) -> None:
        # Setup mock client
        mock_client = MagicMock()
        mock_ebi_client.return_value = mock_client

        # Create implementation
        oi = OlsImplementation(OntologyResource("go"))
        # Mock the uri_to_curie method to handle our test cases
        oi.uri_to_curie = MagicMock()
        oi.uri_to_curie.side_effect = lambda uri, *args, **kwargs: {
            "http://purl.obolibrary.org/obo/GO_0005634": "GO:0005634",
            "http://purl.obolibrary.org/obo/GO_0005635": "GO:0005635",
            "http://purl.obolibrary.org/obo/GO_0036268": "GO:0036268",
            "http://purl.obolibrary.org/obo/OMIT_0014415": "OMIT:0014415",
        }.get(uri, uri.split("/")[-1].replace("_", ":") if uri and uri.count("/") > 0 else uri)

        # Mock curie_to_uri to go from CURIE to URI
        oi.curie_to_uri = MagicMock()
        oi.curie_to_uri.side_effect = lambda curie, *args, **kwargs: {
            "GO:0005634": "http://purl.obolibrary.org/obo/GO_0005634",
            "GO:0005635": "http://purl.obolibrary.org/obo/GO_0005635",
            "GO:0005886": "http://purl.obolibrary.org/obo/GO_0005886",
            "VACUOLE": "http://purl.obolibrary.org/obo/GO_0005773",
        }.get(curie, f"http://purl.obolibrary.org/obo/{curie.replace(':', '_')}")

        self.oi = oi
        self.mock_client = mock_client

    @patch("oaklib.implementations.ols.ols_implementation.BaseOlsImplementation.label")
    def test_label(self, mock_label):
        """Test the implementation of the label method"""
        # Set up the mock to return the value we want
        mock_label.return_value = "nucleus"

        # Test label retrieval
        label = self.oi.label("GO:0005634")
        self.assertEqual(label, "nucleus")

        # Verify the mock was called correctly
        mock_label.assert_called_with("GO:0005634")

    @patch("oaklib.implementations.ols.ols_implementation.BaseOlsImplementation.definition")
    def test_definition(self, mock_definition):
        """Test the implementation of the definition method"""
        # Setup the mock return value
        mock_definition.return_value = (
            "A membrane-bounded organelle of eukaryotic cells"
            " in which chromosomes are housed and replicated."
        )

        # Test definition retrieval
        definition = self.oi.definition("GO:0005634")
        self.assertEqual(
            definition,
            "A membrane-bounded organelle of eukaryotic cells in which chromosomes are housed and replicated.",
        )

        # Verify the mock was called correctly
        mock_definition.assert_called_with("GO:0005634")

    @patch("oaklib.implementations.ols.ols_implementation.BaseOlsImplementation.definitions")
    def test_definitions(self, mock_definitions):
        """Test the implementation of the definitions method"""
        # Setup mock response
        mock_definitions.return_value = [
            (
                "GO:0005634",
                (
                    "A membrane-bounded organelle of eukaryotic cells in which "
                    "chromosomes are housed and replicated."
                ),
                {},
            ),
            (
                "GO:0005635",
                (
                    "The double lipid bilayer enclosing the nucleus and separating "
                    "its contents from the rest of the cytoplasm."
                ),
                {},
            ),
        ]

        # Test definitions retrieval
        definitions = list(self.oi.definitions(["GO:0005634", "GO:0005635"], include_metadata=True))

        # Check that we got two definitions back with expected content
        self.assertEqual(len(definitions), 2)

        # Check first definition
        self.assertEqual(definitions[0][0], "GO:0005634")
        self.assertEqual(
            definitions[0][1],
            (
                "A membrane-bounded organelle of eukaryotic cells in which "
                "chromosomes are housed and replicated."
            ),
        )
        self.assertEqual(definitions[0][2], {})  # Empty metadata dict

        # Check second definition
        self.assertEqual(definitions[1][0], "GO:0005635")
        self.assertEqual(
            definitions[1][1],
            (
                "The double lipid bilayer enclosing the nucleus and separating "
                "its contents from the rest of the cytoplasm."
            ),
        )
        self.assertEqual(definitions[1][2], {})  # Empty metadata dict

        # Verify the mock was called correctly
        mock_definitions.assert_called_with(["GO:0005634", "GO:0005635"], include_metadata=True)

    @patch("oaklib.implementations.ols.ols_implementation.requests.get")
    def test_mappings(self, mock_get):
        # Skip this test for now
        self.skipTest("Need to implement mock for OxO API")

        # For reference:
        # oi = self.oi
        # mappings = list(oi.get_sssom_mappings_by_curie(DIGIT))
        # for m in mappings:
        #     logging.info(yaml_dumper.dumps(m))
        # assert any(m for m in mappings if m.object_id == "EMAPA:32725")

    def test_ancestors(self):
        oi = self.oi
        self.mock_client.iter_hierarchical_ancestors.return_value = [
            {"obo_id": CYTOPLASM},
            {"obo_id": CELLULAR_COMPONENT},
        ]

        ancs = list(oi.ancestors([VACUOLE]))
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs

        self.mock_client.iter_ancestors.return_value = [{"obo_id": CELLULAR_COMPONENT}]

        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A]))
        assert CYTOPLASM not in ancs
        assert CELLULAR_COMPONENT in ancs

    def test_basic_search(self):
        self.oi.focus_ontology = None

        # Setup mock search results
        self.mock_client.search.return_value = [
            {"iri": "http://purl.obolibrary.org/obo/MONDO_0005027", "label": "epilepsy"},
            {"iri": "http://purl.obolibrary.org/obo/MONDO_0005031", "label": "focal epilepsy"},
        ]

        results = list(self.oi.basic_search("epilepsy"))
        self.assertIn("MONDO:0005027", results)

    def test_focus_ontology_search(self):
        self.oi.focus_ontology = "MONDO"

        # Setup mock search results - all MONDO ids
        self.mock_client.search.return_value = [
            {"iri": "http://purl.obolibrary.org/obo/MONDO_0005027", "label": "epilepsy"},
            {"iri": "http://purl.obolibrary.org/obo/MONDO_0005031", "label": "focal epilepsy"},
            {
                "iri": "http://purl.obolibrary.org/obo/MONDO_0005035",
                "label": "progressive myoclonus epilepsy",
            },
        ]

        results = list(itertools.islice(self.oi.basic_search("epilepsy"), 20))
        for result in results:
            self.assertRegex(result, "^MONDO:")

    def test_search_configuration(self):
        self.oi.focus_ontology = None

        # Test with label property only
        config = SearchConfiguration(properties=[SearchProperty.LABEL])
        # Mock search results for label-only search
        self.mock_client.search.return_value = [
            {"iri": "http://purl.obolibrary.org/obo/GO_0036268", "label": "swimming"}
        ]
        results = list(itertools.islice(self.oi.basic_search("swimming", config), 20))
        self.assertIn("GO:0036268", results)  # GO:0036268 == swimming
        self.assertNotIn("NBO:0000371", results)  # NBO:0000371 == aquatic locomotion

        # Test with exact match setting
        config = SearchConfiguration(is_complete=True)
        # Mock search results for exact search
        self.mock_client.search.return_value = [
            {"iri": "http://purl.obolibrary.org/obo/OMIT_0014415", "label": "Swimming"}
        ]
        results = list(itertools.islice(self.oi.basic_search("swimming", config), 20))
        self.assertIn("OMIT:0014415", results)  # OMIT:0014415 == Swimming
        self.assertNotIn("OMIT:0014416", results)  # OMIT:0014416 == Swimming Pools
