import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.axioms.logical_definition_summarizer import (
    logical_definitions_to_matrix,
    parse_axes_to_config,
)
from tests import INPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"

CASES = [
    (
        "d,f",
        [
            {
                "defined_class": ["GO:0009893"],
                "genus": ["GO:0065007"],
                "metabolic_process": ["RO:0002213"],
            }
        ],
    ),
    ("d,g", [{"defined_class": ["GO:0009893"], "biological_regulation": ["GO:0009893"]}]),
    (
        "d,p",
        [
            {
                "defined_class": ["GO:0009893"],
                "genus": ["GO:0065007"],
                "positively_regulates": ["GO:0008152"],
            }
        ],
    ),
    (
        "f,g",
        [
            {
                "filler": ["GO:0008152"],
                "biological_regulation": ["GO:0009892", "GO:0009893", "GO:0019222"],
            }
        ],
    ),
    (
        "f,p",
        [
            {
                "filler": ["GO:0008152"],
                "positively_regulates": ["GO:0009893"],
                "negatively_regulates": ["GO:0009892"],
                "regulates": ["GO:0019222"],
            }
        ],
    ),
    (
        "f",
        [
            {
                "filler": ["GO:0008152"],
                "positively_regulates": ["GO:0009893"],
                "negatively_regulates": ["GO:0009892"],
                "regulates": ["GO:0019222"],
            }
        ],
    ),
    # use organelle
    (
        "g,f",
        [
            {
                "genus": ["GO:0043226"],
                "membrane": ["GO:0043227"],
                "intracellular_anatomical_structure": ["GO:0043229"],
            }
        ],
    ),
    (
        "g,p",
        [
            {"genus": ["GO:0043226"], "has_part": ["GO:0043227"], "part_of": ["GO:0043229"]},
            {"genus": ["GO:0016020"], "part_of": ["GO:0031090", "GO:0031965", "GO:0098590"]},
        ],
    ),
]


class TestLogicalDefinitionSummarizer(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.ldefs = list(oi.logical_definitions(oi.entities()))

    def test_summarizer(self):
        ldefs = self.ldefs
        for case in CASES:
            (cfg_str, expected) = case
            cfg = parse_axes_to_config(cfg_str)
            rows = logical_definitions_to_matrix(self.oi, ldefs, cfg)
            for row in rows:
                slim_row = {k: v for k, v in row.items() if v and v != [""]}
                if slim_row in expected:
                    expected.remove(slim_row)
            self.assertEqual([], expected, f"Expected rows not found in output in {case}")
