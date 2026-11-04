"""Equivalence tests for the SQL-backed ``SqlImplementation.roots`` override (issue #881).

The override must return exactly the same set of root CURIEs as the
interface-level (naive) implementation for every combination of parameters,
while doing the work in the database engine instead of materializing every
relationship into Python.
"""
import unittest
from pathlib import Path

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation

INPUT_DIR = Path(__file__).parent.parent / "input"
DB = INPUT_DIR / "go-nucleus.db"


class TestSqlRootsEquivalence(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = get_adapter(str(DB))
        self.assertIsInstance(self.adapter, SqlImplementation)

    def _base_roots(self, **kwargs):
        # Force the interface-level (naive) implementation via super() so the
        # SQL override under test is not exercised here.
        return set(super(SqlImplementation, self.adapter).roots(**kwargs))

    def test_roots_matches_base_default(self):
        override = set(self.adapter.roots())
        base = self._base_roots()
        self.assertGreater(len(override), 0)
        self.assertEqual(override, base)

    def test_roots_matches_base_with_predicates(self):
        override = set(self.adapter.roots(predicates=[IS_A]))
        base = self._base_roots(predicates=[IS_A])
        self.assertEqual(override, base)

    def test_roots_matches_base_with_id_prefixes(self):
        override = set(self.adapter.roots(id_prefixes=["GO"]))
        base = self._base_roots(id_prefixes=["GO"])
        self.assertEqual(override, base)

    def test_roots_matches_base_with_predicates_and_prefixes(self):
        override = set(self.adapter.roots(predicates=[IS_A], id_prefixes=["GO"]))
        base = self._base_roots(predicates=[IS_A], id_prefixes=["GO"])
        self.assertEqual(override, base)

    def test_roots_ignores_owl_thing(self):
        # With ignore_owl_thing=False the trivial owl:Thing root may appear.
        override = set(self.adapter.roots(ignore_owl_thing=False))
        base = self._base_roots(ignore_owl_thing=False)
        self.assertEqual(override, base)


if __name__ == "__main__":
    unittest.main()
