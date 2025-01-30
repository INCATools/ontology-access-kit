import json
import logging
import unittest
from copy import deepcopy

from curies import Converter

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.resource import OntologyResource
from oaklib.utilities.obograph_utils import (
    as_multi_digraph,
    compress_all_graph_ids,
    depth_first_ordering,
    expand_all_graph_ids,
    filter_by_predicates,
    graph_as_dict,
    graph_ids,
    graph_to_d3viz_objects,
    graph_to_tree_display,
    graph_to_tree_structure,
    induce_graph_prefix_map,
    shortest_paths,
    trim_graph,
)
from tests import (
    CELLULAR_ANATOMICAL_ENTITY,
    CELLULAR_COMPONENT,
    CELLULAR_ORGANISMS,
    CYTOPLASM,
    HUMAN,
    IMBO,
    INPUT_DIR,
    INTRACELLULAR,
    MEMBRANE,
    NUCLEAR_MEMBRANE,
    NUCLEUS,
    ORGANELLE,
    OUTPUT_DIR,
    PLASMA_MEMBRANE,
    VACUOLE,
)

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.saved.owl"


class TestOboGraphUtils(unittest.TestCase):
    def setUp(self) -> None:
        resource = OntologyResource(slug="go-nucleus.obo", directory=INPUT_DIR, local=True)
        oi = ProntoImplementation(resource)
        self.oi = oi
        self.graph = oi.as_obograph()

    def test_graph_ids(self):
        ids = list(graph_ids(self.graph))
        expected_ids = [NUCLEUS, PART_OF, HUMAN]
        expected_edges = [(NUCLEAR_MEMBRANE, PART_OF, NUCLEUS)]
        graph_edges = [(e.sub, e.pred, e.obj) for e in self.graph.edges]
        for id in expected_ids:
            self.assertIn(id, ids)
        for s, p, o in expected_edges:
            self.assertIn((s, p, o), graph_edges)
        prefix_map = induce_graph_prefix_map(self.graph, self.oi.converter)
        expected_prefix_map = {
            "GO": "http://purl.obolibrary.org/obo/GO_",
            "BFO": "http://purl.obolibrary.org/obo/BFO_",
            "CL": "http://purl.obolibrary.org/obo/CL_",
            "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
            "NCBITaxon": "http://purl.obolibrary.org/obo/NCBITaxon_",
            "RO": "http://purl.obolibrary.org/obo/RO_",
            "PATO": "http://purl.obolibrary.org/obo/PATO_",
            "CARO": "http://purl.obolibrary.org/obo/CARO_",
            "NCBITaxon_Union": "http://purl.obolibrary.org/obo/NCBITaxon_Union_",
            "owl": "http://www.w3.org/2002/07/owl#",
        }
        self.assertDictEqual(expected_prefix_map, prefix_map)
        g = deepcopy(self.graph)
        converter = Converter.from_prefix_map(prefix_map)
        expand_all_graph_ids(g, converter)
        graph_edges = [(e.sub, e.pred, e.obj) for e in g.edges]
        ids = list(graph_ids(g))
        for id in expected_ids:
            self.assertNotIn(id, ids)
            self.assertIn(converter.expand(id), ids)
        for s, p, o in expected_edges:
            self.assertIn(
                (converter.expand(s), converter.expand(p), converter.expand(o)), graph_edges
            )
        prefix_map = induce_graph_prefix_map(g, self.oi.converter)
        self.assertDictEqual(expected_prefix_map, prefix_map)
        compress_all_graph_ids(g, converter)
        self.assertCountEqual(self.graph.nodes, g.nodes)
        self.assertEqual(len(self.graph.edges), len(g.edges))

    def test_as_json(self):
        obj = graph_as_dict(self.graph)
        json_obj = json.dumps(obj)
        self.assertIn('{"id": "GO:0003674"', json_obj)
        # https://github.com/althonos/pronto/issues/163
        # self.assertIn('{"sub": "CL:0000000", "pred": "BFO:0000051", "obj": "GO:0005634"}', json_obj)

    def test_as_networkx(self):
        mdg = as_multi_digraph(self.graph)
        self.assertIn(NUCLEUS, mdg.nodes)
        for e in mdg.edges(data=True):
            logging.info(f"SU={e}")
        self.assertIn(
            ("GO:0005634", "GO:0031965", {"predicate": "BFO:0000050"}), mdg.edges(data=True)
        )

    def test_filter_by_predicates(self):
        g = self.graph
        g2 = filter_by_predicates(g, predicates=[IS_A, PART_OF])
        self.assertCountEqual(g.nodes, g2.nodes)
        self.assertGreater(len(g.edges), len(g2.edges))
        self.assertGreater(len(g2.edges), 100)

    def test_as_tree_display(self):
        t = graph_to_tree_display(self.graph, predicates=[IS_A])
        lines = t.split("\n")
        self.assertIn("[i] BFO:0000015 ! process", t)
        self.assertNotIn("[p]", t)
        self.assertNotIn(PART_OF, t)
        self.assertGreater(len(lines), 80)
        t = graph_to_tree_display(self.graph, predicates=[IS_A, PART_OF])
        lines = t.split("\n")
        self.assertIn("[i] BFO:0000015 ! process", t)
        self.assertIn("* [p] GO:0019209 ! kinase activator activity", t)
        self.assertGreater(len(lines), 80)

    def test_as_tree_structure(self):
        ts = graph_to_tree_structure(self.graph, predicates=[IS_A])
        objs = [t.model_dump() for t in ts]
        print(json.dumps(objs, indent=2))

    def test_as_d3viz(self):
        for preds in [[IS_A], [IS_A, PART_OF]]:
            for relations_as_nodes in [True, False]:
                objs = graph_to_d3viz_objects(
                    self.graph, predicates=preds, relations_as_nodes=relations_as_nodes
                )
                print(json.dumps(objs, indent=2))

    def test_trim_ancestors(self):
        oi = self.oi
        both = [IS_A, PART_OF]
        expected_list = [
            ([], 0, True, both, 0),
            ([NUCLEUS], 0, True, both, 0),
            ([NUCLEUS], 1, True, both, 1),
            ([NUCLEUS, IMBO], 0, True, both, 1),
            ([NUCLEUS, IMBO], 1, True, both, 5),
            ([NUCLEUS, VACUOLE], 0, True, both, 0),
            ([NUCLEUS, VACUOLE], 1, True, both, 3),
            ([NUCLEUS, VACUOLE, IMBO], 1, True, both, 8),
            ([NUCLEUS, VACUOLE, IMBO], 1, False, [IS_A], 4),
            ([HUMAN, CELLULAR_ORGANISMS], 1, True, [IS_A], 8),
            ([HUMAN, CELLULAR_ORGANISMS], 1, False, [IS_A], 2),
        ]
        if isinstance(oi, OboGraphInterface):
            for ex in expected_list:
                seeds, dist, include_intermediates, predicates, expected_len = ex
                g = oi.ancestor_graph(seeds, predicates=predicates)
                trimmed = trim_graph(
                    g, seeds, distance=dist, include_intermediates=include_intermediates
                )
                if expected_len is not None:
                    self.assertEqual(expected_len, len(trimmed.edges))
                node_ids = [n.id for n in trimmed.nodes]
                for seed in seeds:
                    self.assertIn(seed, node_ids)
        else:
            raise NotImplementedError

    def test_shortest_paths(self):
        """
        Test that the shortest paths are correct.

        :return:
        """
        oi = self.oi
        both = [IS_A, PART_OF]
        hi = 1.0
        lo = 0.001
        expected_list = [
            (NUCLEUS, VACUOLE, both, None, [], []),
            (NUCLEUS, CYTOPLASM, both, None, [], []),
            (
                NUCLEUS,
                CYTOPLASM,
                both,
                {IS_A: hi, PART_OF: lo},
                [INTRACELLULAR],
                [CELLULAR_ANATOMICAL_ENTITY],
            ),
            (NUCLEUS, CYTOPLASM, both, {IS_A: lo, PART_OF: hi}, [CELLULAR_ANATOMICAL_ENTITY], []),
        ]
        if isinstance(oi, OboGraphInterface):
            for ex in expected_list:
                start_curie, end_curie, preds, weights, includes, excludes = ex
                g = oi.ancestor_graph([start_curie, end_curie], predicates=preds)
                paths = shortest_paths(g, [start_curie], [end_curie], predicate_weights=weights)
                for s, o, path in paths:
                    logging.debug(f"{s} -> {o} == {path}")
                    for x in includes:
                        self.assertIn(x, path)
                    for x in excludes:
                        self.assertNotIn(x, path)

    def test_depth_first_ordering(self):
        """
        Test that the depth first ordering of the graph is correct.

        Note that DF ordering may be non-deterministic if the graph is not a tree.
        This test conservatively checks conditions that are guaranteed to hold
        even with DAGs

        :return:
        """
        oi = self.oi
        expected = [
            (
                [CELLULAR_COMPONENT],
                [IS_A, PART_OF],
                [
                    (CELLULAR_COMPONENT, CELLULAR_ANATOMICAL_ENTITY),
                    (CELLULAR_ANATOMICAL_ENTITY, ORGANELLE),
                    (CELLULAR_ANATOMICAL_ENTITY, NUCLEUS),
                ],
            ),
            (
                [CELLULAR_COMPONENT],
                [IS_A],
                [
                    (CELLULAR_COMPONENT, CELLULAR_ANATOMICAL_ENTITY),
                    (CELLULAR_ANATOMICAL_ENTITY, ORGANELLE),
                    (CELLULAR_ANATOMICAL_ENTITY, NUCLEUS),
                    (CELLULAR_ANATOMICAL_ENTITY, MEMBRANE),
                    (MEMBRANE, PLASMA_MEMBRANE),
                ],
            ),
        ]
        for starts, preds, expected_order in expected:
            graph = oi.descendant_graph(starts, predicates=preds)
            ordered = depth_first_ordering(graph)
            if len(starts) == 1:
                self.assertEqual(ordered[0], starts[0])
            for parent, child in expected_order:
                self.assertLess(ordered.index(parent), ordered.index(child), f"{parent} -> {child}")
