import logging
import unittest

from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.utilities.graph.networkx_bridge import relationships_to_multi_digraph
import networkx as nx

from tests import OUTPUT_DIR, INPUT_DIR

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'

KINASE_ACTIVATOR_ACTIVITY = 'GO:0019209'
BIOLOGICAL_PROCESS = 'GO:0008152'

class TestNetworkxBridge(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.mdg = relationships_to_multi_digraph(oi.all_relationships())

    def test_all_paths(self):
        paths = list(nx.all_simple_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY))
        for path in paths:
            logging.info(path)
        assert len(paths) > 10
        paths = list(nx.all_simple_edge_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY))
        for path in paths:
            logging.info(path)
        assert len(paths) > 10
        #paths = list(nx.shortest_simple_paths(self.mdg, BIOLOGICAL_PROCESS, KINASE_ACTIVATOR_ACTIVITY))
        #for path in paths:
        #    print(path)
        #assert len(paths) > 10









