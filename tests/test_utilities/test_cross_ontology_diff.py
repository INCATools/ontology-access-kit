import unittest

import kgcl_schema.grammar.parser as kgcl_parser
import yaml
from linkml_runtime.dumpers import yaml_dumper

from oaklib import get_adapter
from oaklib.datamodels.cross_ontology_diff import DiffCategory, RelationalDiff
from oaklib.datamodels.vocabulary import HAS_PART, IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.resource import OntologyResource
from oaklib.utilities.mapping.cross_ontology_diffs import (
    calculate_pairwise_relational_diff,
)
from tests import (
    CELLULAR_COMPONENT,
    EXAMPLE_ONTOLOGY_OBO,
    IMBO,
    INPUT_DIR,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    OUTPUT_DIR,
)

TEST_ONT = INPUT_DIR / "unreciprocated-mapping-test.obo"
TEST_OWL = INPUT_DIR / "unreciprocated-mapping-test.owl"
SSSOM = INPUT_DIR / "unreciprocated-mapping-test.sssom.tsv"
EXPECTED_L2R = INPUT_DIR / "unreciprocated-mapping-test.expected.l2r.diff.yaml"
EXPECTED_BIDI = INPUT_DIR / "unreciprocated-mapping-test.expected.bidi.diff.yaml"
TEST_OUT = OUTPUT_DIR / "unreciprocated-mapping-test.diff.yaml"


class TestStructuralDiff(unittest.TestCase):
    def setUp(self) -> None:
        """
        Creates handles for all implementations to be tested
        """
        resource = OntologyResource(slug=str(TEST_ONT), local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.owl_oi = SparqlImplementation(OntologyResource(str(TEST_OWL)))

    def test_initial_check(self):
        cases = [
            ("Y:5", [IS_A], ["Y:5"]),
            ("Y:5", [IS_A, IS_A], ["Y:5"]),
        ]
        for oi in [self.oi, self.owl_oi]:
            for subject, preds, ancs in cases:
                self.assertEqual(ancs, list(oi.ancestors([subject], predicates=preds)))

    def test_structural_diff(self):
        cases = [(EXPECTED_L2R, False), (EXPECTED_BIDI, True)]
        for expected_file, bidirectional in cases:
            with open(expected_file) as f:
                expected_results = yaml.safe_load(f)
            expected_results = [RelationalDiff(**obj) for obj in expected_results]
            # TODO: restore all checks
            # for oi in [self.oi, self.owl_oi]:
            for oi in [self.oi]:
                results = list(
                    calculate_pairwise_relational_diff(
                        oi, oi, ["X", "Y", "Z"], bidirectional=bidirectional
                    )
                )
                yaml_dumper.dump(results, str(TEST_OUT))
                self.assertCountEqual(expected_results, results)

    def test_structural_diff_with_preds(self):
        bidirectional = False
        with open(EXPECTED_L2R) as f:
            expected_results = yaml.safe_load(f)
        expected_results = [RelationalDiff(**obj) for obj in expected_results]
        # TODO: restore all checks
        # for oi in [self.oi, self.owl_oi]:
        for oi in [self.oi]:
            results = list(
                calculate_pairwise_relational_diff(
                    oi, oi, ["X", "Y", "Z"], predicates=[IS_A, PART_OF], bidirectional=bidirectional
                )
            )
            yaml_dumper.dump(results, str(TEST_OUT))
            self.assertCountEqual(expected_results, results)
            results = list(
                calculate_pairwise_relational_diff(
                    oi, oi, ["X", "Y", "Z"], predicates=[PART_OF], bidirectional=bidirectional
                )
            )
            # logging.info(yaml_dumper.dumps(results))
            self.assertEqual(2, len(results))

    def test_restrict_to_sources(self):
        for oi in [self.oi, self.owl_oi]:
            results = list(calculate_pairwise_relational_diff(oi, oi, ["Z"]))
            self.assertEqual([], results)

    def test_with_patch(self):
        """
        Tests cross-ontology diffs by successively applying patches to the source ontology

        This test involves successive versions of the same ontology, so we use
        identity_mappings (note this might be better done using a conventional diff,
        but it serves to test the functionality here).

        Each time we apply a patch, we check that the diffs are as expected.

        Note that the diffs are non-monotonic: adding a new patch can change
        an older diff
        """
        left_oi = get_adapter(str(EXAMPLE_ONTOLOGY_OBO))
        right_oi = get_adapter(str(EXAMPLE_ONTOLOGY_OBO))
        if not isinstance(left_oi, OboGraphInterface):
            raise ValueError("Left implementation must be OboGraphInterface")
        if not isinstance(right_oi, OboGraphInterface):
            raise ValueError("Left implementation must be OboGraphInterface")
        cases = [
            (
                f"delete edge {NUCLEUS} {IS_A} {IMBO}",
                [
                    RelationalDiff(
                        category=DiffCategory.NoRelationship,
                        left_subject_id=NUCLEUS,
                        left_object_id=IMBO,
                        left_predicate_id=IS_A,
                        right_subject_id=NUCLEUS,
                        right_object_id=IMBO,
                    )
                ],
            ),
            (
                f"create edge {NUCLEUS} {HAS_PART} {NUCLEAR_MEMBRANE}",
                [
                    RelationalDiff(
                        category=DiffCategory.NonEntailedRelationship,
                        left_subject_id=NUCLEUS,
                        left_object_id=IMBO,
                        left_predicate_id=IS_A,
                        right_subject_id=NUCLEUS,
                        right_object_id=IMBO,
                    ),
                    RelationalDiff(
                        category=DiffCategory.NoRelationship,
                        left_subject_id=NUCLEUS,
                        left_object_id=NUCLEAR_MEMBRANE,
                        left_predicate_id=HAS_PART,
                        right_subject_id=NUCLEUS,
                        right_object_id=NUCLEAR_MEMBRANE,
                    ),
                ],
            ),
        ]
        entities = list(left_oi.descendants([CELLULAR_COMPONENT], [IS_A]))
        for patch_kgcl, expected_results in cases:
            # cumulatively apply patches
            # print(f"Patching with {patch_kgcl}")
            patch = kgcl_parser.parse_statement(patch_kgcl)
            if not isinstance(right_oi, PatcherInterface):
                raise ValueError(f"{type(right_oi)} is not a patcher")
            right_oi.apply_patch(patch)
            # for r in right_oi.relationships([NUCLEUS]):
            #     print(f"R={r}")
            if not isinstance(right_oi, OboGraphInterface):
                raise ValueError(f"{type(right_oi)} is not a patcher")
            results = list(
                calculate_pairwise_relational_diff(
                    left_oi,
                    right_oi,
                    ["GO"],
                    entities=entities,
                    include_identity_mappings=True,
                    bidirectional=True,
                )
            )
            self.assertGreater(len(results), 40)
            results = [r for r in results if str(r.category) != str(DiffCategory.Identical.text)]
            self.assertCountEqual(expected_results, results)
            rev_results = list(
                calculate_pairwise_relational_diff(
                    right_oi,
                    left_oi,
                    ["GO"],
                    entities=entities,
                    include_identity_mappings=True,
                    bidirectional=True,
                )
            )
            rev_results = [
                r for r in rev_results if str(r.category) != str(DiffCategory.Identical.text)
            ]
            self.assertEqual(len(rev_results), len(results))
