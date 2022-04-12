import unittest
from pathlib import Path

from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    add_labels_from_uris, load_mapping_rules
from oaklib.datamodels.mapping_rules_datamodel import MappingRuleCollection, MappingRule, Precondition, Postcondition
from oaklib.datamodels.vocabulary import IS_A, HAS_EXACT_SYNONYM, SKOS_EXACT_MATCH
from sssom.writers import write_table

from tests import OUTPUT_DIR, INPUT_DIR

RULES = INPUT_DIR / 'matcher_rules.yaml'
MATCHER_TEST_ONT = INPUT_DIR / 'matcher-test.owl'
MATCHER_TEST_DB = INPUT_DIR / 'matcher-test.db'
TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.lexical.yaml'
TEST_OUT_INDEX_DB = OUTPUT_DIR / 'go-nucleus.db.lexical.yaml'
TEST_SSSOM_OUT = OUTPUT_DIR / 'go-nucleus.sssom.tsv'
TEST_SSSOM_OUT_FROM_DB = OUTPUT_DIR / 'go-nucleus.sssom.db.tsv'
MATCHER_TEST_SSSOM_OUT = OUTPUT_DIR / 'matcher-test.sssom.tsv'


class TestLexicalIndex(unittest.TestCase):

    def setUp(self) -> None:
        resource = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi

    def test_sssom(self):
        lexical_index = create_lexical_index(self.oi)
        rule0 = MappingRule(postconditions=Postcondition(weight=1.0))
        rule1 = MappingRule(preconditions=Precondition(subject_match_field_one_of=[HAS_EXACT_SYNONYM],
                                                       object_match_field_one_of=[HAS_EXACT_SYNONYM]),
                            postconditions=Postcondition(predicate_id=SKOS_EXACT_MATCH,
                                                         weight=2.0))
        ruleset = MappingRuleCollection(rules=[rule0, rule1])
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset)
        with open(TEST_SSSOM_OUT, 'w', encoding='utf-8') as file:
            write_table(msdf, file)

    def test_sssom_with_rules_file(self):
        resource = OntologyResource(slug=MATCHER_TEST_ONT, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        lexical_index = create_lexical_index(oi)
        add_labels_from_uris(oi)
        ruleset = load_mapping_rules(str(RULES))
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset)
        with open(MATCHER_TEST_SSSOM_OUT, 'w', encoding='utf-8') as file:
            write_table(msdf, file)

    def test_sssom_with_rules_sqlite(self):
        resource = OntologyResource(slug=f'sqlite:///{Path(MATCHER_TEST_DB).absolute()}')
        oi = SqlImplementation(resource)
        self.oi = oi
        #add_labels_from_uris(oi)
        lexical_index = create_lexical_index(oi)
        self.assertGreater(len(lexical_index.groupings), 10)
        save_lexical_index(lexical_index, TEST_OUT_INDEX_DB)
        ruleset = load_mapping_rules(str(RULES))
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset)
        with open(TEST_SSSOM_OUT_FROM_DB, 'w', encoding='utf-8') as file:
            write_table(msdf, file)
