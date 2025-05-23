import logging
import unittest

import pronto
from kgcl_schema.datamodel import kgcl

from oaklib import get_adapter
from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import HAS_PART, IS_A, ONLY_IN_TAXON, PART_OF
from oaklib.implementations import ProntoImplementation
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from oaklib.utilities.obograph_utils import (
    graph_as_dict,
    index_graph_edges_by_object,
    index_graph_edges_by_predicate,
    index_graph_edges_by_subject,
    index_graph_nodes,
)
from oaklib.utilities.validation.definition_ontology_rule import (
    DefinitionOntologyRule,
)
from tests import (
    CELL,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
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


class TestProntoImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        json_resource = OntologyResource(slug="go-nucleus.json", directory=INPUT_DIR, local=True)
        self.json_oi = ProntoImplementation(json_resource)
        self.compliance_tester = ComplianceTester(self)

    def test_obo_json(self) -> None:
        json_oi = self.json_oi
        curies = list(json_oi.entities())
        # for e in curies:
        #    logging.info(e)
        self.assertIn(NUCLEUS, curies)
        # for e in oi_src.all_entity_curies():
        #    self.assertIn(e, curies)
        #    assert e in list(oi_src.all_entity_curies())
        # TODO: pronto obo parsing excludes alt_ids
        # self.assertCountEqual(list(json_oi.all_entity_curies()), list(oi_src.all_entity_curies()))
        # TODO: workaround for https://github.com/althonos/pronto/issues/164
        # json_oi.store
        # (
        #     OntologyResource(slug='go-nucleus.from-json.obo', directory=OUTPUT_DIR, local=True, format='obo')
        #     )

    def test_custom_prefixes(self):
        resource = OntologyResource(slug="alignment-test.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
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
        resource = OntologyResource(
            slug="metadata-map-prefixes-test.obo", directory=INPUT_DIR, local=True
        )
        adapter = ProntoImplementation(resource)
        m = adapter.entity_metadata_map("HP:0000001")
        self.assertIsNotNone(m)
        uri = "http://www.geneontology.org/formats/oboInOwl#foo"
        curie = adapter.uri_to_curie(uri)
        # behavior is currently intentionally undefined
        assert curie == "oio:foo" or curie == "oboInOwl:foo"
        # must be reversible
        assert adapter.curie_to_uri(curie) == uri

    def test_relationship_map(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map("GO:0005773")
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertCountEqual(rels[IS_A], ["GO:0043231"])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi)

    @unittest.skip("TODO: fix")
    def test_rbox_relationships(self):
        self.compliance_tester.test_rbox_relationships(self.oi)

    def test_equiv_relationships(self):
        self.compliance_tester.test_equiv_relationships(self.oi)

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
        assert any(curie for curie in self.oi.entities() if curie == "GO:0008152")

    def test_relations(self):
        oi = self.oi
        label = oi.label(PART_OF)
        assert label.startswith("part")
        t = self.oi.node(PART_OF)
        assert t.id == PART_OF
        assert t.lbl.startswith("part")

    def test_metadata(self):
        for curie in self.oi.entities():
            m = self.oi.entity_metadata_map(curie)
            logging.info(f"{curie} {m}")
        m = self.oi.entity_metadata_map("GO:0005622")
        assert "term_tracker_item" in m.keys()
        assert "https://github.com/geneontology/go-ontology/issues/17776" in m["term_tracker_item"]

    def test_owl_types(self):
        self.compliance_tester.test_owl_types(self.oi)

    def test_labels(self):
        self.compliance_tester.test_labels(self.oi)

    def test_labels_extra(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        """
        oi = self.oi
        label = oi.label("GO:0005773")
        self.assertEqual(str, type(label))
        self.assertEqual(label, "vacuole")
        label = oi.label("FOOBAR:123")
        self.assertIsNone(label)
        # TODO: test strict mode
        label = oi.label(IS_A)
        self.assertIsNotNone(label)

    def test_synonyms(self):
        self.compliance_tester.test_synonyms(self.oi)

    def test_synonym_types(self):
        self.compliance_tester.test_synonym_types(self.oi)

    @unittest.skip("TODO")
    def test_synonym_types_json(self):
        self.compliance_tester.test_synonym_types(self.json_oi)

    def test_defined_bys(self):
        self.compliance_tester.test_defined_bys(self.oi)

    def test_obsolete_entities(self):
        resource = OntologyResource(slug="obsoletion_test.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.compliance_tester.test_obsolete_entities(oi)

    @unittest.skip("Pronto does not handling dangling references")
    def test_skos_mappings(self):
        """
        Tests mappings as SKOS properties.

        :return:
        """
        adapter = get_adapter(f"pronto:{TEST_SKOS_MAPPINGS_ONT}")
        self.compliance_tester.test_skos_mappings(adapter)

    def test_sssom_mappings(self):
        self.compliance_tester.test_sssom_mappings(self.oi)

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.subsets())
        self.assertIn("goslim_aspergillus", subsets)
        self.assertIn("GO:0003674", oi.subset_members("goslim_generic"))
        self.assertNotIn("GO:0003674", oi.subset_members("gocheck_do_not_manually_annotate"))

    def test_save(self):
        oi = ProntoImplementation()
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.create_entity(
            "FOO:1", label="foo", relationships={IS_A: ["FOO:2"], "part_of": ["FOO:3"]}
        )
        oi.store(
            OntologyResource(
                slug="go-nucleus.saved.obo", directory=OUTPUT_DIR, local=True, format="obo"
            )
        )

    @unittest.skip("Avoid network dependencies.")
    def test_from_obo_library(self):
        oi = ProntoImplementation(OntologyResource(local=False, slug="pato.obo"))
        curies = oi.curies_by_label("shape")
        self.assertEqual(["PATO:0000052"], curies)

    @unittest.skip("https://github.com/althonos/pronto/issues/186")
    def test_import_behavior(self):
        """
        Tests behavior of owl:imports

        by default, imports should be followed

        See: https://github.com/INCATools/ontology-access-kit/issues/248
        """
        for slug in ["test_import_root.obo", "test_import_root.obo"]:
            resource = OntologyResource(slug=slug, directory=INPUT_DIR, local=True)
            # currently throws exception
            pronto.Ontology(resource.local_path)
            oi = ProntoImplementation.create(resource)
            terms = list(oi.entities(owl_type="owl:Class"))
            self.assertEqual(2, len(terms))

    def test_no_import_depth(self):
        """
        Tests behavior of owl:imports

        do not follow imports if depth is set to zero

        See: https://github.com/INCATools/ontology-access-kit/issues/248
        """
        for slug in ["test_import_root.obo", "test_import_root.obo"]:
            resource = OntologyResource(slug=slug, directory=INPUT_DIR, local=True, import_depth=0)
            oi = ProntoImplementation(resource)
            terms = list(oi.entities(owl_type="owl:Class"))
            self.assertEqual(1, len(terms))

    @unittest.skip("Hide warnings")
    def test_from_owl(self):
        r = OntologyResource(local=True, slug="go-nucleus.owl", directory=INPUT_DIR)
        oi = ProntoImplementation.create(r)
        rels = list(oi.walk_up_relationship_graph("GO:0005773"))
        for rel in rels:
            logging.info(rel)

    def test_subontology(self):
        subont = self.oi.create_subontology(["GO:0005575", "GO:0005773"])
        subont.store(
            OntologyResource(
                slug="go-nucleus.filtered.obo", directory=OUTPUT_DIR, local=True, format="obo"
            )
        )

    def test_definitions(self):
        self.compliance_tester.test_definitions(self.oi, include_metadata=True)

    def test_store_associations(self):
        self.compliance_tester.test_store_associations(self.oi)

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
        self.compliance_tester.test_extract_graph(self.oi, test_metadata=True)  # TODO

    def test_ancestors_descendants(self):
        self.compliance_tester.test_ancestors_descendants(self.oi)

    @unittest.skip("TODO: relies on relation graph")
    def test_entailed_edges(self):
        oi = self.oi
        with self.assertRaises(NotImplementedError):
            list(oi.relationships([NUCLEUS], include_entailed=True))

    @unittest.skip("TODO: ensure that all test files used by compliance tests are the same")
    def test_subgraph_from_traversal(self):
        self.compliance_tester.test_subgraph_from_traversal(self.oi)

    def test_as_obograph(self):
        self.compliance_tester.test_as_obograph(self.oi)

    def test_save_extract(self):
        g = self.oi.ancestor_graph(VACUOLE)
        oi = ProntoImplementation()
        oi.load_graph(g, replace=True)
        r = OntologyResource(slug=str(TEST_SUBGRAPH_OUT), format="obo", local=True)
        oi.store(r)

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

    @unittest.skip("Pronto does not currently preserve line ordering")
    def test_sort_order_no_edits(self):
        """
        Ensures that dump does not perturb ordering of terms.
        """
        input_path = str(INPUT_DIR / "sort-test.obo")
        output_path = str(OUTPUT_DIR / "sort-test.obo")
        resource = OntologyResource(input_path, local=True)
        oi = ProntoImplementation(resource)
        OUTPUT_DIR.mkdir(exist_ok=True)
        oi.dump(output_path, syntax="obo")
        self.assertTrue(filecmp_difflib(input_path, output_path))

    def test_reflexive_diff(self):
        self.compliance_tester.test_reflexive_diff(self.oi)

    def test_merge(self):
        resource1 = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        resource2 = OntologyResource(slug="interneuron.obo", directory=INPUT_DIR, local=True)
        oi1 = ProntoImplementation(resource1)
        oi2 = ProntoImplementation(resource2)
        self.compliance_tester.test_merge(oi1, oi2)

    def test_diff(self):
        resource = OntologyResource(slug="go-nucleus-modified.obo", directory=INPUT_DIR, local=True)
        oi_modified = ProntoImplementation(resource)
        self.compliance_tester.test_diff(self.oi, oi_modified)

    def test_patcher(self):
        resource = OntologyResource(slug=TEST_ONT, local=True)
        oi = ProntoImplementation(resource)

        def roundtrip(oi_in: OntologyResource):
            out_file = str(OUTPUT_DIR / "post-kgcl.obo")
            oi_in.dump(out_file, syntax="obo")
            resource2 = OntologyResource(slug=out_file, local=True)
            return ProntoImplementation(resource2)

        self.compliance_tester.test_patcher(oi, self.oi, roundtrip_function=roundtrip)

    def test_patcher_extra(self):
        resource = OntologyResource(slug=TEST_SIMPLE_ONT, local=True)
        oi = ProntoImplementation(resource)
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
        oi.apply_patch(kgcl.RemoveUnder(id="x", subject=NUCLEUS, object=IMBO))
        oi.apply_patch(
            kgcl.EdgeDeletion(id="x", subject=NUCLEAR_MEMBRANE, object=NUCLEUS, predicate=PART_OF)
        )
        oi.apply_patch(
            kgcl.EdgeCreation(id="x", subject=NUCLEUS, object=NUCLEAR_MEMBRANE, predicate=HAS_PART)
        )
        out_file = str(OUTPUT_DIR / "post-kgcl.obo")
        oi.dump(out_file, syntax="obo")
        resource = OntologyResource(slug=out_file, local=True)
        oi2 = ProntoImplementation(resource)
        self.assertCountEqual(
            ["cell or subcellular entity", "cellular component", "cellular_component", "foo bar"],
            oi2.entity_aliases(CELLULAR_COMPONENT),
        )
        cases = [
            (NUCLEAR_MEMBRANE, IS_A, ORGANELLE_MEMBRANE),
            (NUCLEAR_MEMBRANE, PART_OF, NUCLEAR_ENVELOPE),
        ]
        self.assertCountEqual(cases, list(oi2.relationships([NUCLEAR_MEMBRANE])))
        self.assertCountEqual(
            [(NUCLEUS, HAS_PART, NUCLEAR_MEMBRANE)], list(oi2.relationships([NUCLEUS]))
        )

    def test_create_ontology_via_patches(self):
        oi = get_adapter("pronto:")
        if isinstance(oi, PatcherInterface):

            def _roundtrip(original_oi: PatcherInterface) -> PatcherInterface:
                out = str(OUTPUT_DIR / "test-create.obo")
                original_oi.dump(out)
                return get_adapter(f"pronto:{out}")

            self.compliance_tester.test_create_ontology_via_patches(
                oi, roundtrip_function=_roundtrip
            )
        else:
            raise NotImplementedError

    # SemanticSimilarityInterface
    def test_common_ancestors(self):
        self.compliance_tester.test_common_ancestors(self.oi)

    @unittest.skip("Not implemented")
    def test_pairwise_similarity(self):
        self.compliance_tester.test_pairwise_similarity(self.oi)

    # validation

    def test_logical_definitions(self):
        self.compliance_tester.test_logical_definitions(self.oi)

    def test_ontology_rules(self):
        # TODO: decide whether ontology rules should be validated
        # as part of each implementation, or as a standalone
        rule = DefinitionOntologyRule()
        results = list(rule.evaluate(self.oi))
        self.assertGreater(len(results), 5)

    # TextAnnotatorInterface tests

    @unittest.skip("TODO: OP labels")
    def test_annotate_text(self):
        self.compliance_tester.test_annotate_text(self.oi)

    # OwlInterface tests

    def test_transitive_object_properties(self):
        self.compliance_tester.test_transitive_object_properties(self.oi)

    @unittest.skip("TODO: pronto throws KeyError on test ontology")
    def test_simple_subproperty_of_chains(self):
        self.compliance_tester.test_simple_subproperty_of_chains(self.oi)
