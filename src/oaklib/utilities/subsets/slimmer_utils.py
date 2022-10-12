"""
Utilities for working with ontology subsets (slims)
----
"""

import logging
from typing import Collection, Dict, List

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE


def filter_redundant(
    oi: OboGraphInterface, curies: Collection[CURIE], predicates: List[PRED_CURIE] = None
) -> List[CURIE]:
    return [curie for curie in curies if not is_redundant(oi, curie, curies, predicates)]


def is_redundant(
    oi: OboGraphInterface,
    curie: CURIE,
    curies: Collection[CURIE],
    predicates: List[PRED_CURIE] = None,
) -> bool:
    for candidate in curies:
        if candidate != curie:
            if curie in list(oi.ancestors(candidate, predicates=predicates)):
                return True
    return False


def roll_up_to_named_subset(
    oi: OboGraphInterface, subset: CURIE, curies: List[CURIE], predicates: List[PRED_CURIE] = None
) -> Dict[CURIE, List[CURIE]]:
    """
    Rolls up all specified curies to a named subset, e.g. goslim_generic

    :param oi: An ontology interface for making label lookups.
    :param subset: Subset to be rolled into.
    :param curies: List of CURIEs to roll up into subset.
    :param predicates: Predicates of interest.
    :return: Dictionary of rolled up subset of CURIEs.
    """
    # see https://metacpan.org/dist/go-perl/view/scripts/map2slim
    terms_in_subset = list(oi.subset_members(subset))
    logging.info(f"Terms in {subset} = {len(terms_in_subset)}")
    return roll_up_to_subset(oi, terms_in_subset, curies, predicates)


def roll_up_to_subset(
    oi: OboGraphInterface,
    terms_in_subset: List[CURIE],
    curies: List[CURIE],
    predicates: List[PRED_CURIE] = None,
) -> Dict[CURIE, List[CURIE]]:
    """
    As :ref:`roll_up_to_named_subset` but with an explicit list of terms to roll up to

    :param oi:
    :param terms_in_subset:
    :param curies:
    :param predicates:
    :return:
    """
    terms_in_subset = set(terms_in_subset)
    subset_anc_map = {
        t: [a for a in oi.ancestors(t, predicates) if a != t and a in terms_in_subset]
        for t in terms_in_subset
    }
    m = {}
    for curie in curies:
        logging.info(f"  Mapping {curie}")
        ancs = list(oi.ancestors(curie, predicates=predicates))
        # print(f'{curie} ANCS={list(ancs)}')
        ancs_in_subset = terms_in_subset.intersection(ancs)
        # print(f'    xx ANCS={list(ancs_in_subset)}')
        redundant = set()
        for a in ancs_in_subset:
            redundant.update(subset_anc_map[a])
        nr_ancs_in_subset = [a for a in ancs_in_subset if a not in redundant]
        m[curie] = nr_ancs_in_subset
    return m
