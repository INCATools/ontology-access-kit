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
    def setUp(self) -> None:
        # Setup mock client
        mock_client = MagicMock()

        # Create implementation
        with patch.object(OlsImplementation, "ols_client_class", return_value=mock_client):
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

    def test_label_from_ols4_payload(self):
        """label() should parse the paged OLS4 ``_embedded.terms`` payload."""
        self.mock_client.get_term.return_value = {
            "_embedded": {
                "terms": [
                    {
                        "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                        "label": "biological_process",
                        "description": ["A biological process ..."],
                    }
                ]
            }
        }
        oi = self.oi
        oi.focus_ontology = "go"
        self.assertEqual(oi.label("GO:0008150"), "biological_process")

    def test_definition_from_ols4_payload(self):
        """definition() should parse OLS4 payloads where description is a list."""
        self.mock_client.get_term.return_value = {
            "_embedded": {
                "terms": [
                    {
                        "iri": "http://purl.obolibrary.org/obo/GO_0008150",
                        "label": "biological_process",
                        "description": ["A biological process represents ..."],
                    }
                ]
            }
        }
        oi = self.oi
        oi.focus_ontology = "go"
        self.assertEqual(oi.definition("GO:0008150"), "A biological process represents ...")

    def test_label_missing_term(self):
        """label() should return None when OLS returns no terms."""
        self.mock_client.get_term.return_value = {"_embedded": {"terms": []}}
        oi = self.oi
        oi.focus_ontology = "go"
        self.assertIsNone(oi.label("GO:9999999"))

    @staticmethod
    def _hal_page(obo_ids, number, total_pages, key="terms"):
        """Build one page of an OLS4 HAL collection response.

        Mirrors the real payload shape: records live under ``_embedded[key]``,
        paging metadata under ``page``, and (crucially) the link to the next
        page is nested under ``_links.next.href`` -- never at ``_links.href``.
        """
        links = {"self": {"href": "https://ols.example/self"}}
        if number + 1 < total_pages:
            links["next"] = {"href": f"https://ols.example/next?page={number + 1}"}
        return {
            "_embedded": {key: [{"obo_id": obo_id} for obo_id in obo_ids]},
            "_links": links,
            "page": {"size": 500, "totalPages": total_pages, "number": number},
        }

    def test_ancestors(self):
        oi = self.oi
        # hierarchicalAncestors endpoint (default, is_a + part_of)
        self.mock_client.get_json.return_value = self._hal_page(
            [CYTOPLASM, CELLULAR_COMPONENT], number=0, total_pages=1
        )

        # reflexive is True by default, so the start term is included
        ancs = list(oi.ancestors([VACUOLE]))
        assert VACUOLE in ancs
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs

        # reflexive=False excludes the start term
        ancs = list(oi.ancestors([VACUOLE], reflexive=False))
        assert VACUOLE not in ancs
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs

        # a bare string CURIE should behave like a single-element list
        ancs = list(oi.ancestors(VACUOLE, reflexive=False))
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs

        # ancestors endpoint (is_a only)
        self.mock_client.get_json.return_value = self._hal_page(
            [CELLULAR_COMPONENT], number=0, total_pages=1
        )
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A], reflexive=False))
        assert CELLULAR_COMPONENT in ancs

    def test_descendants(self):
        oi = self.oi
        self.mock_client.get_json.return_value = self._hal_page(
            [CYTOPLASM, CELLULAR_COMPONENT], number=0, total_pages=1
        )

        # bare string CURIE should not be treated as an iterable of characters
        descs = list(oi.descendants(CELLULAR_COMPONENT, reflexive=False))
        assert CYTOPLASM in descs
        assert CELLULAR_COMPONENT in descs  # returned by the mocked endpoint

        # reflexive includes the start term
        self.mock_client.get_json.return_value = self._hal_page(
            [CYTOPLASM], number=0, total_pages=1
        )
        descs = list(oi.descendants(CELLULAR_COMPONENT, reflexive=True))
        assert CELLULAR_COMPONENT in descs
        assert CYTOPLASM in descs

    def test_descendants_are_not_truncated_to_first_page(self):
        """Descendants must span every page, not just the first.

        Regression test for the OLS adapter silently truncating closure
        queries to the first page (~500 terms). Querying descendants of a
        high-level term such as GO:0005575 (cellular_component) returned only
        491 GO terms via ``ols:go`` versus 4076 via ``sqlite:obo:go``, causing
        silent false negatives in downstream ``reachable_from`` validation.
        See https://github.com/ai4curation/ai-gene-review/issues/1653.

        Here we simulate a three-page response (1200 descendants). A paginator
        that stops after the first page would return only 500; a correct one
        returns all 1200.
        """
        oi = self.oi
        total_pages = 3
        page_terms = [
            [f"GO:{n:07d}" for n in range(0, 500)],
            [f"GO:{n:07d}" for n in range(500, 1000)],
            [f"GO:{n:07d}" for n in range(1000, 1200)],
        ]
        pages = [
            self._hal_page(terms, number=i, total_pages=total_pages)
            for i, terms in enumerate(page_terms)
        ]
        self.mock_client.get_json.side_effect = pages

        descs = {d for d in oi.descendants(CELLULAR_COMPONENT, reflexive=False)}

        expected = {curie for terms in page_terms for curie in terms}
        # All pages collected, not just the first 500.
        self.assertEqual(len(descs), 1200)
        self.assertEqual(descs, expected)
        # And every page was actually fetched (page=0, page=1, page=2).
        self.assertEqual(self.mock_client.get_json.call_count, total_pages)
        requested_pages = [
            call.kwargs.get("params", {}).get("page")
            for call in self.mock_client.get_json.call_args_list
        ]
        self.assertEqual(requested_pages, [0, 1, 2])

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
