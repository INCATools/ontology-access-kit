import logging
import unittest
from copy import deepcopy

from kgcl_schema.datamodel import kgcl

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import HAS_PART, IS_A, ONLY_IN_TAXON, PART_OF
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
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
)
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_SIMPLE_ONT = INPUT_DIR / "go-nucleus-simple.obo"
TEST_ONT_COPY = OUTPUT_DIR / "go-nucleus.copy.obo"
TEST_SUBGRAPH_OUT = OUTPUT_DIR / "vacuole.obo"


class TestSimpleOboImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = SimpleOboImplementation(resource)
        self.oi = oi
        self.compliance_tester = ComplianceTester(self)

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

    def test_relationships_extra(self):
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
        self.assertIn("part_of", entities)

    @unittest.skip("TODO")
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
        print(syns)
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

    @unittest.skip("TODO")
    def test_mappings(self):
        oi = self.oi
        mappings = list(oi.get_sssom_mappings_by_curie(NUCLEUS))
        assert any(m for m in mappings if m.object_id == "Wikipedia:Cell_nucleus")
        self.assertEqual(len(mappings), 2)
        for m in mappings:
            logging.info(f"GETTING {m.object_id}")
            reverse_mappings = list(oi.get_sssom_mappings_by_curie(m.object_id))
            reverse_subject_ids = [m.subject_id for m in reverse_mappings]
            self.assertEqual(reverse_subject_ids, [NUCLEUS])

    def test_definitions(self):
        self.compliance_tester.test_definitions(self.oi)

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.subsets())
        self.assertIn("goslim_aspergillus", subsets)
        self.assertIn("GO:0003674", oi.subset_members("goslim_generic"))
        self.assertNotIn("GO:0003674", oi.subset_members("gocheck_do_not_manually_annotate"))

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

    @unittest.skip("TODO")
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

    @unittest.skip("TODO")
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

    @unittest.skip("TODO")
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
            self.oi, original_oi=original_oi, roundtrip_function=roundtrip
        )

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
