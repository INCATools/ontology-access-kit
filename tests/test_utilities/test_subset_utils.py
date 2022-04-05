import logging
import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.graph.relationship_walker import walk_up
from oaklib.utilities.subsets.slimmer_utils import roll_up_to_named_subset
from oaklib.vocabulary.vocabulary import IS_A, PART_OF
from pronto import Ontology

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'

BIOLOGICAL_PROCESS = 'GO:0008150'
NEGEG_PHOSPH = 'GO:0042326'
NUCLEUS = 'GO:0005634'
DICTYOSTELIUM = 'NCBITaxon:5782'
NUCLEAR_MEMBRANE = 'GO:0031965'


PREDS = [IS_A, PART_OF]

class TestRelationshipWalker(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_roll_up(self):
        oi = self.oi
        m = roll_up_to_named_subset(oi, 'goslim_generic',
                                    [NEGEG_PHOSPH, NUCLEUS, DICTYOSTELIUM, NUCLEAR_MEMBRANE],
                                    predicates=PREDS)
        print(m)
        self.assertCountEqual(m[DICTYOSTELIUM], [])
        self.assertCountEqual(m[NEGEG_PHOSPH], [BIOLOGICAL_PROCESS])
        self.assertCountEqual(m[NUCLEUS], [NUCLEUS])
        #self.assertCountEqual(m[NUCLEAR_MEMBRANE], [NUCLEAR_MEMBRANE])
