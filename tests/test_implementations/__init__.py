"""Compliance tests for multiple interfaces.

See <https://github.com/INCATools/ontology-access-kit/issues/291>_
"""
import json
import logging
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List

import kgcl_schema.grammar.parser as kgcl_parser
from kgcl_schema.datamodel import kgcl
from kgcl_schema.datamodel.kgcl import Change, NodeObsoletion
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.dumpers import json_dumper

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.datamodels import obograph
from oaklib.datamodels.association import Association
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty
from oaklib.datamodels.vocabulary import (
    CONSIDER_REPLACEMENT,
    CONTRIBUTOR,
    CREATED,
    CREATOR,
    DEPRECATED_PREDICATE,
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    HAS_EXACT_SYNONYM,
    HAS_PART,
    INVERSE_OF,
    IS_A,
    LOCATED_IN,
    NEVER_IN_TAXON,
    OIO_CREATED_BY,
    OIO_CREATION_DATE,
    OIO_SUBSET_PROPERTY,
    OIO_SYNONYM_TYPE_PROPERTY,
    ONLY_IN_TAXON,
    OWL_CLASS,
    OWL_THING,
    PART_OF,
    RDFS_DOMAIN,
    RDFS_RANGE,
    SUBPROPERTY_OF,
    TERM_REPLACED_BY,
    TERM_TRACKER_ITEM,
)
from oaklib.interfaces import (
    MappingProviderInterface,
    SearchInterface,
    TextAnnotatorInterface,
)
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
    associations_subjects,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import (
    Distance,
    OboGraphInterface,
    TraversalConfiguration,
)
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.utilities.kgcl_utilities import generate_change_id
from tests import (
    ARCHAEA,
    BACTERIA,
    BIOLOGICAL_PROCESS,
    BONE_FRACTURE,
    CATALYTIC_ACTIVITY,
    CAUSALLY_UPSTREAM_OF,
    CELL,
    CELL_CORTEX,
    CELL_CORTEX_REGION,
    CELL_PERIPHERY,
    CELLULAR_ANATOMICAL_ENTITY,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    CYTOPLASMIC_REGION,
    ENDOMEMBRANE_SYSTEM,
    EUKARYOTA,
    FAKE_ID,
    FUNGI,
    GENE1,
    GENE2,
    GENE3,
    GENE4,
    GENE5,
    GENE6,
    GENE7,
    GENE8,
    GENE9,
    HUMAN,
    IMBO,
    INPUT_DIR,
    INTRACELLULAR,
    INTRACELLULAR_ORGANELLE,
    MAMMALIA,
    NUCLEAR_ENVELOPE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    OPISTHOKONTA,
    PHENOTYPIC_ABNORMALITY,
    PHOTORECEPTOR_OUTER_SEGMENT,
    PHOTOSYNTHETIC_MEMBRANE,
    PLASMA_MEMBRANE,
    PROCESS,
    PROTEIN1,
    PROTEIN2,
    REGULATED_BY,
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

    def test_definitions(self, oi: BasicOntologyInterface, include_metadata=False):
        """
        Tests text definition lookup.

        :param oi:
        :param include_metadata:
        :return:
        """
        test = self.test
        tdef = oi.definition(NUCLEUS)
        test.assertTrue(tdef.startswith("A membrane-bounded organelle of eukaryotic cells"))
        test.assertIsNone(oi.definition(FAKE_ID))
        if include_metadata:
            tdefs = list(oi.definitions([NUCLEUS, VACUOLE], include_metadata=True))
            test.assertEqual(2, len(tdefs))
            [tdef_nucleus] = [tdef for tdef in tdefs if tdef[0] == NUCLEUS]
            [tdef_vacuole] = [tdef for tdef in tdefs if tdef[0] == VACUOLE]
            test.assertTrue(
                tdef_nucleus[1].startswith("A membrane-bounded organelle of eukaryotic cells")
            )
            test.assertCountEqual(["GOC:go_curators"], tdef_nucleus[2][HAS_DBXREF])

    def test_owl_types(self, oi: BasicOntologyInterface, skip_oio=False):
        test = self.test
        cases = [
            (NUCLEUS, OWL_CLASS),
            (FAKE_ID, None),
            # (PART_OF, OWL_OBJECT_PROPERTY),
        ]
        if not skip_oio:
            cases.extend(
                [
                    ("goslim_generic", OIO_SUBSET_PROPERTY),
                    ("systematic_synonym", OIO_SYNONYM_TYPE_PROPERTY),
                ]
            )
        for entity, expected in cases:
            if expected is None:
                test.assertEqual([], oi.owl_type(entity))
            else:
                test.assertEqual([expected], oi.owl_type(entity), f"Failed for {entity}")
            if expected:
                entities = list(oi.entities(owl_type=expected))
                test.assertIn(entity, entities, f"{entity} not found in query for {expected}")
                for e2, expected2 in cases:
                    if expected2 != expected:
                        test.assertNotIn(
                            e2, entities, f"{e2} unexpectedly found in query for {expected}"
                        )

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

    def test_defined_bys(self, oi: BasicOntologyInterface):
        """
        Tests lookup of defined_by by ID.

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (VACUOLE, "GO"),
            (CYTOPLASM, "GO"),
            (SUBATOMIC_PARTICLE, "CHEBI"),
            (HUMAN, "NCBITaxon"),
        ]
        actual = list(oi.defined_bys([c[0] for c in cases]))
        test.assertCountEqual(cases, actual)

    def test_subsets(self, oi: BasicOntologyInterface):
        test = self.test
        subsets = list(oi.subsets())
        test.assertIn("goslim_aspergillus", subsets)
        test.assertIn("GO:0003674", oi.subset_members("goslim_generic"))
        test.assertNotIn("GO:0003674", oi.subset_members("gocheck_do_not_manually_annotate"))

    def test_metadata(self, oi: MetadataInterface):
        test = self.test
        for curie in oi.entities():
            m = oi.entity_metadata_map(curie)
            logging.info(f"{curie} {m}")
        m = oi.entity_metadata_map(INTRACELLULAR)
        test.assertIn(TERM_TRACKER_ITEM, m.keys())  # TODO: check this generalizes
        test.assertIn(
            "https://github.com/geneontology/go-ontology/issues/17776", m[TERM_TRACKER_ITEM]
        )

    def test_obsolete_entities(self, oi: SearchInterface):
        """
        Tests lookup of defined_by by ID.

        :param oi: this should be for obsoletion_test.{obo,owl,...}
        :return:
        """
        test = self.test
        obsoletes_excluding_merged = list(oi.obsoletes(include_merged=False))
        obsoletes = list(oi.obsoletes())
        test.assertCountEqual(["CL:2", "CL:3", "CL:5", "CL:6"], obsoletes_excluding_merged)
        test.assertCountEqual(
            ["CL:1a1", "CL:1a2", "CL:4a1", "CL:1a3", "CL:2", "CL:3", "CL:5", "CL:6"], obsoletes
        )
        all_entities = set(list(oi.entities(filter_obsoletes=False)))
        all_non_obsolete_entities = set(list(oi.entities(filter_obsoletes=True)))
        ixn = all_non_obsolete_entities.intersection(obsoletes)
        # Note: the test file has intentional illegalities, 4a1 is an alt_id as well as a primary id
        # TODO: unify what the expected behavior is for this
        test.assertTrue(len(ixn) == 0 or ixn == {"CL:4a1"})
        test.assertCountEqual(all_entities, all_non_obsolete_entities.union(obsoletes))
        # test.assertCountEqual(obsoletes, all_entities.difference(all_non_obsolete_entities))
        for x in obsoletes:
            mm = oi.entity_metadata_map(x)
            test.assertEquals([True], mm[DEPRECATED_PREDICATE])
        cases = [
            ("CL:1", [], []),
            ("CL:1a1", ["CL:1"], []),
            ("CL:1a2", ["CL:1"], []),
            ("CL:1a3", ["CL:1"], []),
            ("CL:2", ["CL:2replacement"], []),
            ("CL:3", [], ["CL:3cons1", "CL:3cons2"]),
            ("CL:4a1", ["CL:4"], []),
            ("CL:5", ["CL:6"], []),
            ("CL:6", ["CL:7"], []),
        ]
        for curie, replaced_by, consider in cases:
            actual_replaced_by = [
                r[2]
                for r in oi.obsoletes_migration_relationships([curie])
                if r[1] == TERM_REPLACED_BY
            ]
            actual_consider = [
                r[2]
                for r in oi.obsoletes_migration_relationships([curie])
                if r[1] == CONSIDER_REPLACEMENT
            ]
            test.assertCountEqual(
                replaced_by, actual_replaced_by, f"replaced_by did not match for {curie}"
            )
            test.assertCountEqual(consider, actual_consider)
            for r in replaced_by:
                terms = list(
                    oi.basic_search(
                        curie,
                        config=SearchConfiguration(
                            properties=SearchProperty(SearchProperty.REPLACEMENT_IDENTIFIER)
                        ),
                    )
                )
                test.assertCountEqual([r], terms, f"replaced_by did not match for {curie}")

    def test_multilingual(self, oi: BasicOntologyInterface):
        """
        Tests multilingual capabilities

        :param oi: use an adapter for the HPO international subset
        :return:
        """
        test = self.test
        langs = list(oi.languages())
        expected_langs = ["cs", "tr", "fr", "nl"]
        test.assertCountEqual(expected_langs, langs)
        test.assertTrue(oi.multilingual)
        lang_labels = [
            (
                PHENOTYPIC_ABNORMALITY,
                "en",
                "Phenotypic abnormality",
                "A phenotypic abnormality.",
                True,
            ),
            (
                PHENOTYPIC_ABNORMALITY,
                "fr",
                "Anomalie phénotypique",
                "une anomalie phénotypique",
                True,
            ),
            (
                PHENOTYPIC_ABNORMALITY,
                "cs",
                "Fenotypová abnormalita",
                "Fenotypová abnormalita",
                True,
            ),
            (PHENOTYPIC_ABNORMALITY, "nl", "Fenotypische abnormaliteit", None, True),
            (
                BONE_FRACTURE,
                "en",
                "Bone fracture",
                "A partial or complete breakage of the continuity of a bone.",
                True,
            ),
            (BONE_FRACTURE, "nl", "Bone fracture", None, False),  # defaults to english
        ]
        test.assertEqual("en", oi.default_language)
        for curie, lang, expected_label, expected_definition, present in lang_labels:
            labels = list(oi.labels([curie]))
            test.assertGreater(len(labels), 0)
            label = oi.label(curie, lang=lang)
            test.assertEquals(expected_label, label, f"Label for {lang} did not match")
            label_tuples = list(oi.multilingual_labels([curie]))
            if present:
                test.assertIn(
                    lang,
                    [lang[2] or "en" for lang in label_tuples],
                    f"Label for {lang} not found in {label_tuples} for {curie}",
                )
            label_tuples = list(oi.multilingual_labels([curie], langs=[lang]))
            if present:
                test.assertIn(lang, [lang[2] or "en" for lang in label_tuples])
            other_langs = [lang for lang in expected_langs if lang != lang]
            label_tuples = list(oi.multilingual_labels([curie], langs=other_langs))
            test.assertGreater(len(label_tuples), 0)
            test.assertNotIn(lang, [lang[2] for lang in label_tuples])
            defn = oi.definition(curie, lang=lang)
            if expected_definition is not None:
                test.assertEquals(expected_definition, defn, f"Definition for {lang} did not match")
            defns = list(oi.definitions([curie], lang=lang))
            if expected_definition is None:
                pass
                # test.assertEqual(0, len(defns), f"Expected no definition for {lang} for {curie}")
            else:
                test.assertEqual(1, len(defns), f"Expected one definition for {lang} for {curie}")
                test.assertEqual(
                    expected_definition, defns[0][1], f"Definition for {lang} did not match"
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
        # test retrieval of mapping dict
        nm = oi.create_normalization_map(
            oi.entities(), source_prefixes=["GO"], target_prefixes=["Wikipedia"]
        )
        test.assertGreater(len(nm), 0)
        test.assertEqual("Wikipedia:Cell_nucleus", nm[NUCLEUS])
        test.assertEqual("Wikipedia:Vacuole", nm[VACUOLE])
        test.assertTrue(
            all([k.startswith("GO") and v.startswith("Wikipedia:") for k, v in nm.items()])
        )
        # test case normalization
        nm = oi.create_normalization_map(
            oi.entities(), source_prefixes=["GO"], target_prefixes=["WIKIPEDIA"]
        )
        test.assertGreater(len(nm), 0)
        test.assertEqual("WIKIPEDIA:Cell_nucleus", nm[NUCLEUS])
        test.assertEqual("WIKIPEDIA:Vacuole", nm[VACUOLE])
        test.assertTrue(
            all([k.startswith("GO") and v.startswith("WIKIPEDIA:") for k, v in nm.items()])
        )
        # test case normalization, where the source is lower case
        entities_lc = [x.lower() for x in oi.entities()]
        nm = oi.create_normalization_map(
            entities_lc,
            source_prefixes=["GO"],
            target_prefixes=["WIKIPEDIA"],
            prefix_alias_map={"Wikipedia": "WIKIPEDIA", "GO": "go"},
        )
        test.assertGreater(len(nm), 0, "expected case conversion to work")
        test.assertEqual("WIKIPEDIA:Cell_nucleus", nm[NUCLEUS.lower()])
        test.assertEqual("WIKIPEDIA:Vacuole", nm[VACUOLE.lower()])
        test.assertTrue(
            all([k.startswith("go") and v.startswith("WIKIPEDIA:") for k, v in nm.items()])
        )
        cases = [
            (NUCLEUS, ["Wikipedia:Cell_nucleus", "NIF_Subcellular:sao1702920020"]),
            (VACUOLE, ["Wikipedia:Vacuole"]),
            (MAMMALIA, []),
        ]
        for curie, expected_mappings in cases:
            # test normalization
            for m in expected_mappings:
                prefix = m.split(":")[0]
                normalized_id = oi.normalize(curie, target_prefixes=[prefix])
                test.assertEqual(m, normalized_id)
                m_upper = m.replace("Wikipedia", "WIKIPEDIA").replace(
                    "NIF_Subcellular", "NIF_SUBCELLULAR"
                )
                test.assertEqual(m_upper, oi.normalize(curie, target_prefixes=[prefix.upper()]))
                test.assertEqual(
                    m_upper,
                    oi.normalize(
                        curie.lower(), target_prefixes=[prefix.upper()], source_prefixes=["GO"]
                    ),
                )
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
                reverse_mappings = list(oi.sssom_mappings(m.object_id))
                reverse_subject_ids = [m.subject_id for m in reverse_mappings]
                test.assertIn(curie, reverse_subject_ids)
            prefixes = [x.split(":")[0] for x in expected_mappings]
            for prefix in prefixes:
                mappings = list(oi.sssom_mappings(curie, source=prefix))
                expected_with_prefix = [x for x in expected_mappings if x.startswith(prefix)]
                test.assertCountEqual(
                    expected_with_prefix,
                    [m.object_id for m in mappings],
                    f"expected mappings({curie})[{prefix}]",
                )

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

    def test_rbox_relationships(self, oi: BasicOntologyInterface):
        """
        Tests relationships between relationship types

        :param oi:
        :return:
        """
        test = self.test
        cases = [
            (REGULATES, [CAUSALLY_UPSTREAM_OF], REGULATED_BY, PROCESS, PROCESS),
        ]
        for curie, is_as, inv, domain, range in cases:
            logging.info(f"TESTS FOR {curie}")
            for p, expected in [
                (SUBPROPERTY_OF, is_as),
                (RDFS_DOMAIN, [domain]),
                (RDFS_RANGE, [range]),
                (INVERSE_OF, [inv]),
            ]:
                parents = [r[2] for r in oi.relationships([curie], predicates=[p])]
                test.assertCountEqual(
                    expected, parents, f"expected {p}({curie}) = {expected} got {parents}"
                )
                parents = [r[2] for r in oi.relationships([curie]) if r[1] == p]
                test.assertCountEqual(
                    expected, parents, f"expected {p}({curie}) = {expected} got {parents}"
                )

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

    def test_synonym_types(self, oi: OboGraphInterface):
        """
        Tests that synonym types can be retrieved.

        Note that in the OboGraph data model, *scope* (exact, broad, etc.) is distinct
        from the optional *type* (ontology specific, e.g. ABBREVIATION) of a synonym.

        We use the standard test ontology which has a "systematic_synonym" type on
        one of the synonyms.
        """
        test = self.test
        node = oi.node(NUCLEUS, include_metadata=True)
        cases = [
            (1, "hasExactSynonym", "cell nucleus", [], "systematic_synonym"),
            (
                2,
                "hasNarrowSynonym",
                "horsetail nucleus",
                ["GOC:mah", "GOC:vw", "GOC:al", "PMID:15030757"],
                None,
            ),
        ]

        def _check(syns: List[obograph.SynonymPropertyValue]):
            found = {}
            for syn in syns:
                matched = False
                for case in cases:
                    num, pred, label, xrefs, typ = case
                    if (
                        pred == syn.pred
                        and label == syn.val
                        and sorted(xrefs) == sorted(syn.xrefs)
                        and typ == syn.synonymType
                    ):
                        found[num] = True
                        matched = True
                test.assertTrue(matched, f"Unexpected synonym: {syn}")
            for case in cases:
                test.assertIn(case[0], found, f"Missing synonym: {case}")

        _check(node.meta.synonyms)
        syns = list(oi.synonym_property_values(NUCLEUS))
        _check([syn[1] for syn in syns])

    def test_dump_obograph(self, oi: BasicOntologyInterface):
        """
        Tests conformance of dump method with obograph json syntax.

        Exports to json, and then parses output using json adapter.

        :param oi:
        :return:
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = Path(tmpdirname) / "tmp_obograph.json"
            oi.dump(str(fname), "json")
            oi2 = get_adapter(f"obograph:{fname.as_posix()}")

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

    def test_disjoint_with(self, oi: OwlInterface):
        """
        Tests querying for disjoint pairs

        :param oi:
        :return:
        """
        test = self.test
        pairs = list(oi.disjoint_pairs())
        expected = [
            ("BFO:0000002", "BFO:0000003"),
            ("BFO:0000004", "BFO:0000020"),
            ("CL:0000000", "GO:0043226"),
            ("GO:0003674", "GO:0008150"),
            ("GO:0003674", "GO:0005575"),
            ("GO:0005575", "GO:0008150"),
            ("GO:0005634", "GO:0005737"),
            ("NCBITaxon:10239", "NCBITaxon:131567"),
            ("NCBITaxon:2", "NCBITaxon:2759"),
            ("NCBITaxon:2", "NCBITaxon:2157"),
            ("NCBITaxon:2157", "NCBITaxon:2759"),
            ("NCBITaxon:2611352", "NCBITaxon:554915"),
            ("NCBITaxon:2611352", "NCBITaxon:33154"),
            ("NCBITaxon:2611352", "NCBITaxon:33090"),
            ("NCBITaxon:33090", "NCBITaxon:554915"),
            ("NCBITaxon:33090", "NCBITaxon:33154"),
            ("NCBITaxon:33154", "NCBITaxon:554915"),
        ]
        for pair in pairs:
            test.assertTrue(
                pair in expected or pair[::-1] in expected, f"Unexpected disjoint pair: {pair}"
            )
        for case in expected:
            test.assertTrue(
                case in pairs or case[::-1] in pairs, f"Expected disjoint pair not found: {case}"
            )
        for case in expected:
            for c in case:
                c_pairs = list(oi.disjoint_pairs([c]))
                test.assertTrue(
                    case in c_pairs or case[::-1] in c_pairs,
                    f"Expected disjoint pair not found for {c}: {case}",
                )
                test.assertFalse(
                    any(c for c_pair in c_pairs if c not in c_pair),
                    f"Unexpected disjoint pair for {c}: {case}",
                )
            test.assertTrue(
                oi.is_disjoint(case[0], case[1]),
                f"Expected disjoint pair not found for {c}: {case}",
            )
            test.assertTrue(
                oi.is_disjoint(case[1], case[0]),
                f"Expected disjoint pair not found for {c}: {case}",
            )
            if isinstance(oi, SemanticSimilarityInterface):
                c1, c2 = case
                cds = list(oi.common_descendants(c1, c2, predicates=[IS_A]))
                test.assertFalse(cds, f"Did not common descendants: {c1}, {c2} = {cds}")
        entailed_cases = [
            (NUCLEUS, BIOLOGICAL_PROCESS),
            (NUCLEUS, CELL_CORTEX),
            (CELL, VACUOLE),
        ]
        for c1, c2 in entailed_cases:
            test.assertTrue(oi.is_disjoint(c1, c2), f"Expected disjoint pair: {c1}, {c2}")
            test.assertTrue(oi.is_disjoint(c2, c1), f"Expected disjoint pair: {c1}, {c2}")
        negative_cases = [
            (NUCLEUS, NUCLEAR_MEMBRANE),
            (NUCLEAR_MEMBRANE, CELL_CORTEX),
            (NUCLEUS, CELLULAR_COMPONENT),
            (NUCLEUS, NUCLEUS),
            ("CHEBI:33250", "CHEBI:33250"),
            ("CHEBI:24431", "CHEBI:24431"),
        ]
        for c1, c2 in negative_cases:
            test.assertFalse(oi.is_disjoint(c1, c2), f"Unexpected disjoint pair: {c1}, {c2}")
            test.assertFalse(oi.is_disjoint(c2, c1), f"Unexpected disjoint pair: {c1}, {c2}")
        for c in oi.entities(owl_type=OWL_CLASS):
            test.assertFalse(oi.is_disjoint(c, c), f"Unexpected disjoint pair: {c}, {c}")
            if isinstance(oi, SemanticSimilarityInterface):
                cds = list(oi.common_descendants(c, c, predicates=[IS_A]))
                test.assertTrue(cds, f"Expected common descendants: {c}, {c}")
                test.assertIn(c, cds, f"ExpectedIn: {c}, {cds}")

    def test_merge(self, target: MergeInterface, source: BasicOntologyInterface):
        """
        Tests ability to merge a source ontology into a target.

        :param target:
        :param source:
        :return:
        """
        test = self.test
        target_entities = set(target.entities(owl_type=OWL_CLASS))
        source_entities = set(source.entities(owl_type=OWL_CLASS))
        target.merge([source])
        merged_entities = set(target.entities(owl_type=OWL_CLASS))
        diff = merged_entities.difference(target_entities.union(source_entities))
        for x in diff:
            print(x)
        test.assertCountEqual(target_entities.union(source_entities), merged_entities)
        in_both = target_entities.intersection(source_entities)
        test.assertIn(CELL, in_both)
        # TODO
        # test.assertIn(PART_OF, list(target.entities()))

    def test_reflexive_diff(self, oi: DifferInterface):
        """
        Tests that the reflexive diff is empty

        :param oi:
        :return:
        """
        test = self.test
        diff = list(oi.diff(oi))
        for ch in diff:
            logging.info(ch)
        test.assertEqual(0, len(diff), f"Reflexive diff is not empty: {diff}")

    def test_diff(self, oi: DifferInterface, oi_modified: DifferInterface):
        """
        Tests diff implementation by comparing two ontologies.

        :param oi:
        :param oi_modified:
        :return:
        """
        n_unexpected = 0
        test = self.test
        diff = list(oi.diff(oi_modified))
        FIXED_ID = "test"
        expected = [
            kgcl.RemoveSynonym(
                id=FIXED_ID, about_node=CATALYTIC_ACTIVITY, old_value="enzyme activity"
            ),
            kgcl.NewSynonym(
                id=FIXED_ID, about_node=CATALYTIC_ACTIVITY, new_value="catalytic activity"
            ),
            kgcl.NodeRename(
                id=FIXED_ID,
                about_node=CATALYTIC_ACTIVITY,
                new_value="enzyme activity",
                old_value="catalytic activity",
            ),
            kgcl.NodeDeletion(id=FIXED_ID, about_node="GO:0033673"),
        ]
        for ch in diff:
            ch.id = FIXED_ID
            if ch in expected:
                expected.remove(ch)
            else:
                logging.error(f"Unexpected change: {ch}")
                n_unexpected += 1
            ch.type = type(ch).__name__
        test.assertEqual(0, len(expected), f"Expected changes not found: {expected}")
        expected_rev = [
            kgcl.NewSynonym(
                id=FIXED_ID, about_node=CATALYTIC_ACTIVITY, new_value="enzyme activity"
            ),
            kgcl.RemoveSynonym(
                id=FIXED_ID, about_node=CATALYTIC_ACTIVITY, old_value="catalytic activity"
            ),
            kgcl.NodeRename(
                id=FIXED_ID,
                about_node=CATALYTIC_ACTIVITY,
                old_value="enzyme activity",
                new_value="catalytic activity",
            ),
            kgcl.ClassCreation(id=FIXED_ID, about_node="GO:0033673"),
        ]
        rdiff = list(oi_modified.diff(oi))
        for ch in rdiff:
            ch.id = FIXED_ID
            if ch in expected_rev:
                expected_rev.remove(ch)
            else:
                logging.error(f"Unexpected change: {ch}")
                n_unexpected += 1
            ch.type = type(ch).__name__
        test.assertEqual(0, len(expected_rev), f"Expected changes not found: {expected_rev}")
        test.assertEqual(0, n_unexpected)
        # test diff summary
        summary = oi.diff_summary(oi_modified)
        logging.info(summary)
        residual = summary["__RESIDUAL__"]
        cases = [
            ("RemoveSynonym", 1),
            ("NewSynonym", 1),
            ("NodeDeletion", 1),
            ("All_Synonym", 2),
        ]
        for typ, expected in cases:
            test.assertEqual(expected, residual[typ])

    def test_subgraph_from_traversal(self, oi: OboGraphInterface):
        """
        Tests subgraph_from_traversal in OboGraphInterface

        :param oi: OboGraphInterface
        :return:
        """
        test = self.test
        cases = [
            (
                [NUCLEUS, VACUOLE],
                [IS_A, PART_OF],
                Distance.TRANSITIVE,
                Distance.ZERO,
                20,
                25,
                [NUCLEUS, VACUOLE, IMBO, CYTOPLASM],
                [(NUCLEUS, IS_A, IMBO), (IMBO, IS_A, INTRACELLULAR_ORGANELLE)],
            ),
            (
                [NUCLEUS, VACUOLE],
                [IS_A, PART_OF],
                Distance.TRANSITIVE,
                Distance.DIRECT,
                22,
                27,
                [NUCLEAR_MEMBRANE, NUCLEAR_MEMBRANE],
                [(NUCLEAR_MEMBRANE, PART_OF, NUCLEUS)],
            ),
            (
                [NUCLEUS, VACUOLE],
                [IS_A],
                Distance.DIRECT,
                Distance.DIRECT,
                4,
                2,
                [IMBO],
                [(NUCLEUS, IS_A, IMBO)],
            ),
            ([], [IS_A, PART_OF], Distance.TRANSITIVE, Distance.TRANSITIVE, 0, 0, [], []),
            ([NUCLEUS, VACUOLE], [IS_A, PART_OF], Distance.ZERO, Distance.ZERO, 0, 0, [], []),
        ]
        for case in cases:
            (
                seeds,
                predicates,
                up_dist,
                down_dist,
                expected_num_nodes,
                expected_num_edges,
                expected_nodes_subset,
                expected_edges_subset,
            ) = case
            traversal = TraversalConfiguration(up_distance=up_dist, down_distance=down_dist)
            graph = oi.subgraph_from_traversal(seeds, predicates=predicates, traversal=traversal)
            test.assertEqual(expected_num_nodes, len(graph.nodes))
            test.assertEqual(expected_num_edges, len(graph.edges))
            node_ids = [n.id for n in graph.nodes]
            for node_id in expected_nodes_subset:
                test.assertIn(node_id, node_ids, f"Failed for case: {case}")
            edge_ids = [(e.sub, e.pred, e.obj) for e in graph.edges]
            for edge_id in expected_edges_subset:
                test.assertIn(edge_id, edge_ids)

    def test_extract_graph(self, oi: OboGraphInterface, test_metadata=False):
        test = self.test
        # TODO: add tests when test dataset is unified
        cases = [
            ([NUCLEUS], False, 1, 0, []),
            ([NUCLEUS, NUCLEAR_ENVELOPE], False, 2, 1, []),
            # ([NUCLEUS, NUCLEAR_ENVELOPE], True, 2, 6, []),
            ([NUCLEUS, IMBO, NUCLEAR_ENVELOPE], False, 3, 2, []),
        ]
        for nodes, dangling, num_nodes, num_edges, expected in cases:
            g = oi.extract_graph(nodes, dangling=dangling)
            test.assertEqual(num_nodes, len(g.nodes))
            test.assertEqual(num_edges, len(g.edges))
            node_ids = [n.id for n in g.nodes]
            for node_id in nodes:
                node_uri = oi.curie_to_uri(node_id)
                test.assertTrue(node_uri in node_ids or node_id in node_ids)
            for e in expected:
                test.assertIn(e, g.edges)
            if NUCLEUS in nodes:
                node_uri = oi.curie_to_uri(NUCLEUS)
                node = [n for n in g.nodes if n.id == node_uri or n.id == NUCLEUS][0]
                test.assertTrue(node.id == NUCLEUS or node.id == node_uri)
                test.assertEqual("nucleus", node.lbl)
                if test_metadata:
                    test.assertGreater(len(node.meta.subsets), 0)
                    defn = node.meta.definition
                    test.assertTrue(defn.val.startswith("A membrane-bounded"))
                    test.assertCountEqual(["GOC:go_curators"], defn.xrefs)
                    syns = node.meta.synonyms
                    test.assertTrue(any(s for s in syns if s.val == "cell nucleus"))
                    test.assertTrue(any(s for s in syns if s.val == "horsetail nucleus"))

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
        :param roundtrip_function: a function to create a new PatchInterface.
        :return:
        """
        test = self.test
        # Each change is a tuple of:
        #   - instantiated change object, following KGCL model
        #   - expects_raises - if True then applying the change is expected to raise an exception
        #   - test_func - a function that checks the state of the ontology post-change
        #   - expanded_changes - in some cases a change will be expanded into multiple changes
        cases = [
            (
                kgcl.NodeRename(id=generate_change_id(), about_node=VACUOLE, new_value="VaCuOlE"),
                False,
                lambda oi: test.assertEqual(
                    "VaCuOlE",
                    oi.label(VACUOLE),
                ),
                None,
            ),
            (
                NodeObsoletion(id=generate_change_id(), about_node=CELL_PERIPHERY),
                False,
                lambda oi: test.assertIn(
                    CELL_PERIPHERY,
                    oi.obsoletes(),
                ),
                None,
            ),
            (
                kgcl.NodeObsoletionWithDirectReplacement(
                    id=generate_change_id(),
                    about_node=NUCLEUS,
                    has_direct_replacement=NUCLEAR_MEMBRANE,
                ),
                False,
                [
                    lambda oi: test.assertIn(
                        NUCLEUS,
                        oi.obsoletes(),
                    ),
                    lambda oi: test.assertEqual(
                        [NUCLEAR_MEMBRANE],
                        oi.entity_metadata_map(NUCLEUS).get(TERM_REPLACED_BY, []),
                    ),
                ],
                None,
            ),
            (NodeObsoletion(id=generate_change_id(), about_node=FAKE_ID), True, None, None),
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
                [
                    kgcl.NewSynonym(
                        id=generate_change_id(),
                        about_node=CELLULAR_COMPONENT,
                        new_value="foo bar",
                    ),
                    kgcl.RemoveSynonym(
                        id=generate_change_id(),
                        about_node=CELLULAR_COMPONENT,
                        old_value="subcellular entity",
                    ),
                ],
            ),
            (
                kgcl.NewSynonym(id=generate_change_id(), about_node=FUNGI, new_value="shroom"),
                False,
                lambda oi: test.assertCountEqual(
                    ["shroom", "fungi", "Fungi", "Mycota"],
                    oi.entity_aliases(FUNGI),
                ),
                None,
            ),
            (
                kgcl.RemoveSynonym(
                    id=generate_change_id(),
                    about_node=OPISTHOKONTA,
                    old_value="Fungi/Metazoa group",
                ),
                False,
                lambda oi: test.assertCountEqual(
                    ["Opisthokonta", "opisthokonts"],
                    oi.entity_aliases(OPISTHOKONTA),
                ),
                None,
            ),
            (
                kgcl.NewTextDefinition(
                    id=generate_change_id(),
                    about_node=OPISTHOKONTA,
                    new_value="It is an opisthokonta.",
                ),
                False,
                lambda oi: test.assertEqual(
                    "It is an opisthokonta.",
                    oi.definition(OPISTHOKONTA),
                ),
                None,
            ),
            (
                kgcl.NodeTextDefinitionChange(
                    id=generate_change_id(),
                    about_node=BIOLOGICAL_PROCESS,
                    new_value="It is a biological process.",
                ),
                False,
                lambda oi: test.assertEqual(
                    "It is a biological process.",
                    oi.definition(BIOLOGICAL_PROCESS),
                ),
                None,
            ),
        ]
        # Apply changes and test the end-state is as expected
        for case in cases:
            change, expects_raises, test_func, expanded_changes = case
            if expects_raises:
                with test.assertRaises(ValueError):
                    oi.apply_patch(change)
            else:
                oi.apply_patch(change)
                if isinstance(test_func, list):
                    [t(oi) for t in test_func]
                else:
                    test_func(oi)
        if roundtrip_function:
            # pass through a save and reload
            oi2 = roundtrip_function(oi)
        else:
            # just use the original ontology
            oi2 = oi
        # gather all changes that do not raise errors
        # (gather as dict objects to make more comparable)
        expected_changes = []
        for case in cases:
            change, expects_raises, test_func, expanded_changes = case
            if test_func:
                # re-apply test function
                if isinstance(test_func, list):
                    [t(oi2) for t in test_func]
                else:
                    test_func(oi2)
            if not expects_raises:
                if not expanded_changes:
                    expanded_changes = [change]
                for change in expanded_changes:
                    change_obj = _as_json_dict_no_id(change)
                    # if "old_value" in change_obj:
                    #    del change_obj["old_value"]
                    expected_changes.append(change_obj)
        # perform a diff between the original ontology and the post-change ontology;
        # compare these with the expected changes
        if original_oi:
            diffs = original_oi.diff(oi2)
            for diff in diffs:
                kgcl_diff = render(diff)
                logging.info(kgcl_diff)
                change_obj = _as_json_dict_no_id(diff)
                if "old_value" in change_obj and "new_value" in change_obj:
                    del change_obj["old_value"]
                if change_obj in expected_changes:
                    expected_changes.remove(change_obj)
                else:
                    raise ValueError(f"Cannot find: {change_obj} in {expected_changes}")
            test.assertCountEqual([], expected_changes)

    def test_patcher_obsoletion_chains(self, get_adapter_function: Callable):
        """
        Tests logic for expanding multiple obsoletions.

        An obsoletion change can be expanded into multiple additional changes,
        to *rewire* the ontology around the removed class.

        This rewiring should also work when multiple obsoletions are
        combined together

        :param get_adapter_function: function to generate a fresh adapter
        """
        test = self.test
        cases = [
            ([CYTOPLASM], "cannot be obsoleted as used in logical definition", []),
            ([VACUOLE], None, [(ENDOMEMBRANE_SYSTEM, HAS_PART, IMBO)]),
            (
                [ENDOMEMBRANE_SYSTEM],
                None,
                [(NUCLEAR_ENVELOPE, PART_OF, CELLULAR_ANATOMICAL_ENTITY)],
            ),
            (
                [ENDOMEMBRANE_SYSTEM, VACUOLE],
                None,
                [(NUCLEAR_ENVELOPE, PART_OF, CELLULAR_ANATOMICAL_ENTITY)],
            ),
            (
                [VACUOLE, ENDOMEMBRANE_SYSTEM],
                None,
                [(NUCLEAR_ENVELOPE, PART_OF, CELLULAR_ANATOMICAL_ENTITY)],
            ),
            ([NUCLEAR_ENVELOPE], None, [(NUCLEAR_MEMBRANE, PART_OF, ENDOMEMBRANE_SYSTEM)]),
            (
                [NUCLEAR_ENVELOPE, ENDOMEMBRANE_SYSTEM],
                None,
                [(NUCLEAR_MEMBRANE, PART_OF, CELLULAR_ANATOMICAL_ENTITY)],
            ),
            (
                [NUCLEAR_ENVELOPE, ENDOMEMBRANE_SYSTEM, VACUOLE],
                None,
                [(NUCLEAR_MEMBRANE, PART_OF, CELLULAR_ANATOMICAL_ENTITY)],
            ),
            (
                [CYTOPLASMIC_REGION],
                None,
                [(CELL_CORTEX_REGION, IS_A, CYTOPLASM), (CELL_CORTEX_REGION, PART_OF, CYTOPLASM)],
            ),
            ([CELL_CORTEX_REGION, CELL_CORTEX], None, []),
            ([CELL_CORTEX_REGION, CELL_CORTEX, CYTOPLASMIC_REGION, CYTOPLASM], None, []),
            (
                [CYTOPLASM, CELL_CORTEX_REGION, CELL_CORTEX, CYTOPLASMIC_REGION],
                "order of obsoletion is wrong",
                [],
            ),
        ]
        for obsoletions, failure_reason, expected_edges in cases:
            commands = [f"obsolete {t}" for t in obsoletions]
            changes = [kgcl_parser.parse_statement(c) for c in commands]
            oi = get_adapter_function()
            current_obsolete_entities = list(oi.obsoletes())
            for o in obsoletions:
                test.assertNotIn(o, current_obsolete_entities)
            current_relationships = list(oi.relationships())
            for e in expected_edges:
                test.assertNotIn(e, current_relationships)
            if failure_reason:
                with test.assertRaises(ValueError):
                    oi.expand_changes(changes, apply=True)
                continue
            # expanded_changes = oi.expand_changes(changes, apply=False)
            # for change in expanded_changes:
            #    print(json_dumper.dumps(change))
            expanded_changes = oi.expand_changes(changes, apply=True)
            logging.info(f"Expanded changes: {len(expanded_changes)}")
            test.assertGreater(len(expanded_changes), 1)
            refreshed_obsolete_entities = list(oi.obsoletes())
            for o in obsoletions:
                test.assertIn(o, refreshed_obsolete_entities)
            test.assertCountEqual(
                obsoletions, set(refreshed_obsolete_entities) - set(current_obsolete_entities)
            )
            refreshed_relationships = list(oi.relationships())
            for e in expected_edges:
                test.assertIn(e, refreshed_relationships)

    def test_add_contributors(self, oi: PatcherInterface, legacy: bool = True):
        """
        Tests adding contributor metadata using default properties

        :param oi:
        :param legacy: if True, assume legacy oboInOwl properties
        :return:
        """
        test = self.test
        contributors = ["orcid:1234", "orcid:5678"]
        date = "2022-02-02"
        creator = contributors[0]
        oi.add_contributors(NUCLEUS, contributors)
        oi.set_creator(NUCLEUS, creator)
        oi.set_creation_date(NUCLEUS, date)
        mm = oi.entity_metadata_map(NUCLEUS)
        test.assertCountEqual(mm[CONTRIBUTOR], contributors)
        if legacy:
            test.assertEqual(mm[OIO_CREATED_BY], [creator])
            test.assertEqual(mm[OIO_CREATION_DATE], [date])
        else:
            test.assertEqual(mm[CREATOR], [creator])
            test.assertEqual(mm[CREATED], [date])

    def test_summary_statistics(self, oi: SummaryStatisticsInterface):
        """
        Tests ability to produce summary statistics
        :param oi:
        :return:
        """
        test = self.test
        oi.include_residuals = True
        stats = oi.branch_summary_statistics(include_entailed=True)
        test.assertEqual(247, stats.class_count)
        test.assertEqual(94, stats.class_count_with_text_definitions)
        test.assertEqual(16, stats.subset_count)
        test.assertEqual(12, stats.class_count_by_subset["obo:go#goslim_yeast"].filtered_count)
        test.assertEqual(23, stats.edge_count_by_predicate[PART_OF].filtered_count)
        test.assertEqual(223, stats.edge_count_by_predicate[IS_A].filtered_count)
        test.assertEqual(591108, stats.entailed_edge_count_by_predicate[IS_A].filtered_count)
        test.assertEqual(255, stats.distinct_synonym_count)
        test.assertEqual(264, stats.synonym_statement_count)
        test.assertEqual(
            136, stats.synonym_statement_count_by_predicate[HAS_EXACT_SYNONYM].filtered_count
        )
        test.assertEqual(152, stats.mapping_statement_count_by_predicate[HAS_DBXREF].filtered_count)
        stats_cc = oi.branch_summary_statistics("cc", branch_roots=[CELLULAR_COMPONENT])
        test.assertEqual(23, stats_cc.class_count)
        test.assertEqual(23, stats_cc.class_count_with_text_definitions)
        test.assertEqual(19, stats_cc.edge_count_by_predicate[PART_OF].filtered_count)
        test.assertEqual(26, stats_cc.edge_count_by_predicate[IS_A].filtered_count)
        test.assertEqual(29, stats_cc.distinct_synonym_count)
        test.assertEqual(29, stats_cc.synonym_statement_count)
        test.assertEqual(
            14, stats_cc.synonym_statement_count_by_predicate[HAS_EXACT_SYNONYM].filtered_count
        )
        test.assertEqual(
            17, stats_cc.mapping_statement_count_by_predicate[HAS_DBXREF].filtered_count
        )
        stats_ns = oi.branch_summary_statistics(
            "cc_namespace", property_values={"oio:hasOBONamespace": "cellular_component"}
        )
        test.assertEqual(23, stats_ns.class_count)
        test.assertEqual(23, stats_ns.class_count_with_text_definitions)
        test.assertEqual(19, stats_ns.edge_count_by_predicate[PART_OF].filtered_count)
        test.assertEqual(26, stats_ns.edge_count_by_predicate[IS_A].filtered_count)
        test.assertEqual(29, stats_ns.distinct_synonym_count)
        test.assertEqual(29, stats_ns.synonym_statement_count)
        test.assertEqual(
            14, stats_ns.synonym_statement_count_by_predicate[HAS_EXACT_SYNONYM].filtered_count
        )
        test.assertEqual(
            17, stats_ns.mapping_statement_count_by_predicate[HAS_DBXREF].filtered_count
        )
        logging.info("Test grouping by OBO Namespace")
        global_stats = oi.global_summary_statistics(group_by="oio:hasOBONamespace")
        gs_cc = global_stats.partitions["cellular_component"]
        test.assertEqual(14, gs_cc.subset_count)
        test.assertEqual(8, gs_cc.class_count_by_subset["obo:go#goslim_yeast"].filtered_count)
        test.assertCountEqual(
            [
                "cellular_component",
                "biological_process",
                "molecular_function",
                "external",
                "__RESIDUAL__",
            ],
            list(global_stats.partitions.keys()),
        )
        for k, v in vars(stats_ns).items():
            if isinstance(v, int):
                test.assertEqual(v, getattr(gs_cc, k))
        logging.info("Test grouping by prefix")
        global_stats = oi.global_summary_statistics(group_by="sh:prefix")
        ro_stats = global_stats.partitions["RO"]
        test.assertEqual(0, ro_stats.class_count)
        test.assertEqual(88, ro_stats.object_property_count)
        test.assertEqual(13, ro_stats.distinct_synonym_count)
        test.assertEqual(14, ro_stats.synonym_statement_count)
        go_stats = global_stats.partitions["GO"]
        test.assertEqual(74, go_stats.class_count)
        test.assertEqual(0, go_stats.object_property_count)
        test.assertEqual(23, go_stats.edge_count_by_predicate[PART_OF].filtered_count)
        test.assertEqual(104, go_stats.edge_count_by_predicate[IS_A].filtered_count)
        test.assertEqual(15, go_stats.subset_count)
        test.assertEqual(179, go_stats.distinct_synonym_count)
        test.assertEqual(179, go_stats.synonym_statement_count)
        # check numbers agree
        go_stats2 = oi.branch_summary_statistics(prefixes=["GO"])
        ro_stats2 = oi.branch_summary_statistics(prefixes=["RO"])
        for s1, s2 in [(go_stats, go_stats2), (ro_stats, ro_stats2)]:
            for k, v in vars(s1).items():
                if isinstance(v, int):
                    test.assertEqual(v, getattr(s2, k))

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

    def test_class_enrichment(self, oi: ClassEnrichmentCalculationInterface):
        """
        Tests statistical overrepresentation of classes.

        :param oi:
        :return:
        """
        test = self.test
        data = {
            NUCLEUS: [GENE1],
            NUCLEAR_MEMBRANE: [GENE2, GENE3],
            NUCLEAR_ENVELOPE: [GENE3, GENE6, GENE7],
            VACUOLE: [GENE4, GENE5],
            IMBO: [GENE8, GENE9],
        }
        assoc_cases = []
        for t, genes in data.items():
            for g in genes:
                assoc_cases.append(Association(g, LOCATED_IN, t))
        oi.add_associations(assoc_cases)
        assocs = list(oi.associations())
        test.assertCountEqual(assoc_cases, assocs)
        cases = [
            ([GENE1, GENE6, GENE7], 0.5, None, None, None, [NUCLEUS]),
            ([GENE1, GENE6, GENE7], 0.5, [], None, None, [NUCLEAR_ENVELOPE]),
            # exact overlap
            ([GENE3, GENE6, GENE7], 0.5, None, None, [NUCLEAR_ENVELOPE], [NUCLEAR_ENVELOPE]),
            # nuclear membrane is before nucleus as less common overall
            ([GENE1, GENE2, GENE3], 1.0, None, None, [NUCLEAR_MEMBRANE], [NUCLEAR_MEMBRANE]),
            ([GENE1, GENE2, GENE3], 0.05, None, None, [], []),
            ([GENE1, GENE2, GENE4, GENE5, GENE6], 0.5, None, None, [VACUOLE, CYTOPLASM], [VACUOLE]),
            ([GENE8, GENE9], 1.0, None, None, [IMBO], None),
        ]
        for case in cases:
            genes, cutoff, preds, background, expected, expected_nr = case
            if preds is None:
                preds = [IS_A, PART_OF]
            results = list(
                oi.enriched_classes(
                    genes,
                    background=background,
                    cutoff=1.0,
                    autolabel=True,
                    object_closure_predicates=preds,
                )
            )
            logging.info(f"\nGene set: {genes} preds: {preds}")
            for r in results:
                redundant = (
                    r.ancestor_of_more_informative_result,
                    r.descendant_of_more_informative_result,
                )
                logging.info(f"  C: {r.class_id} ({r.class_label}) p: {r.p_value} {redundant}")
            if expected is not None:
                test.assertCountEqual(
                    expected,
                    [r.class_id for r in results[0 : len(expected)]],
                    msg=f"Failed for {case}",
                )
            if expected_nr is not None:
                test.assertCountEqual(
                    expected_nr,
                    [
                        r.class_id
                        for r in results[0 : len(expected_nr)]
                        if not r.ancestor_of_more_informative_result
                        or r.descendant_of_more_informative_result
                    ],
                    msg=f"Failed NR for {case}",
                )

    def test_common_ancestors(self, oi: SemanticSimilarityInterface):
        """
        Tests behavior of common ancestors and most recent common ancestors.

        Pairs of entities are tested to determine if their common ancestors and
        MRCAs match what is expected, when filtered by a specified predicate list.

        :param oi:
        :return:
        """
        test = self.test
        expected = [
            (NUCLEUS, NUCLEUS, [IS_A], None, [NUCLEUS]),
            (NUCLEUS, VACUOLE, [IS_A], None, [IMBO]),
            (NUCLEUS, IMBO, [IS_A], None, [IMBO]),
            # (NUCLEUS, NUCLEUS, [], None, [NUCLEUS]),
            (NUCLEUS, NUCLEUS, [IS_A, PART_OF], None, [NUCLEUS]),
            (NUCLEAR_ENVELOPE, NUCLEUS, [IS_A, PART_OF], None, [NUCLEUS]),
            (NUCLEAR_ENVELOPE, NUCLEUS, [IS_A], None, [CELLULAR_ANATOMICAL_ENTITY]),
            (BIOLOGICAL_PROCESS, NUCLEUS, [IS_A], [OWL_THING], [OWL_THING]),
        ]
        for x, y, preds, expected_ancs, expected_mrcas in expected:
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
                    test.assertGreaterEqual(m[child], m[parent])
            else:
                test.assertGreater(m[child], m[parent])

    def test_pairwise_similarity(self, oi: SemanticSimilarityInterface):
        test = self.test
        # test non-existent item
        test.assertEqual([(OWL_THING, 0.0)], list(oi.information_content_scores([OWL_THING])))
        sim = oi.pairwise_similarity(NUCLEUS, FAKE_ID)
        test.assertEqual(0.0, sim.ancestor_information_content, "fake id should have no IC")
        test.assertEqual(0.0, sim.jaccard_similarity)
        terms = [NUCLEUS, FAKE_ID]
        pairs = list(oi.all_by_all_pairwise_similarity(terms, terms, predicates=[IS_A]))
        test.assertEqual(4, len(pairs))
        for pair in pairs:
            if pair.subject_id == pair.object_id:
                test.assertGreater(
                    pair.jaccard_similarity,
                    0.99,
                    f"self similarity should be 1.0; {pair.subject_id}",
                )
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
                    test.assertGreater(
                        pair.phenodigm_score, 0.5, f"expected phenodigm match for {pair}"
                    )
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

    # TextAnnotatorInterface tests
    def test_annotate_text(self, oi: TextAnnotatorInterface):
        test = self.test
        cases = [
            (
                "The nucleus is the part of the cell that contains the DNA.",
                3,
                [(NUCLEUS, "nucleus", 5, 11), (PART_OF, "part of", 20, 26), (CELL, "cell", 32, 35)],
            ),
        ]
        for text, n, expected in cases:
            anns = list(oi.annotate_text(text))
            anns = sorted(anns, key=lambda x: x.subject_start)
            test.assertEqual(n, len(anns))
            for i, ann in enumerate(anns):
                print(ann)
                object_id, object_label, subject_start, subject_end = expected[i]
                test.assertEqual(object_id, ann.object_id)
                test.assertEqual(object_label, ann.object_label)
                test.assertEqual(subject_start, ann.subject_start)
                test.assertEqual(subject_end, ann.subject_end)
