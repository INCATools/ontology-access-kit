import logging
import tempfile
import unittest
from pathlib import Path

from kgcl_schema.datamodel import kgcl
from oaklib.datamodels.search import SearchConfiguration, SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import AxiomFilter
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from pyhornedowl.model import EquivalentClasses, SubClassOf

from tests import BIOLOGICAL_PROCESS, CHEBI_NUCLEUS, HUMAN, INPUT_DIR, NUCLEUS, VACUOLE
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.ofn"
TEST_GRAPH_PROJECTION_ONT = INPUT_DIR / "graph_projection.owl"
TEST_INST_ONT = INPUT_DIR / "inst.ofn"
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

    def test_relationships(self):
        self.compliance_tester.test_relationships(self.oi)

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
