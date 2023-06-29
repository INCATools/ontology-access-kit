import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib import get_implementation_from_shorthand
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.poi.pickled_poi_implementation import (
    PickledPoiImplementation,
)
from oaklib.implementations.poi.poi_implementation import PoiImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from tests import (
    IMBO,
    INPUT_DIR,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    OUTPUT_DIR,
    VACUOLE,
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
        self.oi = PoiImplementation(wrapped_adapter=inner_oi)
        self.compliance_tester = ComplianceTester(self)

    def test_dump(self):
        oi = self.oi
        oi.dump(TEST_DUMP_OUT)
        oi2 = PickledPoiImplementation(pickle_path=TEST_DUMP_OUT)
        self.assertEqual(oi.ontology_index, oi2.ontology_index)

    def test_impl(self):
        oi = self.oi
        # for e in oi.entities():
        oix = oi.ontology_index
        self.assertCountEqual(oi.closure_predicates, [IS_A, PART_OF])
        cases = [
            (NUCLEUS, "nucleus"),
            (VACUOLE, "vacuole"),
        ]
        for case in cases:
            e, label = case
            e_ix = oix.curie_to_int[e]
            self.assertEqual(e, oix.int_to_curie[e_ix])
            self.assertEqual(oi.label(e), label)
            num_descs1 = oix.reflexive_descendant_count_map[e_ix]
            num_descs2 = len(list(oi.wrapped_adapter.descendants(e, predicates=[IS_A, PART_OF])))
            self.assertEqual(num_descs1, num_descs2)
            ancs1 = list(oi.ancestors(e, predicates=[IS_A, PART_OF]))
            if not isinstance(oi.wrapped_adapter, OboGraphInterface):
                raise NotImplementedError
            ancs2 = set(oi.wrapped_adapter.ancestors(e, predicates=[IS_A, PART_OF]))
            self.assertCountEqual(ancs1, ancs2)
            with self.assertRaises(ValueError):
                # we expect to fail as only a single predicate index is supported
                list(oi.ancestors(e, predicates=[IS_A]))

    def test_label(self):
        self.compliance_tester.test_labels(self.oi)

    @unittest.skip("TODO")
    def test_ic(self):
        oi = self.oi
        oix = oi.ontology_index
        self.compliance_tester.test_information_content_scores(oi)
        cases = [(NUCLEUS, IMBO), (NUCLEAR_MEMBRANE, NUCLEUS)]
        for sub, sup in cases:
            self.assertGreater(
                oi.get_information_content(sub, predicates=[IS_A, PART_OF]),
                oi.get_information_content(sup, predicates=[IS_A, PART_OF]),
            )
        for e in oi.entities():
            e_ix = oix.curie_to_int[e]
            ic = oi.get_information_content(e, predicates=[IS_A, PART_OF])
            num_descs1 = oix.reflexive_descendant_count_map[e_ix]
            num_descs2 = len(set(oi.wrapped_adapter.descendants(e, predicates=[IS_A, PART_OF])))
            self.assertEqual(num_descs1, num_descs2)
            self.assertGreaterEqual(ic, 0.0)
            original_ic = oi.wrapped_adapter.get_information_content(e, predicates=[IS_A, PART_OF])
            self.assertAlmostEqual(original_ic or 0.0, ic, places=1)

    @unittest.skip("TODO")
    def test_pairwise_similarity(self):
        oi = self.oi
        sim = oi.termset_pairwise_similarity(
            [NUCLEUS, VACUOLE], [NUCLEAR_ENVELOPE], predicates=[IS_A, PART_OF], labels=True
        )
        logging.info(yaml_dumper.dumps(sim))
        self.compliance_tester.test_pairwise_similarity(self.oi, isa_partof_only=True)
