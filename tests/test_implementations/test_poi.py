import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib import get_implementation_from_shorthand
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from oaklib.implementations.poi.poi_implementation import PoiImplementation
from oaklib.implementations.obograph.obograph_implementation import OboGraphImplementation
from tests import (
    INPUT_DIR,
    NUCLEUS,
    OUTPUT_DIR,
)
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_DB = INPUT_DIR / "go-nucleus.db"
TEST_DUMP_OUT = OUTPUT_DIR / "go-nucleus-bitwise.pickle"


class TestPoiImplementation(unittest.TestCase):
    """
    Tests in-memory python ontology index.
    """

    def setUp(self) -> None:
        inner_oi = get_implementation_from_shorthand(f"sqlite:{str(TEST_DB)}")
        #if isinstance(inner_oi, OboGraphImplementation):
        self.oi = PoiImplementation(wrapped_adapter=inner_oi)
        #else:
        #    raise NotImplementedError(f"{inner_oi} not a OG")
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

