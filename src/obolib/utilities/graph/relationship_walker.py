from copy import copy
from dataclasses import dataclass
from typing import List, Union, Dict, Iterable, Tuple

from obolib.interfaces.basic_ontology_interface import RELATIONSHIP, BasicOntologyInterface
from obolib.types import CURIE, PRED_CURIE

#PATH = Tuple[CURIE, List[PRED_CURIE], CURIE]
PATH = List[RELATIONSHIP]


def walk_up(oi: BasicOntologyInterface, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[RELATIONSHIP]:
    """
    Walks up the relation graph from a seed set of curies or individual curie, returning the full ancestry graph

    Note: this may be inefficient for remote endpoints, in future a graph walking endpoint will implement this

    :param oi:
    :param start_curies:
    :param predicates:
    :return:
    """
    if isinstance(start_curies, CURIE):
        next_curies = [start_curies]
    else:
        next_curies = copy(start_curies) # do not mutate
    rels = []
    visited = copy(next_curies)
    while len(next_curies) > 0:
        next_curie = next_curies.pop()
        for pred, fillers in oi.get_outgoing_relationships_by_curie(next_curie).items():
            if not predicates or pred in predicates:
                for filler in fillers:
                    if filler not in visited:
                        next_curies.append(filler)
                        visited.append(filler)
                    rels.append((next_curie, pred, filler))
    for rel in rels:
        yield rel

