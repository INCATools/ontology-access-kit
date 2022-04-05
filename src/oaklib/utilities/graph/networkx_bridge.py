"""
Utilities for working with networkx
-----------------------------------

NetworkX is a popular python package for working with graphs
"""
from collections import Iterable

import networkx as nx
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP


def relationships_to_multi_digraph(relationships: Iterable[RELATIONSHIP], reverse: bool = True) -> nx.MultiDiGraph:
    """
    Converts an OBOGraph to NetworkX

    :param relationships:
    :param reverse: treat subject as the networkx parent
    :return:
    """
    g = nx.MultiDiGraph()
    for rel in relationships:
        if reverse:
            g.add_edge(rel[2], rel[0], predicate=rel[1])
        else:
            g.add_edge(rel[0], rel[2], predicate=rel[1])
    return g
