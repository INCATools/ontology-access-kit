import itertools
import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper
from oaklib.implementations.bioportal.bioportal_implementation import BioportalImplementation

from tests import DIGIT, HUMAN, NEURON, VACUOLE

class TestBioportal(unittest.TestCase):

    def setUp(self) -> None:
        impl = BioportalImplementation()
        try:
            impl.load_bioportal_api_key()
        except ValueError:
            self.skipTest('Skipping bioportal tests, no API key set')
        self.impl = impl

    def test_text_annotator(self):
        results = list(self.impl.annotate_text('hippocampal neuron from human'))
        for ann in results:
            logging.info(ann)
        assert any(r for r in results if r.object_id == HUMAN)
        assert any(r for r in results if r.object_id == NEURON)


    def test_search(self):
        results = list(itertools.islice(self.impl.basic_search('tentacle pocket'), 20))
        assert 'CEPH:0000259' in results


    def test_mappings(self):
        mappings = list(self.impl.get_sssom_mappings_by_curie(DIGIT))
        for m in mappings:
            print(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == 'http://purl.obolibrary.org/obo/NCIT_C73791')

        # FMA:24879 cannot be converted to the IRI recognized by BioPortal automatically,
        # but this tests that the call to get_sssom_mappings_by_curie does not error out
        mappings = list(self.impl.get_sssom_mappings_by_curie('FMA:24879'))
        assert mappings == []

    
    def test_ancestors(self):
        ancestors = list(self.impl.ancestors(VACUOLE))
        assert 'http://purl.obolibrary.org/obo/GO_0005575' in ancestors # cellular_component
        assert 'http://purl.obolibrary.org/obo/GO_0005737' in ancestors # cytoplasm
