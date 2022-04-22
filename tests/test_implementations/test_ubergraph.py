import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper
from oaklib.implementations.ubergraph.ubergraph_implementation import UbergraphImplementation
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR, VACUOLE, DIGIT, CYTOPLASM, CELLULAR_COMPONENT, CELL, SHAPE, NEURON, \
    PHOTORECEPTOR_OUTER_SEGMENT

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'

ICMBO = 'GO:0043231'

@unittest.skip('Server down')
class TestUbergraphImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = UbergraphImplementation()
        self.oi = oi

    def test_relationships(self):
        ont = self.oi
        rels = ont.get_outgoing_relationships_by_curie(VACUOLE)
        for k, v in rels.items():
            logging.info(f'{k} = {v}')
        self.assertIn('GO:0043231', rels[IS_A])
        self.assertIn(CYTOPLASM, rels[PART_OF])

    def test_entailed_relationships(self):
        ont = self.oi
        rels = list(ont.entailed_outgoing_relationships_by_curie(VACUOLE))
        for rel in rels:
            print(rel)
        self.assertIn((IS_A, VACUOLE), rels)
        self.assertIn((IS_A, ICMBO), rels)
        self.assertIn((IS_A, CELLULAR_COMPONENT), rels)
        self.assertIn((PART_OF, CYTOPLASM), rels)
        self.assertIn((PART_OF, CELL), rels)

    def test_labels(self):
        label = self.oi.get_label_by_curie(DIGIT)
        self.assertEqual(label, 'digit')
        self.assertIn(DIGIT, self.oi.get_curies_by_label(label))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        logging.info(syns)
        assert 'cellular component' in syns

    def test_definition(self):
        defn = self.oi.get_definition_by_curie('GO:0005575')
        logging.info(defn)
        assert defn

    #@unittest.skip('Too slow')
    def test_search(self):
        config = SearchConfiguration(complete=True).use_label_only()
        curies = list(self.oi.basic_search('limb', config=config))
        print(curies)
        assert 'UBERON:0002101' in curies

    # OboGraph

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors([VACUOLE]))
        #for a in ancs:
        #    print(a)
        self.assertIn(VACUOLE, ancs)
        self.assertIn(CYTOPLASM, ancs)
        self.assertIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A]))
        #for a in ancs:
        #    print(a)
        self.assertIn(VACUOLE, ancs)
        self.assertNotIn(CYTOPLASM, ancs)
        self.assertNotIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A, PART_OF]))
        #for a in ancs:
        #    print(a)
        self.assertIn(VACUOLE, ancs)
        self.assertIn(CYTOPLASM, ancs)
        self.assertIn(CELL, ancs)
        self.assertIn(CELLULAR_COMPONENT, ancs)

    def test_descendants(self):
        oi = self.oi
        descs = list(oi.descendants([CYTOPLASM]))
        #for a in descs:
        #    print(a)
        self.assertIn(VACUOLE, descs)
        self.assertIn(CYTOPLASM, descs)
        descs = list(oi.descendants([CYTOPLASM], predicates=[IS_A]))
        #for a in descs:
        #    print(f'IS_A DESC: {a}')
        self.assertIn(CYTOPLASM, descs)
        self.assertNotIn(VACUOLE, descs)

    def test_ancestor_graph(self):
        oi = self.oi
        for preds in [None, [IS_A], [IS_A, PART_OF]]:
            g = oi.ancestor_graph([VACUOLE], predicates=preds)
            #print(yaml_dumper.dumps(g))
            assert len(g.nodes) > 0
            assert len(g.edges) > 0
            node_ids = [n.id for n in g.nodes]
            edges = [(e.sub, e.pred, e.obj) for e in g.edges]
            assert VACUOLE in node_ids
            assert CELLULAR_COMPONENT in node_ids
            if preds == [IS_A]:
                assert CELL not in node_ids
            else:
                assert CELL in node_ids

    def test_gap_fill(self):
        oi = self.oi
        rels = list(oi.gap_fill_relationships([NEURON, PHOTORECEPTOR_OUTER_SEGMENT], predicates=[IS_A, PART_OF]))
        for rel in rels:
            print(rel)

    def test_extract_triples(self):
        oi = self.oi
        for t in oi.extract_triples([SHAPE]):
            print(t)
