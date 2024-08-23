import logging
import unittest
from typing import List

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.taxon_constraints import SubjectTerm, Taxon, TaxonConstraint
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.types import TAXON_CURIE
from oaklib.utilities.taxon.taxon_constraint_utils import parse_gain_loss_file
from tests import (
    BACTERIA,
    CELLULAR_ORGANISMS,
    DICTYOSTELIUM,
    DICTYOSTELIUM_DISCOIDEUM,
    EUKARYOTA,
    FUNGI,
    FUNGI_OR_BACTERIA,
    FUNGI_OR_DICTYOSTELIUM,
    HUMAN,
    INPUT_DIR,
    INTRACELLULAR,
    MAMMALIA,
    MEMBRANE,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    OUTPUT_DIR,
    PHOTOSYNTHETIC_MEMBRANE,
    PLANTS_OR_CYANOBACTERIA,
    REGULATION_OF_BIOLOGICAL_PROCESS,
    REGULATION_OF_PHOSPHORYLATION,
    SOROCARP_STALK_DEVELOPMENT,
)

GAIN_LOSS_FILE = INPUT_DIR / "go-evo-gains-losses.csv"
TEST_INCONSISTENT = INPUT_DIR / "taxon-constraint-test.obo"  # contains deliberate errors
DB = INPUT_DIR / "go-nucleus.db"
TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"

PREDICATES = [IS_A, PART_OF]


def create_subject_term(
    term: str,
    only: List[TAXON_CURIE],
    never: List[TAXON_CURIE],
    present: List[TAXON_CURIE] = None,
) -> SubjectTerm:
    if present is None:
        present = []
    return SubjectTerm(
        id=term,
        only_in=[TaxonConstraint(taxon=Taxon(t)) for t in only],
        never_in=[TaxonConstraint(taxon=Taxon(t)) for t in never],
        present_in=[TaxonConstraint(taxon=Taxon(t)) for t in present],
    )


class TestTaxonConstraintsUtils(unittest.TestCase):
    def setUp(self) -> None:
        oi = ProntoImplementation(OntologyResource(slug=str(TEST_ONT), local=True))
        self.oi = oi
        oi.cache_lookups = True
        # oi.precompute_direct_constraint_cache()
        fake_oi = ProntoImplementation(OntologyResource(slug=str(TEST_INCONSISTENT), local=True))
        self.fake_oi = fake_oi

    def test_all(self):
        """
        Tests multiple possible combinations of taxon constraints.
        """
        # CASES TUPLES:
        # subject_id,
        # predicates,
        # include_redundant,
        # include_redundant_with_only_in,
        # expected_never,
        # expected_only,
        # expected_present_in,
        # desc,
        cases = [
            (MEMBRANE, None, True, True, [], [], [HUMAN, FUNGI], "No TCs on general term"),
            (
                INTRACELLULAR,
                [IS_A, PART_OF],
                True,
                True,
                [],
                [CELLULAR_ORGANISMS],
                [HUMAN, FUNGI],
                "intracellular implies cell, which implies cellular organism",
            ),
            (
                INTRACELLULAR,
                [IS_A, PART_OF],
                False,
                True,
                [],
                [CELLULAR_ORGANISMS],
                [HUMAN, FUNGI],
                "intracellular implies cell, which implies cellular organism (nr)",
            ),
            (NUCLEUS, [], True, True, [BACTERIA], [EUKARYOTA], [HUMAN, FUNGI], "TCs are direct"),
            (NUCLEAR_MEMBRANE, [], True, True, [], [], [HUMAN, FUNGI], "direct present-in"),
            (
                NUCLEAR_MEMBRANE,
                None,
                False,
                True,
                [BACTERIA],
                [EUKARYOTA],
                [HUMAN, FUNGI],
                "mix of inferred/direct",
            ),
            (
                NUCLEUS,
                [],
                False,
                False,
                [],
                [EUKARYOTA],
                [HUMAN, FUNGI],
                "never in bacteria redundant with only in eukaryota",
            ),
            (
                NUCLEUS,
                None,
                False,
                True,
                [BACTERIA],
                [EUKARYOTA],
                [HUMAN, FUNGI],
                "use ALL predicates (no redundant)",
            ),
            (NUCLEUS, [IS_A], True, True, [BACTERIA], [EUKARYOTA], [], "use is-a only"),
            (
                NUCLEUS,
                [IS_A, PART_OF],
                True,
                True,
                [BACTERIA],
                [EUKARYOTA, CELLULAR_ORGANISMS],
                [HUMAN, FUNGI],
                "includes redundant from ancestors (nucleus)",
            ),
            (
                NUCLEUS,
                [IS_A, PART_OF],
                False,
                True,
                [BACTERIA],
                [EUKARYOTA],
                [HUMAN, FUNGI],
                "excludes redundant from ancestors (nucleus)",
            ),
            (NUCLEAR_ENVELOPE, [], True, True, [], [], [HUMAN, FUNGI], "No TCs on direct"),
            (
                NUCLEAR_ENVELOPE,
                [IS_A, PART_OF],
                True,
                True,
                [BACTERIA],
                [EUKARYOTA, CELLULAR_ORGANISMS],
                [HUMAN, FUNGI],
                "includes redundant from ancestors (nuclear envelope)",
            ),
            (
                NUCLEAR_ENVELOPE,
                [IS_A, PART_OF],
                False,
                True,
                [BACTERIA],
                [EUKARYOTA],
                [HUMAN, FUNGI],
                "excludes redundant from ancestors (nuclear envelope)",
            ),
            (
                PHOTOSYNTHETIC_MEMBRANE,
                None,
                False,
                True,
                [],
                [PLANTS_OR_CYANOBACTERIA],
                [],
                "plants and some bacteria",
            ),
            (
                PHOTOSYNTHETIC_MEMBRANE,
                None,
                True,
                True,
                [],
                [CELLULAR_ORGANISMS, PLANTS_OR_CYANOBACTERIA],
                [],
                "plants and some bacteria",
            ),
        ]
        for case in cases:
            (
                subject_id,
                predicates,
                include_redundant,
                include_redundant_with_only_in,
                expected_never,
                expected_only,
                expected_present_in,
                desc,
            ) = case
            logging.debug(f"Case={case}")
            desc = f""""DESC={desc}
                        term={subject_id} preds={predicates}
                        redundant? {include_redundant} ({include_redundant_with_only_in})
                        N={expected_never}
                        O={expected_only}
                        P={expected_present_in}"""
            st = self.oi.get_term_with_taxon_constraints(
                subject_id,
                predicates,
                include_redundant=include_redundant is not False,
                include_never_in_even_if_redundant_with_only_in=include_redundant_with_only_in,
            )
            never = list(set([tc.taxon.id for tc in st.never_in]))
            only = list(set([tc.taxon.id for tc in st.only_in]))
            present_in = list(set([tc.taxon.id for tc in st.present_in]))
            logging.debug(
                f"D: {desc}, preds={predicates}, only_in={only}, never_in={never}, present_in={present_in}"
            )
            self.assertCountEqual(expected_never, never, f"Never in mismatch: {desc}")
            self.assertCountEqual(expected_only, only, desc)
            self.assertCountEqual(expected_present_in, present_in, desc)
            test_st = self.oi.get_term_with_taxon_constraints(
                subject_id, predicates, include_redundant=False
            )
            evaluated_st = self.oi.eval_candidate_taxon_constraint(test_st, predicates=predicates)
            for tc in evaluated_st.only_in + evaluated_st.never_in:
                if not tc.redundant:
                    print(yaml_dumper.dumps(evaluated_st))
                    print(yaml_dumper.dumps(tc))
                self.assertTrue(tc.redundant, f"Redundant with only_in: {tc}")

    def test_eval_candidates(self):
        oi = self.oi

        def make_tcs(
            term: str,
            only: List[TAXON_CURIE],
            never: List[TAXON_CURIE],
            present: List[TAXON_CURIE] = None,
        ) -> SubjectTerm:
            if present is None:
                present = []
            return SubjectTerm(
                id=term,
                only_in=[TaxonConstraint(taxon=Taxon(t)) for t in only],
                never_in=[TaxonConstraint(taxon=Taxon(t)) for t in never],
                present_in=[TaxonConstraint(taxon=Taxon(t)) for t in present],
            )

        cases = [
            (
                MEMBRANE,
                [HUMAN],
                [],
                [],
                False,
                [],
                [],
                [],
                "fake: membrane only in humans conflicts with present-in Fungi",
            ),
            (
                MEMBRANE,
                [],
                [HUMAN],
                [],
                False,
                [],
                [],
                [],
                "fake: membrane never in humans conflicts with present-in Human",
            ),
            (
                SOROCARP_STALK_DEVELOPMENT,
                [DICTYOSTELIUM_DISCOIDEUM],
                [HUMAN],
                [DICTYOSTELIUM_DISCOIDEUM],
                True,
                [],
                [],
                [HUMAN],
                "never in redundant with only in",
            ),
            (
                SOROCARP_STALK_DEVELOPMENT,
                [DICTYOSTELIUM],
                [DICTYOSTELIUM_DISCOIDEUM],
                [],
                True,
                [DICTYOSTELIUM],
                [],
                [],
                "fake example - novel never-in",
            ),
        ]
        for case in cases:
            logging.debug(case)
            (
                subject_id,
                only,
                never,
                present,
                satisfiable,
                only_in_redundant,
                never_in_redundant,
                never_in_redundant_only_in,
                desc,
            ) = case
            desc = f"{desc} ({subject_id})"
            candidate_st = make_tcs(subject_id, only, never, present)
            st = oi.eval_candidate_taxon_constraint(candidate_st)
            logging.info(yaml_dumper.dumps(st))
            self.assertEqual(satisfiable, not st.unsatisfiable, desc)
            self.assertCountEqual(
                only_in_redundant, [tc.taxon.id for tc in st.only_in if tc.redundant], desc
            )
            self.assertCountEqual(
                never_in_redundant, [tc.taxon.id for tc in st.never_in if tc.redundant], desc
            )
            self.assertCountEqual(
                never_in_redundant_only_in,
                [tc.taxon.id for tc in st.never_in if tc.redundant_with_only_in],
            )

    def test_eval_candidates2(self):
        oi = self.oi

        def make_tcs(
            term: str,
            only: List[TAXON_CURIE],
            never: List[TAXON_CURIE],
            present: List[TAXON_CURIE] = None,
        ) -> SubjectTerm:
            if present is None:
                present = []
            return SubjectTerm(
                id=term,
                only_in=[TaxonConstraint(taxon=Taxon(t)) for t in only],
                never_in=[TaxonConstraint(taxon=Taxon(t)) for t in never],
                present_in=[TaxonConstraint(taxon=Taxon(t)) for t in present],
            )

        # test: refine the only_in, never_in already entailed
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(
                SOROCARP_STALK_DEVELOPMENT,
                [DICTYOSTELIUM_DISCOIDEUM],
                [HUMAN],
                [DICTYOSTELIUM_DISCOIDEUM],
            ),
        )
        self.assertFalse(st.unsatisfiable)
        # logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.never_in[0].redundant)
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        self.assertFalse(st.only_in[0].redundant)
        # test: identical only_in, [fake] more specific never_in
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(
                SOROCARP_STALK_DEVELOPMENT,
                [DICTYOSTELIUM],
                [DICTYOSTELIUM_DISCOIDEUM],
                [],
            ),
        )
        # logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertFalse(st.never_in[0].redundant_with_only_in)
        # test: multiple
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(
                SOROCARP_STALK_DEVELOPMENT,
                [DICTYOSTELIUM, FUNGI_OR_DICTYOSTELIUM],
                [FUNGI, FUNGI_OR_BACTERIA],
                [DICTYOSTELIUM_DISCOIDEUM],
            ),
        )
        logging.info(yaml_dumper.dumps(st))
        # logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        [never_in_fungi] = [tc for tc in st.never_in if tc.taxon.id == FUNGI]
        self.assertTrue(never_in_fungi.redundant)
        self.assertTrue(never_in_fungi.redundant_with_only_in)
        [never_in_union] = [tc for tc in st.never_in if tc.taxon.id == FUNGI_OR_BACTERIA]
        self.assertFalse(never_in_union.redundant)
        self.assertTrue(never_in_union.redundant_with_only_in)
        [only_in_dicty] = [tc for tc in st.only_in if tc.taxon.id == DICTYOSTELIUM]
        self.assertTrue(only_in_dicty.redundant)
        # self.assertEqual(only_in_dicty.redundant_with[0].taxon.id, DICTYOSTELIUM)
        # self.assertEqual(
        #    only_in_dicty.redundant_with[0].via_terms[0].id, SOROCARP_STALK_DEVELOPMENT
        # )
        [only_in_union] = [tc for tc in st.only_in if tc.taxon.id == FUNGI_OR_DICTYOSTELIUM]
        self.assertTrue(only_in_union.redundant)
        self.assertEqual(only_in_union.redundant_with[0].taxon.id, DICTYOSTELIUM)
        # self.assertEqual(only_in_union.redundant_with[0].via_terms[0].id, SOROCARP_STALK_DEVELOPMENT)
        # test: nuclear envelope, redundant assertion
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(
                NUCLEAR_ENVELOPE,
                [CELLULAR_ORGANISMS],
                [BACTERIA],
                [HUMAN, DICTYOSTELIUM_DISCOIDEUM],
            ),
        )
        logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertTrue(st.only_in[0].redundant)
        self.assertEqual(EUKARYOTA, st.only_in[0].redundant_with[0].taxon.id)
        self.assertEqual(NUCLEUS, st.only_in[0].redundant_with[0].via_terms[0].id)
        self.assertFalse(st.never_in[0].redundant, "not strictly redundant")
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        # self.assertEqual(st.only_in[0].redundant_with[0].subject, NUCLEUS)
        # test: nuclear envelope, [fake] non-redundant
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(NUCLEAR_ENVELOPE, [CELLULAR_ORGANISMS], [BACTERIA], [HUMAN, DICTYOSTELIUM])
        )
        # logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.unsatisfiable)
        self.assertFalse(st.never_in[0].redundant, "not strictly redundant")
        self.assertTrue(st.never_in[0].redundant_with_only_in)
        self.assertTrue(st.only_in[0].redundant)
        # self.assertEqual(st.only_in[0].redundant_with[0].subject, NUCLEUS)
        self.assertEqual(st.only_in[0].redundant_with[0].taxon.id, EUKARYOTA)
        self.assertEqual(st.only_in[0].redundant_with[0].via_terms[0].id, NUCLEUS)
        # fake assertion
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(NUCLEUS, [MAMMALIA], [HUMAN], [DICTYOSTELIUM_DISCOIDEUM])
        )
        self.assertEqual(True, st.unsatisfiable)
        # logging.info(yaml_dumper.dumps(st))
        self.assertFalse(st.never_in[0].redundant)
        self.assertFalse(st.never_in[0].redundant_with_only_in)
        self.assertFalse(st.only_in[0].redundant)
        # bad ID
        # with self.assertRaises(ValueError):
        #    st = oi.eval_candidate_taxon_constraint(make_tcs(NUCLEUS, [], ["X:1"]))
        # with self.assertRaises(ValueError):
        #    st = oi.eval_candidate_taxon_constraint(make_tcs(NUCLEUS, ["X:1"], []))
        st = oi.eval_candidate_taxon_constraint(make_tcs(NUCLEUS, [], []))
        assert st.never_in == []
        assert st.only_in == []
        # test: unsat, from never in
        st = oi.eval_candidate_taxon_constraint(make_tcs(NUCLEUS, [], [CELLULAR_ORGANISMS]))
        # logging.info(yaml_dumper.dumps(st))
        self.assertTrue(st.unsatisfiable)
        # test: unsat, from never in [FAKE EXAMPLE]
        st = oi.eval_candidate_taxon_constraint(
            make_tcs(NUCLEUS, [], [DICTYOSTELIUM], [DICTYOSTELIUM_DISCOIDEUM])
        )
        # logging.info(yaml_dumper.dumps(st))
        self.assertTrue(st.unsatisfiable)

    def test_taxon_subclass(self):
        self.assertIn(CELLULAR_ORGANISMS, list(self.oi.ancestors(BACTERIA, predicates=[IS_A])))
        self.assertIn(
            CELLULAR_ORGANISMS, list(self.oi.ancestors(FUNGI_OR_BACTERIA, predicates=[IS_A]))
        )
        self.assertIn(FUNGI_OR_BACTERIA, list(self.oi.ancestors(FUNGI, predicates=[IS_A])))
        self.assertIn(FUNGI_OR_BACTERIA, list(self.oi.ancestors(BACTERIA, predicates=[IS_A])))

    def test_unsatisfiable(self):
        """
        Tests detection of inconsistencies.
        """
        # use a fake ontology with a deliberate error (phosphorylation is only in mammals)
        fake_oi = self.fake_oi
        cases = [
            (PHOTOSYNTHETIC_MEMBRANE, None, False, "direct conflict with fake only_in to Mammalia"),
            (NUCLEUS, None, False, "conflicts due to nuclear envelope"),
            (NUCLEAR_ENVELOPE, None, False, "conflicts with fake present-in to Bacteria"),
            (
                REGULATION_OF_BIOLOGICAL_PROCESS,
                None,
                True,
                "causes conflicts deeper but not itself unsat",
            ),
            (
                REGULATION_OF_PHOSPHORYLATION,
                None,
                False,
                "conflict as phosphorylation has a present-in Mammalia",
            ),
            (
                REGULATION_OF_PHOSPHORYLATION,
                [IS_A, PART_OF],
                True,
                "no conflict without regulates link",
            ),
        ]
        for subject, preds, satisfiable, desc in cases:
            st = fake_oi.get_term_with_taxon_constraints(subject, predicates=preds)
            logging.debug(yaml_dumper.dumps(st))
            self.assertEqual(bool(st.unsatisfiable), not satisfiable, f"{desc} // {subject}")

    def test_all_entities(self):
        oi = self.oi
        term_curies = [t for t in oi.entities() if t.startswith("GO:")]
        for t in term_curies:
            st = oi.get_term_with_taxon_constraints(t)
            logging.info(yaml_dumper.dumps(st))
            oi.get_taxon_constraints_description(st)
            # logging.info(desc)

    def test_parser(self):
        with open(GAIN_LOSS_FILE) as file:
            events = list(parse_gain_loss_file(file))
            for st in events:
                self.assertTrue(all(tc.evolutionary for tc in st.only_in))
                self.assertTrue(all(tc.evolutionary for tc in st.never_in))
            self.assertGreater(len(events), 10)
