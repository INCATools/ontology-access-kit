import logging
import shutil
import unittest

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import IS_A, PART_OF, RDF_TYPE
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
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

TEST_RDF = INPUT_DIR / "go-nucleus.owl.ttl"
TEST_INST_RDF = INPUT_DIR / "inst.owl.ttl"
TEST_MUTABLE_RDF = OUTPUT_DIR / "go-nucleus.owl.ttl"


class TestSparqlImplementation(unittest.TestCase):
    def setUp(self) -> None:
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_RDF)))
        self.oi = oi

    def test_relationships(self):
        oi = self.oi
        self.assertIsNotNone(oi.graph)
        rels = list(oi.outgoing_relationships(VACUOLE))
        self.assertEqual(2, len(rels))
        rels = oi.outgoing_relationship_map(VACUOLE)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertIn("GO:0043231", rels[IS_A])
        self.assertIn("GO:0005737", rels[PART_OF])

    def test_instance_graph(self):
        oi = SparqlImplementation(OntologyResource(slug=str(TEST_INST_RDF)))
        self.assertIsNotNone(oi.graph)
        expected = [
            ("http://example.org/i1", "http://example.org/p", "http://example.org/j"),
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

    def test_parents(self):
        parents = self.oi.hierararchical_parents(VACUOLE)
        # logging.info(parents)
        assert "GO:0043231" in parents

    def test_labels(self):
        label = self.oi.label(NUCLEUS)
        logging.info(label)
        self.assertEqual(label, "nucleus")
        self.assertEqual(self.oi.curies_by_label(label), [NUCLEUS])

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
