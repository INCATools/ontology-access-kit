import itertools
import logging
import unittest
from unittest import mock

from linkml_runtime.dumpers import yaml_dumper

from oaklib.implementations.ontoportal.bioportal_implementation import (
    BioPortalImplementation,
)
from oaklib.utilities.apikey_manager import get_apikey_value
from tests import CELLULAR_COMPONENT, CYTOPLASM, DIGIT, HUMAN, NEURON, VACUOLE


# Helper function to mark integration tests
def integration_test(test_method):
    """Decorator to mark integration tests that require API access."""
    test_method._integration_test = True
    return test_method


# @unittest.skip("Skipping bioportal tests")
class TestBioportal(unittest.TestCase):
    """
    Tests :ref:`BioportalImplementation`
    """

    def setUp(self) -> None:
        cls = BioPortalImplementation
        api_key = None
        try:
            api_key = get_apikey_value(cls.ontoportal_client_class.name)
        except ValueError:
            self.skipTest("no API key for this source {}".format(cls.ontoportal_client_class.name))
        if not api_key:
            self.skipTest("Skipping bioportal tests, no API key set")
        impl = cls(api_key=api_key)
        self.impl = impl

    @integration_test
    def test_text_annotator(self):
        results = list(self.impl.annotate_text("hippocampal neuron from human"))
        for ann in results:
            logging.info(ann)
        assert any(r for r in results if r.object_id == HUMAN)
        assert any(r for r in results if r.object_id == NEURON)

    @integration_test
    def test_search(self):
        results = list(itertools.islice(self.impl.basic_search("tentacle pocket"), 20))
        assert "CEPH:0000259" in results

    @integration_test
    def test_search_pagination(self):
        # bioportal defaults to pagesize=50 so this should require 3 pages of results
        results = list(itertools.islice(self.impl.basic_search("brain"), 150))
        self.assertIn("CLAO:0001044", results)

    @unittest.skip("This test appears to be fragile")
    @integration_test
    def test_mappings(self):
        mappings = list(self.impl.get_sssom_mappings_by_curie(DIGIT))
        for m in mappings:
            logging.info(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == "NCIT:C40186")

        # FMA:24879 cannot be converted to the IRI recognized by BioPortal automatically,
        # but this tests that the call to get_sssom_mappings_by_curie does not error out
        mappings = list(self.impl.get_sssom_mappings_by_curie("FMA:24879"))
        assert mappings == []

    @integration_test
    def test_ancestors(self):
        ancestors = list(self.impl.ancestors(VACUOLE))
        assert CELLULAR_COMPONENT in ancestors  # cellular_component
        assert CYTOPLASM in ancestors  # cytoplasm

    @integration_test
    def test_ontologies(self):
        ontologies = list(self.impl.ontologies())
        self.assertTrue(ontologies)
        self.assertIn("OBI", ontologies)
        self.assertIn("UBERON", ontologies)

    @integration_test
    def test_node(self):
        # Test retrieving a node from a real API endpoint
        self.impl.focus_ontology = "GO"
        node = self.impl.node("GO:0004022", include_metadata=True)

        # Verify we got a node back
        self.assertIsNotNone(node)
        self.assertEqual(node.id, "GO:0004022")
        self.assertEqual(node.type, "CLASS")

        # The label should be present
        self.assertIsNotNone(node.lbl)

        # Check that metadata was included
        self.assertTrue(hasattr(node, "meta") and node.meta is not None)

        # This node should have at least one synonym
        self.assertTrue(len(node.meta.synonyms) > 0)

        # Check that the definition is present
        self.assertIsInstance(node.meta.definition.val, str)

    @integration_test
    def test_ontology_versions(self):
        versions = list(self.impl.ontology_versions("FMA"))
        self.assertTrue(versions)
        self.assertIn("5.0.0", versions)
        self.assertIn("v3.2.1", versions)

    @integration_test
    def test_entities(self):
        # Testing with a small ontology to keep test execution time reasonable
        self.impl.focus_ontology = "STY"  # Semantic Types ontology is relatively small
        entities = list(itertools.islice(self.impl.entities(), 20))
        self.assertTrue(entities)
        # Check we have valid CURIEs returned
        for entity in entities:
            self.assertIn(":", entity)
        # Check we have cached labels for the entities
        self.assertTrue(len(self.impl.label_cache) > 0)

    @mock.patch("ontoportal_client.api.PreconfiguredOntoPortalClient.get_response")
    def test_node_mock(self, mock_get_response):
        # Create mock response for node request
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "@id": "http://purl.bioontology.org/ontology/STY/T116",
            "prefLabel": "Amino Acid, Peptide, or Protein",
            "synonym": [
                {"value": "Amino Acids", "scope": "RELATED"},
                {"value": "Peptides", "scope": "RELATED"},
                {"value": "Proteins", "scope": "RELATED"},
            ],
            "definition": [
                {"value": "Amino acids and chains of amino acids connected by peptide linkages."}
            ],
            "obsolete": False,
        }

        # Set up the mock response
        mock_get_response.return_value = mock_response

        # Call the node method
        node = self.impl.node("STY:T116", include_metadata=True)

        # Verify the node was created correctly
        self.assertEqual(node.id, "STY:T116")
        self.assertEqual(node.lbl, "Amino Acid, Peptide, or Protein")
        self.assertEqual(node.type, "CLASS")

        # Check metadata is parsed correctly
        self.assertTrue(hasattr(node, "meta"))

        # Check definition
        self.assertEqual(
            node.meta.definition.val,
            "Amino acids and chains of amino acids connected by peptide linkages.",
        )

        # Check not obsolete
        self.assertEqual(node.meta.deprecated, False)

        # Check synonyms
        self.assertEqual(len(node.meta.synonyms), 3)

        # Verify all synonyms were parsed correctly
        found_synonyms = {s.val: s.pred for s in node.meta["synonyms"]}
        self.assertEqual(found_synonyms["Amino Acids"], "hasRelatedSynonym")
        self.assertEqual(found_synonyms["Peptides"], "hasRelatedSynonym")
        self.assertEqual(found_synonyms["Proteins"], "hasRelatedSynonym")

        # Verify request was made with correct URL and parameters
        mock_get_response.assert_called_once()
        call_args = mock_get_response.call_args[0]
        self.assertIn("/ontologies/STY/classes/", call_args[0])
        self.assertIn("include", mock_get_response.call_args[1]["params"])

    @mock.patch("ontoportal_client.api.PreconfiguredOntoPortalClient.get_response")
    def test_entities_mock(self, mock_get_response):
        # Create mock response for the first page
        mock_response1 = mock.MagicMock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            "collection": [
                {
                    "@id": "http://purl.bioontology.org/ontology/STY/T001",
                    "prefLabel": "Entity 1",
                },
                {
                    "@id": "http://purl.bioontology.org/ontology/STY/T002",
                    "prefLabel": "Entity 2",
                },
            ],
            "links": {"nextPage": "https://data.bioontology.org/ontologies/STY/classes?page=2"},
        }

        # Create mock response for the second page
        mock_response2 = mock.MagicMock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            "collection": [
                {
                    "@id": "http://purl.bioontology.org/ontology/STY/T003",
                    "prefLabel": "Entity 3",
                },
                {
                    "@id": "http://purl.bioontology.org/ontology/STY/T004",
                    "prefLabel": "Entity 4",
                },
            ],
            "links": {"nextPage": None},
        }

        # Set up the side effect to return different responses for different calls
        mock_get_response.side_effect = [mock_response1, mock_response2]

        # Set up the implementation
        self.impl.focus_ontology = "STY"

        # Call the entities method and check results
        entities = list(self.impl.entities())

        # We should have 4 entities
        self.assertEqual(len(entities), 4)

        # Check specific entities are present
        self.assertIn("STY:T001", entities)
        self.assertIn("STY:T002", entities)
        self.assertIn("STY:T003", entities)
        self.assertIn("STY:T004", entities)

        # Check that labels were cached
        self.assertEqual(self.impl.label_cache["STY:T001"], "Entity 1")
        self.assertEqual(self.impl.label_cache["STY:T002"], "Entity 2")
        self.assertEqual(self.impl.label_cache["STY:T003"], "Entity 3")
        self.assertEqual(self.impl.label_cache["STY:T004"], "Entity 4")

        # Check that get_response was called twice (once for each page)
        self.assertEqual(mock_get_response.call_count, 2)

        # Verify first call was to the base URL with appropriate parameters
        self.assertEqual(mock_get_response.call_args_list[0][0][0], "/ontologies/STY/classes")

        # Verify second call was to the next page URL
        self.assertEqual(
            mock_get_response.call_args_list[1][0][0],
            "https://data.bioontology.org/ontologies/STY/classes?page=2",
        )

    @mock.patch(
        "oaklib.implementations.ontoportal.bioportal_implementation.BioPortalImplementation"
    )
    def test_ontology_metadata(self, mock_impl):
        mock_impl.return_value = {
            "id": "OBI",
            "title": "Ontology for Biomedical Investigations",
            "hasOntologyLanguage": "OWL",
            "released": "2024-01-22T18:11:12-08:00",
            "creationDate": "2024-01-22T18:11:18-08:00",
            "homepage": "http://purl.obolibrary.org/obo/obi",
            "publication": "http://purl.obolibrary.org/obo/obi/Technical_Reports",
            "documentation": "http://purl.obolibrary.org/obo/obi/wiki",
            "version": "2024-01-09",
            "description": 'OBI is an ontology of investigations, the protocols and instrumentation used,\
                the material used, the data generated and the types of analysis performed on it.\
                <br><br>\r\nTo import,<br>\r\nLatest version:\
                <a href="http://purl.obolibrary.org/obo/obi.owl">http://purl.obolibrary.org/obo/obi.owl</a><br>\
                \r\n<br>\r\nLatest release notes at <a href="http://purl.obolibrary.org/obo/obi/release-notes.html">\
                http://purl.obolibrary.org/obo/obi/release-notes.html</a><br>\r\n<br>\r\nNote: BFO 2.0 pre-Graz\
                      release (not official release version) was used in this release.',
            "status": "production",
            "submissionId": 53,
            "submission_uri": "https://data.bioontology.org/ontologies/OBI/submissions/53",
            "type": "http://data.bioontology.org/metadata/OntologySubmission",
        }
        metadata = self.impl.ontology_metadata_map("OBI")
        self.assertIn("title", metadata)
        self.assertEqual(metadata["title"], "Ontology for Biomedical Investigations")
        self.assertIn("homepage", metadata)
        self.assertEqual(metadata["homepage"], "http://purl.obolibrary.org/obo/obi")
        # ! The following test is commented out because the metadata does not have the "classes" fields any more.
        # self.assertIn("classes", metadata)
        # self.assertIsInstance(metadata["classes"], int)
