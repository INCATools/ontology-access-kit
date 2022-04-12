import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.lexical.yaml'


class TestLexicalIndex(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.lexical_index = create_lexical_index(oi)

    def test_index_contents(self):
        groupings = self.lexical_index.groupings['cell periphery']
        self.assertEqual(len(groupings.relationships), 2)
        self.assertCountEqual(['GO:0005938', 'GO:0071944'], [r.element for r in groupings.relationships])

    def test_save(self):
        save_lexical_index(self.lexical_index, TEST_OUT)

