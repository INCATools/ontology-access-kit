import unittest

from oaklib import get_adapter
from oaklib.interfaces import MappingProviderInterface
from oaklib.utilities.mapping.boomer_utils import BoomerEngine, DiffType
from tests import EXAMPLE_ONTOLOGY_DB, INPUT_DIR, NUCLEUS, VACUOLE

EXAMPLE = INPUT_DIR / "boomer-example.md"
GO_EXAMPLE = INPUT_DIR / "boomer-fake-go-example.md"


class TestBoomerUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = BoomerEngine()
        self.engine.load(EXAMPLE)

    def test_filter(self):
        ben = self.engine
        cases = [
            (0.01, None, 7),
            (0.8, None, 0),
            (None, None, 7),
            (None, 0.3, 0),
        ]
        for minc, maxc, expected_n in cases:
            ms = list(ben.mappings(minimum_confidence=minc, maximum_confidence=maxc))
            # for m in ms:
            #    print(m)
            self.assertEqual(expected_n, len(ms))

    def test_compare(self):
        """
        tests BoomerEngine.compare against a fake GO example
        """
        ben = BoomerEngine()
        ben.load(GO_EXAMPLE)
        adapter = get_adapter(str(EXAMPLE_ONTOLOGY_DB))
        if not isinstance(adapter, MappingProviderInterface):
            raise AssertionError(f"{EXAMPLE_ONTOLOGY_DB} can't supply mappings")
        current_mappings = list(adapter.all_sssom_mappings())
        self.assertGreater(len(current_mappings), 10)
        cases = [
            (0.99, False, False, []),
            (0.99, True, True, []),
            (
                0.75,
                False,
                False,
                [
                    (DiffType.NEW, NUCLEUS, "FAKE:1"),
                    (DiffType.CONFLICT, NUCLEUS, "Wikipedia:Cell_nucleus"),
                    (DiffType.CONFLICT, VACUOLE, "Wikipedia:Vacuole"),
                ],
            ),
            (
                0.75,
                True,
                False,
                [
                    (DiffType.NEW, NUCLEUS, "FAKE:1"),
                    (DiffType.REJECT, NUCLEUS, "Wikipedia:Cell_nucleus"),
                    (DiffType.CONFLICT, VACUOLE, "Wikipedia:Vacuole"),
                ],
            ),
            (
                0.75,
                True,
                True,
                [
                    (DiffType.NEW, NUCLEUS, "FAKE:1"),
                    (DiffType.REJECT, NUCLEUS, "Wikipedia:Cell_nucleus"),
                    (DiffType.OK, VACUOLE, "Wikipedia:Vacuole"),
                ],
            ),
        ]
        for minimum_confidence, reject_non_exact, promote_xref_to_exact, expected in cases:
            results = list(
                ben.compare(
                    current_mappings,
                    minimum_confidence=minimum_confidence,
                    reject_non_exact=reject_non_exact,
                    promote_xref_to_exact=promote_xref_to_exact,
                )
            )
            result_tups = [(r[0], r[2].subject_id, r[2].object_id) for r in results]
            self.assertCountEqual(expected, result_tups)
