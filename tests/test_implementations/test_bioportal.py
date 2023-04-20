import itertools
import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.implementations.ontoportal.bioportal_implementation import (
    BioPortalImplementation,
)
from oaklib.utilities.apikey_manager import get_apikey_value
from tests import CELLULAR_COMPONENT, CYTOPLASM, DIGIT, HUMAN, NEURON, VACUOLE


# TODO: use mock tests
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

    def test_text_annotator(self):
        results = list(self.impl.annotate_text("hippocampal neuron from human"))
        for ann in results:
            logging.info(ann)
        assert any(r for r in results if r.object_id == HUMAN)
        assert any(r for r in results if r.object_id == NEURON)

    def test_search(self):
        results = list(itertools.islice(self.impl.basic_search("tentacle pocket"), 20))
        assert "CEPH:0000259" in results

    def test_search_pagination(self):
        # bioportal defaults to pagesize=50 so this should require 3 pages of results
        results = list(itertools.islice(self.impl.basic_search("brain"), 150))
        self.assertIn("CLAO:0001044", results)

    def test_mappings(self):
        mappings = list(self.impl.get_sssom_mappings_by_curie(DIGIT))
        for m in mappings:
            logging.info(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == "NCIT:C40186")

        # FMA:24879 cannot be converted to the IRI recognized by BioPortal automatically,
        # but this tests that the call to get_sssom_mappings_by_curie does not error out
        mappings = list(self.impl.get_sssom_mappings_by_curie("FMA:24879"))
        assert mappings == []

    def test_ancestors(self):
        ancestors = list(self.impl.ancestors(VACUOLE))
        assert CELLULAR_COMPONENT in ancestors  # cellular_component
        assert CYTOPLASM in ancestors  # cytoplasm

    def test_ontologies(self):
        ontologies = list(self.impl.ontologies())
        self.assertTrue(ontologies)
        self.assertIn("OBI", ontologies)
        self.assertIn("UBERON", ontologies)

    def test_ontology_versions(self):
        versions = list(self.impl.ontology_versions("FMA"))
        self.assertTrue(versions)
        self.assertIn("5.0.0", versions)
        self.assertIn("v3.2.1", versions)

    def test_ontology_metadata(self):
        metadata = self.impl.ontology_metadata_map("OBI")
        self.assertIn("title", metadata)
        self.assertEqual(metadata["title"], "Ontology for Biomedical Investigations")
        self.assertIn("homepage", metadata)
        self.assertEqual(metadata["homepage"], "http://purl.obolibrary.org/obo/obi")
        self.assertIn("classes", metadata)
        self.assertIsInstance(metadata["classes"], int)
