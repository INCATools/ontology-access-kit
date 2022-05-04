import json
import logging
import unittest

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.graph.relationship_walker import walk_up
from oaklib.utilities.obograph_utils import as_multi_digraph, graph_as_dict, graph_to_tree, filter_by_predicates
from oaklib.datamodels.vocabulary import IS_A, PART_OF
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
        # https://github.com/althonos/pronto/issues/163
        #self.assertIn('{"sub": "CL:0000000", "pred": "BFO:0000051", "obj": "GO:0005634"}', json_obj)

    def test_as_networkx(self):
        mdg = as_multi_digraph(self.graph)
        found = False
        self.assertIn(NUCLEUS, mdg.nodes)
        for e in mdg.edges(data=True):
            logging.info(f'SU={e}')
        self.assertIn(('GO:0005634', 'GO:0031965', {'predicate': 'BFO:0000050'}), mdg.edges(data=True))

    def test_filter_by_predicates(self):
        g = self.graph
        g2 = filter_by_predicates(g, predicates=[IS_A, PART_OF])
        self.assertCountEqual(g.nodes, g2.nodes)
        self.assertGreater(len(g.edges), len(g2.edges))
        self.assertGreater(len(g2.edges), 100)

    def test_as_tree(self):
        t = graph_to_tree(self.graph, predicates=[IS_A])
        lines = t.split('\n')
        self.assertIn('[i] BFO:0000015 ! process', t)
        self.assertNotIn('[p]', t)
        self.assertNotIn(PART_OF, t)
        self.assertGreater(len(lines), 100)
        t = graph_to_tree(self.graph, predicates=[IS_A, PART_OF])
        lines = t.split('\n')
        self.assertIn('[i] BFO:0000015 ! process', t)
        self.assertIn('* [p] GO:0019209 ! kinase activator activity', t)
        self.assertGreater(len(lines), 100)

