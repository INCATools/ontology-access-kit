import unittest

import curies
from linkml_runtime.loaders import json_loader

from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFHIRConverter
from oaklib.datamodels.fhir import CodeSystem
from oaklib.datamodels.obograph import GraphDocument
from oaklib.interfaces.basic_ontology_interface import get_default_prefix_map
from tests import IMBO, INPUT_DIR, NUCLEUS, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

ONT = INPUT_DIR / "go-nucleus.json"
OUT = OUTPUT_DIR / "go-nucleus.fhir.codesystem.json"


class OboGraphToFHIRTest(unittest.TestCase):
    """Tests OBO JSON -> FHIR."""

    def setUp(self):
        self.converter = OboGraphToFHIRConverter()
        self.converter.curie_converter = curies.Converter.from_prefix_map(get_default_prefix_map())
        self.compliance_tester = ComplianceTester(self)

    def test_convert(self):
        """Tests parsing then converting to fhir documents."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        self.converter.dump(gd, OUT, include_all_predicates=True)
        cs: CodeSystem
        cs = json_loader.load(str(OUT), target_class=CodeSystem)
        self.assertEqual("CodeSystem", cs.resourceType)
        [nucleus_concept] = [c for c in cs.concept if c.code == NUCLEUS]
        self.assertEqual("nucleus", nucleus_concept.display)
        self.assertTrue(nucleus_concept.definition.startswith("A membrane-bounded organelle"))
        parents = [x for x in nucleus_concept.property if x.code == "parent"]
        self.assertEqual(len(parents), 1)
        self.assertTrue(parents[0].valueCode == IMBO)
