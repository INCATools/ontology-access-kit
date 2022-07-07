"""Test Wikidata Implementation."""
import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.wikidata.wikidata_implementation import (
    WikidataImplementation,
)

WD_PECTORAL_FIN_MORPHOGENESIS = "wikidata:Q22298706"
WD_ER = "wikidata:Q79927"
WD_SLY_SYNDROME = "wikidata:Q1750471"
WD_MPS = "wikidata:Q1479681"


@unittest.skip(
    "Causes timeouts. See https://stackoverflow.com/questions/61803586/wikidata-forbidden-access"
)
class TestWikidataImplementation(unittest.TestCase):
    """Test Wikidata Implementation."""

    def setUp(self) -> None:
        """Set up."""
        oi = WikidataImplementation()
        self.oi = oi

    def test_relationships(self):
        """Test relationships."""
        oi = self.oi
        rels = oi.get_outgoing_relationship_map_by_curie(WD_SLY_SYNDROME)
        for k, vs in rels.items():
            print(f"{k}")
            for v in vs:
                print(f"  = {v}")

    @unittest.skip("Too slow")
    def test_relationships_slow(self):
        """Test relationships slow."""
        oi = self.oi
        rels = oi.get_outgoing_relationship_map_by_curie(WD_SLY_SYNDROME)
        for k, vs in rels.items():
            print(f'{k} "{oi.get_label_by_curie(k)}"')
            for v in vs:
                print(f'  = {v} "{oi.get_label_by_curie(v)}"')

    def test_labels(self):
        """Test labels."""
        label = self.oi.get_label_by_curie(WD_SLY_SYNDROME)
        # print(label)
        self.assertIn(WD_SLY_SYNDROME, self.oi.get_curies_by_label(label))

    def test_synonyms(self):
        """Test synonyms."""
        syns = self.oi.aliases_by_curie(WD_SLY_SYNDROME)
        logging.info(syns)
        assert "mucopolysaccharidosis VII" in syns

    def test_definition(self):
        """Test definition."""
        defn = self.oi.get_definition_by_curie(WD_PECTORAL_FIN_MORPHOGENESIS)
        logging.info(f"DEF={defn}")
        assert defn

    def test_search(self):
        """Test search."""
        oi = self.oi
        config = SearchConfiguration(is_partial=False, limit=3)
        curies = list(oi.basic_search("endoplasmic reticulum", config=config))
        tups = list(oi.get_labels_for_curies(curies))
        # print(tups)
        self.assertIn((WD_ER, "endoplasmic reticulum"), tups)

    # OboGraph

    def test_ancestors(self):
        """Test ancestors."""
        oi = self.oi
        ancs = list(oi.ancestors([WD_SLY_SYNDROME], predicates=[IS_A, "wdp:P1199"]))
        for a in ancs:
            print(a)
        for curie, label in oi.get_labels_for_curies(ancs):
            print(f"{curie} ! {label}")
        self.assertIn(WD_MPS, ancs)

    def test_descendants(self):
        """Test descendants."""
        oi = self.oi
        results = list(oi.descendants([WD_MPS], predicates=[IS_A]))
        for a in results:
            print(a)
        self.assertIn(WD_SLY_SYNDROME, results)
        for curie, label in oi.get_labels_for_curies(results):
            print(f"D: {curie} ! {label}")

    def test_ancestor_graph(self):
        """Test ancestor graph."""
        oi = self.oi
        for preds in [[IS_A], [IS_A, PART_OF]]:
            g = oi.ancestor_graph([WD_MPS], predicates=preds)
            print(yaml_dumper.dumps(g))
            assert len(g.nodes) > 0
            assert len(g.edges) > 0
            [n.id for n in g.nodes]
            [(e.sub, e.pred, e.obj) for e in g.edges]

    def test_extract_triples(self):
        """Test extract triples."""
        oi = self.oi
        for t in oi.extract_triples([WD_MPS]):
            print(t)
