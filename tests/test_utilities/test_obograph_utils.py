import json
import logging
import unittest

from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.utilities.obograph_utils import as_multi_digraph, graph_as_dict
from obolib.vocabulary.vocabulary import IS_A
from pronto import Ontology

from tests import OUTPUT_DIR, INPUT_DIR
from tests.test_cli import NUCLEUS

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestOboGraphUtils(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.graph = oi.as_obograph()

    def test_as_json(self):
        obj = graph_as_dict(self.graph)
        json_obj = json.dumps(obj)
        self.assertIn('{"id": "GO:0003674"', json_obj)
        self.assertIn('{"sub": "CL:0000000", "pred": "has_part", "obj": "GO:0005634"}', json_obj)

    def test_as_networkx(self):
        mdg = as_multi_digraph(self.graph)
        found = False
        self.assertIn(NUCLEUS, mdg.nodes)
        for e in mdg.edges(data=True):
            print(f'SU={e}')
        self.assertIn(('GO:0005634', 'GO:0031965', {'predicate': 'part_of'}), mdg.edges(data=True))