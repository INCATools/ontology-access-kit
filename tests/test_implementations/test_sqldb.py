import logging
import unittest

import yaml
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from tests import OUTPUT_DIR, INPUT_DIR, CELLULAR_COMPONENT, VACUOLE, CYTOPLASM

DB = INPUT_DIR / 'go-nucleus.db'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'


class TestSqlDatabaseImplementation(unittest.TestCase):

    def setUp(self) -> None:
        print(f'DB={str(DB)}')
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{str(DB)}'))
        self.oi = oi

    def test_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationships_by_curie(VACUOLE)
        for k, v in rels.items():
            print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ['GO:0043231'])
        self.assertCountEqual(rels[PART_OF], ['GO:0005737'])

    def test_all_nodes(self):
        for curie in self.oi.all_entity_curies():
            print(curie)

    def test_labels(self):
        label = self.oi.get_label_by_curie(VACUOLE)
        self.assertEqual(label, 'vacuole')

    def test_get_labels_for_curies(self):
        oi = self.oi
        curies = oi.curies_by_subset('goslim_generic')
        tups = list(oi.get_labels_for_curies(curies))
        for curie, label in tups:
            print(f'{curie} ! {label}')
        assert (VACUOLE, 'vacuole') in tups
        assert (CYTOPLASM, 'cytoplasm') in tups
        self.assertEqual(11, len(tups))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        print(syns)
        assert 'cellular component' in syns

    # OboGraphs tests
    def test_obograph_node(self):
        n = self.oi.node(CELLULAR_COMPONENT)
        assert n.id == CELLULAR_COMPONENT
        assert n.label == 'cellular_component'
        assert n.meta.definition.val.startswith('A location, ')

    def test_obograph(self):
        g = self.oi.ancestor_graph(VACUOLE)
        obj = graph_as_dict(g)
        #print(yaml.dump(obj))
        assert g.nodes
        assert g.edges

    def test_descendants(self):
        curies = list(self.oi.descendants(CELLULAR_COMPONENT))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants([CELLULAR_COMPONENT]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants(CELLULAR_COMPONENT, predicates=[IS_A]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A]))
        assert CELLULAR_COMPONENT not in curies
        assert VACUOLE not in curies
        assert CYTOPLASM in curies

    def test_ancestors(self):
        curies = list(self.oi.ancestors(VACUOLE))
        for curie in curies:
            print(curie)
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.ancestors([VACUOLE]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM in curies
        curies = list(self.oi.ancestors(VACUOLE, predicates=[IS_A]))
        assert CELLULAR_COMPONENT in curies
        assert VACUOLE in curies
        assert CYTOPLASM not in curies



    # QC
    def test_no_definitions(self):
        missing = list(self.oi.term_curies_without_definitions())
        for curie in missing:
            logging.info(curie)
        assert 'CHEBI:36357' in missing
        assert CELLULAR_COMPONENT not in missing

    def test_search(self):
        oi = self.oi
        for curie in oi.basic_search('intracellular'):
            print(curie)
        self.assertIn('GO:0005622', oi.basic_search('intracellular'))
        self.assertEqual(list(oi.basic_search('protoplasm')), ['GO:0005622'])
        self.assertEqual(list(oi.basic_search('protoplasm', SearchConfiguration(include_aliases=False))), [])
