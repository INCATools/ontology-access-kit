"""Tests for: Obographs to FHIR converter"""
import os
import unittest
from typing import List

import curies
import requests
from linkml_runtime.loaders import json_loader

from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFHIRConverter
from oaklib.datamodels.fhir import CodeSystem
from oaklib.datamodels.obograph import GraphDocument
from oaklib.interfaces.basic_ontology_interface import get_default_prefix_map
from tests import IMBO, INPUT_DIR, NUCLEUS, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

DOWNLOAD_TESTS_ON = False


class OboGraphToFHIRTest(unittest.TestCase):
    """Tests OBO JSON -> FHIR. Different ontologies have unique structures, so test some specifics for those."""

    @staticmethod
    def _load_ontology(url: str, download_path: str, use_cache: bool = True) -> GraphDocument:
        """Downloads ontology if needed, and loads it."""
        if not os.path.exists(download_path) and use_cache:
            r = requests.get(url)
            with open(download_path, "wb") as f:
                f.write(r.content)
            return json_loader.load(str(download_path), target_class=GraphDocument)
        elif use_cache:
            return json_loader.load(str(download_path), target_class=GraphDocument)
        return json_loader.load(url, target_class=GraphDocument)

    def _load_and_convert(self, outpath: str, obograph_path: str, dl_url: str = None) -> CodeSystem:
        """Loads and converts an ontology."""
        if dl_url:
            gd: GraphDocument = self._load_ontology(dl_url, obograph_path)
        else:
            gd: GraphDocument = json_loader.load(str(obograph_path), target_class=GraphDocument)
        self.converter.dump(gd, outpath, include_all_predicates=True)
        return json_loader.load(str(outpath), target_class=CodeSystem)

    def setUp(self):
        """Set up tests"""
        self.converter = OboGraphToFHIRConverter()
        self.converter.curie_converter = curies.Converter.from_prefix_map(get_default_prefix_map())
        self.compliance_tester = ComplianceTester(self)

    def test_convert_go_nucleus(self):
        """General test & specifis for go nucleus."""
        ont = INPUT_DIR / "go-nucleus.json"
        out = OUTPUT_DIR / "CodeSystem-go-nucleus.json"
        cs: CodeSystem = self._load_and_convert(out, ont)
        self.assertEqual("CodeSystem", cs.resourceType)
        [nucleus_concept] = [c for c in cs.concept if c.code == NUCLEUS]
        self.assertEqual("nucleus", nucleus_concept.display)
        self.assertTrue(nucleus_concept.definition.startswith("A membrane-bounded organelle"))
        parents = [x for x in nucleus_concept.property if x.code == "parent"]
        self.assertEqual(len(parents), 1)
        self.assertTrue(parents[0].valueCode == IMBO)

    def test_convert_mondo(self):
        """Tests specific to Mondo."""
        if DOWNLOAD_TESTS_ON:
            dl_url = (
                "https://github.com/"
                "HOT-Ecosystem/owl-on-fhir-content/releases/download/2022-12-20/mondo.owl.obographs.json"
            )
            dl_path = OUTPUT_DIR / "mondo.owl.obographs.json"
            out = OUTPUT_DIR / "CodeSystem-Mondo.json"
            cs: CodeSystem = self._load_and_convert(out, dl_path, dl_url)
            self.assertGreater(cs.concept, 40000)
            prop_uris: List[str] = [p.uri for p in cs.property]
            self.assertIn("http://purl.obolibrary.org/obo/RO_0002353", prop_uris)

    def test_convert_hpo(self):
        """Tests specific to HPO."""
        if DOWNLOAD_TESTS_ON:
            dl_url = (
                "https://github.com/"
                "HOT-Ecosystem/owl-on-fhir-content/releases/download/2022-12-20/hpo.owl.obographs.json"
            )
            dl_path = OUTPUT_DIR / "hpo.owl.obographs.json"
            out = OUTPUT_DIR / "CodeSystem-HPO.json"
            cs: CodeSystem = self._load_and_convert(out, dl_path, dl_url)
            self.assertGreater(cs.concept, 30000)
            prop_uris: List[str] = [p.uri for p in cs.property]
            self.assertIn("http://purl.obolibrary.org/obo/RO_0002353", prop_uris)

    def test_convert_comploinc(self):
        """Tests specific to CompLOINC."""
        if DOWNLOAD_TESTS_ON:
            dl_url = (
                "https://github.com/"
                "HOT-Ecosystem/owl-on-fhir-content/releases/download/2022-12-20/comploinc.owl.obographs.json"
            )
            dl_path = OUTPUT_DIR / "comploinc.owl.obographs.json"
            out = OUTPUT_DIR / "CodeSystem-CompLOINC.json"
            cs: CodeSystem = self._load_and_convert(out, dl_path, dl_url)
            self.assertGreater(cs.concept, 5000)
            prop_uris: List[str] = [p.uri for p in cs.property]
            self.assertIn("https://loinc.org/hasComponent", prop_uris)
