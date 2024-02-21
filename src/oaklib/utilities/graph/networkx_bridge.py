"""
Utilities for working with networkx
-----------------------------------

NetworkX is a popular python package for working with graphs
"""

from collections import defaultdict
from typing import Dict, Iterable, List, Tuple

import networkx as nx
from sssom_schema import Mapping

from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP
from oaklib.types import CURIE, PRED_CURIE


def mappings_to_graph(mappings: Iterable[Mapping]) -> nx.Graph:
    g = nx.Graph()
    for m in mappings:
        g.add_edge(m.subject_id, m.object_id)
    return g


def relationships_to_multi_digraph(
    relationships: Iterable[RELATIONSHIP], reverse: bool = True
) -> nx.MultiDiGraph:
    """
    Converts an OBOGraph to NetworkX

    :param relationships:
    :param reverse: treat subject as the networkx parent (default true)
    :return:
    """
    g = nx.MultiDiGraph()
    for rel in relationships:
        if reverse:
            g.add_edge(rel[2], rel[0], predicate=rel[1])
        else:
            g.add_edge(rel[0], rel[2], predicate=rel[1])
    return g


def transitive_reduction(relationships: Iterable[RELATIONSHIP]) -> Iterable[RELATIONSHIP]:
    relationships = list(relationships)
    tuples = [(o, s) for s, p, o in relationships]
    g = nx.DiGraph(tuples)
    reduced = nx.transitive_reduction(g)
    for r in relationships:
        s, p, o = r
        if (o, s) in reduced.edges:
            yield r


def transitive_reduction_by_predicate(
    relationships: Iterable[RELATIONSHIP],
) -> Iterable[RELATIONSHIP]:
    """
    Performs a simple transitive reduction of a graph, in which each predicate is treated as independent,
    and forming its own distinct graph

    :param relationships:
    :return:
    """
    relationships = list(relationships)
    tuples_dict: Dict[PRED_CURIE, List[Tuple[CURIE, CURIE]]] = defaultdict(list)
    rels_dict: Dict[PRED_CURIE, List[RELATIONSHIP]] = defaultdict(list)
    for s, p, o in relationships:
        if o != s:
            tuples_dict[p].append((o, s))
        rels_dict[p].append((s, p, o))
    for p, tuples in tuples_dict.items():
        g = nx.DiGraph(tuples)
        if not nx.is_directed_acyclic_graph(g):
            cycles = [(s, o) for (s, o) in g.edges() if g.has_edge(o, s)]
            for s, o in cycles:
                g.remove_edge(s, o)
        reduced = nx.transitive_reduction(g)
        for r in rels_dict[p]:
            s, _, o = r
            if (o, s) in reduced.edges:
                yield r
