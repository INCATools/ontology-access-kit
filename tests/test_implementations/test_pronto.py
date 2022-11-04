import logging
import unittest

import pronto
from kgcl_schema.datamodel import kgcl

from oaklib import get_implementation_from_shorthand
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
from oaklib.utilities.validation.definition_ontology_rules import (
    TextAndLogicalDefinitionMatchOntologyRule,
)
from tests import (
    CELL,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    INPUT_DIR,
    NUCLEUS,
    OUTPUT_DIR,
    VACUOLE,
)
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_SIMPLE_ONT = INPUT_DIR / "go-nucleus-simple.obo"
TEST_ONT_COPY = OUTPUT_DIR / "go-nucleus.copy.obo"
TEST_SUBGRAPH_OUT = OUTPUT_DIR / "vacuole.obo"


class TestProntoImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

    def test_obo_json(self) -> None:
        resource = OntologyResource(slug="go-nucleus.json", directory=INPUT_DIR, local=True)
        json_oi = ProntoImplementation(resource)
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

    def test_relationship_map(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map("GO:0005773")
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertCountEqual(rels[IS_A], ["GO:0043231"])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi)

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

    def test_defined_bys(self):
        self.compliance_tester.test_defined_bys(self.oi)

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
            # print(resource.local_path)
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
        self.compliance_tester.test_definitions(self.oi)

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

    def test_patcher(self):
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
        out_file = str(OUTPUT_DIR / "post-kgcl.obo")
        oi.dump(out_file, syntax="obo")
        resource = OntologyResource(slug=out_file, local=True)
        oi2 = ProntoImplementation(resource)
        self.assertCountEqual(
            ["cell or subcellular entity", "cellular component", "cellular_component", "foo bar"],
            oi2.entity_aliases(CELLULAR_COMPONENT),
        )

    def test_create_ontology_via_patches(self):
        oi = get_implementation_from_shorthand("pronto:")
        if isinstance(oi, PatcherInterface):

            def _roundtrip(original_oi: PatcherInterface) -> PatcherInterface:
                out = str(OUTPUT_DIR / "test-create.obo")
                original_oi.dump(out)
                return get_implementation_from_shorthand(f"pronto:{out}")

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
        rule = TextAndLogicalDefinitionMatchOntologyRule()
        results = list(rule.evaluate(self.oi))
        self.assertGreater(len(results), 5)
