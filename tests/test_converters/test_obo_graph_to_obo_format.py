import unittest

import curies
from linkml_runtime.loaders import json_loader

from oaklib import OntologyResource
from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.datamodels.obograph import GraphDocument
from oaklib.implementations import SimpleOboImplementation
from oaklib.interfaces.basic_ontology_interface import get_default_prefix_map
from tests import INPUT_DIR, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

ONT = INPUT_DIR / "go-nucleus.json"
OUT = OUTPUT_DIR / "go-nucleus-roundtrip.obo"


class OboGraphToOboFormatTest(unittest.TestCase):
    """Tests OBO JSON -> RDF/OWL."""

    def setUp(self):
        self.converter = OboGraphToOboFormatConverter()
        self.converter.curie_converter = curies.Converter.from_prefix_map(get_default_prefix_map())
        self.compliance_tester = ComplianceTester(self)

    def test_convert(self):
        """Tests parsing then converting to obo format document."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        obodoc = self.converter.convert(gd)
        with open(OUT, "w", encoding="UTF-8") as f:
            obodoc.dump(f)
        oi = SimpleOboImplementation(OntologyResource(OUT))
        self.compliance_tester.test_definitions(oi)
        # self.compliance_tester.test_sssom_mappings(oi)
        self.compliance_tester.test_relationships(oi)
