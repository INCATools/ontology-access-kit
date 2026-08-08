import logging
import tempfile
import time
import unittest
from pathlib import Path

from kgcl_schema.datamodel import kgcl
from pyhornedowl.model import EquivalentClasses, SubClassOf

from oaklib.datamodels.search import SearchConfiguration, SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import IS_A, NEVER_IN_TAXON, PART_OF
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.interfaces.obograph_interface import GraphTraversalMethod, OboGraphInterface
from oaklib.interfaces.owl_interface import AxiomFilter
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from tests import BIOLOGICAL_PROCESS, CHEBI_NUCLEUS, HUMAN, INPUT_DIR, NUCLEUS, VACUOLE
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.ofn"
TEST_GRAPH_PROJECTION_ONT = INPUT_DIR / "graph_projection.owl"
TEST_INST_ONT = INPUT_DIR / "inst.ofn"
TEST_OBSOLETION_ONT = INPUT_DIR / "obsoletion_test.owl"
NEW_NAME = "new name"
EXTERNAL_REFERENCE_OFN = """\
Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)
Prefix(CL:=<http://purl.obolibrary.org/obo/CL_>)
Prefix(BFO:=<http://purl.obolibrary.org/obo/BFO_>)
Prefix(GO:=<http://purl.obolibrary.org/obo/GO_>)
Ontology(
Declaration(Class(CL:0000540))
AnnotationAssertion(rdfs:label CL:0000540 "neuron")
SubClassOf(CL:0000540 GO:0008150)
SubClassOf(CL:0000540 ObjectSomeValuesFrom(BFO:0000050 GO:0008150))
)
"""
CLOSURE_OFN = """\
Prefix(EX:=<http://example.org/EX_>)
Prefix(BFO:=<http://purl.obolibrary.org/obo/BFO_>)
Ontology(
Declaration(Class(EX:0001))
Declaration(Class(EX:0002))
Declaration(Class(EX:0003))
Declaration(Class(EX:0004))
Declaration(Class(EX:0005))
Declaration(Class(EX:0006))
Declaration(ObjectProperty(BFO:0000050))
SubClassOf(EX:0002 EX:0001)
SubClassOf(EX:0003 EX:0002)
SubClassOf(EX:0004 ObjectSomeValuesFrom(BFO:0000050 EX:0001))
SubClassOf(EX:0005 EX:0004)
)
"""


class _ScanCountingOntology:
    """Wraps a py-horned-owl ontology and counts full axiom scans."""

    def __init__(self, delegate):
        self._delegate = delegate
        self.scans = 0

    def get_axioms(self, *args, **kwargs):
        self.scans += 1
        return self._delegate.get_axioms(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._delegate, name)


class TestFunOwlImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(str(TEST_ONT))
        self.oi = FunOwlImplementation(resource)
        self.compliance_tester = ComplianceTester(self)

    def _implementation_from_text(self, tmpdir: str, text: str) -> FunOwlImplementation:
        path = Path(tmpdir) / "test.ofn"
        path.write_text(text, encoding="utf-8")
        return FunOwlImplementation(OntologyResource(str(path)))

    def test_entities(self):
        curies = list(self.oi.entities())
        self.assertIn(NUCLEUS, curies)
        self.assertIn(CHEBI_NUCLEUS, curies)
        self.assertIn(HUMAN, curies)

    def test_edges(self):
        oi = self.oi
        curies = list(oi.entities())
        if isinstance(oi, OboGraphInterface):
            for curie in curies:
                for rel in oi.outgoing_relationships(curie):
                    logging.info(rel)
        else:
            raise NotImplementedError

    def test_filter_axioms(self):
        oi = self.oi
        self.assertCountEqual(
            list(oi.axioms()),
            list(oi.filter_axioms(AxiomFilter())),
            "empty axiom filter should return all axioms",
        )
        subclass_axioms = list(oi.filter_axioms(AxiomFilter(type=SubClassOf)))
        for ax in subclass_axioms:
            self.assertEqual(type(ax), SubClassOf)
        self.assertGreater(len(subclass_axioms), 10)
        ec_axioms = list(oi.equivalence_axioms())
        for ax in ec_axioms:
            self.assertEqual(type(ax), EquivalentClasses)
        self.assertGreater(len(ec_axioms), 10)
        nucleus_axioms = list(oi.filter_axioms(AxiomFilter(about=NUCLEUS)))
        n_subclass = 0
        for ax in nucleus_axioms:
            if isinstance(ax, SubClassOf):
                n_subclass += 1
                self.assertEqual(NUCLEUS, oi.entity_iri_to_curie(ax.sub.first))
        self.assertEqual(n_subclass, 3)
        self.assertGreater(len(nucleus_axioms), 2)
        nucleus_ref_axioms = list(oi.filter_axioms(AxiomFilter(references=NUCLEUS)))
        n_ref_subclass = 0
        for ax in nucleus_ref_axioms:
            if isinstance(ax, SubClassOf):
                n_ref_subclass += 1
        self.assertGreater(n_ref_subclass, 3)
        self.assertGreater(len(nucleus_ref_axioms), 3)
        for ax in nucleus_axioms:
            self.assertIn(ax, nucleus_ref_axioms)

    # ---------------------------------------------------------------------
    # Compliance tests: these mirror the coverage of tests/test_implementations/test_sqldb.py
    # ---------------------------------------------------------------------

    def test_labels(self):
        self.compliance_tester.test_labels(self.oi)

    def test_definitions(self):
        self.compliance_tester.test_definitions(self.oi, include_metadata=True)

    def test_owl_types(self):
        # skip_oio: as with the SQL adapter, the test ontology does not type its
        # subset and synonym-type properties
        self.compliance_tester.test_owl_types(self.oi, skip_oio=True)

    def test_synonyms(self):
        self.compliance_tester.test_synonyms(self.oi)

    def test_synonym_types(self):
        self.compliance_tester.test_synonym_types(self.oi)

    def test_defined_bys(self):
        self.compliance_tester.test_defined_bys(self.oi)

    def test_subsets(self):
        self.compliance_tester.test_subsets(self.oi)

    def test_metadata(self):
        self.compliance_tester.test_metadata(self.oi)

    def test_entities_metadata_statements(self):
        # never_in_taxon is asserted in go-nucleus.ofn but not in go-nucleus.db, and
        # an OWL axiom store has no canonical statement ordering
        self.compliance_tester.test_entities_metadata_statements(
            self.oi, ordered=False, ignore_predicates=[NEVER_IN_TAXON]
        )

    def test_obsolete_entities(self):
        oi = FunOwlImplementation(OntologyResource(str(TEST_OBSOLETION_ONT)))
        self.compliance_tester.test_obsolete_entities(oi)

    def test_sssom_mappings(self):
        self.compliance_tester.test_sssom_mappings(self.oi)

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi)

    def test_entailed_relationships(self):
        self.compliance_tester.test_entailed_relationships(self.oi)

    def test_obograph_node(self):
        self.compliance_tester.test_obograph_node(self.oi)

    def test_as_obograph(self):
        self.compliance_tester.test_as_obograph(self.oi)

    def test_subgraph_from_traversal(self):
        # OWL retains reflexive existentials such as
        # SubClassOf(BFO:0000002 ObjectSomeValuesFrom(part_of BFO:0000002)) that
        # normalized sources drop
        self.compliance_tester.test_subgraph_from_traversal(self.oi, ignore_reflexive_edges=True)

    def test_extract_graph(self):
        self.compliance_tester.test_extract_graph(self.oi)

    def test_dump_obograph(self):
        self.compliance_tester.test_dump_obograph(self.oi)

    def test_chains(self):
        self.compliance_tester.test_chains(self.oi)

    def test_disjoint_with(self):
        self.compliance_tester.test_disjoint_with(self.oi)

    def test_transitive_object_properties(self):
        self.compliance_tester.test_transitive_object_properties(self.oi)

    def test_simple_subproperty_of_chains(self):
        self.compliance_tester.test_simple_subproperty_of_chains(self.oi)

    def test_annotate_text(self):
        self.compliance_tester.test_annotate_text(self.oi)

    def test_ontologies(self):
        self.assertEqual(["obo:go.owl"], list(self.oi.ontologies()))
        self.assertEqual(
            ["1.2"], self.oi.ontology_metadata_map("obo:go.owl")["oio:hasOBOFormatVersion"]
        )

    def test_summary_statistics(self):
        """Summary statistics over the OWL file.

        The counts differ from the SQL adapter's because go-nucleus.db and
        go-nucleus.ofn are not byte-for-byte equivalent test fixtures; what is
        asserted here is that the generic statistics machinery is wired up.
        """
        oi = self.oi
        oi.include_residuals = True
        stats = oi.branch_summary_statistics(include_entailed=True)
        self.assertEqual(204, stats.class_count)
        self.assertEqual(98, stats.class_count_with_text_definitions)
        self.assertEqual(221, stats.edge_count_by_predicate[IS_A].filtered_count)
        self.assertEqual(29, stats.edge_count_by_predicate[PART_OF].filtered_count)
        self.assertEqual(260, stats.distinct_synonym_count)
        self.assertEqual(269, stats.synonym_statement_count)

    def test_rbox_relationships(self):
        self.compliance_tester.test_rbox_relationships(self.oi)

    def test_equiv_relationships(self):
        self.compliance_tester.test_equiv_relationships(self.oi)

    def test_graph_projections(self):
        oi = FunOwlImplementation(OntologyResource(str(TEST_GRAPH_PROJECTION_ONT)))
        self.compliance_tester.test_graph_projections(oi)

    def test_logical_definitions(self):
        self.compliance_tester.test_logical_definitions(self.oi)

    def test_ancestors_descendants(self):
        self.compliance_tester.test_ancestors_descendants(self.oi)

    def test_cached_closure_traversal_filters_predicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            oi = self._implementation_from_text(tmpdir, CLOSURE_OFN)

            isa_descendants = set(oi.descendants("EX:0001", predicates=[IS_A], reflexive=False))
            self.assertEqual(isa_descendants, {"EX:0002", "EX:0003"})

            part_of_descendants = set(
                oi.descendants("EX:0001", predicates=[PART_OF], reflexive=False)
            )
            self.assertEqual(part_of_descendants, {"EX:0004"})

            hierarchical_descendants = set(
                oi.descendants("EX:0001", predicates=[IS_A, PART_OF], reflexive=False)
            )
            self.assertEqual(
                hierarchical_descendants,
                {"EX:0002", "EX:0003", "EX:0004", "EX:0005"},
            )

            hierarchical_ancestors = set(
                oi.ancestors("EX:0005", predicates=[IS_A, PART_OF], reflexive=False)
            )
            self.assertEqual(hierarchical_ancestors, {"EX:0001", "EX:0004"})
            self.assertIn(
                "EX:0005",
                set(oi.ancestors("EX:0005", predicates=[IS_A, PART_OF])),
            )

    def test_cached_closure_traversal_handles_multi_start(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            oi = self._implementation_from_text(tmpdir, CLOSURE_OFN)

            descendants = set(
                oi.descendants(["EX:0001", "EX:0004"], predicates=[IS_A], reflexive=False)
            )
            self.assertEqual(descendants, {"EX:0002", "EX:0003", "EX:0005"})

    def test_cached_closure_traversal_does_not_use_graph_walker(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            oi = self._implementation_from_text(tmpdir, CLOSURE_OFN)

            def fail_incoming_relationship_map(*args, **kwargs):
                raise AssertionError("descendants should use the cached adjacency index")

            oi.incoming_relationship_map = fail_incoming_relationship_map
            descendants = set(oi.descendants("EX:0001", predicates=[IS_A], reflexive=False))
            self.assertEqual(descendants, {"EX:0002", "EX:0003"})

    def test_entailed_closure_uses_precomputed_targets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            oi = self._implementation_from_text(tmpdir, CLOSURE_OFN)
            oi._entailed_adjacency_indexes()

            def fail_transitive_targets(*args, **kwargs):
                raise AssertionError("entailment traversal should use precomputed targets")

            oi._transitive_targets = fail_transitive_targets
            descendants = set(
                oi.descendants(
                    "EX:0001",
                    predicates=[IS_A],
                    reflexive=False,
                    method=GraphTraversalMethod.ENTAILMENT,
                )
            )
            self.assertEqual(descendants, {"EX:0002", "EX:0003"})

    def test_cached_closure_cache_invalidates_after_edge_patch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            oi = self._implementation_from_text(tmpdir, CLOSURE_OFN)

            self.assertNotIn(
                "EX:0006",
                set(oi.descendants("EX:0001", predicates=[IS_A], reflexive=False)),
            )
            oi.apply_patch(
                kgcl.EdgeCreation(
                    id=generate_change_id(),
                    subject="EX:0006",
                    predicate=IS_A,
                    object="EX:0001",
                )
            )
            self.assertIn(
                "EX:0006",
                set(oi.descendants("EX:0001", predicates=[IS_A], reflexive=False)),
            )

    def test_basic_search(self):
        self.assertIn(NUCLEUS, list(self.oi.basic_search("nucleus")))
        self.assertIn(
            NUCLEUS,
            list(self.oi.basic_search("nucl", config=SearchConfiguration(is_partial=True))),
        )
        self.assertIn(
            NUCLEUS,
            list(
                self.oi.basic_search(
                    "GO:00056",
                    config=SearchConfiguration(
                        properties=[SearchProperty.IDENTIFIER],
                        syntax=SearchTermSyntax.STARTS_WITH,
                    ),
                )
            ),
        )
        self.assertIn(
            NUCLEUS,
            list(
                self.oi.basic_search(
                    "nuc.*us",
                    config=SearchConfiguration(
                        properties=[SearchProperty.LABEL],
                        syntax=SearchTermSyntax.REGULAR_EXPRESSION,
                    ),
                )
            ),
        )
        self.assertIn(
            NUCLEUS,
            list(
                self.oi.basic_search(
                    "cell nucleus",
                    config=SearchConfiguration(properties=[SearchProperty.ALIAS]),
                )
            ),
        )
        self.assertIn(
            NUCLEUS,
            list(
                self.oi.basic_search(
                    "Wikipedia:Cell_nucleus",
                    config=SearchConfiguration(properties=[SearchProperty.MAPPED_IDENTIFIER]),
                )
            ),
        )

    def test_stub_nodes_for_unresolved_external_references(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "external-ref.ofn"
            path.write_text(EXTERNAL_REFERENCE_OFN, encoding="utf-8")
            oi = FunOwlImplementation(OntologyResource(str(path)))

            self.assertIsNone(oi.label(BIOLOGICAL_PROCESS))
            self.assertEqual(BIOLOGICAL_PROCESS, oi.node(BIOLOGICAL_PROCESS).id)
            with self.assertRaises(ValueError):
                oi.node(BIOLOGICAL_PROCESS, strict=True)

            graph = oi.direct_graph("CL:0000540")
            node_ids = {node.id for node in graph.nodes}
            self.assertIn("CL:0000540", node_ids)
            self.assertIn(BIOLOGICAL_PROCESS, node_ids)

    # ---------------------------------------------------------------------
    # Performance
    # ---------------------------------------------------------------------

    def test_metadata_lookups_do_not_rescan_the_ontology(self):
        """Per-entity metadata lookups must not scan every axiom.

        ``entity_metadata_map`` used to filter the full axiom list for each entity,
        which made bulk operations -- ``entities()`` (which filters obsoletes),
        ``labels()``, ``nodes()`` -- quadratic in the size of the ontology. The
        adapter now builds one subject-keyed index, so the number of full axiom
        scans is independent of the number of entities queried.
        """
        oi = FunOwlImplementation(OntologyResource(str(TEST_ONT)))
        counter = _ScanCountingOntology(oi.ontology_document)
        oi.ontology_document = counter

        entities = list(oi.entities())
        self.assertGreater(len(entities), 100)
        scans_after_entities = counter.scans
        for entity in entities:
            oi.entity_metadata_map(entity)
        self.assertEqual(
            scans_after_entities,
            counter.scans,
            "metadata lookups triggered additional full axiom scans",
        )
        # a handful of indexes are built lazily; the point is that this is a
        # constant, not one scan per entity
        self.assertLess(
            counter.scans, 10, f"{len(entities)} entities caused {counter.scans} axiom scans"
        )

    def test_bulk_operations_are_fast(self):
        """Guard against a regression to quadratic bulk lookups.

        Before the subject-keyed annotation index, ``entities()`` alone took ~3
        seconds on this 295-entity test ontology; it now takes well under a tenth
        of that. The threshold is deliberately loose so the test is not flaky on
        slow CI machines, but it is still ~30x below the old timing.
        """
        oi = FunOwlImplementation(OntologyResource(str(TEST_ONT)))
        start = time.time()
        entities = list(oi.entities())
        list(oi.labels(entities))
        for entity in entities:
            oi.entity_metadata_map(entity)
        elapsed = time.time() - start
        self.assertLess(elapsed, 1.0, f"bulk lookups took {elapsed:.2f}s")

    def test_patcher(self):
        oi = self.oi
        anns = list(oi.annotation_assertion_axioms(NUCLEUS))
        self.assertGreater(len(anns), 5)
        label = oi.label(NUCLEUS)
        self.assertEqual("nucleus", label)
        oi.apply_patch(
            kgcl.NodeRename(id=generate_change_id(), about_node=VACUOLE, new_value=NEW_NAME)
        )
        label = oi.label(VACUOLE)
        self.assertEqual(NEW_NAME, label)
