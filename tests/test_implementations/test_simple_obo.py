import logging
import unittest
from copy import deepcopy

from kgcl_schema.datamodel import kgcl

from oaklib import get_adapter
from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    HAS_PART,
    IS_A,
    ONLY_IN_TAXON,
    PART_OF,
    TERM_TRACKER_ITEM,
)
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_DEF,
    TAG_SYNONYM,
    QuotedText,
    TagValue,
    XrefList,
)
from oaklib.query import query_terms_iterator
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from oaklib.utilities.obograph_utils import (
    graph_as_dict,
    index_graph_edges_by_object,
    index_graph_edges_by_predicate,
    index_graph_edges_by_subject,
    index_graph_nodes,
)
from tests import (
    BIOLOGICAL_ENTITY,
    CELL,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    FAKE_ID,
    FAKE_PREDICATE,
    HUMAN,
    IMBO,
    INPUT_DIR,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    ORGANELLE_MEMBRANE,
    OUTPUT_DIR,
    VACUOLE,
    filecmp_difflib,
)
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_SIMPLE_ONT = INPUT_DIR / "go-nucleus-simple.obo"
TEST_ONT_COPY = OUTPUT_DIR / "go-nucleus.copy.obo"
TEST_SUBGRAPH_OUT = OUTPUT_DIR / "vacuole.obo"
TEST_SKOS_MAPPINGS_ONT = INPUT_DIR / "mapping-predicates-test.obo"


class TestSimpleOboImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = SimpleOboImplementation(resource)
        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

    def test_parser(self):
        """
        Tests low-level parser methods.

        This may be moved to a separate test class in future, as it does
        not pertain to testing of the interface.
        """
        obodoc = self.oi.obo_document
        nuc = obodoc.stanzas[NUCLEUS]
        tvs = nuc.tag_values
        [defn] = [tv for tv in tvs if tv.tag == TAG_DEF]
        self.assertEqual(TAG_DEF, defn.tag)
        self.assertTrue(defn.value.startswith('"A membrane-bounded organelle'))
        toks = defn.tokenize()
        tok0, tok1 = toks
        self.assertIsInstance(tok0, QuotedText)
        self.assertIsInstance(tok1, XrefList)
        tv = TagValue(TAG_SYNONYM, '"abc def ghi" EXACT [PMID:1, PMID:2]')
        toks = tv.tokenize()
        self.assertGreater(len(toks), 2)

    def test_custom_prefixes(self):
        resource = OntologyResource(slug="alignment-test.obo", directory=INPUT_DIR, local=True)
        oi = SimpleOboImplementation(resource)
        cases = [
            ("XX:1", "http://purl.obolibrary.org/obo/XX_1"),
            (NUCLEUS, "http://purl.obolibrary.org/obo/GO_0005634"),
            ("schema:Person", "http://schema.org/Person"),
            ("FOO:1", None),
        ]
        for curie, iri in cases:
            self.assertEqual(oi.curie_to_uri(curie), iri, f"in expand curie: {curie}")
            if iri is not None:
                self.assertEqual(oi.uri_to_curie(iri), curie, f"in contract iri: {iri}")

    def test_conflicting_oio_prefixes(self):
        """
        See https://github.com/INCATools/ontology-access-kit/issues/702
        """
        # TODO: DRY. This is currently duplicative of a pronto test
        resource = OntologyResource(
            slug="metadata-map-prefixes-test.obo", directory=INPUT_DIR, local=True
        )
        adapter = SimpleOboImplementation(resource)
        m = adapter.entity_metadata_map("HP:0000001")
        self.assertIsNotNone(m)
        uri = "http://www.geneontology.org/formats/oboInOwl#foo"
        curie = adapter.uri_to_curie(uri)
        # behavior is currently intentionally undefined
        assert curie == "oio:foo" or curie == "oboInOwl:foo"
        # must be reversible
        assert adapter.curie_to_uri(curie) == uri

    def test_relationships_extra(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map("GO:0005773")
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertCountEqual(rels[IS_A], ["GO:0043231"])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi)

    @unittest.skip("Contents of go-nucleus file need to be aligned")
    def test_entailed_relationships(self):
        self.compliance_tester.test_entailed_relationships(self.oi)

    def test_rbox_relationships(self):
        self.compliance_tester.test_rbox_relationships(self.oi)

    def test_equiv_relationships(self):
        self.compliance_tester.test_equiv_relationships(self.oi)

    @unittest.skip("TODO")
    def test_gci_relationships(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map(CELL)
        self.assertCountEqual(rels[IS_A], ["CARO:0000003"])
        self.assertCountEqual(rels[ONLY_IN_TAXON], [CELLULAR_ORGANISMS])
        self.assertNotIn(PART_OF, rels)  # GCI relations excluded

    def test_incoming_relationships(self):
        oi = self.oi
        rels = oi.incoming_relationship_map(CYTOPLASM)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertCountEqual(rels[IS_A], ["GO:0005938", "GO:0099568"])
        self.assertCountEqual(rels[PART_OF], ["GO:0005773", "GO:0099568"])

    def test_all_terms(self):
        entities = list(self.oi.entities())
        self.assertIn(NUCLEUS, entities)
        self.assertIn(CELLULAR_COMPONENT, entities)
        self.assertIn(PART_OF, entities)

    @unittest.skip("TODO")
    def test_relations(self):
        oi = self.oi
        label = oi.label(PART_OF)
        assert label.startswith("part")
        t = self.oi.node(PART_OF)
        assert t.id == PART_OF
        assert t.lbl.startswith("part")

    def test_metadata(self):
        self.compliance_tester.test_metadata(self.oi)

    def test_shorthand(self):
        oi = self.oi
        cases = [
            (PART_OF, "part_of"),
            (TERM_TRACKER_ITEM, "term_tracker_item"),
        ]
        for curie, shorthand in cases:
            self.assertEqual(oi.map_shorthand_to_curie(shorthand), curie)
            self.assertEqual(oi.map_curie_to_shorthand(curie), shorthand)

    def test_labels(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        """
        oi = self.oi
        label = oi.label(VACUOLE)
        self.assertEqual(str, type(label))
        self.assertEqual(label, "vacuole")
        lbls = list(oi.labels([VACUOLE, NUCLEUS]))
        self.assertCountEqual([(VACUOLE, "vacuole"), (NUCLEUS, "nucleus")], lbls)
        label = oi.label("FOOBAR:123")
        self.assertIsNone(label)
        # TODO: test strict mode
        label = oi.label(IS_A)
        self.assertIsNotNone(label)

    def test_owl_types(self):
        self.compliance_tester.test_owl_types(self.oi)

    def test_synonyms(self):
        self.compliance_tester.test_synonyms(self.oi)

    def test_synonyms_extra(self):
        syns = self.oi.entity_aliases("GO:0005575")
        # logging.info(syns)
        self.assertCountEqual(
            syns,
            [
                "cellular_component",
                "cellular component",
                "cell or subcellular entity",
                "subcellular entity",
            ],
        )
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

    def test_sssom_mappings(self):
        self.compliance_tester.test_sssom_mappings(self.oi)

    def test_skos_mappings(self):
        """
        Tests mappings as SKOS properties.

        :return:
        """
        adapter = get_adapter(f"simpleobo:{TEST_SKOS_MAPPINGS_ONT}")
        self.compliance_tester.test_skos_mappings(adapter)

    def test_definitions(self):
        self.compliance_tester.test_definitions(self.oi, include_metadata=True)

    def test_subsets(self):
        self.compliance_tester.test_subsets(self.oi)

    def test_obsolete_entities(self):
        resource = OntologyResource(slug="obsoletion_test.obo", directory=INPUT_DIR, local=True)
        oi = SimpleOboImplementation(resource)
        self.compliance_tester.test_obsolete_entities(oi)

    def test_save(self):
        oi = SimpleOboImplementation()
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.create_entity(
            "FOO:1", label="foo", relationships={IS_A: ["FOO:2"], "part_of": ["FOO:3"]}
        )
        oi.store(
            OntologyResource(
                slug="go-nucleus.saved.obo", directory=OUTPUT_DIR, local=True, format="obo"
            )
        )

    def test_qc(self):
        oi = self.oi
        for t in oi.term_curies_without_definitions():
            logging.info(t)
        self.assertIn("CARO:0000003", oi.term_curies_without_definitions())

    def test_walk_up(self):
        oi = self.oi
        rels = list(oi.walk_up_relationship_graph("GO:0005773"))
        logging.info("ALL")
        for rel in rels:
            logging.info(rel)
        assert ("GO:0043227", HAS_PART, "GO:0016020") in rels
        logging.info("**IS_A")
        rels = list(oi.walk_up_relationship_graph("GO:0005773", predicates=[IS_A]))
        for rel in rels:
            logging.info(rel)
            self.assertEqual(rel[1], IS_A)
        assert ("GO:0043227", HAS_PART, "GO:0016020") not in rels
        assert ("GO:0110165", IS_A, "CARO:0000000") in rels

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors("GO:0005773"))
        for a in ancs:
            logging.info(a)
        assert "NCBITaxon:1" in ancs
        assert "GO:0005773" in ancs  # reflexive
        ancs = list(oi.ancestors("GO:0005773", predicates=[IS_A]))
        for a in ancs:
            logging.info(a)
        assert "NCBITaxon:1" not in ancs
        assert "GO:0005773" in ancs  # reflexive
        assert "GO:0043231" in ancs  # reflexive

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
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A, PART_OF]))
        assert VACUOLE in descs
        assert CYTOPLASM in descs
        g = self.oi.ancestor_graph(CYTOPLASM)
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == CYTOPLASM]))

    def test_extract_graph(self):
        self.compliance_tester.test_extract_graph(self.oi, test_metadata=False)  # TODO

    @unittest.skip("TODO")
    def test_subgraph_from_traversal(self):
        self.compliance_tester.test_subgraph_from_traversal(self.oi)

    def test_as_obograph(self):
        self.compliance_tester.test_as_obograph(self.oi)

    def test_ancestors_descendants(self):
        self.compliance_tester.test_ancestors_descendants(self.oi)

    def test_search_aliases(self):
        config = SearchConfiguration(properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, ["GO:0003824"])
        config = SearchConfiguration()
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, [])

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("cytoplasm", config=config))
        # logging.info(curies)
        assert CYTOPLASM in curies

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        curies = list(self.oi.basic_search("nucl", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search("nucl", config=config))
        # logging.info(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_regex(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        curies = list(self.oi.basic_search("^nucl", config=config))
        logging.info(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_dump(self):
        copy = "go-nucleus.copy.obo"
        OUTPUT_DIR.mkdir(exist_ok=True)
        self.oi.dump(str(OUTPUT_DIR / copy), syntax="obo")

    def test_sort_order_no_edits(self):
        """
        Ensures that dump does not perturb ordering of terms.
        """
        input_path = str(INPUT_DIR / "sort-test.obo")
        output_path = str(OUTPUT_DIR / "sort-test.obo")
        resource = OntologyResource(input_path, local=True)
        oi = SimpleOboImplementation(resource)
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.dump(output_path, syntax="obo")
        self.assertTrue(filecmp_difflib(input_path, output_path))
        stanza_length_before_sort = len(oi.obo_document.stanzas)
        stanza_keys_before_sort = oi.obo_document.stanzas.keys()
        # try ordering stanzas (but do not ordering within a stanza)
        oi.obo_document.order_stanzas()
        stanza_length_after_sort = len(oi.obo_document.stanzas)
        stanza_keys_after_sort = oi.obo_document.stanzas.keys()
        oi.dump(output_path, syntax="obo")
        # AssertFalse because the stanzas are sorted.
        self.assertFalse(filecmp_difflib(input_path, output_path))
        self.assertEqual(stanza_length_before_sort, stanza_length_after_sort)
        self.assertEqual(stanza_keys_before_sort, stanza_keys_after_sort)

    @unittest.skip(
        "Currently not guaranteed same as OWLAPI: see https://github.com/owlcollab/oboformat/issues/138"
    )
    def test_sort_order_with_forced_reorder(self):
        """
        Ensures that dump does not perturb ordering of terms after normalization
        """
        input_path = str(INPUT_DIR / "sort-test.obo")
        output_path = str(OUTPUT_DIR / "sort-test.obo")
        resource = OntologyResource(input_path, local=True)
        oi = SimpleOboImplementation(resource)
        oi.obo_document.normalize_line_order()
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.dump(output_path, syntax="obo")
        self.assertTrue(filecmp_difflib(input_path, output_path))

    def test_merge(self):
        resource1 = OntologyResource(slug=TEST_ONT, directory=INPUT_DIR, local=True)
        resource2 = OntologyResource(slug="interneuron.obo", directory=INPUT_DIR, local=True)
        oi1 = SimpleOboImplementation(resource1)
        oi2 = SimpleOboImplementation(resource2)
        self.compliance_tester.test_merge(oi1, oi2)

    def test_reflexive_diff(self):
        self.compliance_tester.test_reflexive_diff(self.oi)

    def test_diff(self):
        resource = OntologyResource(slug="go-nucleus-modified.obo", directory=INPUT_DIR, local=True)
        oi_modified = SimpleOboImplementation(resource)
        self.compliance_tester.test_diff(self.oi, oi_modified)

    def test_patcher(self):
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = SimpleOboImplementation(resource)
        original_oi = deepcopy(oi)

        def roundtrip(oi_in: OntologyResource):
            out_file = str(OUTPUT_DIR / "post-kgcl.obo")
            oi_in.dump(out_file, syntax="obo")
            resource2 = OntologyResource(slug=out_file, local=True)
            return SimpleOboImplementation(resource2)

        self.compliance_tester.test_patcher(
            oi, original_oi=original_oi, roundtrip_function=roundtrip
        )

    def test_patcher_obsoletion_chains(self):
        resource = OntologyResource(slug=TEST_ONT, local=True)
        self.compliance_tester.test_patcher_obsoletion_chains(
            lambda: SimpleOboImplementation(resource)
        )

    def test_add_contributors(self):
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = SimpleOboImplementation(resource)
        self.assertTrue(oi.uses_legacy_properties)
        self.compliance_tester.test_add_contributors(oi, legacy=True)
        oi.dump(str(OUTPUT_DIR / "go-nucleus-contributors.obo"), syntax="obo")

    def test_add_contributors_non_legacy(self):
        """Tests adding contributor metadata using newer standard properties"""
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = SimpleOboImplementation(resource)
        oi.set_uses_legacy_properties(False)
        self.assertFalse(oi.uses_legacy_properties)
        self.compliance_tester.test_add_contributors(oi, legacy=False)
        oi.dump(str(OUTPUT_DIR / "go-nucleus-contributors2.obo"), syntax="obo")

    def test_patcher2(self):
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = SimpleOboImplementation(resource)
        oi.apply_patch(
            kgcl.NodeRename(id=generate_change_id(), about_node=VACUOLE, new_value="VaCuOlE")
        )
        oi.apply_patch(kgcl.NodeObsoletion(id=generate_change_id(), about_node=NUCLEUS))
        with self.assertRaises(ValueError):
            oi.apply_patch(kgcl.NodeObsoletion(id="x", about_node="NO SUCH TERM"))
        # oi.apply_patch(kgcl.NodeDeletion(id=generate_change_id(), about_node=NUCLEAR_ENVELOPE))
        oi.apply_patch(
            kgcl.SynonymReplacement(
                id="x",
                about_node=CELLULAR_COMPONENT,
                old_value="subcellular entity",
                new_value="foo bar",
            )
        )
        oi.apply_patch(
            kgcl.NewSynonym(id=generate_change_id(), about_node=HUMAN, new_value="people")
        )
        oi.apply_patch(kgcl.RemoveUnder(id="x", subject=NUCLEUS, object=IMBO))
        oi.apply_patch(
            kgcl.EdgeDeletion(id="x", subject=NUCLEAR_MEMBRANE, object=NUCLEUS, predicate=PART_OF)
        )
        oi.apply_patch(kgcl.NodeDeletion(id=generate_change_id(), about_node=BIOLOGICAL_ENTITY))
        out_file = str(OUTPUT_DIR / "post-kgcl.obo")
        oi.dump(out_file, syntax="obo")
        resource = OntologyResource(slug=out_file, local=True)
        oi2 = SimpleOboImplementation(resource)
        self.assertCountEqual(
            ["cell or subcellular entity", "cellular component", "cellular_component", "foo bar"],
            oi2.entity_aliases(CELLULAR_COMPONENT),
        )
        self.assertCountEqual(
            ["people", "Homo sapiens"],
            oi2.entity_aliases(HUMAN),
        )
        self.assertNotIn((NUCLEUS, IS_A, IMBO), list(oi2.relationships([NUCLEUS])))
        cases = [
            (NUCLEAR_MEMBRANE, IS_A, ORGANELLE_MEMBRANE, True),
            (NUCLEAR_MEMBRANE, PART_OF, NUCLEAR_ENVELOPE, True),
            (NUCLEAR_MEMBRANE, PART_OF, NUCLEUS, False),
        ]
        rels = list(oi2.relationships([NUCLEAR_MEMBRANE]))
        for s, p, o, is_in in cases:
            rel = s, p, o
            if is_in:
                self.assertIn(rel, rels)
            else:
                self.assertNotIn(rel, rels)

        self.assertTrue(BIOLOGICAL_ENTITY not in oi2.entities())

    def test_migrate_curies(self):
        """
        Tests migrate_curies operations works on a simple obo backend

        This test is a mutation test, so a copy of the test database will be made
        """
        oi = self.oi
        label = oi.label(NUCLEUS)
        preds = [IS_A, PART_OF]
        preds_rewired = [IS_A, FAKE_PREDICATE]
        expected_ancs = list(oi.ancestors(NUCLEUS, predicates=preds, reflexive=False))
        expected_descs = list(oi.descendants(NUCLEUS, predicates=preds, reflexive=False))
        oi.migrate_curies({NUCLEUS: FAKE_ID, PART_OF: FAKE_PREDICATE})
        out_file = str(OUTPUT_DIR / "post-migrate.obo")
        oi.dump(out_file, syntax="obo")
        self.assertEqual(label, oi.label(FAKE_ID))
        self.assertIsNone(oi.label(NUCLEUS))
        self.assertEqual([FAKE_ID], oi.curies_by_label("nucleus"))
        # query with rewired preds should be the same
        self.assertCountEqual(
            expected_ancs, list(oi.ancestors(FAKE_ID, predicates=preds_rewired, reflexive=False))
        )
        # query with UNrewired preds should be incomplete
        self.assertNotIn(CELL, oi.ancestors(NUCLEUS, predicates=preds, reflexive=False))
        # query with rewired preds should be the same
        self.assertCountEqual(
            expected_descs, list(oi.descendants(FAKE_ID, predicates=preds_rewired, reflexive=False))
        )
        # query with UNrewired preds should be incomplete
        self.assertNotIn(NUCLEAR_MEMBRANE, oi.ancestors(NUCLEUS, predicates=preds, reflexive=False))

    def test_entity_alias_map(self):
        """Test aliases."""
        resource = OntologyResource(slug="test_simpleobo.obo", directory=INPUT_DIR, local=True)
        impl = SimpleOboImplementation(resource)
        alias_list = []
        for curie in query_terms_iterator((".all",), impl):
            for pred, aliases in impl.entity_alias_map(curie).items():
                for alias in aliases:
                    alias_list.append(dict(curie=curie, pred=pred, alias=alias))

        self.assertEqual(len(alias_list), 3)

    # TextAnnotatorInterface tests
    def test_annotate_text(self):
        self.compliance_tester.test_annotate_text(self.oi)

    # OwlInterface tests

    @unittest.skip("Not implemented")
    def test_disjoint_with(self):
        self.compliance_tester.test_disjoint_with(self.oi)

    def test_transitive_object_properties(self):
        self.compliance_tester.test_transitive_object_properties(self.oi)

    def test_simple_subproperty_of_chains(self):
        self.compliance_tester.test_simple_subproperty_of_chains(self.oi)
