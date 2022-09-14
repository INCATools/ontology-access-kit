"""
Utilities for traversing Ontology Graphs
====================


"""
import logging
from copy import copy
from typing import Iterable, List, Union

from oaklib.interfaces.basic_ontology_interface import (
    RELATIONSHIP,
    BasicOntologyInterface,
)
from oaklib.types import CURIE, PRED_CURIE

# PATH = Tuple[CURIE, List[PRED_CURIE], CURIE]
PATH = List[RELATIONSHIP]


def walk_up(
    oi: BasicOntologyInterface,
    start_curies: Union[CURIE, List[CURIE]],
    predicates: List[PRED_CURIE] = None,
) -> Iterable[RELATIONSHIP]:
    """
    Walks up the relation graph from a seed set of curies or individual curie, returning the full ancestry graph

    Note: this may be inefficient for remote endpoints, in future a graph walking endpoint will implement this

    :param oi: An ontology interface for making label lookups.
    :param start_curies: Seed CURIE(s) to walk from.
    :param predicates: Predicates of interest.
    :return:
    """
    if isinstance(start_curies, CURIE):
        next_curies = [start_curies]
    else:
        next_curies = copy(start_curies)  # do not mutate
    rels = []
    visited = copy(next_curies)
    while len(next_curies) > 0:
        logging.debug(f"Walking graph; {len(next_curies)} in stack; {next_curies} {predicates}")
        next_curie = next_curies.pop()
        for pred, filler in oi.outgoing_relationships(next_curie, predicates):
            if filler not in visited:
                next_curies.append(filler)
                visited.append(filler)
            rels.append((next_curie, pred, filler))
    for rel in rels:
        yield rel


def walk_down(
    oi: BasicOntologyInterface,
    start_curies: Union[CURIE, List[CURIE]],
    predicates: List[PRED_CURIE] = None,
) -> Iterable[RELATIONSHIP]:
    """
    As walk_up, but traversing incoming, not outgoing relationships

    :param oi:An ontology interface for making label lookups.
    :param start_curies: Seed CURIE(s) to walk from.
    :param predicates: Predicates of interest.
    :return:
    """
    if isinstance(start_curies, CURIE):
        next_curies = [start_curies]
    else:
        next_curies = copy(start_curies)  # do not mutate
    rels = []
    visited = copy(next_curies)
    while len(next_curies) > 0:
        next_curie = next_curies.pop()
        for pred, subjects in oi.incoming_relationship_map(next_curie).items():
            if not predicates or pred in predicates:
                for subject in subjects:
                    if subject not in visited:
                        next_curies.append(subject)
                        visited.append(subject)
                    rels.append((subject, pred, next_curie))
    for rel in rels:
        yield rel
