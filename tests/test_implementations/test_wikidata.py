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
    def setUp(self) -> None:
        oi = WikidataImplementation()
        self.oi = oi

    def test_relationships(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map(WD_SLY_SYNDROME)
        for k, vs in rels.items():
            logging.info(f"{k}")
            for v in vs:
                logging.info(f"  = {v}")

    @unittest.skip("Too slow")
    def test_relationships_slow(self):
        oi = self.oi
        rels = oi.outgoing_relationship_map(WD_SLY_SYNDROME)
        for k, vs in rels.items():
            logging.info(f'{k} "{oi.label(k)}"')
            for v in vs:
                logging.info(f'  = {v} "{oi.label(v)}"')

    def test_labels(self):
        label = self.oi.label(WD_SLY_SYNDROME)
        # logging.info(label)
        self.assertIn(WD_SLY_SYNDROME, self.oi.curies_by_label(label))

    def test_synonyms(self):
        syns = self.oi.entity_aliases(WD_SLY_SYNDROME)
        logging.info(syns)
        assert "mucopolysaccharidosis VII" in syns

    def test_definition(self):
        defn = self.oi.definition(WD_PECTORAL_FIN_MORPHOGENESIS)
        logging.info(f"DEF={defn}")
        assert defn

    def test_search(self):
        oi = self.oi
        config = SearchConfiguration(is_partial=False, limit=3)
        curies = list(oi.basic_search("endoplasmic reticulum", config=config))
        tups = list(oi.labels(curies))
        # logging.info(tups)
        self.assertIn((WD_ER, "endoplasmic reticulum"), tups)

    # OboGraph

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors([WD_SLY_SYNDROME], predicates=[IS_A, "wdp:P1199"]))
        for a in ancs:
            logging.info(a)
        for curie, label in oi.labels(ancs):
            logging.info(f"{curie} ! {label}")
        self.assertIn(WD_MPS, ancs)

    def test_descendants(self):
        oi = self.oi
        results = list(oi.descendants([WD_MPS], predicates=[IS_A]))
        for a in results:
            logging.info(a)
        self.assertIn(WD_SLY_SYNDROME, results)
        for curie, label in oi.labels(results):
            logging.info(f"D: {curie} ! {label}")

    def test_ancestor_graph(self):
        oi = self.oi
        for preds in [[IS_A], [IS_A, PART_OF]]:
            g = oi.ancestor_graph([WD_MPS], predicates=preds)
            logging.info(yaml_dumper.dumps(g))
            assert len(g.nodes) > 0
            assert len(g.edges) > 0
            [n.id for n in g.nodes]
            [(e.sub, e.pred, e.obj) for e in g.edges]

    def test_extract_triples(self):
        oi = self.oi
        for t in oi.extract_triples([WD_MPS]):
            logging.info(t)
