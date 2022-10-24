"""Compliance tests for multiple interfaces.

See <https://github.com/INCATools/ontology-access-kit/issues/291>_
"""
import json
import logging
import tempfile
import unittest
from dataclasses import dataclass
from typing import Callable

import kgcl_schema.grammar.parser as kgcl_parser
from kgcl_schema.datamodel import kgcl
from kgcl_schema.datamodel.kgcl import Change, NodeObsoletion
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.dumpers import json_dumper, yaml_dumper

from oaklib import BasicOntologyInterface, get_implementation_from_shorthand
from oaklib.datamodels import obograph
from oaklib.datamodels.association import Association
from oaklib.datamodels.vocabulary import (
    EQUIVALENT_CLASS,
    IS_A,
    LOCATED_IN,
    NEVER_IN_TAXON,
    ONLY_IN_TAXON,
    OWL_THING,
    PART_OF,
)
from oaklib.interfaces import MappingProviderInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
    associations_subjects,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.utilities.kgcl_utilities import generate_change_id
from tests import (
    ARCHAEA,
    BACTERIA,
    BIOLOGICAL_PROCESS,
    CELL,
    CELL_CORTEX,
    CELL_PERIPHERY,
    CELLULAR_ANATOMICAL_ENTITY,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    EUKARYOTA,
    FAKE_ID,
    FUNGI,
    HUMAN,
    IMBO,
    INPUT_DIR,
    MAMMALIA,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    PHOTORECEPTOR_OUTER_SEGMENT,
    PHOTOSYNTHETIC_MEMBRANE,
    PLASMA_MEMBRANE,
    PROTEIN1,
    PROTEIN2,
    REGULATES,
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
    Tests for compliance against expected behavior.

    This is intended to be called from an implementation-specific unit test.
    Each such unit test can call compliance within this class.

    It is recommended that within the `setUp` method of the unit test,
    the following is performed.

    >>> self.compliance_tester = ComplianceTester(self)

    Then individual test can call this:

    >>> def test_foo(self):
    >>>    self.compliance_tester.test_foo(self.oi)
    """

    test: unittest.TestCase
    """Link back to implementation-specific unit test."""

    def test_definitions(self, oi: BasicOntologyInterface):
        """
        Tests text definition lookup.

        :param oi:
        :return:
        """
        test = self.test
        tdef = oi.definition(NUCLEUS)
        test.assertTrue(tdef.startswith("A membrane-bounded organelle of eukaryotic cells"))
        test.assertIsNone(oi.definition(FAKE_ID))

    def test_labels(self, oi: BasicOntologyInterface):
        """
        Tests lookup of labels by ID and reverse operation.

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (VACUOLE, "vacuole"),
            (CYTOPLASM, "cytoplasm"),
            (NUCLEAR_MEMBRANE, "nuclear membrane"),
            # (REGULATES, "regulates"),
        ]
        for curie, label in cases:
            test.assertEqual(label, oi.label(curie))
        for curie, label in cases:
            test.assertEqual([curie], oi.curies_by_label(label))
        tups = list(oi.labels(curie for curie, _ in cases))
        test.assertCountEqual(tups, cases)
        tups = list(oi.labels(list(oi.entities())))
        for case in cases:
            test.assertIn(case, tups)
        test.assertIsNone(oi.label(FAKE_ID))
        test.assertEqual([], list(oi.labels([FAKE_ID], allow_none=False)))
        test.assertEqual([(FAKE_ID, None)], list(oi.labels([FAKE_ID], allow_none=True)))
        test.assertEqual([(FAKE_ID, None)], list(oi.labels([FAKE_ID])))
        # test.assertIn("part of", oi.label(PART_OF))
        test.assertIn("regulates", oi.label(REGULATES))

    def test_synonyms(self, oi: BasicOntologyInterface):
        test = self.test
        syns = oi.entity_aliases("GO:0005575")
        # logging.info(syns)
        test.assertCountEqual(
            syns,
            [
                "cellular_component",
                "cellular component",
                "cell or subcellular entity",
                "subcellular entity",
            ],
        )
        syns = oi.entity_aliases(NUCLEUS)
        logging.info(syns)
        test.assertCountEqual(syns, ["nucleus", "cell nucleus", "horsetail nucleus"])
        syn_pairs = list(oi.entity_alias_map(NUCLEUS).items())
        test.assertCountEqual(
            syn_pairs,
            [
                ("oio:hasExactSynonym", ["cell nucleus"]),
                ("oio:hasNarrowSynonym", ["horsetail nucleus"]),
                ("rdfs:label", ["nucleus"]),
            ],
        )

    def test_sssom_mappings(self, oi: MappingProviderInterface):
        """
        Tests conformance of MappingProviderInterface.

        Also as a side-effect tests simple mapping retrieval from the BasicOntologyInterface

        - Tests retrieval in both directions (subject as query vs object as query)

        TODO: the test ontology does not yet include an example of using skos annotations

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (NUCLEUS, ["Wikipedia:Cell_nucleus", "NIF_Subcellular:sao1702920020"]),
            (VACUOLE, ["Wikipedia:Vacuole"]),
            (MAMMALIA, []),
        ]
        for curie, expected_mappings in cases:
            mappings = list(oi.sssom_mappings(curie))
            mapping_objects = [m.object_id for m in mappings]
            test.assertCountEqual(
                expected_mappings,
                mapping_objects,
                f"expected mappings({curie}) = {expected_mappings} got {mapping_objects}",
            )
            mapping_objects = [m[2] for m in oi.simple_mappings([curie])]
            test.assertCountEqual(
                expected_mappings,
                mapping_objects,
                f"expected simple mappings({curie}) = {expected_mappings} got {mapping_objects}",
            )
            for m in mappings:
                reverse_mappings = list(oi.get_sssom_mappings_by_curie(m.object_id))
                reverse_subject_ids = [m.subject_id for m in reverse_mappings]
                test.assertIn(curie, reverse_subject_ids)

    def test_relationships(self, oi: BasicOntologyInterface, ignore_annotation_edges=False):
        """
        Tests relationship methods for compliance.

        :param oi:
        :param ignore_annotation_edges: ignore edges representing OWL annotation assertion axioms
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
            logging.info(f"TESTS FOR {curie}")
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
        Tests equivalence relationship methods for compliance.

        The test suite includes a single equivalence axiom between named classes,
        between CHEBI and BFO roles.

        :param oi:
        :return:
        """
        test = self.test
        pairs = [("BFO:0000023", "CHEBI:50906")]
        for c1, c2 in pairs:
            for s1, s2 in [(c1, c2), (c2, c1)]:
                rels = oi.outgoing_relationship_map(s1)
                test.assertCountEqual(rels[EQUIVALENT_CLASS], [s2])

    def test_logical_definitions(self, oi: OboGraphInterface):
        test = self.test
        cases = [
            (CELL_CORTEX, [CYTOPLASM], [(PART_OF, CELL_PERIPHERY)]),
        ]
        for case in cases:
            defined_class, genus_ids, rels = case
            ldefs = list(oi.logical_definitions([defined_class]))
            test.assertIsNotNone(ldefs)
            test.assertEqual(1, len(ldefs))
            ldef = ldefs[0]
            test.assertCountEqual(genus_ids, ldef.genusIds)
            restrs = [
                obograph.ExistentialRestrictionExpression(propertyId=x[0], fillerId=x[1])
                for x in rels
            ]
            test.assertCountEqual(restrs, ldef.restrictions)
        # unionOfs should NOT be included
        test.assertEqual([], list(oi.logical_definitions("NCBITaxon_Union:0000030")))

    def test_obograph_node(self, oi: OboGraphInterface):
        test = self.test
        node = oi.node(NUCLEUS)
        print(yaml_dumper.dumps(node))
        test.assertEqual(NUCLEUS, node.id)
        test.assertEqual("nucleus", node.lbl)
        meta = node.meta
        test.assertTrue(meta.definition.val.startswith("A membrane-"))
        test.assertCountEqual(
            ["NIF_Subcellular:sao1702920020", "Wikipedia:Cell_nucleus"], [s.val for s in meta.xrefs]
        )
        test.assertCountEqual(
            [("hasExactSynonym", "cell nucleus"), ("hasNarrowSynonym", "horsetail nucleus")],
            [(s.pred, s.val) for s in meta.synonyms],
        )
        test.assertIn("obo:go#goslim_yeast", meta.subsets)
        nodes = list(oi.nodes())
        test.assertGreater(len(nodes), 10)
        test.assertIn(NUCLEUS, [n.id for n in nodes])

    def test_dump_obograph(self, oi: BasicOntologyInterface):
        """
        Tests conformance of dump method with obograph json syntax.

        Exports to json, and then parses output using json adapter.

        :param oi:
        :return:
        """
        file = tempfile.NamedTemporaryFile("w")
        oi.dump(file.name, "json")
        file.seek(0)
        oi2 = get_implementation_from_shorthand(f"obograph:{file.name}")
        self.test_labels(oi2)
        self.test_definitions(oi2)
        self.test_synonyms(oi2)
        self.test_logical_definitions(oi2)
        # TODO:
        # self.test_sssom_mappings(oi2)
        # TODO:
        # self.test_logical_definitions(oi2)
        # TODO: align test cases
        # self.test_relationships(oi2)

    def test_patcher(
        self,
        oi: PatcherInterface,
        original_oi: DifferInterface = None,
        roundtrip_function: Callable = None,
    ):
        """
        Tests conformance to a patcher interface.

        This will apply changes to an input ontology, it will then diff the modified ontology
        to recapitulate the changes.

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
                # TODO: raise exception
                print(f"Cannot find: {change_obj}")
                # else:
                #    raise ValueError(f"Cannot find: {change_obj}")
            # not all changes are easily recapitulated yet; e.g.
            for ch in expected_changes:
                # TODO: raise exception
                print(f"Expected change not found: {ch}")
            test.assertLessEqual(len(expected_changes), 3)

    def test_create_ontology_via_patches(
        self, oi: PatcherInterface, roundtrip_function: Callable = None
    ):
        """
        Tests creation of de-novo ontology from KGCL patch commands.

        Optionally performs a roundtrip test.

        :param oi:
        :param roundtrip_function:
        :return:
        """
        test = self.test
        with open(str(INPUT_DIR / "test-create.kgcl.txt")) as file:
            for line in file.readlines():
                if line.startswith("#"):
                    continue
                line = line.strip()
                change = kgcl_parser.parse_statement(line)
                oi.apply_patch(change)
        entity_labels = list(oi.labels(oi.entities()))
        test.assertIn(("X:1", "limb"), entity_labels)
        if roundtrip_function:
            oi2 = roundtrip_function(oi)
        else:
            oi2 = oi
        test.assertCountEqual(entity_labels, list(oi2.labels(oi2.entities())))

    def test_store_associations(self, oi: AssociationProviderInterface):
        """
        Tests ability to store then retrieve associations.

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (PROTEIN1, LOCATED_IN, NUCLEUS),
            (PROTEIN1, LOCATED_IN, VACUOLE),
            (PROTEIN2, LOCATED_IN, NUCLEAR_MEMBRANE),
        ]
        assoc_cases = [Association(*a) for a in cases]
        oi.add_associations(assoc_cases)
        assocs = list(oi.associations())
        test.assertCountEqual(assoc_cases, assocs)
        assocs = list(oi.associations(subjects=[PROTEIN1, PROTEIN2]))
        test.assertCountEqual(assoc_cases, assocs)
        for p in [PROTEIN1, PROTEIN2]:
            assocs = list(oi.associations([p]))
            filtered_cases = [case for case in assoc_cases if case.subject == p]
            test.assertCountEqual(filtered_cases, assocs)
        # direct queries
        test.assertEqual(
            [PROTEIN1], list(associations_subjects(oi.associations(objects=[NUCLEUS])))
        )
        test.assertEqual(
            [PROTEIN1], list(associations_subjects(oi.associations(objects=[VACUOLE])))
        )
        test.assertEqual(
            [PROTEIN1], list(associations_subjects(oi.associations(objects=[NUCLEUS, VACUOLE])))
        )
        test.assertEqual(
            [PROTEIN2], list(associations_subjects(oi.associations(objects=[NUCLEAR_MEMBRANE])))
        )
        # closures
        test.assertEqual(
            [PROTEIN1],
            list(
                associations_subjects(
                    oi.associations(objects=[IMBO], object_closure_predicates=[IS_A])
                )
            ),
        )
        test.assertEqual(
            [PROTEIN1, PROTEIN2],
            list(
                associations_subjects(
                    oi.associations(objects=[IMBO], object_closure_predicates=[IS_A, PART_OF])
                )
            ),
        )
        # test map
        assocs = list(
            oi.map_associations(
                [PROTEIN1, PROTEIN2],
                object_closure_predicates=[IS_A, PART_OF],
                subset_entities=[IMBO, HUMAN],
            )
        )
        for a in assocs:
            test.assertEqual(a.object, IMBO)
        assocs = list(
            oi.map_associations(
                [PROTEIN1, PROTEIN2],
                object_closure_predicates=[IS_A, PART_OF],
                subset_entities=[HUMAN, PHOTOSYNTHETIC_MEMBRANE],
            )
        )
        test.assertEqual([], assocs)
        counts = oi.association_subject_counts(object_closure_predicates=[IS_A, PART_OF])
        count_map = {}
        for k, v in counts:
            count_map[k] = v
            test.assertLessEqual(v, 2)
        test.assertEqual(1, count_map[NUCLEAR_MEMBRANE])
        test.assertEqual(2, count_map[NUCLEUS])
        test.assertEqual(2, count_map[IMBO])
        if isinstance(oi, SemanticSimilarityInterface):
            try:
                self.test_information_content_scores(oi, use_associations=True)
            except NotImplementedError:
                logging.info(f"Not yet implemented for {type(oi)}")

    def test_common_ancestors(self, oi: SemanticSimilarityInterface):
        """
        Tests behavior of common ancestors and most recent common ancestors.

        Pairs of entities are tested to determine if their common ancestors and
        MRCAs match what is expected, when filtered by a specified predicate list.

        :param oi:
        :return:
        """
        test = self.test
        expecteced = [
            (NUCLEUS, NUCLEUS, [IS_A], None, [NUCLEUS]),
            (NUCLEUS, VACUOLE, [IS_A], None, [IMBO]),
            (NUCLEUS, IMBO, [IS_A], None, [IMBO]),
            # (NUCLEUS, NUCLEUS, [], None, [NUCLEUS]),
            (NUCLEUS, NUCLEUS, [IS_A, PART_OF], None, [NUCLEUS]),
            (NUCLEAR_ENVELOPE, NUCLEUS, [IS_A, PART_OF], None, [NUCLEUS]),
            (NUCLEAR_ENVELOPE, NUCLEUS, [IS_A], None, [CELLULAR_ANATOMICAL_ENTITY]),
            (BIOLOGICAL_PROCESS, NUCLEUS, [IS_A], [OWL_THING], [OWL_THING]),
        ]
        for x, y, preds, expected_ancs, expected_mrcas in expecteced:
            ancs = list(oi.common_ancestors(x, y, preds))
            ancs_flipped = list(oi.common_ancestors(y, x, preds))
            mrcas = list(oi.most_recent_common_ancestors(x, y, preds))
            mrcas_flipped = list(oi.most_recent_common_ancestors(y, x, preds))
            if expected_ancs is not None:
                test.assertCountEqual(expected_ancs, ancs)
            test.assertCountEqual(
                expected_mrcas, mrcas, f"different MRCA results for {x} v {y} with {preds}"
            )
            for a in mrcas:
                test.assertIn(a, ancs)
            test.assertCountEqual(ancs, ancs_flipped)
            test.assertCountEqual(mrcas, mrcas_flipped)

    def test_information_content_scores(
        self, oi: SemanticSimilarityInterface, use_associations: bool = False
    ):
        """
        Tests calculation of IC scores.

        Ensures the constraint that child terms should have greater than or equal IC to their parents.

        When the ontology is used as the corpus, the constraint is stronger, and it must be less than.

        :param oi:
        :param use_associations: use associations as the background set
        :return:
        """
        test = self.test
        terms = [
            NUCLEUS,
            VACUOLE,
            NUCLEAR_ENVELOPE,
            PHOTORECEPTOR_OUTER_SEGMENT,
            IMBO,
            CELLULAR_COMPONENT,
            FUNGI,
            EUKARYOTA,
            OWL_THING,
        ]
        posets = [
            (FUNGI, EUKARYOTA),
            (NUCLEAR_ENVELOPE, NUCLEUS),
            (NUCLEUS, IMBO),
            (IMBO, CELLULAR_COMPONENT),
        ]
        m = {}
        for curie, score in oi.information_content_scores(
            terms, object_closure_predicates=[IS_A, PART_OF], use_associations=use_associations
        ):
            m[curie] = score
        # universal root node always has zero information
        test.assertEqual(m[OWL_THING], 0.0)
        for child, parent in posets:
            if use_associations:
                if child in m and parent in m:
                    print(f"{m[child]} > {m[parent]}")
                    test.assertGreaterEqual(m[child], m[parent])
            else:
                test.assertGreater(m[child], m[parent])

    def test_pairwise_similarity(self, oi: SemanticSimilarityInterface):
        test = self.test
        # test non-existent item
        test.assertEqual([(OWL_THING, 0.0)], list(oi.information_content_scores([OWL_THING])))
        sim = oi.pairwise_similarity(NUCLEUS, FAKE_ID)
        # print(sim)
        test.assertEqual(0.0, sim.ancestor_information_content)
        test.assertEqual(0.0, sim.jaccard_similarity)
        terms = [NUCLEUS, FAKE_ID]
        pairs = list(oi.all_by_all_pairwise_similarity(terms, terms, predicates=[IS_A]))
        test.assertEqual(4, len(pairs))
        for pair in pairs:
            if pair.subject_id == pair.object_id:
                test.assertGreater(pair.jaccard_similarity, 0.99)
            else:
                test.assertEqual(0.0, pair.ancestor_information_content)
        terms = [
            NUCLEUS,
            VACUOLE,
            NUCLEAR_ENVELOPE,
            PLASMA_MEMBRANE,
            BACTERIA,
            CELLULAR_ORGANISMS,
            FAKE_ID,
        ]
        # test each member vs itself
        pairs = list(oi.all_by_all_pairwise_similarity(terms, terms, predicates=[IS_A]))
        distances = {}
        for pair in pairs:
            if pair.subject_id == pair.object_id:
                test.assertGreater(pair.jaccard_similarity, 0.99)
                if pair.subject_id == FAKE_ID:
                    test.assertIsNone(pair.phenodigm_score)
                else:
                    test.assertGreater(pair.phenodigm_score, 0.5)
            distances[(pair.subject_id, pair.object_id)] = 1 - pair.jaccard_similarity
        # test triangle inequality
        for x in terms:
            for y in terms:
                for z in terms:
                    test.assertGreaterEqual(
                        distances[(x, y)] + distances[(y, z)], distances[(x, z)]
                    )
        termsets = [
            (
                [NUCLEUS, VACUOLE],
                [NUCLEAR_ENVELOPE],
                [IS_A],
                3.0,
                3.0,
            ),
            (
                [NUCLEUS, VACUOLE],
                [NUCLEAR_ENVELOPE],
                [IS_A, PART_OF],
                5.6,
                5.8,
            ),
            (
                [CYTOPLASM, BACTERIA],
                [CYTOPLASM, BACTERIA],
                [IS_A, PART_OF],
                5.2,
                5.4,
            ),
            ([NUCLEUS, VACUOLE], [BACTERIA, ARCHAEA], [IS_A], 0.0, 0.0),
        ]
        error_range = 1.0
        for ts in termsets:
            ts1, ts2, ps, expected_avg, expected_max = ts
            sim = oi.termset_pairwise_similarity(ts1, ts2, predicates=ps, labels=True)
            test.assertLess(
                abs(sim.average_score - expected_avg), error_range, f"TermSet: {ts} Sim: {sim}"
            )
            test.assertLess(abs(sim.best_score - expected_max), error_range)
