import logging
import shutil
import unittest

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import HAS_DBXREF, IS_A, PART_OF, RDF_TYPE
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.mappers.ontology_metadata_mapper import OntologyMetadataMapper
from oaklib.resource import OntologyResource
from oaklib.selector import get_adapter
from oaklib.utilities.obograph_utils import (
    graph_as_dict,
    index_graph_edges_by_object,
    index_graph_edges_by_predicate,
    index_graph_edges_by_subject,
    index_graph_nodes,
)
from tests import (
    CATALYTIC_ACTIVITY,
    CELL_CORTEX,
    CELLULAR_COMPONENT,
    CYTOPLASM,
    DIGIT,
    FAKE_ID,
    FAKE_PREDICATE,
    INPUT_DIR,
    NUCLEAR_ENVELOPE,
    NUCLEUS,
    OUTPUT_DIR,
    SHAPE,
    VACUOLE,
)
from tests.test_implementations import ComplianceTester

TEST_RDF = INPUT_DIR / "go-nucleus.owl.ttl"
INTERNEURON_RDF = INPUT_DIR / "interneuron.owl.ttl"
TEST_INST_RDF = INPUT_DIR / "inst.owl.ttl"
TEST_MUTABLE_RDF = OUTPUT_DIR / "go-nucleus.owl.ttl"
TEST_IMPORTER = INPUT_DIR / "test_import_root.owl"


class TestSparqlImplementation(unittest.TestCase):
    def setUp(self) -> None:
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_RDF)))
        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi, ignore_annotation_edges=True)

    def test_sssom_mappings(self):
        self.compliance_tester.test_sssom_mappings(self.oi)

    def test_relationships_extra(self):
        oi = self.oi
        self.assertIsNotNone(oi.graph)
        rels = list(oi.outgoing_relationships(VACUOLE))
        self.assertEqual(2, len(rels))
        rels = oi.outgoing_relationship_map(VACUOLE)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertIn("GO:0043231", rels[IS_A])
        self.assertIn("GO:0005737", rels[PART_OF])
        rels = oi.outgoing_relationship_map(NUCLEUS)

    def test_instance_graph(self):
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_INST_RDF)))
        self.assertIsNotNone(oi.graph)
        entities = list(oi.entities())
        self.assertEqual(
            [
                "http://example.org/test",
                "http://example.org/p",
                "http://example.org/a",
                "http://example.org/b",
                "http://example.org/c",
                "http://example.org/i1",
                "http://example.org/i2",
                "http://example.org/j",
            ],
            entities,
        )
        expected = [
            ("http://example.org/i1", "http://example.org/p", "http://example.org/j"),
            ("http://example.org/i2", "http://example.org/p", "http://example.org/a"),
            ("http://example.org/i1", RDF_TYPE, "http://example.org/c"),
            ("http://example.org/b", IS_A, "http://example.org/a"),
        ]
        for curie in oi.entities():
            rels = oi.outgoing_relationships(curie)
            for k, v in rels:
                t = (curie, k, v)
                if t in expected:
                    expected.remove(t)
        self.assertEqual([], expected)
        rels = list(oi.relationships())
        self.assertCountEqual(
            [
                ("http://example.org/b", "rdfs:subClassOf", "http://example.org/a"),
                ("http://example.org/b", "http://example.org/p", "http://example.org/a"),
                ("http://example.org/c", "rdfs:subClassOf", "http://example.org/b"),
                ("http://example.org/i1", "http://example.org/p", "http://example.org/j"),
                ("http://example.org/i1", "rdf:type", "http://example.org/c"),
                ("http://example.org/i2", "http://example.org/p", "http://example.org/a"),
            ],
            rels,
        )

    def test_parents(self):
        parents = self.oi.hierarchical_parents(VACUOLE)
        # logging.info(parents)
        assert "GO:0043231" in parents

    def test_labels(self):
        """Standard label compliance test."""
        self.compliance_tester.test_labels(self.oi)

    def test_skos_profile(self):
        """
        Tests that vocabularies that uses the skos vocabulary works as expected.

        This makes use of a skos profile, which is a mapping from OMO
        properties to SKOS
        """
        soil_oi = get_adapter(str(INPUT_DIR / "soil-profile.skos.nt"))
        soil_oi.prefix_map()["soilprofile"] = "http://anzsoil.org/def/au/asls/soil-profile/"
        soil_oi.ontology_metamodel_mapper = OntologyMetadataMapper(
            [], curie_converter=soil_oi.converter
        )
        soil_oi.ontology_metamodel_mapper.use_skos_profile()
        self.assertEqual(
            ["skos:prefLabel"], soil_oi.ontology_metamodel_mapper.map_curie("rdfs:label")
        )
        self.assertEqual("skos:prefLabel", soil_oi.ontology_metamodel_mapper.label_curie())
        soil_oi.multilingual = True
        self.assertTrue(soil_oi.multilingual)
        soil_oi.preferred_language = "en"
        label_cases = [
            ("soilprofile:voids", "Voids"),
            ("soilprofile:soil-water-regime", "Soil water regime"),
        ]
        elabels = list(soil_oi.labels(soil_oi.entities()))
        for curie, label in label_cases:
            self.assertIn((curie, label), elabels)
            self.assertEqual(label, soil_oi.label(curie))
            config = SearchConfiguration(is_partial=False, properties=[SearchProperty.LABEL])
            curies = list(soil_oi.basic_search(label, config=config))
            self.assertEqual([curie], curies)
            # TODO:
            # self.assertEqual([curie], soil_oi.curies_by_label(label))
        tdef = soil_oi.definition("soilprofile:voids-cracks")
        self.assertEqual("Planar voids", tdef)

    @unittest.skip("TODO")
    def test_subontology(self):
        oi = self.oi
        self.assertIsNotNone(oi.named_graph)
        label = oi.label(DIGIT)
        self.assertIsNone(label)
        # logging.info(label)
        # self.assertEqual(label, 'digit')
        self.assertEqual("shape", oi.label(SHAPE))

    def test_dump(self):
        OUTPUT_DIR.mkdir(exist_ok=True)
        self.oi.dump(TEST_MUTABLE_RDF, "ttl")

    @unittest.skip("TODO")
    def test_set_label(self):
        self.oi.set_label(NUCLEUS, "foo")
        OUTPUT_DIR.mkdir(exist_ok=True)
        self.oi.dump(TEST_MUTABLE_RDF, "ttl")

    def test_synonyms(self):
        syns = self.oi.entity_aliases(CELLULAR_COMPONENT)
        logging.info(syns)
        assert "cellular component" in syns
        assert "cellular_component" in syns
        syns = self.oi.entity_aliases(NUCLEUS)
        logging.info(syns)
        self.assertCountEqual(syns, ["nucleus", "cell nucleus", "horsetail nucleus"])
        syn_pairs = list(self.oi.entity_alias_map(NUCLEUS).items())
        self.assertCountEqual(
            syn_pairs,
            [
                ("oio:hasExactSynonym", ["cell nucleus"]),
                ("oio:hasNarrowSynonym", ["horsetail nucleus"]),
                ("rdfs:label", ["nucleus"]),
            ],
        )

    def test_all_entity_curies(self):
        curies = list(self.oi.entities())
        self.assertGreater(len(curies), 100)
        self.assertIn(NUCLEUS, curies)

    def test_definition(self):
        defn = self.oi.definition(CELLULAR_COMPONENT)
        assert defn.startswith("A location, relative to cellular compartments")

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("nucleus", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.LABEL])
        curies = list(self.oi.basic_search("nucleus", config=config))
        assert NUCLEUS in curies
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        assert curies == []
        config = SearchConfiguration(is_partial=False, properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        assert CATALYTIC_ACTIVITY in curies

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        # non-exact matches across all ontobee are slow: restrict to pato
        curies = list(self.oi.basic_search("ucl", config=config))
        # logging.info(curies)
        self.assertGreater(len(curies), 1)
        assert NUCLEUS in curies

    def test_obograph(self):
        g = self.oi.ancestor_graph(VACUOLE)
        nix = index_graph_nodes(g)
        self.assertEqual(nix[VACUOLE].lbl, "vacuole")
        v2c = obograph.Edge(sub=VACUOLE, pred=PART_OF, obj=CYTOPLASM)
        six = index_graph_edges_by_subject(g)
        self.assertIn(v2c, six[VACUOLE])
        self.assertNotIn(v2c, six[CYTOPLASM])
        oix = index_graph_edges_by_object(g)
        self.assertIn(v2c, oix[CYTOPLASM])
        self.assertNotIn(v2c, oix[VACUOLE])
        pix = index_graph_edges_by_predicate(g)
        self.assertIn(v2c, pix[PART_OF])
        self.assertNotIn(v2c, pix[IS_A])
        graph_as_dict(g)
        assert "nodes" in g
        assert "edges" in g
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == VACUOLE]))
        ancs = list(self.oi.ancestors(VACUOLE, predicates=[IS_A, PART_OF]))
        assert VACUOLE in ancs
        assert CYTOPLASM in ancs

    def test_descendants(self):
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A, PART_OF]))
        self.assertIn(VACUOLE, descs)
        self.assertIn(CYTOPLASM, descs)
        self.assertIn(CELL_CORTEX, descs)
        for desc in descs:
            self.assertIn(CYTOPLASM, list(self.oi.ancestors(desc, predicates=[IS_A, PART_OF])))
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[PART_OF]))
        self.assertIn(VACUOLE, descs)
        self.assertIn(CYTOPLASM, descs)
        self.assertNotIn(CELL_CORTEX, descs)
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A]))
        self.assertNotIn(VACUOLE, descs)
        self.assertIn(CYTOPLASM, descs)
        self.assertIn(CELL_CORTEX, descs)
        self.assertEqual([NUCLEUS], list(self.oi.descendants(NUCLEUS, predicates=[IS_A])))

    @unittest.skip("node metadata not yet implemented")
    def test_extract_graph(self):
        self.compliance_tester.test_extract_graph(self.oi)

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.subsets())
        self.assertIn("goslim_generic", subsets)
        self.assertIn(NUCLEUS, list(oi.subset_members("goslim_generic")))
        self.assertIn((NUCLEUS, "goslim_generic"), list(oi.terms_subsets([NUCLEUS])))
        with self.assertRaises(ValueError):
            list(oi.subset_members("no_such_subset"))

    def test_node_type(self):
        self.assertEqual("CLASS", self.oi.node(NUCLEUS).type)
        self.assertEqual("PROPERTY", self.oi.node(PART_OF).type)

    def test_ontology_metadata(self):
        oi = self.oi
        ontologies = list(oi.ontologies())
        self.assertEqual(1, len(ontologies))
        m = oi.ontology_metadata_map(ontologies[0])
        self.assertIn("rdf:type", m)

    def test_summary_statistics(self):
        """
        Tests summary statistics computed with aggregate queries.

        Expected values were checked against direct counts over the RDF graph.
        """
        oi = self.oi
        stats = oi.branch_summary_statistics()
        self.assertEqual(204, stats.class_count)
        self.assertEqual(28, stats.deprecated_class_count)
        self.assertEqual(176, stats.non_deprecated_class_count)
        self.assertEqual(98, stats.class_count_with_text_definitions)
        self.assertEqual(4262, stats.rdf_triple_count)
        self.assertEqual(336, stats.subclass_of_axiom_count)
        self.assertEqual(63, stats.equivalent_classes_axiom_count)
        self.assertEqual(16, stats.subset_count)
        self.assertEqual(269, stats.synonym_statement_count)
        self.assertEqual(260, stats.distinct_synonym_count)
        self.assertEqual(162, stats.mapping_statement_count_by_predicate[HAS_DBXREF].filtered_count)
        self.assertEqual(221, stats.edge_count_by_predicate[IS_A].filtered_count)
        self.assertEqual(29, stats.edge_count_by_predicate[PART_OF].filtered_count)
        self.assertIn("goslim_generic", stats.class_count_by_subset)
        self.assertIn("Wikipedia", stats.mapping_statement_count_by_object_source)
        cc_classes = set(oi.descendants([CELLULAR_COMPONENT], predicates=[IS_A]))
        stats_cc = oi.branch_summary_statistics("cc", branch_roots=[CELLULAR_COMPONENT])
        self.assertEqual(len(cc_classes), stats_cc.class_count)
        stats_go = oi.branch_summary_statistics("go", prefixes=["GO"])
        self.assertLess(stats_go.class_count, stats.class_count)
        self.assertEqual(28, stats_go.deprecated_class_count)
        grouped = oi.global_summary_statistics(group_by="oio:hasOBONamespace")
        self.assertEqual(25, grouped.partitions["cellular_component"].class_count)

    def test_query_with_retries(self):
        """Tests transient errors are retried, and other errors are not."""
        from unittest.mock import MagicMock, patch
        from urllib.error import HTTPError

        from oaklib.implementations.sparql.abstract_sparql_implementation import (
            MAX_QUERY_ATTEMPTS,
            _query_with_retries,
        )

        def http_error(code):
            return HTTPError("http://example.org", code, "error", None, None)

        sw = MagicMock()
        sw.queryAndConvert.side_effect = [http_error(503), ConnectionResetError(), {"ok": 1}]
        with patch("time.sleep") as sleep:
            self.assertEqual({"ok": 1}, _query_with_retries(sw))
        self.assertEqual(3, sw.queryAndConvert.call_count)
        self.assertEqual(2, sleep.call_count)
        sw = MagicMock()
        sw.queryAndConvert.side_effect = http_error(400)
        with patch("time.sleep"), self.assertRaises(HTTPError):
            _query_with_retries(sw)
        self.assertEqual(1, sw.queryAndConvert.call_count)
        sw = MagicMock()
        sw.queryAndConvert.side_effect = http_error(503)
        with patch("time.sleep"), self.assertRaises(HTTPError):
            _query_with_retries(sw)
        self.assertEqual(MAX_QUERY_ATTEMPTS, sw.queryAndConvert.call_count)

    def test_clone_wrapper(self):
        """Tests connection settings are kept for queries run in parallel."""
        import SPARQLWrapper

        from oaklib.implementations.sparql.abstract_sparql_implementation import _clone_wrapper

        sw = SPARQLWrapper.SPARQLWrapper("http://example.org/sparql", agent="test-agent")
        sw.addCustomHttpHeader("X-Test", "1")
        sw.setCredentials("user", "pw")
        sw.setTimeout(30)
        clone = _clone_wrapper(sw)
        self.assertEqual("http://example.org/sparql", clone.endpoint)
        self.assertEqual("test-agent", clone.agent)
        self.assertEqual({"X-Test": "1"}, clone.customHttpHeaders)
        self.assertEqual(("user", "pw"), (clone.user, clone.passwd))
        self.assertEqual(30, clone.timeout)

    def test_statistics_filter_escaping(self):
        filters = self.oi._statistics_entity_filter(property_values={"rdfs:label": 'a "b"'})
        self.assertIn('= "a \\"b\\""', filters[0])

    def test_blazegraph_search_clause(self):
        """Tests the search clause for Blazegraph endpoints honors the search syntax."""
        oi = self.oi

        def clause(term, **kwargs):
            return oi._blazegraph_search_clause(term, SearchConfiguration(**kwargs))

        self.assertEqual('?v bds:search "nucleus"', clause("nucleus"))
        self.assertIn('FILTER(str(?v) = "nucleus")', clause("nucleus", is_partial=False))
        self.assertIn('bds:search "nucl*"', clause("nucl", syntax=SearchTermSyntax.STARTS_WITH))
        self.assertIn(
            'strStarts(str(?v), "nucl")', clause("nucl", syntax=SearchTermSyntax.STARTS_WITH)
        )
        partial = clause("ucle", is_partial=True)
        self.assertIn('contains(str(?v), "ucle")', partial)
        self.assertNotIn("bds:search", partial)
        regex = clause('^nucl\\w+ "x"', syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        self.assertEqual('FILTER(regex(str(?v), "^nucl\\\\w+ \\"x\\"", "i"))', regex)

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search("nucl", config=config))
        # logging.info(curies)
        # self.assertGreater(len(curie), 1)
        assert NUCLEUS in curies

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.oi.basic_search("nucl.* envelope$", config=config))
        logging.info(curies)
        # self.assertGreater(len(curie), 1)
        assert NUCLEAR_ENVELOPE in curies

    def test_mutable(self):
        """
        Tests the SPARQL store can be modified

        Currently only tests
        """
        shutil.copyfile(TEST_RDF, TEST_MUTABLE_RDF)
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_MUTABLE_RDF)))
        label = oi.label(NUCLEUS)
        preds = [IS_A, PART_OF]
        preds2 = [IS_A, FAKE_PREDICATE]
        ancestors = list(oi.ancestors(NUCLEUS, predicates=preds, reflexive=False))
        descendants = list(oi.descendants(NUCLEUS, predicates=preds, reflexive=False))
        oi.migrate_curies({NUCLEUS: FAKE_ID, PART_OF: FAKE_PREDICATE})
        self.assertEqual(label, oi.label(FAKE_ID))
        self.assertIsNone(oi.label(NUCLEUS))
        self.assertCountEqual(ancestors, oi.ancestors(FAKE_ID, predicates=preds2, reflexive=False))
        self.assertCountEqual([], list(oi.ancestors(NUCLEUS, predicates=preds, reflexive=False)))
        self.assertCountEqual(
            descendants, oi.descendants(FAKE_ID, predicates=preds2, reflexive=False)
        )
        self.assertCountEqual([], list(oi.descendants(NUCLEUS, predicates=preds, reflexive=False)))
        oi.save()

    @unittest.skip("not yet implemented")
    def test_import_behavior(self):
        """
        Tests behavior of owl:imports

        by default, imports should be followed

        See: https://github.com/INCATools/ontology-access-kit/issues/248
        """
        resource = OntologyResource(slug=str(TEST_IMPORTER))
        oi = SparqlImplementation(resource)
        terms = list(oi.entities(owl_type="owl:Class"))
        self.assertCountEqual(["PATO:1", "PATO:2"], terms)

    # SemanticSimilarity
    def test_common_ancestors(self):
        # TODO: this is currently slow
        self.compliance_tester.test_common_ancestors(self.oi)

    def test_merge(self):
        source = SparqlImplementation(OntologyResource(slug=str(INTERNEURON_RDF)))
        self.compliance_tester.test_merge(self.oi, source)

    def test_annotate_text(self):
        self.compliance_tester.test_annotate_text(self.oi)
