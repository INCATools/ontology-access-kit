import json
import logging
import unittest

from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom
from obolib.utilities.obograph_utils import as_multi_digraph, graph_as_dict
from obolib.vocabulary.vocabulary import IS_A
from pronto import Ontology
from sssom.writers import write_table

from tests import OUTPUT_DIR, INPUT_DIR
from tests.test_cli import NUCLEUS

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.lexical.yaml'
TEST_SSSOM_OUT = OUTPUT_DIR / 'go-nucleus.sssom.tsv'


class TestLexicalIndex(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation.create(resource)
        self.oi = oi
        self.lexical_index = create_lexical_index(oi)

    def test_index_contents(self):
        groupings = self.lexical_index.groupings['cell periphery']
        self.assertEqual(len(groupings.relationships), 2)
        self.assertCountEqual(['GO:0005938', 'GO:0071944'], [r.element for r in groupings.relationships])

    def test_save(self):
        save_lexical_index(self.lexical_index, TEST_OUT)

    def test_sssom(self):
        msdf = lexical_index_to_sssom(self.oi, self.lexical_index)
        with open(TEST_SSSOM_OUT, 'w', encoding='utf-8') as file:
            write_table(msdf, file)
