import logging
import unittest

import yaml
from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.vocabulary import HAS_PART, IS_A, PART_OF
from oaklib.implementations.aggregator.aggregator_implementation import (
    AggregatorImplementation,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import graph_as_dict
from tests import (
    CELLULAR_COMPONENT,
    CYTOPLASM,
    INPUT_DIR,
    INTERNEURON,
    NUCLEUS,
    OUTPUT_DIR,
    TISSUE,
    VACUOLE,
)

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_ONT2 = INPUT_DIR / "interneuron.obo"


class TestAggregator(unittest.TestCase):
    """
    Tests the ability to wrap multiple implementations as if it were a single source
    """

    def setUp(self) -> None:
        resource1 = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        resource2 = OntologyResource(slug="interneuron.obo", directory=INPUT_DIR, local=True)
        oi1 = ProntoImplementation(resource1)
        oi2 = ProntoImplementation(resource2)
        self.oi = AggregatorImplementation(implementations=[oi1, oi2])

    def test_relationships(self):
        oi = self.oi
        rels = oi.get_outgoing_relationship_map_by_curie("GO:0005773")
        # for k, v in rels.items():
        #    print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ["GO:0043231"])
        self.assertCountEqual(rels[PART_OF], [CYTOPLASM])
        rels = oi.get_outgoing_relationship_map_by_curie(TISSUE)
        # for k, v in rels.items():
        #    print(f'{k} = {v}')
        self.assertCountEqual(rels[IS_A], ["UBERON:0010000"])

    def test_all_terms(self):
        curies = list(self.oi.all_entity_curies())
        self.assertIn(NUCLEUS, curies)
        self.assertIn(INTERNEURON, curies)

    def test_relations(self):
        oi = self.oi
        label = oi.get_label_by_curie(PART_OF)
        assert label.startswith("part")
        t = self.oi.node(PART_OF)
        assert t.id == PART_OF
        assert t.lbl.startswith("part")

    @unittest.skip("TODO")
    def test_metadata(self):
        for curie in self.oi.all_entity_curies():
            m = self.oi.metadata_map_by_curie(curie)
            print(f"{curie} {m}")
        m = self.oi.metadata_map_by_curie("GO:0005622")
        assert "term_tracker_item" in m.keys()
        assert "https://github.com/geneontology/go-ontology/issues/17776" in m["term_tracker_item"]

    def test_labels(self):
        """
        Tests labels can be retrieved, and no label is retrieved when a term does not exist
        :return:
        """
        oi = self.oi
        label = oi.get_label_by_curie(VACUOLE)
        self.assertEqual(str, type(label))
        self.assertEqual(label, "vacuole")
        label = oi.get_label_by_curie("FOOBAR:123")
        self.assertIsNone(label)
        # TODO: test strict mode
        label = oi.get_label_by_curie(IS_A)
        self.assertIsNotNone(label)
        self.assertEqual("interneuron", oi.get_label_by_curie(INTERNEURON))
        self.assertEqual("tissue", oi.get_label_by_curie(TISSUE))

    def test_synonyms(self):
        syns = self.oi.aliases_by_curie(CELLULAR_COMPONENT)
        self.assertCountEqual(
            syns,
            [
                "cellular_component",
                "cellular component",
                "cell or subcellular entity",
                "subcellular entity",
            ],
        )
        syns = self.oi.aliases_by_curie("CL:0000100")
        self.assertCountEqual(syns, ["motoneuron", "motor neuron"])
        self.assertCountEqual(
            self.oi.aliases_by_curie(TISSUE),
            ["tissue", "simple tissue", "tissue portion", "portion of tissue"],
        )

    def test_subsets(self):
        oi = self.oi
        subsets = list(oi.all_subset_curies())
        self.assertIn("goslim_aspergillus", subsets)
        self.assertIn("GO:0003674", oi.curies_by_subset("goslim_generic"))
        self.assertNotIn("GO:0003674", oi.curies_by_subset("gocheck_do_not_manually_annotate"))
        self.assertIn(TISSUE, oi.curies_by_subset("pheno_slim"))

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors("GO:0005773"))
        for a in ancs:
            logging.info(a)
        assert "NCBITaxon:1" in ancs
        assert "GO:0005773" in ancs  # reflexive
        ancs = list(oi.ancestors("GO:0005773", predicates=[IS_A]))
        # for a in ancs:
        #    print(a)
        assert "NCBITaxon:1" not in ancs
        assert "GO:0005773" in ancs  # reflexive
        assert "GO:0043231" in ancs  # reflexive
        ancs = list(oi.ancestors(TISSUE, predicates=[IS_A, PART_OF]))
        for a in ancs:
            print(a)
        assert "UBERON:0010000" in ancs

    def test_obograph(self):
        g = self.oi.ancestor_graph(VACUOLE)
        obj = graph_as_dict(g)
        assert "nodes" in g
        assert "edges" in g
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == VACUOLE]))
        ancs = list(self.oi.ancestors(VACUOLE, predicates=[IS_A, PART_OF]))
        assert VACUOLE in ancs
        assert CYTOPLASM in ancs
        descs = list(self.oi.descendants(CYTOPLASM, predicates=[IS_A, PART_OF]))
        assert VACUOLE in descs
        assert CYTOPLASM in descs
        g = self.oi.ancestor_graph(CYTOPLASM)
        # check is reflexive
        self.assertEqual(1, len([n for n in g.nodes if n.id == CYTOPLASM]))
        g = self.oi.ancestor_graph(TISSUE)
        print(yaml_dumper.dumps(g))
        assert self.oi.node(TISSUE).lbl == "tissue"
