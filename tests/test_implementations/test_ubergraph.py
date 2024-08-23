import logging
import unittest

from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations import UbergraphImplementation
from tests import (
    CELL,
    CELLULAR_ANATOMICAL_ENTITY,
    CELLULAR_COMPONENT,
    CYTOPLASM,
    DIGIT,
    IMBO,
    INTRACELLULAR,
    NEURON,
    NUCLEAR_ENVELOPE,
    NUCLEUS,
    PHOTORECEPTOR_OUTER_SEGMENT,
    SHAPE,
    THYLAKOID,
    VACUOLE,
)


class TestUbergraphImplementation(unittest.TestCase):
    """
    Tests for the UbergraphImplementation class.

    Note: this test performs live queries against a remote endpoint.
    As such it is inherently fragile, and may fail if either:

     - the remote endpoint is down
     - the remote endpoint changes its data model
     - the remote endpoint changes its data
    """

    def setUp(self) -> None:
        oi = UbergraphImplementation()
        self.oi = oi

    def test_relationships(self):
        """
        Tests asserted and non-asserted relationships.

        Note: we try and make this test as non-fragile as possible
        by choosing a relatively stable part of GO, but it is still
        possible that upstream changes will break this test.
        """
        ont = self.oi
        rels = ont.outgoing_relationship_map(VACUOLE)
        for k, v in rels.items():
            logging.info(f"{k} = {v}")
        self.assertIn(IMBO, rels[IS_A])
        self.assertIn(CYTOPLASM, rels[PART_OF])
        rels = list(ont.relationships([VACUOLE]))
        for rel in rels:
            logging.info(rel)
        self.assertNotIn((VACUOLE, IS_A, CELLULAR_COMPONENT), rels)
        self.assertIn((VACUOLE, PART_OF, CYTOPLASM), rels)

    def test_entailed_relationships(self):
        ont = self.oi
        rels = list(ont.entailed_outgoing_relationships(VACUOLE))
        self.assertIn((IS_A, VACUOLE), rels)
        self.assertIn((IS_A, IMBO), rels)
        self.assertIn((IS_A, CELLULAR_COMPONENT), rels)
        self.assertIn((PART_OF, CYTOPLASM), rels)
        self.assertIn((PART_OF, CELL), rels)

    def test_labels(self):
        label = self.oi.label(DIGIT)
        self.assertEqual(label, "digit")
        self.assertIn(DIGIT, self.oi.curies_by_label(label))

    def test_synonyms(self):
        syns = self.oi.entity_aliases(CELLULAR_COMPONENT)
        logging.info(syns)
        assert "cellular component" in syns

    @unittest.skip("This test is too rigid as synonyms are liable to change")
    def test_synonyms_granular(self):
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

    def test_definition(self):
        defn = self.oi.definition(CELLULAR_COMPONENT)
        logging.info(defn)
        self.assertTrue(defn.startswith("A location"))

    def test_search(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("limb", config=config))
        logging.info(curies)
        assert "UBERON:0002101" in curies

    # OboGraph
    # @unittest.skip("HTTP Error 504: Gateway Time-out")
    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors([VACUOLE]))
        # for a in ancs:
        #    logging.info(a)
        self.assertIn(VACUOLE, ancs)
        self.assertIn(CYTOPLASM, ancs)
        self.assertIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A]))
        # for a in ancs:
        #    logging.info(a)
        self.assertIn(VACUOLE, ancs)
        self.assertNotIn(CYTOPLASM, ancs)
        self.assertNotIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A, PART_OF]))
        # for a in ancs:
        #    logging.info(a)
        self.assertIn(VACUOLE, ancs)  # reflexive
        self.assertIn(CYTOPLASM, ancs)
        self.assertIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)
        ancs = list(oi.ancestors([VACUOLE], predicates=[PART_OF]))
        # NOT reflexive
        # self.assertIn(VACUOLE, ancs)
        self.assertIn(CELL, ancs)

    def test_descendants(self):
        oi = self.oi
        descs = list(oi.descendants([CYTOPLASM]))
        # for a in descs:
        #    logging.info(a)
        self.assertIn(VACUOLE, descs)
        self.assertIn(CYTOPLASM, descs)
        descs = list(oi.descendants([CYTOPLASM], predicates=[IS_A]))
        # for a in descs:
        #    logging.info(f'IS_A DESC: {a}')
        self.assertIn(CYTOPLASM, descs)
        self.assertNotIn(VACUOLE, descs)

    def test_ancestor_graph(self):
        oi = self.oi
        for preds in [None, [IS_A], [IS_A, PART_OF]]:
            g = oi.ancestor_graph([VACUOLE], predicates=preds)
            # logging.info(yaml_dumper.dumps(g))
            assert len(g.nodes) > 0
            assert len(g.edges) > 0
            node_ids = [n.id for n in g.nodes]
            [(e.sub, e.pred, e.obj) for e in g.edges]
            assert VACUOLE in node_ids
            assert CELLULAR_COMPONENT in node_ids
            if preds == [IS_A]:
                assert CELL not in node_ids
            else:
                assert CELL in node_ids

    def test_gap_fill(self):
        oi = self.oi
        rels = list(
            oi.gap_fill_relationships(
                [NEURON, PHOTORECEPTOR_OUTER_SEGMENT, CELLULAR_COMPONENT],
                predicates=[IS_A, PART_OF],
            )
        )
        for rel in rels:
            logging.info(rel)
        self.assertEqual(
            rels,
            [
                ("GO:0001750", "BFO:0000050", "CL:0000540"),
                ("GO:0001750", "BFO:0000050", "GO:0005575"),
                ("GO:0001750", "rdfs:subClassOf", "GO:0005575"),
            ],
        )

    @unittest.skip("Timeout")
    def test_common_ancestors(self):
        oi = self.oi
        for preds in [None, [IS_A], [PART_OF], [IS_A, PART_OF]]:
            ancs = list(oi.common_ancestors(NUCLEUS, THYLAKOID, preds))
            logging.info(f"{preds} ==> {ancs}")
            if preds == [PART_OF]:
                # self.assertEqual(ancs, [CELL])
                self.assertIn(CELL, ancs)
            elif preds == [IS_A]:
                self.assertNotIn(CELL, ancs)
                self.assertIn(CELLULAR_COMPONENT, ancs)
            else:
                self.assertIn(CELL, ancs)
                self.assertIn(CELLULAR_COMPONENT, ancs)

    @unittest.skip("Timeout")
    def test_most_recent_common_ancestors(self):
        oi = self.oi
        for preds in [[IS_A], [PART_OF], [IS_A, PART_OF]]:
            ancs = list(oi.most_recent_common_ancestors(NUCLEUS, THYLAKOID, preds))
            logging.info(f"{preds} ==> {ancs}")
            if preds == [PART_OF]:
                self.assertEqual(ancs, [CELL])
            elif preds == [IS_A]:
                self.assertNotIn(CELL, ancs)
                self.assertIn(CELLULAR_COMPONENT, ancs)
            else:
                self.assertIn(CELL, ancs)
                self.assertIn(CELLULAR_COMPONENT, ancs)

    @unittest.skip("Error 503: Service Temporarily Unavailable")
    def test_semsim(self):
        """
        Tests semantic similarity

        :return:
        """
        # NOTE: this test may be too rigid and may be better moved to an integration test,
        # some results may not be deterministic
        oi = self.oi
        ic = oi.get_information_content(NEURON)
        self.assertGreater(ic, 2.0)
        pairs = [
            (NUCLEUS, THYLAKOID),
            (NUCLEAR_ENVELOPE, THYLAKOID),
            (NUCLEAR_ENVELOPE, NUCLEUS),
            (NUCLEUS, NUCLEUS),
        ]
        for s, o in pairs:
            for preds in [[IS_A], [IS_A, PART_OF], [PART_OF]]:
                sim = oi.pairwise_similarity(s, o, predicates=preds)
                # logging.info(preds)
                # logging.info(yaml_dumper.dumps(sim))
                if (s, o) == (NUCLEUS, THYLAKOID):
                    if preds == [IS_A]:
                        self.assertEqual(sim.ancestor_id, CELLULAR_ANATOMICAL_ENTITY)
                    elif preds == [PART_OF]:
                        self.assertEqual(sim.ancestor_id, CELL)
                elif (s, o) == (NUCLEAR_ENVELOPE, NUCLEUS):
                    if preds == [IS_A, PART_OF]:
                        assert sim.ancestor_id == NUCLEUS or sim.ancestor_id == INTRACELLULAR
                        # TODO: determine by more specific class is not returned
                        # self.assertEqual(sim.ancestor_id, NUCLEUS)
                elif (s, o) == (NUCLEUS, NUCLEUS):
                    if IS_A in preds:
                        assert sim.ancestor_id == NUCLEUS or sim.ancestor_id == INTRACELLULAR
                        # TODO: determine by more specific class is not returned
                        # self.assertEqual(sim.ancestor_id, NUCLEUS)

    @unittest.skip("HTTP Error 502: Bad Gateway")
    def test_extract_triples(self):
        oi = self.oi
        for t in oi.extract_triples([SHAPE]):
            logging.info(t)
