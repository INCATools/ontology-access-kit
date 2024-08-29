import logging
import unittest

from oaklib.implementations import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.mapping.cross_ontology_diffs import (
    calculate_pairwise_relational_diff,
)
from tests import EXTERNAL_DB_DIR

DB_FOLDER = EXTERNAL_DB_DIR / "unreciprocated-mapping-test.obo"


class TestSqlite(unittest.TestCase):
    def setUp(self) -> None:
        if EXTERNAL_DB_DIR.exists():
            self.skip = False
            dbs = {}
            db_dir = EXTERNAL_DB_DIR.absolute()
            for db in ["mp", "hp", "uberon", "emapa"]:
                path = f"sqlite:///{db_dir}/{db}.db"
                logging.info(path)
                r = OntologyResource(slug=path, local=True)
                dbs[db] = SqlImplementation(r)
            self.dbs = dbs
        else:
            self.skip = True
            logging.info("Skipping sqlite tests")

    @unittest.skip("TOO SLOW")
    def test_structural_diff(self):
        if self.skip:
            return
        dbs = self.dbs
        results = list(
            calculate_pairwise_relational_diff(dbs["uberon"], dbs["emapa"], ["UBERON", "EMAPA"])
        )
        for r in results:
            logging.info(r)
