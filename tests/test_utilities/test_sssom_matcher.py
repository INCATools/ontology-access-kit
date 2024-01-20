import unittest
from pathlib import Path

import yaml
from sssom.parsers import to_mapping_set_document
from sssom.writers import write_table
from sssom_schema import Mapping

from oaklib import get_adapter
from oaklib.datamodels.cross_ontology_diff import EntityReference
from oaklib.datamodels.mapping_rules_datamodel import (
    MappingRule,
    MappingRuleCollection,
    Postcondition,
    Precondition,
)
from oaklib.datamodels.vocabulary import (
    HAS_BROAD_SYNONYM,
    HAS_DBXREF,
    HAS_EXACT_SYNONYM,
    HAS_RELATED_SYNONYM,
    IS_A,
    SEMAPV,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import (
    add_labels_from_uris,
    create_lexical_index,
    lexical_index_to_sssom,
    load_mapping_rules,
    precondition_holds,
    save_lexical_index,
)
from tests import (
    CELL_CORTEX,
    CELL_PERIPHERY,
    CELLULAR_COMPONENT,
    INPUT_DIR,
    OUTPUT_DIR,
    PHOTOSYNTHETIC_MEMBRANE,
    THYLAKOID,
    object_is_subsumed_by_member_of,
)

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

    def test_sssom_with_subset(self):
        """
        Tests using lexmatch where only a subset is attempted to be matched.

        Use cases here include matching certain branches or inclusion lists
        """
        for oi in self.ois:
            lexical_index = create_lexical_index(oi)
            entities = list(oi.descendants([CELLULAR_COMPONENT], predicates=[IS_A]))
            msdf = lexical_index_to_sssom(oi, lexical_index, subjects=entities, objects=entities)
            msdoc = to_mapping_set_document(msdf)
            cases = [
                Mapping(
                    subject_id=CELL_CORTEX,
                    object_id=CELL_PERIPHERY,
                    predicate_id=SKOS_CLOSE_MATCH,
                    mapping_justification=EntityReference(SEMAPV.LexicalMatching.value),
                ),
                Mapping(
                    subject_id=THYLAKOID,
                    object_id=PHOTOSYNTHETIC_MEMBRANE,
                    predicate_id=SKOS_CLOSE_MATCH,
                    mapping_justification=EntityReference(SEMAPV.LexicalMatching.value),
                ),
            ]
            # for m in msdoc.mapping_set.mappings:
            #    print(m)
            self.assertEqual(2, len(msdoc.mapping_set.mappings))
            for c in cases:
                self.assertTrue(
                    object_is_subsumed_by_member_of(c, msdoc.mapping_set.mappings),
                    f"mapping not found: {c}",
                )
            with open(TEST_SSSOM_OUT, "w", encoding="utf-8") as file:
                write_table(msdf, file)

    def test_rules(self):
        m1 = Mapping(
            subject_id=CELL_CORTEX,
            object_id=CELL_PERIPHERY,
            predicate_id=SKOS_CLOSE_MATCH,
            mapping_justification=EntityReference(SEMAPV.LexicalMatching.value),
            subject_match_field=HAS_EXACT_SYNONYM,
            object_match_field=HAS_RELATED_SYNONYM,
        )
        cases = [
            (
                m1,
                MappingRule(
                    preconditions=Precondition(subject_match_field_one_of=[HAS_EXACT_SYNONYM])
                ),
                True,
            ),
            (
                m1,
                MappingRule(
                    preconditions=Precondition(subject_match_field_one_of=[HAS_RELATED_SYNONYM])
                ),
                False,
            ),
            (
                m1,
                MappingRule(
                    preconditions=Precondition(
                        subject_match_field_one_of=[HAS_EXACT_SYNONYM, HAS_RELATED_SYNONYM]
                    )
                ),
                True,
            ),
            (m1, MappingRule(preconditions=Precondition()), True),
        ]
        for m, rule, expected_true in cases:
            self.assertEqual(
                precondition_holds(rule.preconditions, m),
                expected_true,
                f"precondition {rule.preconditions} not met for {m}",
            )

    def test_sssom_with_rules_file(self):
        resource = OntologyResource(slug=MATCHER_TEST_ONT, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        lexical_index = create_lexical_index(oi)
        add_labels_from_uris(oi)
        ruleset = load_mapping_rules(str(RULES))
        metadata = yaml.safe_load(MATCHER_META_YML.read_text())
        msdf = lexical_index_to_sssom(self.oi, lexical_index, ruleset=ruleset, meta=metadata)
        with open(MATCHER_TEST_SSSOM_OUT, "w", encoding="utf-8") as file:
            write_table(msdf, file)
        msdoc = to_mapping_set_document(msdf)
        cases = [
            Mapping(
                subject_id="http://example.org/x/bone_element",
                object_id="http://example.org/z/bone_tissue",
                predicate_id=SKOS_CLOSE_MATCH,
                confidence=0.5,
                subject_match_field=HAS_BROAD_SYNONYM,
                object_match_field=HAS_BROAD_SYNONYM,
                mapping_justification=EntityReference(SEMAPV.LexicalMatching.value),
            ),
            # the rules file scores xref matches HIGH
            Mapping(
                subject_id="http://example.org/y/lung",
                object_id="http://example.org/z/lung",
                predicate_id=SKOS_EXACT_MATCH,
                confidence=0.94,
                subject_match_field=HAS_DBXREF,
                object_match_field=HAS_DBXREF,
                mapping_justification=EntityReference(SEMAPV.LexicalMatching.value),
            ),
        ]
        # for m in msdoc.mapping_set.mappings:
        #    print(m)
        self.assertEqual(42, len(msdoc.mapping_set.mappings))
        for c in cases:
            self.assertTrue(
                object_is_subsumed_by_member_of(c, msdoc.mapping_set.mappings, float_abs_tol=0.01),
                f"mapping not found: {c}",
            )

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

    def test_three_way_alignment(self):
        """
        Tests using an intermediate ontology to align two ontologies.

        See `<https://github.com/INCATools/ontology-access-kit/issues/585>_`
        """
        base_name = "three-way-mapping"
        base_dir = INPUT_DIR / base_name
        expected = [
            {
                "subject_id": "FBbt:1",
                "predicate_id": "skos:closeMatch",
                "object_id": "ZFA:1",
                "mapping_justification": "semapv:LexicalMatching",
                "subject_label": "fbbt1",
                "object_label": "zfa1",
                "mapping_tool": "oaklib",
                "confidence": 0.5,
                "subject_match_field": ["oio:hasDbXref-INVERSE"],
                "object_match_field": ["oio:hasDbXref"],
                "match_string": ["cl:1"],
            },
            {
                "subject_id": "FBbt:2",
                "predicate_id": "skos:closeMatch",
                "object_id": "ZFA:2",
                "mapping_justification": "semapv:LexicalMatching",
                "subject_label": "fbbt2",
                "object_label": "zfa2",
                "mapping_tool": "oaklib",
                "confidence": 0.5,
                "subject_match_field": ["oio:hasDbXref-INVERSE"],
                "object_match_field": ["oio:hasDbXref-INVERSE"],
                "match_string": ["uberon:2"],
            },
            {
                "subject_id": "FBbt:3",
                "predicate_id": "skos:closeMatch",
                "object_id": "ZFA:3",
                "mapping_justification": "semapv:LexicalMatching",
                "subject_label": "fbbt3",
                "object_label": "zfa3",
                "mapping_tool": "oaklib",
                "confidence": 0.5,
                "subject_match_field": ["rdf:ID"],
                "object_match_field": ["oio:hasDbXref-INVERSE"],
                "match_string": ["fbbt:3"],
            },
            {
                "subject_id": "FBbt:4",
                "predicate_id": "skos:closeMatch",
                "object_id": "ZFA:4",
                "mapping_justification": "semapv:LexicalMatching",
                "subject_label": "fbbt4",
                "object_label": "zfa4",
                "mapping_tool": "oaklib",
                "confidence": 0.5,
                "subject_match_field": ["oio:hasDbXref-INVERSE"],
                "object_match_field": ["rdf:ID"],
                "match_string": ["zfa:4"],
            },
            {
                "subject_id": "FBbt:5",
                "predicate_id": "skos:closeMatch",
                "object_id": "ZFA:5",
                "mapping_justification": "semapv:LexicalMatching",
                "subject_label": "fbbt5",
                "object_label": "zfa5",
                "mapping_tool": "oaklib",
                "confidence": 0.5,
                "subject_match_field": ["skos:exactMatch"],
                "object_match_field": ["skos:exactMatch"],
                "match_string": ["caro:5"],
            },
        ]

        def _as_dict(m: Mapping) -> dict:
            return {k: v for k, v in m.__dict__.items() if not k.startswith("_") and v}

        import sssom.writers as sssom_writers

        for pfx, sfx in [("", ".obo"), ("", ".owl.ttl")]:
            adapter = get_adapter(f"{pfx}{base_dir}{sfx}")
            li = create_lexical_index(adapter)
            subjects = [f"FBbt:{i}" for i in range(1, 6)]
            objects = [f"ZFA:{i}" for i in range(1, 6)]
            msdf = lexical_index_to_sssom(adapter, li, subjects=subjects, objects=objects)
            msdoc = to_mapping_set_document(msdf)
            output = str(OUTPUT_DIR / f"{base_name}-from-{sfx}.sssom.tsv")
            with open(output, "w", encoding="utf-8") as file:
                sssom_writers.write_table(msdf, file)
            mappings = [_as_dict(m) for m in msdoc.mapping_set.mappings]
            print(mappings)
            self.assertCountEqual(expected, mappings)
