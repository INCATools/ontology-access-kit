import logging
import unittest

import yaml
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.cli import search, main
from pronto import Ontology

from tests import OUTPUT_DIR, INPUT_DIR
from click.testing import CliRunner

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_DB = INPUT_DIR / 'go-nucleus.db'
BAD_ONTOLOGY_DB = INPUT_DIR / 'bad-ontology.db'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'
NUCLEUS = 'GO:0005634'
ATOM = 'CHEBI:33250'

class TestCommandLineInterface(unittest.TestCase):

    def setUp(self) -> None:
        runner = CliRunner(mix_stderr=False)
        self.runner = runner

    def test_main_help(self):
        result = self.runner.invoke(main, ['--help'])
        out = result.stdout
        err = result.stderr
        self.assertIn('search', out)
        self.assertIn('subset', out)
        self.assertIn('validate', out)
        self.assertEqual(0, result.exit_code)

    ## OBOGRAPH

    def test_obograph_local(self):
        for input_arg in [str(TEST_ONT), f'sqlite:{TEST_DB}']:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'ancestors', 'nucl'])
            out = result.stdout
            assert 'GO:0043226 ! organelle' in out
            result = self.runner.invoke(main, ['-i', input_arg, 'ancestors', '-p', 'i', 'plasma membrane'])
            out = result.stdout
            assert 'GO:0016020 ! membrane' in out
            assert 'GO:0043226 ! organelle' not in out
            result = self.runner.invoke(main, ['-i', input_arg, 'descendants', '-p', 'i', 'GO:0016020'])
            out = result.stdout
            # TODO:
            #assert 'GO:0016020 ! membrane' not in out
            assert 'GO:0043226 ! organelle' not in out

    ## SEARCH

    def test_search_help(self):
        result = self.runner.invoke(main, ['search', '--help'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)

    def test_search_local(self):
        for input_arg in [str(TEST_ONT), f'sqlite:{TEST_DB}']:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'search', 'nucl'])
            out = result.stdout
            err = result.stderr
            if result.exit_code != 0:
                print(f'INPUT: {input_arg} code = {result.exit_code}')
                print(f'OUTPUT={out}')
                print(f'ERR={err}')
            logging.info(f'OUTPUT={out}')
            logging.info(f'ERR={err}')
            self.assertEqual(0, result.exit_code)
            self.assertIn(NUCLEUS, out)
            self.assertIn('nucleus', out)
            self.assertEqual("", err)

    def test_search_pronto_obolibrary(self):
        result = self.runner.invoke(main, ['-i', 'obolibrary:pato.obo', 'search', 'shape'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn('PATO:0002021', out)
        self.assertEqual("", err)

    ## VALIDATE

    def test_validate_help(self):
        result = self.runner.invoke(main, ['validate', '--help'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)

    def test_validate_bad_ontology(self):
        for input_arg in [f'sqlite:{BAD_ONTOLOGY_DB}']:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'validate'])
            out = result.stdout
            err = result.stderr
            logging.info(f'ERR={err}')
            self.assertEqual(0, result.exit_code)
            self.assertIn('EXAMPLE:1', out)
            self.assertIn('EXAMPLE:2', out)
            self.assertEqual("", err)

    def test_check_definitions(self):
        for input_arg in [TEST_ONT, f'sqlite:{TEST_DB}']:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'check-definitions'])
            out = result.stdout
            err = result.stderr
            logging.info(f'ERR={err}')
            self.assertEqual(0, result.exit_code)
            self.assertIn(ATOM, out)
            self.assertEqual("", err)

    ## LEXICAL

    def test_lexmatch_owl(self):
        outfile = f'{OUTPUT_DIR}/matcher-test-cli.owl.sssom.tsv'
        result = self.runner.invoke(main, ['-i', f'{INPUT_DIR}/matcher-test.owl', 'lexmatch', '-R', f'{INPUT_DIR}/matcher_rules.yaml',
                                           '-o', outfile])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn('skos:closeMatch', contents)
            self.assertIn('skos:exactMatch', contents)
        # TODO: currently pronto produces various warnings when parsing OWL
        #self.assertEqual("", err)

    def test_lexmatch_sqlite(self):
        outfile = f'{OUTPUT_DIR}/matcher-test-cli.db.sssom.tsv'
        result = self.runner.invoke(main, ['-i', f'sqlite:{INPUT_DIR}/matcher-test.db', 'lexmatch', '-R', f'{INPUT_DIR}/matcher_rules.yaml',
                                           '-o', outfile])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        with open(outfile) as stream:
            contents = "\n".join(stream.readlines())
            self.assertIn('skos:closeMatch', contents)
            self.assertIn('skos:exactMatch', contents)
            self.assertIn('x:bone_element', contents)
            self.assertIn('bone tissue', contents)