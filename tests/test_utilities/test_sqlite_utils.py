import sqlite3
import unittest

from oaklib.implementations.sqldb.sqlite_utils import (
    sqlite_bulk_load,
    sqlite_bulk_load2,
)
from tests import INPUT_DIR, OUTPUT_DIR

TSV = INPUT_DIR / "foo.tsv"
DB = OUTPUT_DIR / "test.db"
TBL_NAME = "my_tbl"


class TestSqliteUtils(unittest.TestCase):
    def test_bulkload(self):
        if DB.exists():
            DB.unlink()
        sqlite_bulk_load(DB, TSV, TBL_NAME, cols=["a", "b", "c"])
        con = sqlite3.connect(str(DB))
        rows = list(con.execute(f"SELECT * FROM {TBL_NAME}"))
        self.assertGreater(len(rows), 5)
        self.assertIn(("MGI", "MGI:1918911", "0610005C13Rik"), rows)

    def test_chunked_bulkload(self):
        if DB.exists():
            DB.unlink()
        args = dict(chunksize=1000, sep="\t", comment="!", names=list("abc"))
        sqlite_bulk_load2(DB, TSV, TBL_NAME, read_csv_args=args)
        con = sqlite3.connect(str(DB))
        rows = list(con.execute(f"SELECT * FROM {TBL_NAME}"))
        self.assertGreater(len(rows), 5)
        self.assertIn(("MGI", "MGI:1918911", "0610005C13Rik"), rows)
