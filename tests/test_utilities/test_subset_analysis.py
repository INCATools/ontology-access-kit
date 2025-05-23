import logging
import unittest

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.subsets.subset_analysis import (
    all_subsets_overlap,
    compare_all_subsets,
    terms_by_subsets,
)
from tests import INPUT_DIR, OUTPUT_DIR

DB = INPUT_DIR / "go-nucleus.db"
TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"

BIOLOGICAL_PROCESS = "GO:0008150"
NEGEG_PHOSPH = "GO:0042326"
NUCLEUS = "GO:0005634"
DICTYOSTELIUM = "NCBITaxon:5782"
NUCLEAR_MEMBRANE = "GO:0031965"


PREDS = [IS_A, PART_OF]


class TestSubsetUtils(unittest.TestCase):
    def setUp(self) -> None:
        # resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        # oi = ProntoImplementation(resource)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))
        # oi.enable_transitive_query_cache()
        self.oi = oi

    def test_terms_by_subsets(self):
        tups = list(terms_by_subsets(self.oi, prefix="GO", subsumed_score=0.5, min_subsets=3))
        # for tup in tups:
        #    logging.info(tup)
        self.assertIn(
            ("GO:0005886", "plasma membrane", "gocheck_do_not_manually_annotate", 0.5), tups
        )
        self.assertIn(("GO:0005737", "cytoplasm", "goslim_pir", 1.0), tups)
        self.assertIn(("GO:0005938", "cell cortex", "goslim_chembl", 0.0), tups)

    def test_all_by_all(self):
        results = list(compare_all_subsets(self.oi, prefix="GO"))
        for r in results:
            # logging.info(f'Basic={r}')
            if r.set1_id == r.set2_id:
                assert r.jaccard_similarity == 1.0
                assert r.dice_similarity == 1.0
            else:
                assert 1.0 >= r.jaccard_similarity >= 0.0
                assert 1.0 >= r.dice_similarity >= 0.0
            assert r.set1_id.startswith("go")
        results = list(compare_all_subsets(self.oi, extend_down=True, prefix="GO"))
        for r in results:
            # logging.info(f'Extended={r}')
            if r.set1_id == r.set2_id:
                assert r.jaccard_similarity == 1.0
                assert r.dice_similarity == 1.0
            else:
                assert 1.0 >= r.jaccard_similarity >= 0.0
                assert 1.0 >= r.dice_similarity >= 0.0
            assert r.set1_id.startswith("go")

    def test_subset_analysis(self):
        oi = self.oi
        results = all_subsets_overlap(oi)
        n = 0
        for score, s1, s2 in results:
            logging.info(f"{score}: {s1} x {s2}")
            if s1 == s2:
                assert score == 1.0
            if s1 == "goslim_yeast" and s2 == "goslim_agr":
                assert score > 0.25
                assert score < 0.5
                n += 1
        assert n == 1
        assert len(results) > 20
