import os
import sqlite3
import unittest
from pathlib import Path

from oaklib.implementations.sqldb.sqlite_utils import (
    sqlite_bulk_load,
    sqlite_bulk_load2,
)
from tests import INPUT_DIR, OUTPUT_DIR

TSV = INPUT_DIR / "foo.tsv"
DB = OUTPUT_DIR / "test.db"
if os.name == "nt":
    _, db = os.path.splitdrive(DB)
    DB = Path(db)
TBL_NAME = "my_tbl"


class TestSqliteUtils(unittest.TestCase):
    # @unittest.skipIf(os.name == "nt", "temporarily skip sqlite3 on Windows")
    def test_bulkload(self):
        if DB.exists():
            DB.unlink()
        sqlite_bulk_load(DB, TSV, TBL_NAME, cols=["a", "b", "c"])
        con = sqlite3.connect(str(DB))
        rows = list(con.execute(f"SELECT * FROM {TBL_NAME}"))
        con.close()
        self.assertEqual(len(rows), 16)
        # Check first row which could be interpreted as column names.
        self.assertIn(("MGI", "MGI:1918911", "0610005C13Rik"), rows)
        # last row
        self.assertIn(("MGI", "MGI:3698435", "0610009E02Rik"), rows)

    @unittest.skipIf(os.name == "nt", "temporarily skip sqlite3 on Windows")
    def test_chunked_bulkload(self):
        if DB.exists():
            DB.unlink()
        args = dict(chunksize=10, sep="\t", comment="!", names=list("abc"))
        sqlite_bulk_load2(DB, TSV, TBL_NAME, read_csv_args=args)
        con = sqlite3.connect(str(DB))
        rows = list(con.execute(f"SELECT * FROM {TBL_NAME}"))
        con.close()
        self.assertEqual(len(rows), 16)
        # first row from first chunk
        self.assertIn(("MGI", "MGI:1918911", "0610005C13Rik"), rows)
        # last row from 2nd (and last) chunk
        self.assertIn(("MGI", "MGI:3698435", "0610009E02Rik"), rows)
