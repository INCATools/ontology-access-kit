import unittest
from collections import Iterator

from linkml_runtime.dumpers import yaml_dumper
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.omk.omk_mapping_utils import unreciprocated_mappings, caclulate_pairwise_relational_diff
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index
from oaklib.utilities.mapping.sssom_utils import mappings_to_pairs
from sssom import Mapping

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'unreciprocated-mapping-test.obo'



class TestUnreciprocated(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug=str(TEST_ONT), local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_unreciprocated(self):
        oi = self.oi
        pairs = mappings_to_pairs(unreciprocated_mappings(oi, oi))
        #for p in pairs:
        #    print(p)
        self.assertCountEqual(pairs, [('X:5', 'Y:5'),
                                      ('Y:2', 'X:1'),
                                      ('Y:4', 'X:4')])
        pairs = mappings_to_pairs(unreciprocated_mappings(oi, oi, filter_unidirectional=False))
        #for p in pairs:
        #    print(p)
        self.assertCountEqual(pairs, [('X:5', 'Y:5'),
                                      ('Y:2', 'X:1'),
                                      ('Y:4', 'X:4'),
                                      ('Y:4', 'Z:4')])

    def test_structural_diff(self):
        oi = self.oi
        results = list(caclulate_pairwise_relational_diff(oi, oi, ['X', 'Y', 'Z']))
        for r in results:
            print(r)
        self.assertCountEqual(results,
                              [('CONSISTENT', 'X:2', 'rdfs:subClassOf', 'X:1', []),
                               ('IDENTICAL', 'X:3', 'rdfs:subClassOf', 'X:2', []),
                               ('MISSING_EDGE', 'X:4', 'rdfs:subClassOf', 'X:3', []),
                               ('OTHER', 'X:5', 'rdfs:subClassOf', 'X:4', []),
                               ('MISSING_EDGE', 'Y:1b', 'rdfs:subClassOf', 'Y:1', []),
                               ('MISSING_EDGE', 'Y:2', 'rdfs:subClassOf', 'Y:1b', []),
                               ('IDENTICAL', 'Y:3', 'rdfs:subClassOf', 'Y:2', []),
                               ('CONSISTENT', 'Y:5', 'BFO:0000050', 'Y:4', [])
                               ])




