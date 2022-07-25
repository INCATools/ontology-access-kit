from typing import Dict, Iterable, List, Tuple

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.semsim.similarity_utils import (
    ListPair,
    compute_all_pairs,
    setwise_jaccard_similarity,
)

SUBSET_DICT = Dict[SUBSET_CURIE, List[CURIE]]
DEFAULT_PREDICATES = [IS_A, PART_OF]


def get_subset_dict(oi: OboGraphInterface) -> SUBSET_DICT:
    """
    Return a dictionary keyed by subset name with value being all subset members

    :param oi: An ontology interface for making label lookups.
    :return:
    """
    return {s: list(oi.subset_members(s)) for s in oi.subsets()}


def terms_by_subsets(
    oi: OboGraphInterface,
    remove_empty: bool = True,
    subsumed_score: float = None,
    min_subsets: int = None,
    prefix: str = None,
) -> Iterable[Tuple]:
    subsets = get_subset_dict(oi)
    subsets = filter_by_prefix(subsets, prefix)
    if remove_empty:
        subsets = {k: v for k, v in subsets.items() if v != []}
    all_curies = set()
    for curies in subsets.values():
        all_curies.update(curies)
    label_map = {curie: label for curie, label in oi.labels(all_curies)}
    predicates = DEFAULT_PREDICATES
    subset_ancs = {}
    if subsumed_score is not None:
        for subset, subset_curies in subsets.items():
            subset_ancs[subset] = set(oi.ancestors(subset_curies, predicates=predicates))
    for curie in all_curies:
        tups = []
        n = 0
        for subset, subset_curies in subsets.items():
            v = 0.0
            if curie in subset_curies:
                v = 1.0
                n += 1
            else:
                if subsumed_score is not None:
                    # if len(set(oi.ancestors(curie, predicates=predicates)).intersection(subset_curies)) > 0:
                    if subset in subset_ancs and curie in subset_ancs[subset]:
                        v = subsumed_score
            tups.append((curie, label_map[curie], subset, v))
        if min_subsets is not None and n < min_subsets:
            continue
        for tup in tups:
            yield tup


def filter_by_prefix(subsets: SUBSET_DICT, prefix: str) -> SUBSET_DICT:
    if prefix:

        def include(x: str):
            return x.startswith(f"{prefix}:")

        return {k: [x for x in v if include(x)] for k, v in subsets.items()}
    else:
        return subsets


def compare_all_subsets(
    oi: OboGraphInterface, extend_down: bool = False, remove_empty: bool = True, prefix: str = None
) -> Iterable[ListPair]:
    """

    :param oi: An ontology interface for making label lookups.
    :return:
    """
    subsets = get_subset_dict(oi)
    if extend_down:
        subsets = extend_subsets_down(oi)
    if prefix:

        def include(x: str):
            return x.startswith(f"{prefix}:")

        subsets = {k: [x for x in v if include(x)] for k, v in subsets.items()}
    if remove_empty:
        subsets = {k: v for k, v in subsets.items() if v != []}
    return compute_all_pairs(subsets)


def extend_subsets_down(
    oi: OboGraphInterface, predicates: List[PRED_CURIE] = DEFAULT_PREDICATES
) -> SUBSET_DICT:
    subsets = get_subset_dict(oi)
    all_curies = set()
    for curies in subsets.values():
        all_curies.update(curies)
    new_subsets = {}
    for subset, curies in subsets.items():
        extended_set = set(oi.descendants(curies, predicates=predicates)).intersection(all_curies)
        new_subsets[subset] = list(extended_set)
    return new_subsets


def subset_overlap(
    oi: OboGraphInterface,
    subset1: SUBSET_CURIE,
    subset2: SUBSET_CURIE,
    predicates: List[PRED_CURIE] = None,
) -> float:
    curies1 = list(oi.subset_members(subset1))
    curies2 = list(oi.subset_members(subset2))
    if predicates is None:
        predicates = [IS_A, PART_OF]
    descs1 = oi.descendants(curies1, predicates=predicates)
    descs2 = oi.descendants(curies2, predicates=predicates)
    return setwise_jaccard_similarity(descs1, descs2)


def all_subsets_overlap(oi: OboGraphInterface) -> List[Tuple[float, SUBSET_CURIE, SUBSET_CURIE]]:
    subsets = list(oi.subsets())
    results = []
    dmap = {s: list(oi.descendants(list(oi.subset_members(s)))) for s in subsets}
    dmap = {k: v for k, v in dmap.items() if len(v) > 0}
    subsets = dmap.keys()
    for s1 in subsets:
        for s2 in subsets:
            if s1 == s2:
                results.append((1.0, s1, s2))
            elif s1 > s2:
                results.append((setwise_jaccard_similarity(dmap[s1], dmap[s2]), s1, s2))
    results.sort(key=lambda tup: 1 - tup[0])
    return results
