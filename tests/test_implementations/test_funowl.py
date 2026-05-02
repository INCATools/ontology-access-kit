import logging
import unittest

from kgcl_schema.datamodel import kgcl
from pyhornedowl.model import EquivalentClasses, SubClassOf

from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import AxiomFilter
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import generate_change_id
from tests import CHEBI_NUCLEUS, HUMAN, INPUT_DIR, NUCLEUS, VACUOLE
from tests.test_implementations import ComplianceTester

TEST_ONT = INPUT_DIR / "go-nucleus.ofn"
TEST_GRAPH_PROJECTION_ONT = INPUT_DIR / "graph_projection.owl"
TEST_INST_ONT = INPUT_DIR / "inst.ofn"
NEW_NAME = "new name"


class TestFunOwlImplementation(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(str(TEST_ONT))
        self.oi = FunOwlImplementation(resource)
        self.compliance_tester = ComplianceTester(self)

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
