import json
import logging
import unittest

from linkml_runtime.loaders import yaml_loader
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.graph.relationship_walker import walk_up
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    add_labels_from_uris, load_mapping_rules
from oaklib.utilities.obograph_utils import as_multi_digraph, graph_as_dict
from oaklib.datamodels.mapping_rules_datamodel import MappingRuleCollection, MappingRule, Precondition, Postcondition
from oaklib.datamodels.vocabulary import IS_A, HAS_EXACT_SYNONYM, SKOS_EXACT_MATCH
from pronto import Ontology
from sssom.writers import write_table

from tests import OUTPUT_DIR, INPUT_DIR
from tests.test_cli import NUCLEUS




class TestChunker(unittest.TestCase):

    def test_chunker(self):
        arr = range(0, 1000)
        n = 0
        for l in chunk(arr, size=100):
            l = list(l)
            assert l[0] == n*100
            n += 1
        assert n == 10
