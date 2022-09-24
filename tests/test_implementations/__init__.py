import json
import logging
import unittest
from dataclasses import dataclass
from typing import Callable

from kgcl_schema.datamodel import kgcl
from kgcl_schema.datamodel.kgcl import Change, NodeObsoletion
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.dumpers import json_dumper

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import (
    EQUIVALENT_CLASS,
    IS_A,
    NEVER_IN_TAXON,
    ONLY_IN_TAXON,
    PART_OF,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.utilities.kgcl_utilities import generate_change_id
from tests import (
    CELL,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    EUKARYOTA,
    HUMAN,
    IMBO,
    MAMMALIA,
    NUCLEUS,
    SUBATOMIC_PARTICLE,
    VACUOLE,
)


def _as_json_dict_no_id(change: Change) -> dict:
    obj = json.loads(json_dumper.dumps(change, inject_type=True))
    del obj["id"]
    return obj


@dataclass
class ComplianceTester:
    """
    Tests for compliance against expected behavior
    """

    test: unittest.TestCase
    """Link back to the calling test"""

    def test_relationships(self, oi: BasicOntologyInterface, ignore_annotation_edges=False):
        """
        Tests relationship methods for compliance

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (NUCLEUS, False, [(NUCLEUS, IS_A, IMBO), (NUCLEUS, ONLY_IN_TAXON, EUKARYOTA)]),
            (VACUOLE, True, [(VACUOLE, IS_A, IMBO), (VACUOLE, PART_OF, CYTOPLASM)]),
            (SUBATOMIC_PARTICLE, True, []),
            (HUMAN, True, [(HUMAN, IS_A, MAMMALIA)]),
            (CELL, True, [(CELL, IS_A, "CARO:0000003"), (CELL, ONLY_IN_TAXON, CELLULAR_ORGANISMS)]),
            (CELLULAR_COMPONENT, True, [(CELLULAR_COMPONENT, IS_A, "BFO:0000040")]),
        ]
        for curie, complete, expected_rels in cases:
            print(f"TESTS FOR {curie}")
            if ignore_annotation_edges:
                expected_rels = [r for r in expected_rels if r[1] != NEVER_IN_TAXON]
            rels = list(oi.relationships([curie]))
            preds = set()
            for rv in expected_rels:
                test.assertIn(rv, rels)
                preds.add(rv[1])
            if complete:
                test.assertCountEqual(expected_rels, rels)
            rels = list(oi.relationships([curie], predicates=list(preds)))
            test.assertCountEqual(expected_rels, rels)
            for p in preds:
                for rel in oi.relationships([curie], predicates=[p]):
                    test.assertIn(rel, expected_rels)
                for r, o in oi.outgoing_relationships(curie, predicates=[p]):
                    test.assertIn((curie, r, o), expected_rels)
            # test reverse
            for s, p, o in expected_rels:
                expected_rel = s, p, o
                rels = list(oi.relationships(None, None, [o]))
                test.assertIn(expected_rel, rels)
                rels = list(oi.relationships(None, [p], [o]))
                test.assertIn(expected_rel, rels)
                rels = list(oi.relationships([s], [p], [o]))
                test.assertEqual([expected_rel], rels)
                irels = list(oi.incoming_relationships(o, predicates=[p]))
                test.assertIn((p, s), irels)

    def test_equiv_relationships(self, oi: BasicOntologyInterface):
        """
        Tests equivalence relationship methods for compliance

        :param oi:
        :return:
        """
        test = self.test
        pairs = [("BFO:0000023", "CHEBI:50906")]
        for c1, c2 in pairs:
            for s1, s2 in [(c1, c2), (c2, c1)]:
                rels = oi.outgoing_relationship_map(s1)
                # print(rels)
                test.assertCountEqual(rels[EQUIVALENT_CLASS], [s2])

    def test_patcher(
        self,
        oi: PatcherInterface,
        original_oi: DifferInterface = None,
        roundtrip_function: Callable = None,
    ):
        """
        Tests conformance to a patcher interface

        This will apply changes to an input ontology, it will then diff the modified ontology
        to recapitulate the changes

        :param oi:
        :param original_oi:
        :param roundtrip_function:
        :return:
        """
        test = self.test
        cases = [
            (
                kgcl.NodeRename(id=generate_change_id(), about_node=VACUOLE, new_value="VaCuOlE"),
                False,
                lambda oi: test.assertEqual(
                    "VaCuOlE",
                    oi.label(VACUOLE),
                ),
            ),
            (
                NodeObsoletion(id=generate_change_id(), about_node=NUCLEUS),
                False,
                lambda oi: test.assertIn(
                    NUCLEUS,
                    oi.obsoletes(),
                ),
            ),
            (NodeObsoletion(id=generate_change_id(), about_node="no such term"), True, None),
            (
                kgcl.SynonymReplacement(
                    id=generate_change_id(),
                    about_node=CELLULAR_COMPONENT,
                    old_value="subcellular entity",
                    new_value="foo bar",
                ),
                False,
                lambda oi: test.assertCountEqual(
                    [
                        "cell or subcellular entity",
                        "cellular component",
                        "cellular_component",
                        "foo bar",
                    ],
                    oi.entity_aliases(CELLULAR_COMPONENT),
                ),
            ),
            (
                kgcl.NewSynonym(id=generate_change_id(), about_node=HUMAN, new_value="people"),
                False,
                lambda oi: test.assertCountEqual(
                    ["people", "Homo sapiens"],
                    oi.entity_aliases(HUMAN),
                ),
            ),
        ]
        for case in cases:
            change, expects_raises, test_func = case
            if expects_raises:
                with test.assertRaises(ValueError):
                    oi.apply_patch(change)
            else:
                oi.apply_patch(change)
                test_func(oi)
        if roundtrip_function:
            oi2 = roundtrip_function(oi)
        else:
            oi2 = oi
        expected_changes = []
        for case in cases:
            change, expects_raises, test_func = case
            if test_func:
                test_func(oi2)
            if not expects_raises:
                change_obj = _as_json_dict_no_id(change)
                expected_changes.append(change_obj)
                print(f"EXPECTS: {change_obj}")
        if original_oi:
            diffs = original_oi.diff(oi2)
            for diff in diffs:
                kgcl_diff = render(diff)
                logging.info(kgcl_diff)
                # print(kgcl_diff)
                change_obj = _as_json_dict_no_id(diff)
                if change_obj in expected_changes:
                    expected_changes.remove(change_obj)
                print(f"Cannot find: {change_obj}")
                # else:
                #    raise ValueError(f"Cannot find: {change_obj}")
            # not all changes are easily recapitulated yet; e.g.
            for ch in expected_changes:
                print(f"Not found: {ch}")
            test.assertLessEqual(len(expected_changes), 3)
