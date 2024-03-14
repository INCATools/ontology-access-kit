import csv
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple, Union

from oaklib.types import CURIE


@dataclass
class ListPair:
    set1_id: str = None
    set2_id: str = None
    list1: List = None
    list2: List = None
    list1_len: int = None
    list2_len: int = None
    intersection_len: int = None
    union_len: int = None
    jaccard_similarity: float = None
    dice_similarity: float = None
    overlap_coefficient: float = None
    subsumes_score: float = None
    subsumed_by_score: float = None


NAMED_COLLECTION = Tuple[str, List]
LIST_OR_SET = Union[List, Set]


def compute_list_pair_statistics(pair: ListPair):
    set1 = set(pair.set1_id)
    set2 = set(pair.set2_id)
    pair.list1_len = len(set1)
    pair.list2_len = len(set2)
    pair.intersection_len = len(set1.intersection(set2))
    pair.union_len = len(set1.union(set2))
    pair.jaccard_similarity = pair.intersection_len / pair.union_len
    pair.dice_similarity = 2 * pair.intersection_len / (pair.list1_len + pair.list2_len)
    pair.overlap_coefficient = pair.intersection_len / min(pair.list1_len, pair.list2_len)
    pair.subsumed_by_score = pair.intersection_len / pair.list1_len
    pair.subsumes_score = pair.intersection_len / pair.list2_len


def compute_all_pairs(sets: Dict[str, List]) -> Iterable[ListPair]:
    """
    compute statistics on all pairs of sets

    :param sets:
    :return:
    """
    for k1, _ in sets.items():
        for k2, _ in sets.items():
            r = ListPair(k1, k2)
            compute_list_pair_statistics(r)
            yield r


def setwise_jaccard_similarity(set1: LIST_OR_SET, set2: LIST_OR_SET) -> float:
    set1 = set(set1)
    set2 = set(set2)
    return len(set1.intersection(set2)) / len(set1.union(set2))


def load_information_content_map(path: str) -> Dict[CURIE, float]:
    """
    Load information content map from file.

    Columns: id, information_content

    Example:
    -------
    >>> from oaklib.utilities.semsim.similarity_utils import load_information_content_map
    >>> icmap = load_information_content_map("tests/input/go-nucleus.ic.tsv")
    >>> ic = icmap["GO:0016310"]
    >>> print(f"{ic:.3f}")
    4.273

    IC tables can be computed using the :ref:`SemanticSimilarityInterface.information_content_scores` method.

    :param path:
    :return: mapping from IDs to information content

    """
    with open(path) as f:
        dr = csv.DictReader(f, delimiter="\t")
        return {row["id"]: float(row["information_content"]) for row in dr}
