import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib import get_implementation_from_shorthand
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.aggregator.aggregator_implementation import (
    AggregatorImplementation,
)
from oaklib.implementations.bitwise.bitwise_implementation import BitwiseImplementation
from oaklib.implementations.bitwise.bitwise_ontology_index import BitwiseOntologyIndex
from oaklib.implementations.bitwise.bitwise_utils import bitmap_from_list, map_bitmap_to_ints
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from tests import (
    CELLULAR_COMPONENT,
    CYTOPLASM,
    INPUT_DIR,
    INTERNEURON,
    NUCLEUS,
    TISSUE,
    VACUOLE, OUTPUT_DIR,
)
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_DB = INPUT_DIR / "go-nucleus.db"
TEST_DUMP_OUT = OUTPUT_DIR / "go-nucleus-bitwise.pickle"


class TestBitwise(unittest.TestCase):
    """
    Tests fast bitwise index.
    """

    def setUp(self) -> None:
        #inner_oi = get_implementation_from_shorthand(f"pronto:{str(TEST_ONT)}")
        inner_oi = get_implementation_from_shorthand(f"sqlite:{str(TEST_DB)}")
        print(inner_oi)
        self.oi = BitwiseImplementation(wrapped_adapter=inner_oi)
        #self.oi.build_index()
        self.compliance_tester = ComplianceTester(self)

    def test_dump(self):
        oi = self.oi
        oi.dump(TEST_DUMP_OUT)

    def test_impl(self):
        oi = self.oi
        #for e in oi.entities():
        oix = oi.ontology_index
        for e in [NUCLEUS]:
            e_ix = oix.curie_to_int[e]
            print(e)
            print(e_ix)
            print(oi.label(e))
            print(list(oi.ancestors(e, predicates=[IS_A, PART_OF])))
            print(list(oi.wrapped_adapter.ancestors(e, predicates=[IS_A, PART_OF])))
            print(list(oi.ontology_index.ancestor_map[e_ix]))

    def test_ic(self):
        oi = self.oi
        self.compliance_tester.test_information_content_scores(oi)
        cases = []
        for e in oi.entities():
            #print(e)
            print(e, oi.get_information_content(e))

    def test_profiles(self):
        #self.compliance_tester.test_pairwise_similarity(self.oi)
        pass

    def test_jaccard(self):
        oi = self.oi
        for e1 in oi.entities():
            for e2 in oi.entities():
                s = oi.pairwise_similarity(e1, e2)
                if s.jaccard_similarity > 0.8:
                    print(e1, e2)
                    print(yaml_dumper.dumps(s))

    def test_index(self):
        oi = self.oi
        oix = oi.ontology_index
        cases = [
            [0],
            [],
            [0,1],
            [10000],
            [1,5,8],
        ]
        for c in cases:
            self.assertEqual(c, map_bitmap_to_ints(bitmap_from_list(c)))
