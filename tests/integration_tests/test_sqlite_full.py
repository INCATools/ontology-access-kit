import logging
import unittest
from collections import Iterator

from linkml_runtime.dumpers import yaml_dumper
from oaklib.implementations import SqlImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.omk.omk_mapping_utils import unreciprocated_mappings, calculate_pairwise_relational_diff
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index
from oaklib.utilities.mapping.sssom_utils import mappings_to_pairs

from tests import OUTPUT_DIR, INPUT_DIR, EXTERNAL_DB_DIR

DB_FOLDER = EXTERNAL_DB_DIR / 'unreciprocated-mapping-test.obo'


class TestSqlite(unittest.TestCase):

    def setUp(self) -> None:
        if EXTERNAL_DB_DIR.exists():
            self.skip = False
            dbs = {}
            db_dir = EXTERNAL_DB_DIR.absolute()
            for db in ['mp', 'hp', 'uberon', 'emapa']:
                path = f'sqlite:///{db_dir}/{db}.db'
                print(path)
                r = OntologyResource(slug=path, local=True)
                dbs[db]= SqlImplementation(r)
            self.dbs = dbs
        else:
            self.skip = True
            logging.info('Skipping sqlite tests')

    @unittest.skip('TOO SLOW')
    def test_structural_diff(self):
        if self.skip:
            return
        dbs = self.dbs
        results = list(calculate_pairwise_relational_diff(dbs['uberon'], dbs['emapa'], ['UBERON', 'EMAPA']))
        for r in results:
            print(r)




