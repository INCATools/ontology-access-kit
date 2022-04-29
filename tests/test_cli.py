import logging
import unittest

from oaklib.cli import search, main
from oaklib.datamodels.vocabulary import IN_TAXON

from tests import OUTPUT_DIR, INPUT_DIR, NUCLEUS, NUCLEAR_ENVELOPE, ATOM, INTERNEURON, BACTERIA, EUKARYOTA, VACUOLE, \
    CELLULAR_COMPONENT, HUMAN, MAMMALIA, SHAPE
from click.testing import CliRunner

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OWL_RDF = INPUT_DIR / 'go-nucleus.owl.ttl'
TEST_DB = INPUT_DIR / 'go-nucleus.db'
TEST_DB = INPUT_DIR / 'go-nucleus.db'
BAD_ONTOLOGY_DB = INPUT_DIR / 'bad-ontology.db'
TEST_OUT = OUTPUT_DIR / 'tmp'


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
        for input_arg in [str(TEST_ONT), f'sqlite:{TEST_DB}', str(TEST_OWL_RDF)]:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'ancestors', NUCLEUS])
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

    def test_gap_fill(self):
        result = self.runner.invoke(main, ['-i', str(TEST_DB), 'viz', '--gap-fill',
                                           '-p', f'i,p,{IN_TAXON}',
                                           NUCLEUS, VACUOLE, CELLULAR_COMPONENT,
                                           '-O', 'json', '-o', str(TEST_OUT)])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        with open(TEST_OUT) as file:
            contents = "\n".join(file.readlines())
            self.assertIn(NUCLEUS, contents)
            self.assertIn(VACUOLE, contents)
            self.assertIn(CELLULAR_COMPONENT, contents)
            # TODO: parse json to check it conforms
            #g = json_loader.loads(contents, target_class=obograph.Graph)



    ## MAPPINGS

    def test_mappings_local(self):
        result = self.runner.invoke(main, ['-i', str(TEST_ONT), 'term-mappings', 'GO:0016740'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        #self.assertIn('EC:2', out)

    ## TAXON

    def test_taxon_constraints_local(self):
        for input_arg in [TEST_ONT, f'sqlite:{TEST_DB}', TEST_OWL_RDF]:
            result = self.runner.invoke(main, ['-i', str(input_arg), 'taxon-constraints', NUCLEUS, '-o', str(TEST_OUT)])
            out = result.stdout
            err = result.stderr
            self.assertEqual(0, result.exit_code)
            with open(TEST_OUT) as file:
                contents = "\n".join(file.readlines())
                self.assertIn('Eukaryota', contents)

    ## SEARCH

    def test_search_help(self):
        result = self.runner.invoke(main, ['search', '--help'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)

    def test_search_local(self):
        for input_arg in [str(TEST_ONT), f'sqlite:{TEST_DB}', TEST_OWL_RDF]:
            logging.info(f'INPUT={input_arg}')
            result = self.runner.invoke(main, ['-i', input_arg, 'search', 'l~nucl'])
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
        result = self.runner.invoke(main, ['-i', 'obolibrary:pato.obo', 'search', 't~shape'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertIn('PATO:0002021', out)   # conical - matches a synonym
        self.assertEqual("", err)
        result = self.runner.invoke(main, ['-i', 'obolibrary:pato.obo', 'search', 'l=shape'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertNotIn('PATO:0002021', out)   # conical - matches a synonym
        self.assertEqual("", err)
        result = self.runner.invoke(main, ['-i', 'obolibrary:pato.obo', 'search', 'shape'])
        out = result.stdout
        err = result.stderr
        self.assertEqual(0, result.exit_code)
        self.assertIn(SHAPE, out)
        self.assertNotIn('PATO:0002021', out)   # conical - matches a synonym
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
        result = self.runner.invoke(main, ['-i', f'pronto:{INPUT_DIR}/matcher-test.owl', 'lexmatch',
                                           '-R', f'{INPUT_DIR}/matcher_rules.yaml',
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