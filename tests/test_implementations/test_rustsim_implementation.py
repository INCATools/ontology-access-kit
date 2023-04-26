import os
import unittest

from rustsim import (
    get_intersection,
    mrca_and_score,
    relationships_to_closure_table,
    semantic_jaccard_similarity,
)

from oaklib.datamodels.vocabulary import IS_A, PART_OF

# from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
# from oaklib.resource import OntologyResource
from oaklib.selector import get_adapter
from tests import ENDOMEMBRANE_SYSTEM, INPUT_DIR, VACUOLE
from tests.test_implementations import ComplianceTester

DB = INPUT_DIR / "go-nucleus.db"


class TestRustSimImplementation(unittest.TestCase):
    """Implementation tests for Rust-based semantic similarity."""

    def setUp(self) -> None:
        """Set up"""
        db = DB.as_posix()
        # this is to drop the drive name from the database path.
        # The main reason for this is use of 2 descriptors [rustsim and sqlite].
        if os.name == "nt":
            _, db = os.path.splitdrive(db)

        self.oi = get_adapter(f"rustsim:sqlite:///{db}")
        self.information_content_scores = {
            "CARO:0000000": 21.05,
            "BFO:0000002": 0.7069,
            "BFO:0000003": 14.89,
        }
        self.compliance_tester = ComplianceTester(self)
        self.predicates = [IS_A, PART_OF]
        self._rust_closure_table = relationships_to_closure_table(
            [r for r in self.oi.relationships(include_entailed=True)]
        )

    # * Testing python bindings for rustsim package.#################################################
    def test_rustsim_jaccard(self):
        """Tests Rust implementations of Jaccard semantic similarity."""
        subj_ancs = set(self.oi.ancestors(VACUOLE, predicates=self.predicates))
        obj_ancs = set(self.oi.ancestors(ENDOMEMBRANE_SYSTEM, predicates=self.predicates))

        jaccard = semantic_jaccard_similarity(
            self._rust_closure_table, VACUOLE, ENDOMEMBRANE_SYSTEM, set(self.predicates)
        )
        calculated_jaccard = len(subj_ancs.intersection(obj_ancs)) / len(subj_ancs.union(obj_ancs))
        self.assertAlmostEqual(calculated_jaccard, jaccard)

    def test_rustsim_mrca(self):
        """Tests Rust implementations of Most Recent Common Ancestor (mrca) with score."""
        expected_tuple = ("CARO:0000000", 21.05)
        mrca = mrca_and_score(self.information_content_scores)
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

    # * ###############################################################################################
    # * Testing RustSimImplementation
    def test_pairwise_similarity(self):
        """Test pairwise similarity."""
        self.compliance_tester.test_pairwise_similarity(self.oi)

    def test_common_ancestors(self):
        """Test common ancestors."""
        self.compliance_tester.test_common_ancestors(self.oi)
