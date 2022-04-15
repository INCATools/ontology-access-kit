import logging
import unittest

import yaml
from oaklib.implementations.aggregator.aggregator_implementation import AggregatorImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.datamodels.vocabulary import IS_A, PART_OF, HAS_PART

from tests import OUTPUT_DIR, INPUT_DIR, VACUOLE, CYTOPLASM, CELLULAR_COMPONENT
from tests.test_cli import NUCLEUS, INTERNEURON

TEST_ONT = INPUT_DIR / 'go-nucleus.obo'
TEST_ONT2 = INPUT_DIR / 'interneuron.obo'


class TestAggregator(unittest.TestCase):
    """
    Tests the ability to wrap multiple implementations as if it were a single source
    """

    def setUp(self) -> None:
        resource1 = OntologyResource(slug='go-nucleus.obo', directory=INPUT_DIR, local=True)
        resource2 = OntologyResource(slug='interneuron.obo', directory=INPUT_DIR, local=True)
        oi1 = ProntoImplementation(resource1)
        oi2 = ProntoImplementation(resource2)
        self.oi = AggregatorImplementation(implementations=[oi1, oi2])

    def test_all_terms(self):
        curies = list(self.oi.all_entity_curies())
        self.assertIn(NUCLEUS, curies)
        self.assertIn(INTERNEURON, curies)

    def test_relations(self):
        oi = self.oi
        label = oi.get_label_by_curie(PART_OF)
        assert label.startswith('part')
        t = self.oi.node(PART_OF)
        assert t.id == PART_OF
        assert t.label.startswith('part')

    @unittest.skip('TODO')
    def test_metadata(self):
        for curie in self.oi.all_entity_curies():
            m = self.oi.metadata_map_by_curie(curie)
            print(f'{curie} {m}')
        m = self.oi.metadata_map_by_curie('GO:0005622')
        assert 'term_tracker_item' in m.keys()
        assert 'https://github.com/geneontology/go-ontology/issues/17776' in m['term_tracker_item']

    def test_labels(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        :return:
        """
        oi = self.oi
        label = oi.get_label_by_curie(VACUOLE)
        self.assertEqual(str,  type(label))
        self.assertEqual(label, 'vacuole')
        label = oi.get_label_by_curie('FOOBAR:123')
        self.assertIsNone(label)
        # TODO: test strict mode
        label = oi.get_label_by_curie(IS_A)
        self.assertIsNotNone(label)
        self.assertEqual('interneuron', oi.get_label_by_curie(INTERNEURON))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        self.assertCountEqual(syns, ['cellular_component',
                                    'cellular component',
                                    'cell or subcellular entity',
                                    'subcellular entity'])
        syns = self.oi.aliases_by_curie('CL:0000100')
        self.assertCountEqual(syns, ['motoneuron', 'motor neuron'])

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.all_subset_curies())
        self.assertIn('goslim_aspergillus', subsets)
        self.assertIn('GO:0003674', oi.curies_by_subset('goslim_generic'))
        self.assertNotIn('GO:0003674', oi.curies_by_subset('gocheck_do_not_manually_annotate'))









