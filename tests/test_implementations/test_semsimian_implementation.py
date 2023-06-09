import os
import unittest

from linkml_runtime.dumpers import yaml_dumper

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
        comparison_oi = get_adapter(f"sqlite:///{self.db}")

        self.oi = oi
        self.other_oi = comparison_oi
        self.db = db
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
