import itertools
import logging
import unittest

from oaklib.implementations.bioportal.bioportal_implementation import BioportalImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR


HUMAN = 'NCBITaxon:9606'
NEURON = 'CL:0000540'

class TestBioportal(unittest.TestCase):

    def setUp(self) -> None:
        oi = BioportalImplementation()
        self.has_apikey = True
        try:
            oi.load_bioportal_api_key()
        except ValueError:
            logging.info('Skipping bioportal tests, no API key set')
            self.has_apikey = False
        self.oi = oi

    def test_text_annotator(self):
        if self.has_apikey:
            results = list(self.oi.annotate_text('hippocampal neuron from human'))
            for ann in results:
                logging.info(ann)
            assert any(r for r in results if r.object_id == HUMAN)
            assert any(r for r in results if r.object_id == NEURON)


    def test_search(self):
        results = list(itertools.islice(self.oi.basic_search('tentacle pocket'), 20))
        assert 'CEPH:0000259' in results