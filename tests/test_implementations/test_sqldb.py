import logging
import unittest

import yaml
from linkml_runtime.dumpers import yaml_dumper
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResultType
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.datamodels.vocabulary import IS_A, PART_OF, LABEL_PREDICATE

from tests import OUTPUT_DIR, INPUT_DIR, CELLULAR_COMPONENT, VACUOLE, CYTOPLASM

DB = INPUT_DIR / 'go-nucleus.db'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'
VALIDATION_REPORT_OUT = OUTPUT_DIR / 'validation-results.tsv'


class TestSqlDatabaseImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{str(DB)}'))
        self.oi = oi
        bad_ont = INPUT_DIR / 'bad-ontology.db'
        self.bad_oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{bad_ont}'))

    def test_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationships_by_curie(VACUOLE)
        self.assertCountEqual(rels[IS_A], ['GO:0043231'])
        self.assertCountEqual(rels[PART_OF], ['GO:0005737'])
        self.assertCountEqual([IS_A, PART_OF], rels)

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

    def test_validate(self):
        oi = self.bad_oi
        results = list(oi.validate())
        with open(VALIDATION_REPORT_OUT, 'w', encoding='utf-8') as stream:
            writer = StreamingCsvWriter(stream)
            for r in results:
                writer.emit(r)
        invalid_ids = set([r.subject for r in results if str(r.severity) == SeverityOptions.ERROR.text])
        problem_ids = set([r.subject for r in results if str(r.severity)])
        logging.info(f'INVALID: {invalid_ids}')
        logging.info(f'PROBLEM: {problem_ids}')
        assert not any(r for r in results if
                       r.subject == 'EXAMPLE:1' and
                       str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning)
        assert not any(r for r in results if
                       r.subject == 'EXAMPLE:8' and
                       str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning and
                       str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:6' and r.predicate == 'obo:TEMP#made_up_object_property' and
                   str(r.type) == ValidationResultType.ClosedConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:6' and r.predicate == 'obo:TEMP#made_up_data_property' and
                   str(r.type) == ValidationResultType.ClosedConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:1' and r.predicate == LABEL_PREDICATE and
                   str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:1' and r.predicate == 'IAO:0000115' and
                   str(r.type) == ValidationResultType.MinCountConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.WARNING.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:2' and r.predicate == LABEL_PREDICATE and
                   str(r.type) == ValidationResultType.MaxCountConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:7' and r.predicate == 'owl:deprecated' and
                   str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:8' and r.predicate == 'skos:exactMatch' and
                   str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        assert any(r for r in results if
                   r.subject == 'EXAMPLE:9' and r.predicate == 'rdfs:label' and
                   str(r.type) == ValidationResultType.DatatypeConstraintComponent.meaning and
                   str(r.severity) == SeverityOptions.ERROR.text)
        self.assertEqual(6, len(invalid_ids))
        self.assertCountEqual({'EXAMPLE:1', 'EXAMPLE:2', 'EXAMPLE:8', 'EXAMPLE:4', 'EXAMPLE:5', 'EXAMPLE:7',
                               'EXAMPLE:6', 'EXAMPLE:9'}, problem_ids)


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
