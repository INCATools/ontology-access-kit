import unittest

import curies
from linkml_runtime.loaders import json_loader

from oaklib import OntologyResource
from oaklib.converters.obo_graph_to_rdf_owl_converter import OboGraphToRdfOwlConverter
from oaklib.datamodels.obograph import GraphDocument
from oaklib.implementations import SparqlImplementation
from oaklib.interfaces.basic_ontology_interface import get_default_prefix_map
from tests import INPUT_DIR, OUTPUT_DIR
from tests.test_implementations import ComplianceTester

ONT = INPUT_DIR / "go-nucleus.json"
OUT = OUTPUT_DIR / "go-nucleus.ttl"


class OboGraphToRdfOwlConverterTest(unittest.TestCase):
    """Tests OBO JSON -> RDF/OWL."""

    def setUp(self):
        self.converter = OboGraphToRdfOwlConverter()
        self.converter.curie_converter = curies.Converter.from_prefix_map(get_default_prefix_map())
        self.compliance_tester = ComplianceTester(self)

    def test_convert(self):
        """Tests parsing then converting to rdflib Graph."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        g = self.converter.convert(gd)
        g.serialize(OUT)
        oi = SparqlImplementation(OntologyResource(OUT))
        # for r in oi.relationships(["GO:0005773"]):
        #    print(r)
        self.compliance_tester.test_synonyms(oi)
        self.compliance_tester.test_definitions(oi)
        self.compliance_tester.test_sssom_mappings(oi)
        self.compliance_tester.test_relationships(oi)
