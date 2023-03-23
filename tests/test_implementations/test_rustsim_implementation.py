import unittest

from rustsim import jaccard_similarity

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.selector import get_adapter
from tests import ENDOMEMBRANE_SYSTEM, INPUT_DIR, VACUOLE

DB = INPUT_DIR.joinpath("go-nucleus.db")


class TestRustSimImplementation(unittest.TestCase):
    """Implementation tests for Rust-based semantic similarity."""

    def setUp(self) -> None:
        """Set up"""
        # Calling get_implementation_from_shorthand() alone fails on Windows
        try:
            oi = get_adapter(f"rustsim:sqlite:///{str(DB)}")
        except FileNotFoundError:
            oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))

        self.oi = oi

    # def test_pairwise_similarity(self):
    #     pass

    def test_rustsim_jaccard(self):
        """Tests Rust implementations of Jaccard semantic similarity."""
        subj_ancs = set(self.oi.ancestors(VACUOLE, predicates=[IS_A, PART_OF]))
        obj_ancs = set(self.oi.ancestors(ENDOMEMBRANE_SYSTEM, predicates=[IS_A, PART_OF]))
        jaccard = jaccard_similarity(subj_ancs, obj_ancs)
        calculated_jaccard = len(subj_ancs.intersection(obj_ancs)) / len(subj_ancs.union(obj_ancs))
        self.assertAlmostEqual(calculated_jaccard, jaccard)
