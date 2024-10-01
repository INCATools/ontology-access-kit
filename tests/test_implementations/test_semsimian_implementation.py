import os
import timeit
import unittest
from importlib.util import find_spec

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.selector import get_adapter
from tests import (
    ENDOMEMBRANE_SYSTEM,
    FUNGI,
    HUMAN,
    INPUT_DIR,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    VACUOLE,
)
from tests.test_implementations import ComplianceTester

DB = INPUT_DIR / "go-nucleus.db"

TEST_IC_MAP = INPUT_DIR / "test_ic.tsv"

EXPECTED_ICS = {
    "CARO:0000000": 21.05,
    "BFO:0000002": 0.7069,
    "BFO:0000003": 14.89,
}


@unittest.skipIf(os.name == "nt", "DB path loading inconsistent on Windows")
@unittest.skipIf(find_spec("semsimian") is None, "Semsimian not available")
class TestSemSimianImplementation(unittest.TestCase):
    """Implementation tests for Rust-based semantic similarity."""

    def setUp(self) -> None:
        """Set up"""
        db = DB.as_posix()

        oi = get_adapter(f"semsimian:sqlite:///{db}")
        comparison_oi = get_adapter(f"sqlite:///{db}")

        self.oi = oi
        self.other_oi = comparison_oi
        self.db = db
        self.compliance_tester = ComplianceTester(self)
        self.subject_terms = {VACUOLE, NUCLEUS, NUCLEAR_MEMBRANE}
        self.object_terms = {ENDOMEMBRANE_SYSTEM, HUMAN, FUNGI}
        self.predicates = {IS_A, PART_OF}
        self.term_pairwise_similarity_attributes = [
            attr
            for attr in vars(TermPairwiseSimilarity)
            if not any(attr.startswith(s) for s in ["class_", "_"])
        ]

    def test_definitions(self):
        """Definitions should be delegated to the wrapped adapter."""
        self.compliance_tester.test_definitions(self.oi, include_metadata=True)

    @unittest.skip("TODO: test with new rust code")
    def test_pairwise_similarity(self):
        if not isinstance(self.oi, SemanticSimilarityInterface):
            raise AssertionError("SemanticSimilarityInterface not implemented")
        self.compliance_tester.test_pairwise_similarity(self.oi)

    def test_compare_pairwise_similarity(self):
        adapter = self.oi
        if not isinstance(adapter, SemanticSimilarityInterface):
            raise AssertionError("SemanticSimilarityInterface not implemented")
        # entities = list(adapter.entities(filter_obsoletes=True, owl_type=OWL_CLASS))
        entities = [VACUOLE, ENDOMEMBRANE_SYSTEM, NUCLEUS, NUCLEAR_MEMBRANE, HUMAN, FUNGI]
        debug = False
        for s in entities:
            for o in entities:
                for preds in [self.predicates]:
                    sim = adapter.pairwise_similarity(s, o, predicates=preds)

                    original_sim = self.other_oi.pairwise_similarity(s, o, predicates=preds)
                    if sim is None:
                        if (
                            original_sim is not None
                            and original_sim.subject_id != original_sim.object_id
                        ):
                            raise ValueError(f"Expected None, got {original_sim}")
                        continue
                    self.assertEqual(sim.subject_id, original_sim.subject_id)
                    self.assertEqual(sim.object_id, original_sim.object_id)
                    self.assertAlmostEqual(
                        sim.jaccard_similarity,
                        original_sim.jaccard_similarity,
                        places=2,
                        msg=f"Jaccard similarity for {s} and {o} with predicates {preds} does not match",
                    )
                    # TODO: we expect these to match with the coming soon version of semsimian
                    if (
                        debug
                        and sim.ancestor_information_content
                        != original_sim.ancestor_information_content
                    ):
                        print("\n\n## COMPARING:")
                        print("Rust:")
                        print(yaml_dumper.dumps(sim))
                        print("Wrapped:")
                        print(yaml_dumper.dumps(original_sim))

    def test_all_by_all_pairwise_similarity(self):
        result = self.oi.all_by_all_pairwise_similarity(
            self.subject_terms, self.object_terms, self.predicates
        )
        sem_similarity_object: TermPairwiseSimilarity = [
            x for x in result if x.subject_id == "GO:0031965" and x.object_id == "GO:0012505"
        ][0]
        self.assertEqual(sem_similarity_object.ancestor_id, "GO:0012505")
        self.assertEqual(sem_similarity_object.jaccard_similarity, 0.4782608695652174)
        self.assertEqual(sem_similarity_object.ancestor_information_content, 5.8496657269155685)
        self.assertEqual(sem_similarity_object.phenodigm_score, 1.672622556711612)

        result2 = self.other_oi.all_by_all_pairwise_similarity(
            self.subject_terms, self.object_terms, self.predicates
        )

        sql_similarity_object: TermPairwiseSimilarity = [
            x for x in result2 if x.subject_id == "GO:0031965" and x.object_id == "GO:0012505"
        ][0]
        self.assertEqual(sem_similarity_object.ancestor_id, sql_similarity_object.ancestor_id)
        self.assertAlmostEqual(
            sem_similarity_object.jaccard_similarity, sql_similarity_object.jaccard_similarity
        )
        self.assertAlmostEqual(
            sem_similarity_object.ancestor_information_content,
            sql_similarity_object.ancestor_information_content,
            places=1,
        )
        self.assertAlmostEqual(
            sem_similarity_object.phenodigm_score, sql_similarity_object.phenodigm_score, places=2
        )

    def test_similarity_with_custom_ic_map(self):
        adapter = self.oi

        adapter.custom_ic_map_path = TEST_IC_MAP.as_posix()

        if not isinstance(adapter, SemanticSimilarityInterface):
            raise AssertionError("SemanticSimilarityInterface not implemented")
        entities = [VACUOLE, ENDOMEMBRANE_SYSTEM]

        for s in entities:
            for o in entities:
                for preds in [self.predicates]:
                    sim = adapter.pairwise_similarity(s, o, predicates=preds)
                    if sim is not None:
                        if s == VACUOLE and o == VACUOLE:
                            self.assertEqual(sim.ancestor_information_content, 5.5)
                        if s == ENDOMEMBRANE_SYSTEM and o == ENDOMEMBRANE_SYSTEM:
                            self.assertEqual(sim.ancestor_information_content, 6.0)
                        if s == VACUOLE and o == ENDOMEMBRANE_SYSTEM:
                            self.assertEqual(sim.ancestor_information_content, 0)
                    else:
                        raise ValueError(f"Did not get similarity for got {s} and {o}")

    def test_all_by_all_similarity_with_custom_ic_map(self):
        adapter = self.oi

        adapter.custom_ic_map_path = TEST_IC_MAP.as_posix()

        if not isinstance(adapter, SemanticSimilarityInterface):
            raise AssertionError("SemanticSimilarityInterface not implemented")
        entities = [VACUOLE, ENDOMEMBRANE_SYSTEM]

        sim = adapter.all_by_all_pairwise_similarity(entities, entities, predicates=self.predicates)

        for s in sim:
            self.assertIsNotNone(s)
            if s.object_id == VACUOLE and s.subject_id == VACUOLE:
                self.assertEqual(s.ancestor_information_content, 5.5)
            if s.object_id == ENDOMEMBRANE_SYSTEM and s.subject_id == ENDOMEMBRANE_SYSTEM:
                self.assertEqual(s.ancestor_information_content, 6.0)
            if s.object_id == VACUOLE and s.subject_id == ENDOMEMBRANE_SYSTEM:
                self.assertEqual(s.ancestor_information_content, 0)
            else:
                pass

    def test_semsimian_object_cache(self):
        start_time = timeit.default_timer()
        _ = list(
            self.oi.all_by_all_pairwise_similarity(
                self.subject_terms, self.object_terms, self.predicates
            )
        )
        end_time = timeit.default_timer()
        time_taken_1 = end_time - start_time

        shuffled_predicate = set(reversed(list(self.predicates)))
        start_time = timeit.default_timer()
        _ = list(
            self.oi.all_by_all_pairwise_similarity(
                self.subject_terms, self.object_terms, shuffled_predicate
            )
        )
        end_time = timeit.default_timer()
        time_taken_2 = end_time - start_time

        self.assertEqual(len(self.oi.semsimian_object_cache), 1)
        self.assertTrue(time_taken_1 > time_taken_2)
