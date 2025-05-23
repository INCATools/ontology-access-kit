import json
import unittest

import curies
from linkml_runtime.loaders import json_loader
from ndex2 import create_nice_cx_from_file

from oaklib.converters.obo_graph_to_cx_converter import OboGraphToCXConverter
from oaklib.datamodels.obograph import GraphDocument
from oaklib.interfaces.basic_ontology_interface import get_default_prefix_map
from tests import INPUT_DIR, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

ONT = INPUT_DIR / "go-nucleus.json"
OUT = OUTPUT_DIR / "go-nucleus.cx"


class OboGraphToCXTest(unittest.TestCase):
    """Tests OBO JSON -> NDEx CX format."""

    def setUp(self):
        self.converter = OboGraphToCXConverter()
        self.converter.curie_converter = curies.Converter.from_prefix_map(get_default_prefix_map())
        self.compliance_tester = ComplianceTester(self)

    def test_convert(self):
        """Tests parsing then converting to cx document."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        doc = self.converter.convert(gd)
        print(doc)
        with open(OUT, "w", encoding="UTF-8") as f:
            json.dump(doc, f)
        cxn = create_nice_cx_from_file(OUT)
        cxn.print_summary()
