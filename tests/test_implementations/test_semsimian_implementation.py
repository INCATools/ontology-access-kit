import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from semsimian import get_intersection, jaccard_similarity, mrca_and_score

from oaklib.datamodels.vocabulary import IS_A, PART_OF, OWL_CLASS

from oaklib.selector import get_adapter
from tests import ENDOMEMBRANE_SYSTEM, INPUT_DIR, VACUOLE, NUCLEUS, NUCLEAR_MEMBRANE, HUMAN, FUNGI
from tests.test_implementations import ComplianceTester

DB = INPUT_DIR / "go-nucleus.db"

EXPECTED_ICS = {
            "CARO:0000000": 21.05,
            "BFO:0000002": 0.7069,
            "BFO:0000003": 14.89,
        }


class TestSemSimianImplementation(unittest.TestCase):
    """Implementation tests for Rust-based semantic similarity."""

    def setUp(self) -> None:
        """Set up"""
        db = DB.as_posix()
        # this is to drop the drive name from the database path.
        # The main reason for this is use of 2 descriptors [semsimian and sqlite].
        if os.name == "nt":
            _, db = os.path.splitdrive(db)

        oi = get_adapter(f"semsimian:sqlite:///{db}")

        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

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
                for preds in [[IS_A, PART_OF]]:
                    sim = adapter.pairwise_similarity(s, o, predicates=preds)
                    original_sim = adapter.wrapped_adapter.pairwise_similarity(s, o, predicates=preds)
                    self.assertEqual(sim.subject_id, original_sim.subject_id)
                    self.assertEqual(sim.object_id, original_sim.object_id)
                    self.assertAlmostEqual(sim.jaccard_similarity, original_sim.jaccard_similarity, places=2, msg=f"Jaccard similarity for {s} and {o} with predicates {preds} does not match")
                    # TODO: we expect these to match with the coming soon version of semsimian
                    if debug and sim.ancestor_information_content != original_sim.ancestor_information_content:
                        print("\n\n## COMPARING:")
                        print("Rust:")
                        print(yaml_dumper.dumps(sim))
                        print("Wrapped:")
                        print(yaml_dumper.dumps(original_sim))

    def test_semsimian_jaccard(self):
        """Tests Rust implementations of Jaccard semantic similarity."""
        subj_ancs = set(self.oi.ancestors(VACUOLE, predicates=[IS_A, PART_OF]))
        obj_ancs = set(self.oi.ancestors(ENDOMEMBRANE_SYSTEM, predicates=[IS_A, PART_OF]))
        jaccard = jaccard_similarity(subj_ancs, obj_ancs)
        calculated_jaccard = len(subj_ancs.intersection(obj_ancs)) / len(subj_ancs.union(obj_ancs))
        self.assertAlmostEqual(calculated_jaccard, jaccard)

    def test_semsimian_mrca(self):
        """Tests Rust implementations of Most Recent Common Ancestor (mrca) with score."""
        expected_tuple = ("CARO:0000000", 21.05)
        mrca = mrca_and_score(EXPECTED_ICS)
        self.assertEqual(mrca, expected_tuple)

    def test_get_intersection(self):
        """Tests Rust implementations of set intersections"""
        subject_ancestors = {
            "GO:0005622",
            "GO:0043229",
            "CARO:0000006",
            "GO:0043227",
            "GO:0043231",
            "NCBITaxon:Union_0000030",
            "owl:Thing",
            "GO:0005634",
            "CARO:0030000",
            "GO:0016020",
            "GO:0005575",
            "CL:0000000",
            "CARO:0000003",
            "NCBITaxon:2759",
            "NCBITaxon:Union_0000025",
            "BFO:0000004",
        }
        object_ancestors = {
            "GO:0005622",
            "GO:0043229",
            "CARO:0000006",
            "GO:0043227",
            "GO:0043231",
            "NCBITaxon:1",
            "GO:0110165",
            "BFO:0000002",
            "CARO:0000000",
        }
        expected_result = {"GO:0005622", "GO:0043229", "CARO:0000006", "GO:0043227", "GO:0043231"}
        result = get_intersection(subject_ancestors, object_ancestors)
        self.assertEqual(result, expected_result)
