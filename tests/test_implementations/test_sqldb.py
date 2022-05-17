import logging
import shutil
import unittest

from linkml_runtime.dumpers import yaml_dumper
from oaklib.datamodels.search_datamodel import SearchTermSyntax, SearchProperty
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResultType
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.datamodels.search import SearchConfiguration
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.resource import OntologyResource
from oaklib.utilities.lexical.lexical_indexer import add_labels_from_uris
from oaklib.utilities.obograph_utils import graph_as_dict
from oaklib.datamodels.vocabulary import IS_A, PART_OF, LABEL_PREDICATE, HAS_PART

from tests import OUTPUT_DIR, INPUT_DIR, CELLULAR_COMPONENT, VACUOLE, CYTOPLASM, NUCLEUS, HUMAN, CHEBI_NUCLEUS, \
    NUCLEAR_ENVELOPE, FAKE_PREDICATE, FAKE_ID

DB = INPUT_DIR / 'go-nucleus.db'
SSN_DB = INPUT_DIR / 'ssn.db'
MUTABLE_DB = OUTPUT_DIR / 'go-nucleus.db'
MUTABLE_SSN_DB = OUTPUT_DIR / 'ssn.db'
TEST_OUT = OUTPUT_DIR / 'go-nucleus.saved.owl'
VALIDATION_REPORT_OUT = OUTPUT_DIR / 'validation-results.tsv'


class TestSqlDatabaseImplementation(unittest.TestCase):

    def setUp(self) -> None:
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{str(DB)}'))
        self.oi = oi
        bad_ont = INPUT_DIR / 'bad-ontology.db'
        self.bad_oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{bad_ont}'))
        self.ssn_oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{SSN_DB}'))

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

    def test_mappings(self):
        mappings = list(self.oi.get_sssom_mappings_by_curie(NUCLEUS))
        #for m in mappings:
        #    print(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == 'Wikipedia:Cell_nucleus')
        self.assertEqual(len(mappings), 2)
        for m in mappings:
            reverse_mappings = list(self.oi.get_sssom_mappings_by_curie(m.object_id))
            reverse_subject_ids = [m.subject_id for m in reverse_mappings]
            self.assertEqual(reverse_subject_ids, [NUCLEUS])

    def test_relation_graph(self):
        oi = self.oi
        self.assertEqual(['RO:0002131', 'RO:0002323', 'BFO:0000051', 'rdfs:subClassOf', 'BFO:0000050'],
                         list(oi.entailed_relationships_between(VACUOLE, CELLULAR_COMPONENT)))
        self.assertEqual([IS_A],
                         list(oi.entailed_relationships_between(VACUOLE, VACUOLE)))
        self.assertEqual([],
                         list(oi.entailed_relationships_between(VACUOLE, NUCLEUS)))
        self.assertEqual(['RO:0002323', 'RO:0002131', 'BFO:0000050'],
                         list(oi.entailed_relationships_between(NUCLEAR_ENVELOPE, NUCLEUS)))

    # OboGraphs tests
    def test_obograph_node(self):
        n = self.oi.node(CELLULAR_COMPONENT)
        assert n.id == CELLULAR_COMPONENT
        assert n.lbl == 'cellular_component'
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

    def test_search_aliases(self):
        config = SearchConfiguration(properties=[SearchProperty.ALIAS])
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, ['GO:0003824'])
        config = SearchConfiguration()
        curies = list(self.oi.basic_search("enzyme activity", config=config))
        self.assertEqual(curies, [])

    def test_search_exact(self):
        config = SearchConfiguration(is_partial=False)
        curies = list(self.oi.basic_search("cytoplasm", config=config))
        #print(curies)
        self.assertCountEqual([CYTOPLASM], curies)

    def test_search_partial(self):
        config = SearchConfiguration(is_partial=True)
        curies = list(self.oi.basic_search("nucl", config=config))
        #print(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_search_sql(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.SQL)
        curies = list(self.oi.basic_search("%nucl%s", config=config))
        #print(curies)
        assert NUCLEUS in curies
        self.assertCountEqual([NUCLEUS, CHEBI_NUCLEUS], curies)

    def test_search_starts_with(self):
        config = SearchConfiguration(syntax=SearchTermSyntax.STARTS_WITH)
        curies = list(self.oi.basic_search("nucl", config=config))
        #print(curies)
        assert NUCLEUS in curies
        self.assertGreater(len(curies), 5)

    def test_gap_fill(self):
        oi = self.oi
        # note that HUMAN will be deselected as it is a singleton in the is-a/part-of graph
        rels = list(oi.gap_fill_relationships([NUCLEUS, VACUOLE, CELLULAR_COMPONENT, HUMAN],
                                              predicates=[IS_A, PART_OF]))
        self.assertEqual(len(rels), 4)
        self.assertCountEqual(rels,
                              [('GO:0005773', 'rdfs:subClassOf', 'GO:0005575'),
                               ('GO:0005634', 'rdfs:subClassOf', 'GO:0005575'),
                               ('GO:0005773', 'BFO:0000050', 'GO:0005575'),
                               ('GO:0005634', 'BFO:0000050', 'GO:0005575')])
        # include has-part
        rels = list(oi.gap_fill_relationships([NUCLEUS, VACUOLE, CELLULAR_COMPONENT, HUMAN],
                                              predicates=[IS_A, PART_OF, HAS_PART]))
        self.assertEqual(len(rels), 6)
        self.assertCountEqual(rels,
                              [('GO:0005773', 'rdfs:subClassOf', 'GO:0005575'),
                               ('GO:0005634', 'rdfs:subClassOf', 'GO:0005575'),
                               ('GO:0005773', 'BFO:0000050', 'GO:0005575'),
                               ('GO:0005634', 'BFO:0000050', 'GO:0005575'),
                               ('GO:0005773', 'BFO:0000051', 'GO:0005575'),
                               ('GO:0005634', 'BFO:0000051', 'GO:0005575')])
        # is-a graph of siblings makes singletons
        rels = list(oi.gap_fill_relationships([NUCLEUS, VACUOLE, HUMAN],
                                              predicates=[IS_A, PART_OF, HAS_PART]))
        self.assertEqual(len(rels), 0)
        # trivial edge case - subset using all terms and all predicates
        rels = list(oi.gap_fill_relationships(list(oi.all_entity_curies())))
        all_rels = list(oi.all_relationships())
        #self.assertEqual(len(rels), len(all_rels))
        for rel in rels:
            if rel not in all_rels:
                print(rel)


    def test_set_label(self):
        """
        Tests the SQL store can be modified

        """
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{MUTABLE_DB}'))
        oi.autosave = True
        label = oi.get_label_by_curie(NUCLEUS)
        self.assertEqual("nucleus", label)
        oi.set_label_for_curie(NUCLEUS, "foo")
        label = oi.get_label_by_curie(NUCLEUS)
        self.assertEqual("foo", label)
        oi.save()
        oi.autosave = False
        label = oi.get_label_by_curie(NUCLEUS)
        self.assertEqual("foo", label)
        oi.set_label_for_curie(NUCLEUS, "bar")
        oi.set_label_for_curie(NUCLEAR_ENVELOPE, "baz")
        self.assertNotEqual("bar", oi.get_label_by_curie(NUCLEUS))
        self.assertNotEqual("baz", oi.get_label_by_curie(NUCLEAR_ENVELOPE))
        oi.save()
        self.assertEqual("bar", oi.get_label_by_curie(NUCLEUS))
        self.assertEqual("baz", oi.get_label_by_curie(NUCLEAR_ENVELOPE))
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{MUTABLE_DB}'))
        self.assertEqual("bar", oi.get_label_by_curie(NUCLEUS))
        self.assertEqual("baz", oi.get_label_by_curie(NUCLEAR_ENVELOPE))

    def test_set_labels_from_iris(self):
        """
        Test ability to generate labels for a semweb-style ontology
        """
        shutil.copyfile(SSN_DB, MUTABLE_SSN_DB)
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{MUTABLE_SSN_DB}'))
        no_label_curies = []
        for curie in oi.all_entity_curies():
            label = oi.get_label_by_curie(curie)
            #print(f'{curie}: {label}')
            if label is None:
                no_label_curies.append(curie)
        oi.autosave = True
        add_labels_from_uris(oi)
        oi.save()
        for curie in no_label_curies:
            label = oi.get_label_by_curie(curie)
            print(f'XXX {curie}: {label}')
            #self.assertIsNotNone(label)

    def test_migrate_curies(self):
        """
        Tests the SQL store can be modified
        """
        shutil.copyfile(DB, MUTABLE_DB)
        oi = SqlImplementation(OntologyResource(slug=f'sqlite:///{MUTABLE_DB}'))
        label = oi.get_label_by_curie(NUCLEUS)
        preds = [IS_A, PART_OF]
        preds2 = [IS_A, FAKE_PREDICATE]
        ancestors = list(oi.ancestors(NUCLEUS, predicates=preds))
        descendants = list(oi.descendants(NUCLEUS, predicates=preds))
        def non_reflexive(l):
            return [a for a in ancestors if a != NUCLEUS and a != PART_OF and a != FAKE_PREDICATE]
        expected_ancs = non_reflexive(ancestors)
        descendants_ancs = non_reflexive(descendants)
        oi.migrate_curies({NUCLEUS: FAKE_ID,
                           PART_OF: FAKE_PREDICATE})
        oi.save()
        self.assertEqual(label, oi.get_label_by_curie(FAKE_ID))
        self.assertIsNone(oi.get_label_by_curie(NUCLEUS))
        self.assertCountEqual(expected_ancs, non_reflexive(oi.ancestors(FAKE_ID, predicates=preds2)))
        self.assertCountEqual([], list(oi.ancestors(NUCLEUS, predicates=preds)))
        self.assertCountEqual(descendants_ancs, non_reflexive(oi.descendants(FAKE_ID, predicates=preds2)))
        self.assertCountEqual([], list(oi.descendants(NUCLEUS, predicates=preds)))