import json
import logging
import unittest

from linkml_runtime.loaders import yaml_loader
from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.resource import OntologyResource
from obolib.utilities.graph.relationship_walker import walk_up
from obolib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    add_labels_from_uris, load_mapping_rules
from obolib.utilities.obograph_utils import as_multi_digraph, graph_as_dict
from obolib.vocabulary.mapping_rules_datamodel import MappingRuleCollection, MappingRule, Precondition, Postcondition
from obolib.vocabulary.vocabulary import IS_A, HAS_EXACT_SYNONYM, SKOS_EXACT_MATCH
from pronto import Ontology
from sssom.writers import write_table

from tests import OUTPUT_DIR, INPUT_DIR
from tests.test_cli import NUCLEUS

RULES = INPUT_DIR / 'matcher_rules.yaml'
MATCHER_TEST_ONT = INPUT_DIR / 'matcher-test.owl'
TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.lexical.yaml'
TEST_SSSOM_OUT = OUTPUT_DIR / 'go-nucleus.sssom.tsv'
MATCHER_TEST_SSSOM_OUT = OUTPUT_DIR / 'matcher-test.sssom.tsv'


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

    def test_sssom(self):
        rule0 = MappingRule(postconditions=Postcondition(weight=1.0))
        rule1 = MappingRule(preconditions=Precondition(subject_match_field_one_of=[HAS_EXACT_SYNONYM],
                                                       object_match_field_one_of=[HAS_EXACT_SYNONYM]),
                            postconditions=Postcondition(predicate_id=SKOS_EXACT_MATCH,
                                                         weight=2.0))
        ruleset = MappingRuleCollection(rules=[rule0, rule1])
        msdf = lexical_index_to_sssom(self.oi, self.lexical_index, ruleset=ruleset)
        with open(TEST_SSSOM_OUT, 'w', encoding='utf-8') as file:
            write_table(msdf, file)

    def test_sssom_with_rules(self):
        resource = OntologyResource(slug=MATCHER_TEST_ONT, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        add_labels_from_uris(oi)
        self.lexical_index = create_lexical_index(oi)
        ruleset  = load_mapping_rules(str(RULES))
        #ruleset = yaml_loader.load(str(RULES), target_class=MappingRuleCollection)
        #ruleset = MappingRuleCollection(rules=[rule0, rule1])
        msdf = lexical_index_to_sssom(self.oi, self.lexical_index, ruleset=ruleset)
        with open(MATCHER_TEST_SSSOM_OUT, 'w', encoding='utf-8') as file:
            write_table(msdf, file)
