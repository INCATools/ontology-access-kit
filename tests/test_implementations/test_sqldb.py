import logging
import shutil
import unittest

from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import yaml_dumper
from semsql.sqla.semsql import Statements
from sqlalchemy import delete

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResultType
from oaklib.datamodels.vocabulary import (
    HAS_PART,
    IS_A,
    LABEL_PREDICATE,
    PART_OF,
    RDF_TYPE,
)
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from oaklib.utilities.lexical.lexical_indexer import add_labels_from_uris
from oaklib.utilities.obograph_utils import graph_as_dict
from tests import (
    CELLULAR_COMPONENT,
    CHEBI_NUCLEUS,
    CYTOPLASM,
    FAKE_ID,
    FAKE_PREDICATE,
    FUNGI,
    HUMAN,
    IMBO,
    INPUT_DIR,
    NUCLEAR_ENVELOPE,
    NUCLEUS,
    OUTPUT_DIR,
    VACUOLE,
)
from tests.test_implementations import ComplianceTester

DB = INPUT_DIR / "go-nucleus.db"
SSN_DB = INPUT_DIR / "ssn.db"
INST_DB = INPUT_DIR / "inst.db"
MUTABLE_DB = OUTPUT_DIR / "go-nucleus.db"
MUTABLE_SSN_DB = OUTPUT_DIR / "ssn.db"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"
VALIDATION_REPORT_OUT = OUTPUT_DIR / "validation-results.tsv"


class TestSqlDatabaseImplementation(unittest.TestCase):
    """Implementation tests for SqlDatabase adapter."""

    def setUp(self) -> None:
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))
        self.oi = oi
        bad_ont = INPUT_DIR / "bad-ontology.db"
        self.bad_oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{bad_ont}"))
        self.ssn_oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{SSN_DB}"))
        self.inst_oi = SqlImplementation(OntologyResource(INST_DB))
        self.compliance_tester = ComplianceTester(self)

    def test_empty_db(self) -> None:
        """Should raise error when connecting to an empty db."""
        res = OntologyResource(slug=f"sqlite:///{str(INPUT_DIR / 'NO_SUCH_FILE')}")
        with self.assertRaises(FileNotFoundError):
            _ = SqlImplementation(res)

    @unittest.skip("Contents of go-nucleus file need to be aligned")
    def test_relationships(self):
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))
        self.compliance_tester.test_relationships(oi, ignore_annotation_edges=False)

    def test_relationships_extra(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map(VACUOLE)
        self.assertCountEqual(rels[IS_A], [IMBO])
        self.assertCountEqual(rels[PART_OF], ["GO:0005737"])
        self.assertCountEqual([IS_A, PART_OF], rels)
        rels = list(oi.outgoing_relationships(VACUOLE))
        self.assertCountEqual([(IS_A, IMBO), (PART_OF, CYTOPLASM)], rels)
        hier_parents = list(oi.hierararchical_parents(VACUOLE))
        self.assertEqual([IMBO], hier_parents)

    def test_instance_graph(self):
        oi = self.inst_oi
        entities = list(oi.entities())
        self.assertEqual(["ex:a", "ex:b", "ex:c", "ex:i1", "ex:j", "ex:p", "ex:test"], entities)
        entities = list(oi.entities(owl_type="owl:Class"))
        self.assertEqual(["ex:a", "ex:b", "ex:c"], entities)
        rels = list(oi.relationships())
        self.assertCountEqual(
            [
                ("ex:b", "ex:p", "ex:a"),
                ("ex:b", "rdfs:subClassOf", "ex:a"),
                ("ex:c", "rdfs:subClassOf", "ex:b"),
                ("ex:i1", "rdf:type", "ex:c"),
                ("ex:i1", "ex:p", "ex:j"),
            ],
            rels,
        )
        rels = list(oi.relationships(include_abox=False))
        self.assertCountEqual(
            [
                ("ex:b", "ex:p", "ex:a"),
                ("ex:b", "rdfs:subClassOf", "ex:a"),
                ("ex:c", "rdfs:subClassOf", "ex:b"),
            ],
            rels,
        )
        rels = list(oi.relationships(include_tbox=False))
        self.assertCountEqual(
            [
                ("ex:i1", "rdf:type", "ex:c"),
                ("ex:i1", "ex:p", "ex:j"),
            ],
            rels,
        )
        rels = list(oi.relationships(predicates=[IS_A, RDF_TYPE]))
        self.assertCountEqual(
            [
                ("ex:b", "rdfs:subClassOf", "ex:a"),
                ("ex:c", "rdfs:subClassOf", "ex:b"),
                ("ex:i1", "rdf:type", "ex:c"),
            ],
            rels,
        )
        rels = list(oi.relationships(subjects=["ex:i1"]))
        self.assertCountEqual(
            [
                ("ex:i1", "rdf:type", "ex:c"),
                ("ex:i1", "ex:p", "ex:j"),
            ],
            rels,
        )
        rels = list(oi.relationships(objects=["ex:a", "ex:c"]))
        self.assertCountEqual(
            [
                ("ex:b", "ex:p", "ex:a"),
                ("ex:b", "rdfs:subClassOf", "ex:a"),
                ("ex:i1", "rdf:type", "ex:c"),
            ],
            rels,
        )

    def test_all_nodes(self):
        for curie in self.oi.entities():
            logging.info(curie)

    def test_labels(self):
        label = self.oi.label(VACUOLE)
        self.assertEqual(label, "vacuole")

    def test_get_labels_for_curies(self):
        oi = self.oi
        curies = oi.subset_members("goslim_generic")
        tups = list(oi.labels(curies))
        for curie, label in tups:
            logging.info(f"{curie} ! {label}")
        assert (VACUOLE, "vacuole") in tups
        assert (CYTOPLASM, "cytoplasm") in tups
        self.assertEqual(11, len(tups))

    def test_synonyms(self):
        syns = self.oi.entity_aliases(CELLULAR_COMPONENT)
        logging.info(syns)
        assert "cellular component" in syns

    def test_mappings(self):
        mappings = list(self.oi.get_sssom_mappings_by_curie(NUCLEUS))
        # for m in mappings:
        #    logging.info(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == "Wikipedia:Cell_nucleus")
        self.assertEqual(len(mappings), 2)
        for m in mappings:
            reverse_mappings = list(self.oi.get_sssom_mappings_by_curie(m.object_id))
            reverse_subject_ids = [m.subject_id for m in reverse_mappings]
            self.assertEqual(reverse_subject_ids, [NUCLEUS])

    def test_relation_graph(self):
        oi = self.oi
        self.assertEqual(
            ["RO:0002131", "RO:0002323", "BFO:0000051", "rdfs:subClassOf", "BFO:0000050"],
            list(oi.entailed_relationships_between(VACUOLE, CELLULAR_COMPONENT)),
        )
        self.assertEqual([IS_A], list(oi.entailed_relationships_between(VACUOLE, VACUOLE)))
        self.assertEqual([], list(oi.entailed_relationships_between(VACUOLE, NUCLEUS)))
        self.assertEqual(
            ["RO:0002323", "RO:0002131", "BFO:0000050"],
            list(oi.entailed_relationships_between(NUCLEAR_ENVELOPE, NUCLEUS)),
        )

    # OboGraphs tests
    def test_obograph_node(self):
        n = self.oi.node(CELLULAR_COMPONENT)
        assert n.id == CELLULAR_COMPONENT
        assert n.lbl == "cellular_component"
        assert n.meta.definition.val.startswith("A location, ")

    # TODO
    def test_obograph_synonyms(self):
        oi = self.oi
        m = oi.synonym_map_for_curies([NUCLEUS, NUCLEAR_ENVELOPE])
        for k, vs in m.items():
            logging.info(k)
            for v in vs:
                logging.info(yaml_dumper.dumps(v))

    def test_obograph(self):
        g = self.oi.ancestor_graph(VACUOLE)
        graph_as_dict(g)
        # logging.info(yaml.dump(obj))
        assert g.nodes
        assert g.edges

    def test_logical_definitions(self):
        eia = "GO:0004857"
        ldefs = list(self.oi.logical_definitions([eia]))
        self.assertEqual(1, len(ldefs))
        ldef = ldefs[0]
        self.assertEqual(eia, ldef.definedClassId)
        self.assertEqual(["GO:0003674"], ldef.genusIds)
        r = obograph.ExistentialRestrictionExpression(
            propertyId="RO:0002212", fillerId="GO:0003824"
        )
        self.assertEqual([r], ldef.restrictions)
        # unionOf logical definitions should NOT be included
        self.assertEqual([], list(self.oi.logical_definitions("NCBITaxon_Union:0000030")))

    def test_descendants(self):
        curies = list(self.oi.descendants(CELLULAR_COMPONENT))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants([CELLULAR_COMPONENT]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants(CELLULAR_COMPONENT, predicates=[IS_A]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A]))
        assert CELLULAR_COMPONENT not in curies
        assert VACUOLE not in curies
        assert CYTOPLASM in curies

    def test_ancestors(self):
        curies = list(self.oi.ancestors(VACUOLE))
        for curie in curies:
            logging.info(curie)
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.ancestors([VACUOLE]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.ancestors(VACUOLE, predicates=[IS_A]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM not in curies

    # QC

    def test_validate(self):
        oi = self.bad_oi
        results = list(oi.validate())
        with open(VALIDATION_REPORT_OUT, "w", encoding="utf-8") as stream:
            writer = StreamingCsvWriter(stream)
            for r in results:
                writer.emit(r)
        invalid_ids = set(
            [r.subject for r in results if str(r.severity) == SeverityOptions.ERROR.text]
        )
        problem_ids = set([r.subject for r in results if str(r.severity)])
        logging.info(f"INVALID: {invalid_ids}")
        logging.info(f"PROBLEM: {problem_ids}")
        assert not any(
            r
            for r in results
            if r.subject == "EXAMPLE:1"
            and str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning
        )
        assert not any(
            r
            for r in results
            if r.subject == "EXAMPLE:8"
            and str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:6"
            and r.predicate == "obo:TEMP#made_up_object_property"
            and str(r.type) == ValidationResultType.ClosedConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:6"
            and r.predicate == "obo:TEMP#made_up_data_property"
            and str(r.type) == ValidationResultType.ClosedConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:1"
            and r.predicate == LABEL_PREDICATE
            and str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:1"
            and r.predicate == "IAO:0000115"
            and str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.WARNING.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:2"
            and r.predicate == LABEL_PREDICATE
            and str(r.type) == ValidationResultType.MaxCountConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:7"
            and r.predicate == "owl:deprecated"
            and str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:8"
            and r.predicate == "skos:exactMatch"
            and str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        assert any(
            r
            for r in results
            if r.subject == "EXAMPLE:9"
            and r.predicate == "rdfs:label"
            and str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning
            and str(r.severity) == SeverityOptions.ERROR.text
        )
        self.assertEqual(6, len(invalid_ids))
        self.assertCountEqual(
            {
                "EXAMPLE:1",
                "EXAMPLE:2",
                "EXAMPLE:8",
                "EXAMPLE:4",
                "EXAMPLE:5",
                "EXAMPLE:7",
                "EXAMPLE:6",
                "EXAMPLE:9",
            },
            problem_ids,
        )

    def test_no_definitions(self):
        missing = list(self.oi.term_curies_without_definitions())
        for curie in missing:
            logging.info(curie)
        assert "CHEBI:36357" in missing
        assert CELLULAR_COMPONENT not in missing

    def test_search_aliases(self):
        config = SearchConfiguration(properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, ["GO:0003824"])
        config = SearchConfiguration()
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, [])
        config = SearchConfiguration(properties=[SearchProperty.ANYTHING])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, ["GO:0003824"])

    def test_search_identifier(self):
        config = SearchConfiguration(
            properties=[SearchProperty.IDENTIFIER], syntax=SearchTermSyntax.STARTS_WITH
        )
        curies = list(self.oi.basic_search("NCBITaxon", config=config))
        self.assertGreater(len(curies), 10)
        for curie in curies:
            assert curie.startswith("NCBITaxon")
        config = SearchConfiguration(
            properties=[SearchProperty.IDENTIFIER], syntax=SearchTermSyntax.REGULAR_EXPRESSION
        )
        curies = list(self.oi.basic_search("^GO:...5773$", config=config))
        self.assertEqual([VACUOLE], curies)

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("cytoplasm", config=config))
        # logging.info(curies)
        self.assertCountEqual([CYTOPLASM], curies)

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        curies = list(self.oi.basic_search("nucl", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_sql(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.SQL)
        curies = list(self.oi.basic_search("%nucl%s", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        self.assertCountEqual([NUCLEUS, CHEBI_NUCLEUS], curies)

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search("nucl", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.oi.basic_search("^nucl.*s$", config=config))
        self.assertCountEqual([NUCLEUS], curies)
        curies = list(self.oi.basic_search("^nucl..s$", config=config))
        self.assertCountEqual([NUCLEUS], curies)
        curies = list(self.oi.basic_search("^nucl.s$", config=config))
        self.assertCountEqual([], curies)
        curies = list(self.oi.basic_search("nucl.*s", config=config))
        self.assertCountEqual([NUCLEUS, CHEBI_NUCLEUS], curies)
        curies = list(self.oi.basic_search("nucl.*", config=config))
        self.assertIn(NUCLEUS, curies)
        self.assertIn(CHEBI_NUCLEUS, curies)
        self.assertGreater(len(curies), 5)
        with self.assertRaises(NotImplementedError):
            list(self.oi.basic_search("(a|b)", config=config))

    def test_multiset_mrcas(self):
        oi = self.oi
        orig_exclude_owl_top_and_bottom = oi.exclude_owl_top_and_bottom
        oi.exclude_owl_top_and_bottom = False
        results = oi.multiset_most_recent_common_ancestors(
            [NUCLEUS, VACUOLE, NUCLEAR_ENVELOPE, FUNGI], predicates=[IS_A, PART_OF], asymmetric=True
        )
        results = list(results)
        expected = [
            ("GO:0005635", "GO:0005773", "GO:0043231"),
            ("GO:0005634", "NCBITaxon:4751", "owl:Thing"),
            ("GO:0005635", "NCBITaxon:4751", "owl:Thing"),
            ("GO:0005634", "GO:0005635", "GO:0005634"),
            ("GO:0005773", "NCBITaxon:4751", "owl:Thing"),
            ("GO:0005634", "GO:0005773", "GO:0043231"),
        ]
        oi.exclude_owl_top_and_bottom = orig_exclude_owl_top_and_bottom
        self.assertCountEqual(expected, list(results))
        for s, o, lca in expected:
            results = list(oi.most_recent_common_ancestors(s, o, predicates=[IS_A, PART_OF]))
            # logging.info(f'{s} {o} == {results}')
            self.assertEqual([lca], results)

    def test_store_associations(self):
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        oi.autosave = True
        self.compliance_tester.test_store_associations(oi)

    def test_gap_fill(self):
        # TODO: improve performance
        oi = self.oi
        # note that HUMAN will be deselected as it is a singleton in the is-a/part-of graph
        rels = list(
            oi.gap_fill_relationships(
                [NUCLEUS, VACUOLE, CELLULAR_COMPONENT, HUMAN], predicates=[IS_A, PART_OF]
            )
        )
        self.assertEqual(len(rels), 4)
        self.assertCountEqual(
            rels,
            [
                ("GO:0005773", "rdfs:subClassOf", "GO:0005575"),
                ("GO:0005634", "rdfs:subClassOf", "GO:0005575"),
                ("GO:0005773", "BFO:0000050", "GO:0005575"),
                ("GO:0005634", "BFO:0000050", "GO:0005575"),
            ],
        )
        # include has-part
        rels = list(
            oi.gap_fill_relationships(
                [NUCLEUS, VACUOLE, CELLULAR_COMPONENT, HUMAN], predicates=[IS_A, PART_OF, HAS_PART]
            )
        )
        self.assertEqual(len(rels), 6)
        self.assertCountEqual(
            rels,
            [
                ("GO:0005773", "rdfs:subClassOf", "GO:0005575"),
                ("GO:0005634", "rdfs:subClassOf", "GO:0005575"),
                ("GO:0005773", "BFO:0000050", "GO:0005575"),
                ("GO:0005634", "BFO:0000050", "GO:0005575"),
                ("GO:0005773", "BFO:0000051", "GO:0005575"),
                ("GO:0005634", "BFO:0000051", "GO:0005575"),
            ],
        )
        # is-a graph of siblings makes singletons
        rels = list(
            oi.gap_fill_relationships(
                [NUCLEUS, VACUOLE, HUMAN], predicates=[IS_A, PART_OF, HAS_PART]
            )
        )
        self.assertEqual(len(rels), 0)
        # trivial edge case - subset using all terms and all predicates
        rels = list(oi.gap_fill_relationships(list(oi.entities())))
        all_rels = list(oi.all_relationships())
        # self.assertEqual(len(rels), len(all_rels))
        for rel in rels:
            if rel not in all_rels:
                logging.info(rel)

    def test_set_label(self):
        """
        Tests the SQL store can be modified

        """
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        oi.autosave = True
        label = oi.label(VACUOLE)
        self.assertEqual("vacuole", label)
        oi.set_label(VACUOLE, "foo")
        label = oi.label(VACUOLE)
        self.assertEqual("foo", label)
        # oi.save()
        oi.autosave = False
        label = oi.label(VACUOLE)
        self.assertEqual("foo", label)
        oi.set_label(NUCLEUS, "bar")
        oi.set_label(NUCLEAR_ENVELOPE, "baz")
        self.assertNotEqual("bar", oi.label(NUCLEUS))
        self.assertNotEqual("baz", oi.label(NUCLEAR_ENVELOPE))
        oi.save()
        self.assertEqual("bar", oi.label(NUCLEUS))
        self.assertEqual("baz", oi.label(NUCLEAR_ENVELOPE))
        # get a fresh copy to ensure changes have persisted
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        self.assertEqual("bar", oi.label(NUCLEUS))
        self.assertEqual("baz", oi.label(NUCLEAR_ENVELOPE))

    def test_set_labels_from_iris(self):
        """
        Test ability to generate labels for a semweb-style ontology
        """
        shutil.copyfile(SSN_DB, MUTABLE_SSN_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_SSN_DB}"))
        no_label_curies = []
        for curie in oi.entities():
            label = oi.label(curie)
            # logging.info(f'{curie}: {label}')
            if label is None:
                no_label_curies.append(curie)
        self.assertGreater(len(no_label_curies), 4)
        oi.autosave = False
        add_labels_from_uris(oi)
        oi.save()
        for curie in no_label_curies:
            label = oi.label(curie)
            # TODO
            # logging.info(f'XXX {curie}: {label}')
            # self.assertIsNotNone(label)

    def test_migrate_curies(self):
        """
        Tests migrate_curies operations works on a SQL backend

        This test is a mutation test, so a copy of the test database will be made
        """
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        label = oi.label(NUCLEUS)
        preds = [IS_A, PART_OF]
        preds2 = [IS_A, FAKE_PREDICATE]
        ancestors = list(oi.ancestors(NUCLEUS, predicates=preds))
        descendants = list(oi.descendants(NUCLEUS, predicates=preds))

        def non_reflexive(anc):
            return [a for a in ancestors if a != NUCLEUS]

        expected_ancs = non_reflexive(ancestors)
        descendants_ancs = non_reflexive(descendants)
        oi.migrate_curies({NUCLEUS: FAKE_ID, PART_OF: FAKE_PREDICATE})
        oi.save()
        self.assertEqual(label, oi.label(FAKE_ID))
        self.assertIsNone(oi.label(NUCLEUS))
        self.assertCountEqual(
            expected_ancs, non_reflexive(oi.ancestors(FAKE_ID, predicates=preds2))
        )
        self.assertCountEqual([], list(oi.ancestors(NUCLEUS, predicates=preds)))
        self.assertCountEqual(
            descendants_ancs, non_reflexive(oi.descendants(FAKE_ID, predicates=preds2))
        )
        self.assertCountEqual([], list(oi.descendants(NUCLEUS, predicates=preds)))

    def test_statements_with_annotations(self):
        oi = self.oi
        for curie in oi.entities():
            for ax in oi.statements_with_annotations(curie):
                logging.info(yaml_dumper.dumps(ax))
        for ax in oi.statements_with_annotations(NUCLEUS):
            logging.info(yaml_dumper.dumps(ax))

    def test_patcher(self):
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        # oi.autosave = True
        oi.apply_patch(kgcl.NodeObsoletion(id=generate_change_id(), about_node=NUCLEUS))
        # with self.assertRaises(ValueError) as e:
        #    oi.apply_patch(kgcl.NodeObsoletion(id='x', about_node='NO SUCH TERM'))
        oi.apply_patch(kgcl.NodeDeletion(id=generate_change_id(), about_node=VACUOLE))
        oi.apply_patch(
            kgcl.NewSynonym(
                id=generate_change_id(),
                about_node=NUCLEAR_ENVELOPE,
                new_value="envelope of nucleus",
            )
        )
        oi.apply_patch(
            kgcl.EdgeCreation(
                id=generate_change_id(), subject=NUCLEUS, predicate=IS_A, object=CELLULAR_COMPONENT
            )
        )
        oi.apply_patch(
            kgcl.EdgeDeletion(id=generate_change_id(), subject=NUCLEUS, predicate=IS_A, object=IMBO)
        )
        # oi.apply_patch(kgcl.NameBecomesSynonym(id=generate_change_id(),
        #                                       about_node=NUCLEAR_ENVELOPE,
        #                                       change_1=kgcl.NodeRename(id='FIXME-1',
        #                                                                )))
        oi.save()
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        obs = list(oi.obsoletes())
        self.assertIn(NUCLEUS, obs)
        self.assertIsNone(oi.label(VACUOLE))
        self.assertIn("envelope of nucleus", oi.entity_aliases(NUCLEAR_ENVELOPE))
        self.assertIn(CELLULAR_COMPONENT, oi.outgoing_relationship_map(NUCLEUS)[IS_A])
        self.assertNotIn(IMBO, oi.outgoing_relationship_map(NUCLEUS)[IS_A])

    def test_sqla_write(self):
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        session = oi.session
        # session.autoflush = True
        rows = list(session.query(Statements))
        # for row in rows:
        #    logging.info(row)
        self.assertGreater(len(rows), 0)
        stmt = delete(Statements)
        session.execute(stmt)
        session.commit()
        logging.info(f"D={session.dirty}")
        rows = list(session.query(Statements))
        for row in rows:
            logging.info(row)
        self.assertEqual([], rows)
        session.commit()
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{MUTABLE_DB}"))
        session = oi.session
        rows = list(session.query(Statements))
        for row in rows:
            logging.info(row)
        self.assertEqual([], rows)

    # SemSim

    def test_information_content_scores(self):
        self.compliance_tester.test_information_content_scores(self.oi, False)

    def test_common_ancestors(self):
        self.compliance_tester.test_common_ancestors(self.oi)

    def test_pairwise_similarity(self):
        self.compliance_tester.test_pairwise_similarity(self.oi)
