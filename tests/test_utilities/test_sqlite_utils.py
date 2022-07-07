"""Test SQLLite utilities."""
import sqlite3
import unittest

from oaklib.implementations.sqldb.sqlite_utils import sqlite_bulk_load
from tests import INPUT_DIR, OUTPUT_DIR

TSV = INPUT_DIR / "foo.tsv"
DB = OUTPUT_DIR / "test.db"
TBL_NAME = "my_tbl"


class TestSqliteUtils(unittest.TestCase):
    """Test SQLLite utilities."""

    def test_bulkload(self):
        """Test backload."""
        if DB.exists():
            DB.unlink()
        sqlite_bulk_load(DB, TSV, TBL_NAME, cat_cmd=["grep", "-v", "\\!"], cols=["a", "b", "c"])
        con = sqlite3.connect(str(DB))
        rows = list(con.execute(f"SELECT * FROM {TBL_NAME}"))
        self.assertGreater(len(rows), 5)
        self.assertIn(("MGI", "MGI:1918911", "0610005C13Rik"), rows)
