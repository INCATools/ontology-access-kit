import unittest
from pathlib import Path

from sssom.io import get_metadata_and_prefix_map
from sssom.writers import write_table

from oaklib.datamodels.mapping_rules_datamodel import (
    MappingRule,
    MappingRuleCollection,
    Postcondition,
    Precondition,
)
from oaklib.datamodels.vocabulary import HAS_EXACT_SYNONYM, SKOS_EXACT_MATCH
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import (
    add_labels_from_uris,
    create_lexical_index,
    lexical_index_to_sssom,
    load_mapping_rules,
    save_lexical_index,
)
from tests import INPUT_DIR, OUTPUT_DIR

RULES = INPUT_DIR / "matcher_rules.yaml"
MATCHER_TEST_ONT = INPUT_DIR / "matcher-test.owl"
MATCHER_TEST_DB = INPUT_DIR / "matcher-test.db"
MATCHER_META_YML = INPUT_DIR / "matcher-meta.yaml"
TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.lexical.yaml"
TEST_OUT_INDEX_DB = OUTPUT_DIR / "go-nucleus.db.lexical.yaml"
TEST_SSSOM_OUT = OUTPUT_DIR / "go-nucleus.sssom.tsv"
TEST_SSSOM_OUT_FROM_DB = OUTPUT_DIR / "go-nucleus.sssom.db.tsv"
MATCHER_TEST_SSSOM_OUT = OUTPUT_DIR / "matcher-test.sssom.tsv"


class TestLexicalIndex(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        self.oi = ProntoImplementation(resource)
        self.sparql_oi = SparqlImplementation(
            OntologyResource(slug="go-nucleus.owl.ttl", directory=INPUT_DIR, local=True)
        )
        self.ois = [self.oi, self.sparql_oi]

    def test_sssom(self):
        for oi in self.ois:
            lexical_index = create_lexical_index(oi)
            rule0 = MappingRule(postconditions=Postcondition(weight=1.0))
            rule1 = MappingRule(
                preconditions=Precondition(
                    subject_match_field_one_of=[HAS_EXACT_SYNONYM],
                    object_match_field_one_of=[HAS_EXACT_SYNONYM],
                ),
                postconditions=Postcondition(predicate_id=SKOS_EXACT_MATCH, weight=2.0),
            )
            ruleset = MappingRuleCollection(rules=[rule0, rule1])
            msdf = lexical_index_to_sssom(oi, lexical_index, ruleset=ruleset)
            with open(TEST_SSSOM_OUT, "w", encoding="utf-8") as file:
                write_table(msdf, file)

    def test_sssom_with_rules_file(self):
        resource = OntologyResource(slug=MATCHER_TEST_ONT, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        lexical_index = create_lexical_index(oi)
        add_labels_from_uris(oi)
        ruleset = load_mapping_rules(str(RULES))
        metadata = get_metadata_and_prefix_map(MATCHER_META_YML)
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset, meta=metadata)
        with open(MATCHER_TEST_SSSOM_OUT, "w", encoding="utf-8") as file:
            write_table(msdf, file)

    def test_sssom_with_rules_sqlite(self):
        resource = OntologyResource(slug=f"sqlite:///{Path(MATCHER_TEST_DB).absolute()}")
        oi = SqlImplementation(resource)
        self.oi = oi
        # add_labels_from_uris(oi)
        lexical_index = create_lexical_index(oi)
        self.assertGreater(len(lexical_index.groupings), 10)
        save_lexical_index(lexical_index, TEST_OUT_INDEX_DB)
        ruleset = load_mapping_rules(str(RULES))
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset)
        with open(TEST_SSSOM_OUT_FROM_DB, "w", encoding="utf-8") as file:
            write_table(msdf, file)
