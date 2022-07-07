"""Test subset utilities."""
import unittest

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.subsets.slimmer_utils import roll_up_to_named_subset
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
    """Test subset utilities."""

    def setUp(self) -> None:
        """Set up."""
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))
        self.oi = oi

    def test_roll_up(self):
        """Test roll up."""
        oi = self.oi
        term_curies = [t for t in oi.all_entity_curies() if t.startswith("GO:")]
        for subset in oi.all_subset_curies():
            # print(f'SUBSET: {subset}')
            m = roll_up_to_named_subset(self.oi, subset, term_curies, predicates=[IS_A, PART_OF])
            n = 0
            for _, mapped_to in m.items():
                # print(f'm[{term}] == {mapped_to}')
                n += len(mapped_to)
            if subset.startswith("chebi"):
                assert n == 0
            if subset == "goslim_yeast":
                self.assertCountEqual(m["GO:0004857"], ["GO:0003674", "GO:0008150"])
            if subset == "goslim_generic":
                self.assertCountEqual(m["GO:0009893"], ["GO:0008150"])
