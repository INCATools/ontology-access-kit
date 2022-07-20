import logging
import unittest
from typing import List

from linkml_runtime.dumpers import yaml_dumper
from oaklib.datamodels.taxon_constraints import SubjectTerm, Taxon, TaxonConstraint
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.types import TAXON_CURIE
from oaklib.utilities.taxon.taxon_constraint_utils import all_term_taxon_constraints, \
    get_term_with_taxon_constraints, eval_candidate_taxon_constraint, parse_gain_loss_file, get_taxon_constraints_description

from tests import OUTPUT_DIR, INPUT_DIR, INTRACELLULAR, CELLULAR_ORGANISMS, PHOTOSYNTHETIC_MEMBRANE, \
    PLANTS_OR_CYANOBACTERIA, SOROCARP_STALK_DEVELOPMENT, DICTYOSTELIUM_DISCOIDEUM, HUMAN, DICTYOSTELIUM, \
    FUNGI_OR_DICTYOSTELIUM, FUNGI, FUNGI_OR_BACTERIA, MAMMALIA
from tests.test_cli import NUCLEUS, NUCLEAR_ENVELOPE, BACTERIA, EUKARYOTA

GAIN_LOSS_FILE = INPUT_DIR / 'go-evo-gains-losses.csv'
TEST_INCONSISTENT = INPUT_DIR / 'taxon-constraint-test.obo'
DB = INPUT_DIR / 'go-nucleus.db'
TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'

PREDICATES = [IS_A, PART_OF]

class TestTaxonConstraintsUtils(unittest.TestCase):

    def setUp(self) -> None:
        oi = ProntoImplementation(OntologyResource(slug=str(TEST_ONT), local=True))
        self.oi = oi
        fake_oi = ProntoImplementation(OntologyResource(slug=str(TEST_INCONSISTENT), local=True))
        self.fake_oi = fake_oi

    def test_never_in(self):
        oi = self.oi
        never, only, _ = all_term_taxon_constraints(oi, NUCLEUS)
        self.assertCountEqual([BACTERIA], never)
        never, only, _ = all_term_taxon_constraints(oi, NUCLEAR_ENVELOPE)
        self.assertCountEqual([BACTERIA], never)
        never, only, _ = all_term_taxon_constraints(oi, NUCLEAR_ENVELOPE, predicates=[IS_A])
        self.assertCountEqual([], never)
        st = get_term_with_taxon_constraints(oi, NUCLEAR_ENVELOPE, include_redundant=True)
        #print(yaml_dumper.dumps(st))
        never = [tc for tc in st.never_in if not tc.redundant]
        assert all(tc.redundant_with_only_in for tc in never)
        only = [tc for tc in st.only_in if not tc.redundant]
        assert all(not tc.redundant_with_only_in for tc in only)
        assert all(tc.taxon.id == EUKARYOTA for tc in only)
        # See: https://github.com/althonos/pronto/issues/163


    def test_intracellular(self):
        oi = self.oi
        t = INTRACELLULAR
        st = get_term_with_taxon_constraints(oi, t, include_redundant=True)
        self.assertCountEqual(st.never_in, [])
        self.assertEqual(1, len(st.only_in))
        never = [tc.taxon.id for tc in st.never_in]
        only = [tc.taxon.id for tc in st.only_in]
        never_nr = [tc.taxon.id for tc in st.never_in if not tc.redundant]
        only_nr = [tc.taxon.id for tc in st.only_in if not tc.redundant]
        never_r = [tc.taxon.id for tc in st.never_in if tc.redundant]
        only_r = [tc.taxon.id for tc in st.only_in if tc.redundant]
        self.assertCountEqual([CELLULAR_ORGANISMS], only)
        self.assertCountEqual([CELLULAR_ORGANISMS], only_nr)
        self.assertCountEqual([], only_r)

    def test_photosynthetic_membrane(self):
        oi = self.oi
        t = PHOTOSYNTHETIC_MEMBRANE
        st = get_term_with_taxon_constraints(oi, t, include_redundant=True)
        #print(yaml_dumper.dumps(st))
        self.assertCountEqual(st.never_in, [])
        self.assertEqual(5, len(st.only_in))
        never = set([tc.taxon.id for tc in st.never_in])
        only = set([tc.taxon.id for tc in st.only_in])
        never_nr = set([tc.taxon.id for tc in st.never_in if not tc.redundant])
        only_nr = set([tc.taxon.id for tc in st.only_in if not tc.redundant])
        never_r = set([tc.taxon.id for tc in st.never_in if tc.redundant])
        only_r = set([tc.taxon.id for tc in st.only_in if tc.redundant])
        self.assertCountEqual([PLANTS_OR_CYANOBACTERIA, CELLULAR_ORGANISMS], only)
        self.assertCountEqual([PLANTS_OR_CYANOBACTERIA], only_nr)
        #print(only_r)
        self.assertCountEqual([PLANTS_OR_CYANOBACTERIA, CELLULAR_ORGANISMS], only_r)

    def test_nuclear_envelope(self):
        oi = self.oi
        t = NUCLEAR_ENVELOPE
        st = get_term_with_taxon_constraints(oi, t, include_redundant=True)
        #print(yaml_dumper.dumps(st))
        self.assertEqual(2, len(st.never_in))
        self.assertEqual(3, len(st.only_in))
        never = set([tc.taxon.id for tc in st.never_in])
        only = set([tc.taxon.id for tc in st.only_in])
        never_nr = set([tc.taxon.id for tc in st.never_in if not tc.redundant])
        only_nr = set([tc.taxon.id for tc in st.only_in if not tc.redundant])
        never_r = set([tc.taxon.id for tc in st.never_in if tc.redundant])
        only_r = set([tc.taxon.id for tc in st.only_in if tc.redundant])
        self.assertCountEqual([BACTERIA], never)
        self.assertCountEqual([BACTERIA], never_nr)
        self.assertCountEqual([], never_r)
        assert st.never_in[0].redundant_with_only_in
        self.assertCountEqual([EUKARYOTA, CELLULAR_ORGANISMS], only)
        self.assertCountEqual([EUKARYOTA], only_nr)
        self.assertCountEqual([CELLULAR_ORGANISMS], only_r)

    def test_candidates(self):
        oi = self.oi
        def make_tcs(term: str, only: List[TAXON_CURIE], never: List[TAXON_CURIE],
                     present: List[TAXON_CURIE] = []) -> SubjectTerm:
            return SubjectTerm(id=term,
                               only_in=[TaxonConstraint(taxon=Taxon(t)) for t in only],
                               never_in=[TaxonConstraint(taxon=Taxon(t)) for t in never],
                               present_in=[TaxonConstraint(taxon=Taxon(t)) for t in present],
                               )
        # test: refine the only_in, never_in already entailed
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(SOROCARP_STALK_DEVELOPMENT,
                                                      [DICTYOSTELIUM_DISCOIDEUM],
                                                      [HUMAN],
                                                      [DICTYOSTELIUM_DISCOIDEUM]))
        self.assertFalse(st.unsatisfiable)
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.never_in[0].redundant)
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        self.assertFalse(st.only_in[0].redundant)
        # test: identical only_in, [fake] more specific never_in
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(SOROCARP_STALK_DEVELOPMENT,
                                                      [DICTYOSTELIUM],
                                                      [DICTYOSTELIUM_DISCOIDEUM],
                                                      [FUNGI_OR_DICTYOSTELIUM]))
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertFalse(st.never_in[0].redundant_with_only_in)
        self.assertTrue(st.only_in[0].redundant)
        self.assertEqual(st.only_in[0].redundant_with[0].taxon.id, DICTYOSTELIUM)
        self.assertEqual(st.only_in[0].redundant_with[0].via_terms[0].id, SOROCARP_STALK_DEVELOPMENT)
        # test: multiple
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(SOROCARP_STALK_DEVELOPMENT,
                                                      [DICTYOSTELIUM, FUNGI_OR_DICTYOSTELIUM],
                                                      [FUNGI, FUNGI_OR_BACTERIA],
                                                      [DICTYOSTELIUM_DISCOIDEUM]))
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        [never_in_fungi] = [tc for tc in st.never_in if tc.taxon.id == FUNGI]
        self.assertTrue(never_in_fungi.redundant)
        self.assertTrue(never_in_fungi.redundant_with_only_in)
        [never_in_union] = [tc for tc in st.never_in if tc.taxon.id == FUNGI_OR_BACTERIA]
        self.assertFalse(never_in_union.redundant)
        self.assertTrue(never_in_union.redundant_with_only_in)
        [only_in_dicty] = [tc for tc in st.only_in if tc.taxon.id == DICTYOSTELIUM]
        self.assertTrue(only_in_dicty.redundant)
        self.assertEqual(only_in_dicty.redundant_with[0].taxon.id, DICTYOSTELIUM)
        self.assertEqual(only_in_dicty.redundant_with[0].via_terms[0].id, SOROCARP_STALK_DEVELOPMENT)
        [only_in_union] = [tc for tc in st.only_in if tc.taxon.id == FUNGI_OR_DICTYOSTELIUM]
        self.assertTrue(only_in_union.redundant)
        self.assertEqual(only_in_union.redundant_with[0].taxon.id, DICTYOSTELIUM)
        #self.assertEqual(only_in_union.redundant_with[0].via_terms[0].id, SOROCARP_STALK_DEVELOPMENT)
        # test: nuclear envelope, redundant assertsion
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(NUCLEAR_ENVELOPE,
                                                      [CELLULAR_ORGANISMS],
                                                      [BACTERIA],
                                                      [HUMAN, DICTYOSTELIUM_DISCOIDEUM]))
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertTrue(st.never_in[0].redundant)
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        self.assertTrue(st.only_in[0].redundant)
        #self.assertEqual(st.only_in[0].redundant_with[0].subject, NUCLEUS)
        self.assertEqual(st.only_in[0].redundant_with[0].taxon.id, EUKARYOTA)
        self.assertEqual(st.only_in[0].redundant_with[0].via_terms[0].id, NUCLEUS)
        # test: nuclear envelope, [fake] non-redundant
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(NUCLEAR_ENVELOPE,
                                                      [CELLULAR_ORGANISMS],
                                                      [BACTERIA],
                                                      [HUMAN, DICTYOSTELIUM]))
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertTrue(st.never_in[0].redundant)
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        self.assertTrue(st.only_in[0].redundant)
        #self.assertEqual(st.only_in[0].redundant_with[0].subject, NUCLEUS)
        self.assertEqual(st.only_in[0].redundant_with[0].taxon.id, EUKARYOTA)
        self.assertEqual(st.only_in[0].redundant_with[0].via_terms[0].id, NUCLEUS)
        # fake assertion
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(NUCLEUS,
                                                      [MAMMALIA],
                                                      [HUMAN],
                                                      [FUNGI]))
        self.assertFalse(st.unsatisfiable)
        #print(yaml_dumper.dumps(st))
        self.assertFalse(st.never_in[0].redundant)
        self.assertFalse(st.never_in[0].redundant_with_only_in)
        self.assertFalse(st.only_in[0].redundant)
        # bad ID
        with self.assertRaises(ValueError) as err:
            st = eval_candidate_taxon_constraint(oi, make_tcs(NUCLEUS, [], ['X:1']))
        with self.assertRaises(ValueError) as err:
            st = eval_candidate_taxon_constraint(oi, make_tcs(NUCLEUS, ['X:1'], []))
        st = eval_candidate_taxon_constraint(oi, make_tcs(NUCLEUS, [], []))
        assert st.never_in == []
        assert st.only_in == []
        # test: unsat, from never in
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(NUCLEUS,
                                                      [],
                                                      [CELLULAR_ORGANISMS]))
        #print(yaml_dumper.dumps(st))
        self.assertTrue(st.unsatisfiable)
        # test: unsat, from never in [FAKE EXAMPLE]
        st = eval_candidate_taxon_constraint(oi,
                                             make_tcs(NUCLEUS,
                                                      [],
                                                      [DICTYOSTELIUM],
                                                      [DICTYOSTELIUM_DISCOIDEUM]))
        #print(yaml_dumper.dumps(st))
        self.assertTrue(st.unsatisfiable)

    def test_taxon_subclass(self):
        self.assertIn(CELLULAR_ORGANISMS, list(self.oi.ancestors(BACTERIA, predicates=[IS_A])))


    def test_unsatisfiable(self):
        fake_oi = self.fake_oi
        st = get_term_with_taxon_constraints(fake_oi, PHOTOSYNTHETIC_MEMBRANE)
        #print(yaml_dumper.dumps(st))

    def test_all(self):
        oi = self.oi
        term_curies = [t for t in oi.all_entity_curies() if t.startswith('GO:')]
        for t in term_curies:
            st = get_term_with_taxon_constraints(oi, t)
            logging.info(yaml_dumper.dumps(st))
            desc = get_taxon_constraints_description(oi, st)
            #print(desc)

    def test_parser(self):
        with open(GAIN_LOSS_FILE) as file:
            for st in parse_gain_loss_file(file):
                logging.info(yaml_dumper.dumps(st))
