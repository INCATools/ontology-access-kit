import itertools
import os
import unittest
from unittest.mock import MagicMock, patch

import requests

from oaklib import get_adapter
from oaklib.datamodels.search import SearchConfiguration, SearchProperty
from oaklib.datamodels.vocabulary import (
    DEPRECATED_PREDICATE,
    HAS_DBXREF,
    HAS_DEFINITION_CURIE,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    IN_SUBSET,
    IS_A,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    PART_OF,
    TERM_REPLACED_BY,
)
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, CYTOPLASM, NUCLEUS, VACUOLE

#: set to run the tests that talk to the live EBI OLS service
RUN_NETWORK_TESTS = bool(os.environ.get("OAKLIB_RUN_NETWORK_TESTS"))

#: A trimmed copy of the real OLS4 payload for GO:0005634, retaining every field the
#: adapter reads. Keeping a realistic record here means the offline tests exercise the
#: same parsing paths as a live query.
NUCLEUS_PAYLOAD = {
    "iri": "http://purl.obolibrary.org/obo/GO_0005634",
    "lang": "en",
    "label": "nucleus",
    "description": ["A membrane-bounded organelle of eukaryotic cells."],
    "synonyms": ["cell nucleus", "horsetail nucleus"],
    "annotation": {
        "database_cross_reference": [
            "NIF_Subcellular:sao1702920020",
            "Wikipedia:Cell_nucleus",
        ],
        "has_obo_namespace": ["cellular_component"],
        "id": ["GO:0005634"],
    },
    "ontology_name": "go",
    "ontology_prefix": "GO",
    "is_obsolete": False,
    "term_replaced_by": None,
    "is_defining_ontology": True,
    "short_form": "GO_0005634",
    "obo_id": "GO:0005634",
    "in_subset": ["goslim_generic", "goslim_yeast"],
    "obo_definition_citation": [
        {
            "definition": "A membrane-bounded organelle of eukaryotic cells.",
            "oboXrefs": [{"database": "GOC", "id": "go_curators"}],
        }
    ],
    "obo_xref": [
        {"database": "NIF_Subcellular", "id": "sao1702920020"},
        {"database": "Wikipedia", "id": "Cell_nucleus"},
    ],
    "obo_synonym": [
        {
            "name": "horsetail nucleus",
            "scope": "hasNarrowSynonym",
            "type": None,
            "xrefs": [
                {"database": "GOC", "id": "al"},
                {"database": "PMID", "id": "15030757"},
            ],
        },
        {
            "name": "cell nucleus",
            "scope": "hasExactSynonym",
            "type": "http://purl.obolibrary.org/obo/go#systematic_synonym",
            "xrefs": [],
        },
    ],
}

#: OLS payload for an obsolete, merged term
OBSOLETE_PAYLOAD = {
    "iri": "http://purl.obolibrary.org/obo/GO_0000004",
    "label": "GO_0000004",
    "description": [],
    "obo_id": "GO:0000004",
    "is_obsolete": True,
    "term_replaced_by": "GO_0008150",
    "ontology_prefix": "GO",
    "annotation": {
        "has obsolescence reason": ["http://purl.obolibrary.org/obo/IAO_0000227"],
        "term replaced by": ["http://purl.obolibrary.org/obo/GO_0008150"],
    },
}


def _terms_response(*terms):
    """Wrap term records the way the OLS4 ``/terms`` endpoint does."""
    return {"_embedded": {"terms": list(terms)}}


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
        mock_client.get_ontology.return_value = {"config": {"hierarchicalProperties": []}}

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
        self.assertIsNone(oi.label("GO:9999999"))
        self.mock_client.get_term.assert_called_once()

    def test_label_missing_iri_http_error(self):
        """label() should cache a 404 for a non-term IRI as a missing label."""
        response = requests.Response()
        response.status_code = 404
        self.mock_client.get_term.side_effect = requests.HTTPError(response=response)
        oi = self.oi
        oi.focus_ontology = "go"
        self.assertIsNone(oi.label(IS_A))
        self.assertIsNone(oi.label(IS_A))
        self.assertIn(IS_A, oi.label_cache)
        self.assertIsNone(oi.label_cache[IS_A])
        self.mock_client.get_term.assert_called_once()

    def test_definition_missing_iri_http_error(self):
        """definition() should cache a 404 for a non-term IRI as missing."""
        response = requests.Response()
        response.status_code = 404
        self.mock_client.get_term.side_effect = requests.HTTPError(response=response)
        oi = self.oi
        oi.focus_ontology = "go"
        self.assertIsNone(oi.definition(IS_A))
        self.assertIsNone(oi.definition(IS_A))
        self.assertIn(IS_A, oi.definition_cache)
        self.assertIsNone(oi.definition_cache[IS_A])
        self.mock_client.get_term.assert_called_once()

    def test_term_lookup_http_error_without_status_is_raised(self):
        """A response-less HTTPError is not a confirmed missing term."""
        oi = self.oi
        oi.focus_ontology = "go"
        for method_name, cache_name in [
            ("label", "label_cache"),
            ("definition", "definition_cache"),
        ]:
            with self.subTest(method=method_name):
                cache = getattr(oi, cache_name)
                cache.clear()
                self.mock_client.get_term.reset_mock()
                error = requests.HTTPError()
                self.mock_client.get_term.side_effect = error
                with self.assertRaises(requests.HTTPError) as raised:
                    getattr(oi, method_name)(IS_A)
                self.assertIs(error, raised.exception)
                self.mock_client.get_term.assert_called_once()
                self.assertNotIn(IS_A, cache)

    def test_term_lookup_non_404_http_errors_are_raised(self):
        """Authentication, throttling, and server failures must not look missing."""
        oi = self.oi
        oi.focus_ontology = "go"
        for method_name, cache_name in [
            ("label", "label_cache"),
            ("definition", "definition_cache"),
        ]:
            for status_code in [401, 403, 429, 500]:
                with self.subTest(method=method_name, status_code=status_code):
                    cache = getattr(oi, cache_name)
                    cache.clear()
                    response = requests.Response()
                    response.status_code = status_code
                    error = requests.HTTPError(response=response)
                    self.mock_client.get_term.side_effect = error
                    with self.assertRaises(requests.HTTPError) as raised:
                        getattr(oi, method_name)(IS_A)
                    self.assertIs(error, raised.exception)
                    self.assertNotIn(IS_A, cache)

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

    def test_entailed_relationships(self):
        oi = self.oi

        def mock_get_json(path, **kwargs):
            if path.endswith("/ancestors"):
                return self._hal_page([CELLULAR_COMPONENT], number=0, total_pages=1)
            if path.endswith("/hierarchicalAncestors"):
                return self._hal_page([CELLULAR_COMPONENT, CYTOPLASM], number=0, total_pages=1)
            raise AssertionError(f"Unexpected path: {path}")

        self.mock_client.get_json.side_effect = mock_get_json

        rels = list(
            oi.relationships(subjects=[VACUOLE], predicates=[IS_A, PART_OF], include_entailed=True)
        )

        self.assertIn((VACUOLE, IS_A, VACUOLE), rels)
        self.assertIn((VACUOLE, IS_A, CELLULAR_COMPONENT), rels)
        self.assertIn((VACUOLE, PART_OF, CYTOPLASM), rels)

    def test_graph_relationships_preserve_unmapped_uris(self):
        """Direct graph edges should retain URIs that cannot be contracted."""
        known_source_iri = "http://purl.obolibrary.org/obo/GO_0005773"
        known_target_iri = "http://purl.obolibrary.org/obo/GO_0005737"
        unknown_source_iri = "http://example.org/unknown_source"
        unknown_target_iri = "http://example.org/unknown_target"
        unknown_predicate_iri = "http://example.org/unknown_predicate"
        unconvertible_iri = "http://example.org/unconvertible"
        self.mock_client.get_json.return_value = {
            "edges": [
                {
                    "source": unknown_source_iri,
                    "uri": unknown_predicate_iri,
                    "target": known_target_iri,
                },
                {
                    "source": known_source_iri,
                    "uri": unknown_predicate_iri,
                    "target": unknown_target_iri,
                },
                {
                    "source": 42,
                    "uri": unknown_predicate_iri,
                    "target": known_target_iri,
                },
                {
                    "source": unconvertible_iri,
                    "uri": unknown_predicate_iri,
                    "target": known_target_iri,
                },
            ]
        }

        def mock_uri_to_curie(uri, *args, **kwargs):
            known_curies = {
                known_source_iri: VACUOLE,
                known_target_iri: CYTOPLASM,
            }
            if uri in known_curies:
                return known_curies[uri]
            if uri == unconvertible_iri:
                return None
            if kwargs.get("use_uri_fallback"):
                return uri
            return None

        self.oi.uri_to_curie.side_effect = mock_uri_to_curie

        incoming = list(self.oi.relationships(objects=[CYTOPLASM]))
        outgoing = list(self.oi.relationships(subjects=[VACUOLE]))

        self.assertEqual({(unknown_source_iri, unknown_predicate_iri, CYTOPLASM)}, set(incoming))
        self.assertEqual({(VACUOLE, unknown_predicate_iri, unknown_target_iri)}, set(outgoing))

    def test_entailed_part_of_rejects_additional_hierarchical_predicates(self):
        """Hierarchy closure differences are ambiguous when OLS configures other predicates."""
        part_of_iri = "http://purl.obolibrary.org/obo/BFO_0000050"
        custom_hierarchy_iri = "http://example.org/custom_hierarchy"
        self.mock_client.get_ontology.return_value = {
            "config": {
                "hierarchicalProperties": [
                    part_of_iri,
                    custom_hierarchy_iri,
                ]
            }
        }

        def mock_uri_to_curie(uri, *args, **kwargs):
            if uri == part_of_iri:
                return PART_OF
            if kwargs.get("use_uri_fallback"):
                return uri
            return None

        self.oi.uri_to_curie.side_effect = mock_uri_to_curie

        with self.assertRaisesRegex(NotImplementedError, "additional hierarchical predicates"):
            list(
                self.oi.relationships(
                    subjects=[VACUOLE],
                    predicates=[IS_A, PART_OF],
                    include_entailed=True,
                )
            )

        self.mock_client.get_json.assert_not_called()
        self.assertTrue(
            all(call.kwargs.get("use_uri_fallback") for call in self.oi.uri_to_curie.call_args_list)
        )

    def test_entailed_isa_ignores_additional_hierarchical_predicates(self):
        """An is-a-only closure remains unambiguous for every OLS hierarchy config."""
        self.mock_client.get_ontology.return_value = {
            "config": {
                "hierarchicalProperties": [
                    "http://purl.obolibrary.org/obo/BFO_0000050",
                    "http://purl.obolibrary.org/obo/RO_0002202",
                ]
            }
        }
        self.mock_client.get_json.return_value = self._hal_page(
            [CELLULAR_COMPONENT], number=0, total_pages=1
        )

        rels = list(
            self.oi.relationships(subjects=[VACUOLE], predicates=[IS_A], include_entailed=True)
        )

        self.assertIn((VACUOLE, IS_A, CELLULAR_COMPONENT), rels)
        self.mock_client.get_ontology.assert_not_called()

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

    def _descendants_endpoint(self, predicates):
        """Return the OLS endpoint hit by ``descendants`` for the given predicates.

        Drives a single-page ``descendants`` call and reads back the path that
        was passed to ``get_json`` (its trailing segment names the endpoint).
        """
        self.mock_client.get_json.reset_mock(side_effect=True)
        self.mock_client.get_json.return_value = self._hal_page(
            [CYTOPLASM], number=0, total_pages=1
        )
        list(self.oi.descendants(CELLULAR_COMPONENT, predicates=predicates))
        path = self.mock_client.get_json.call_args_list[0].args[0]
        return path.rsplit("/", 1)[-1]

    def test_descendants_isa_and_partof_use_hierarchical_endpoint(self):
        """``predicates=[IS_A, PART_OF]`` must query the hierarchical endpoint.

        OLS closes over is_a + part_of via ``hierarchicalDescendants`` (e.g.
        GO:0005634 nucleus has 24 is_a-only descendants but 473 hierarchical
        descendants). OAK selects the endpoint from ``predicates``:

        * ``[IS_A]``            -> ``descendants``              (is_a only)
        * ``[IS_A, PART_OF]``   -> ``hierarchicalDescendants``  (is_a + part_of)
        * ``None`` / unset      -> ``hierarchicalDescendants``  (all relations)

        Note: OLS has no endpoint for an arbitrary predicate subset -- the
        hierarchical endpoint returns the ontology's full hierarchical relation
        set (is_a + part_of for GO), so ``[IS_A, PART_OF]`` is served by it.
        """
        self.assertEqual(self._descendants_endpoint([IS_A]), "descendants")
        self.assertEqual(self._descendants_endpoint([IS_A, PART_OF]), "hierarchicalDescendants")
        # order-independent
        self.assertEqual(self._descendants_endpoint([PART_OF, IS_A]), "hierarchicalDescendants")
        # default (no predicates) also traverses is_a + part_of
        self.assertEqual(self._descendants_endpoint(None), "hierarchicalDescendants")

    def test_descendants_isa_and_partof_paginate_fully(self):
        """The is_a + part_of closure is paged the same way as the is_a one."""
        oi = self.oi
        page_terms = [
            [f"GO:{n:07d}" for n in range(0, 500)],
            [f"GO:{n:07d}" for n in range(500, 730)],
        ]
        pages = [
            self._hal_page(terms, number=i, total_pages=len(page_terms))
            for i, terms in enumerate(page_terms)
        ]
        self.mock_client.get_json.reset_mock(side_effect=True)
        self.mock_client.get_json.side_effect = pages

        descs = set(oi.descendants(CELLULAR_COMPONENT, predicates=[IS_A, PART_OF], reflexive=False))

        self.assertEqual(descs, {curie for terms in page_terms for curie in terms})
        self.assertEqual(len(descs), 730)
        self.assertEqual(self.mock_client.get_json.call_count, 2)

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


class TestOlsTermMetadata(unittest.TestCase):
    """Tests for the term-payload derived features of the OLS adapter.

    These mirror the compliance coverage the SQL adapter gets, but are driven from a
    captured OLS payload so they run offline and deterministically.
    """

    def setUp(self) -> None:
        mock_client = MagicMock()
        mock_client.get_ontology.return_value = {"config": {"hierarchicalProperties": []}}
        mock_client.get_term.return_value = _terms_response(NUCLEUS_PAYLOAD)
        with patch.object(OlsImplementation, "ols_client_class", return_value=mock_client):
            self.oi = OlsImplementation(OntologyResource("go"))
        self.mock_client = mock_client

    def test_is_obograph_interface(self):
        """The OLS adapter serves graph queries, so it must declare the interface."""
        self.assertIsInstance(self.oi, OboGraphInterface)

    def test_term_metadata_is_fetched_once(self):
        """Every property of a term comes from a single HTTP round trip.

        ``label()`` and ``definition()`` used to issue one request each, doubling the
        latency of the most common usage pattern.
        """
        oi = self.oi
        self.assertEqual("nucleus", oi.label(NUCLEUS))
        self.assertTrue(oi.definition(NUCLEUS).startswith("A membrane-bounded organelle"))
        self.assertEqual(3, len(oi.entity_aliases(NUCLEUS)))
        self.assertIn(HAS_DBXREF, oi.entity_metadata_map(NUCLEUS))
        self.mock_client.get_term.assert_called_once()

    def test_labels(self):
        self.assertEqual([(NUCLEUS, "nucleus")], list(self.oi.labels([NUCLEUS])))

    def test_entity_aliases(self):
        self.assertCountEqual(
            ["nucleus", "cell nucleus", "horsetail nucleus"],
            self.oi.entity_aliases(NUCLEUS),
        )

    def test_entity_alias_map(self):
        self.assertEqual(
            {
                "rdfs:label": ["nucleus"],
                HAS_NARROW_SYNONYM: ["horsetail nucleus"],
                HAS_EXACT_SYNONYM: ["cell nucleus"],
            },
            self.oi.entity_alias_map(NUCLEUS),
        )

    def test_synonym_property_values(self):
        synonyms = {spv.val: spv for _, spv in self.oi.synonym_property_values([NUCLEUS])}
        self.assertCountEqual(["cell nucleus", "horsetail nucleus"], synonyms)
        narrow = synonyms["horsetail nucleus"]
        self.assertEqual("hasNarrowSynonym", narrow.pred)
        self.assertCountEqual(["GOC:al", "PMID:15030757"], narrow.xrefs)
        exact = synonyms["cell nucleus"]
        self.assertEqual("hasExactSynonym", exact.pred)
        self.assertEqual("systematic_synonym", exact.synonymType)

    def test_synonyms_missing_from_obo_synonym_are_still_reported(self):
        """OLS does not always repeat flat synonyms in ``obo_synonym``."""
        payload = dict(NUCLEUS_PAYLOAD)
        payload["obo_synonym"] = [NUCLEUS_PAYLOAD["obo_synonym"][0]]
        self.mock_client.get_term.return_value = _terms_response(payload)
        synonyms = {spv.val: spv.pred for _, spv in self.oi.synonym_property_values([NUCLEUS])}
        self.assertEqual(
            {"horsetail nucleus": "hasNarrowSynonym", "cell nucleus": "hasExactSynonym"},
            synonyms,
        )

    def test_definitions_with_metadata(self):
        [(curie, definition, metadata)] = list(
            self.oi.definitions([NUCLEUS], include_metadata=True)
        )
        self.assertEqual(NUCLEUS, curie)
        self.assertTrue(definition.startswith("A membrane-bounded organelle"))
        self.assertEqual(["GOC:go_curators"], metadata[HAS_DBXREF])

    def test_entity_metadata_map(self):
        metadata = self.oi.entity_metadata_map(NUCLEUS)
        self.assertTrue(metadata[HAS_DEFINITION_CURIE][0].startswith("A membrane-bounded"))
        self.assertCountEqual(
            ["NIF_Subcellular:sao1702920020", "Wikipedia:Cell_nucleus"],
            metadata[HAS_DBXREF],
        )
        self.assertCountEqual(["goslim_generic", "goslim_yeast"], metadata[IN_SUBSET])
        self.assertEqual(["cellular_component"], metadata["oio:hasOBONamespace"])
        self.assertNotIn(DEPRECATED_PREDICATE, metadata)

    def test_obsolete_term_metadata(self):
        self.mock_client.get_term.return_value = _terms_response(OBSOLETE_PAYLOAD)
        metadata = self.oi.entity_metadata_map("GO:0000004")
        self.assertEqual([True], metadata[DEPRECATED_PREDICATE])
        self.assertEqual(["GO:0008150"], metadata[TERM_REPLACED_BY])
        self.assertEqual(["IAO:0000227"], metadata["IAO:0000231"])

    def test_terms_subsets(self):
        self.assertCountEqual(
            [(NUCLEUS, "goslim_generic"), (NUCLEUS, "goslim_yeast")],
            list(self.oi.terms_subsets([NUCLEUS])),
        )

    def test_simple_mappings(self):
        self.assertCountEqual(
            [
                (HAS_DBXREF, "NIF_Subcellular:sao1702920020"),
                (HAS_DBXREF, "Wikipedia:Cell_nucleus"),
            ],
            list(self.oi.simple_mappings_by_curie(NUCLEUS)),
        )

    def test_defined_by(self):
        self.assertEqual("GO", self.oi.defined_by(NUCLEUS))

    def test_owl_type_class(self):
        self.assertEqual([OWL_CLASS], self.oi.owl_type(NUCLEUS))

    def test_owl_type_object_property(self):
        """A term lookup that 404s falls through to the properties endpoint."""
        response = requests.Response()
        response.status_code = 404
        self.mock_client.get_term.side_effect = requests.HTTPError(response=response)
        self.mock_client.get_json.return_value = {
            "_embedded": {"properties": [{"iri": "http://purl.obolibrary.org/obo/BFO_0000050"}]}
        }
        self.assertEqual([OWL_OBJECT_PROPERTY], self.oi.owl_type(PART_OF))

    def test_node(self):
        node = self.oi.node(NUCLEUS, include_metadata=True)
        self.assertEqual(NUCLEUS, node.id)
        self.assertEqual("nucleus", node.lbl)
        self.assertEqual("CLASS", node.type)
        self.assertTrue(node.meta.definition.val.startswith("A membrane-bounded"))
        self.assertEqual(["GOC:go_curators"], node.meta.definition.xrefs)
        self.assertCountEqual(
            ["NIF_Subcellular:sao1702920020", "Wikipedia:Cell_nucleus"],
            [xref.val for xref in node.meta.xrefs],
        )
        self.assertCountEqual(["goslim_generic", "goslim_yeast"], node.meta.subsets)
        self.assertCountEqual(
            [("hasExactSynonym", "cell nucleus"), ("hasNarrowSynonym", "horsetail nucleus")],
            [(spv.pred, spv.val) for spv in node.meta.synonyms],
        )

    def test_node_for_unknown_entity(self):
        self.mock_client.get_term.return_value = _terms_response()
        node = self.oi.node("GO:9999999")
        self.assertEqual("GO:9999999", node.id)
        self.assertIsNone(node.lbl)
        with self.assertRaises(ValueError):
            self.oi.node("GO:9999999", strict=True)

    def test_entities_populates_the_term_cache(self):
        """Paging through terms should prime the cache, not force a refetch per term."""
        self.mock_client.get_json.return_value = {
            "_embedded": {"terms": [NUCLEUS_PAYLOAD]},
            "page": {"size": 500, "totalPages": 1, "number": 0},
        }
        self.assertEqual([NUCLEUS], list(self.oi.entities()))
        self.mock_client.get_term.reset_mock()
        self.assertEqual("nucleus", self.oi.label(NUCLEUS))
        self.mock_client.get_term.assert_not_called()

    def test_entities_rejects_unsupported_owl_type(self):
        with self.assertRaises(NotImplementedError):
            list(self.oi.entities(owl_type=OWL_OBJECT_PROPERTY))

    def test_language_specific_label(self):
        """A language tag bypasses ``get_term`` so the ``lang`` parameter can be passed."""
        self.mock_client.get_json.return_value = _terms_response(
            {**NUCLEUS_PAYLOAD, "label": "noyau", "lang": "fr"}
        )
        self.assertEqual("noyau", self.oi.label(NUCLEUS, lang="fr"))
        self.assertEqual("nucleus", self.oi.label(NUCLEUS))
        params = self.mock_client.get_json.call_args.kwargs["params"]
        self.assertEqual("fr", params["lang"])

    def test_ontology_metadata_map(self):
        self.mock_client.get_ontology.return_value = {
            "config": {
                "title": "Gene Ontology",
                "version": "2026-06-15",
                "fileLocation": "http://purl.obolibrary.org/obo/go/extensions/go-plus.owl",
            }
        }
        metadata = self.oi.ontology_metadata_map("go")
        self.assertEqual(["Gene Ontology"], metadata["dcterms:title"])
        self.assertEqual(["2026-06-15"], metadata["owl:versionInfo"])
        self.assertEqual(["2026-06-15"], list(self.oi.ontology_versions("go")))

    def test_languages(self):
        self.mock_client.get_ontology.return_value = {"languages": ["en", "fr", "cs"]}
        self.assertCountEqual(["en", "fr", "cs"], list(self.oi.languages()))
        self.assertTrue(self.oi.multilingual)


@unittest.skipUnless(
    RUN_NETWORK_TESTS,
    "network test; set OAKLIB_RUN_NETWORK_TESTS=1 to enable",
)
class TestOlsLive(unittest.TestCase):
    """End-to-end tests against the live EBI OLS service.

    These are excluded from the default run because they depend on an external
    service, but they are what guarantees the offline payloads above stay honest.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.oi = get_adapter("ols:go")

    def test_label_and_definition(self):
        self.assertEqual("nucleus", self.oi.label(NUCLEUS))
        self.assertTrue(self.oi.definition(NUCLEUS).startswith("A membrane-bounded organelle"))

    def test_aliases(self):
        aliases = self.oi.entity_aliases(NUCLEUS)
        self.assertIn("nucleus", aliases)
        self.assertIn("cell nucleus", aliases)

    def test_metadata_map(self):
        metadata = self.oi.entity_metadata_map(NUCLEUS)
        self.assertIn("Wikipedia:Cell_nucleus", metadata[HAS_DBXREF])
        self.assertIn("goslim_generic", metadata[IN_SUBSET])

    def test_node(self):
        node = self.oi.node(NUCLEUS, include_metadata=True)
        self.assertEqual("nucleus", node.lbl)
        self.assertTrue(node.meta.definition.val)

    def test_ancestors(self):
        ancestors = list(self.oi.ancestors([VACUOLE], predicates=[IS_A, PART_OF]))
        self.assertIn(CELLULAR_COMPONENT, ancestors)
        self.assertIn(CYTOPLASM, ancestors)

    def test_descendants_are_complete(self):
        """Closure queries must page through the whole result set."""
        descendants = list(self.oi.descendants(CELLULAR_COMPONENT, predicates=[IS_A]))
        self.assertGreater(len(descendants), 1000)

    def test_owl_types(self):
        self.assertEqual([OWL_CLASS], self.oi.owl_type(NUCLEUS))
        self.assertEqual([OWL_OBJECT_PROPERTY], self.oi.owl_type(PART_OF))

    def test_multilingual(self):
        hp = get_adapter("ols:hp")
        self.assertIn("fr", list(hp.languages()))
        self.assertEqual("Phenotypic abnormality", hp.label("HP:0000118"))
        self.assertEqual("Anomalie phénotypique", hp.label("HP:0000118", lang="fr"))
