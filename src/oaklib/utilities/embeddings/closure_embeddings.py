"""
Closure ("multi-hot") encoding of ontology terms.

Each term is encoded as a binary vector over a vocabulary of terms, with a 1 at the
position of each of its reflexive ancestors. Under this encoding, classic set-based
semantic similarity measures become vector comparisons; e.g. Jaccard over closure
vectors is identical to the ancestor-set Jaccard used by
:meth:`SemanticSimilarityInterface.pairwise_similarity`.
"""

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np

from oaklib.datamodels.vocabulary import IS_A, OWL_THING
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE

__all__ = [
    "closure_embeddings",
]


def closure_embeddings(
    adapter: OboGraphInterface,
    curies: Iterable[CURIE],
    predicates: Optional[List[PRED_CURIE]] = None,
    vocabulary: Optional[List[CURIE]] = None,
    weights: Optional[Dict[CURIE, float]] = None,
) -> Tuple[List[CURIE], List[CURIE], np.ndarray]:
    """
    Encode terms as multi-hot vectors of their reflexive ancestors.

    If ``weights`` is supplied, each ancestor's position holds its weight (e.g. its
    information content) instead of 1; ancestors without a weight get 0.

    Unless ``vocabulary`` is supplied, the vector dimensions are the union of the
    ancestors of the requested terms. Vectors are therefore only comparable with
    other vectors produced by the same call (or with the same vocabulary).

    :param adapter: an adapter that can compute ancestors
    :param curies: the terms to encode
    :param predicates: predicates to traverse; defaults to is_a
    :param vocabulary: the terms that make up the vector dimensions
    :param weights: optional weight for each ancestor, e.g. information content
    :return: tuple of (encoded curies, vocabulary, matrix of shape (len(curies), len(vocabulary)))
    """
    if predicates is None:
        predicates = [IS_A]
    curies = list(dict.fromkeys(curies))
    closures = {
        c: set(adapter.ancestors(c, predicates=predicates, reflexive=True)) - {OWL_THING}
        for c in curies
    }
    if vocabulary is None:
        vocabulary = sorted(set().union(*closures.values())) if closures else []
    index = {t: i for i, t in enumerate(vocabulary)}
    matrix = np.zeros((len(curies), len(vocabulary)), dtype=np.float32)
    for row, c in enumerate(curies):
        for anc in closures[c]:
            col = index.get(anc)
            if col is not None:
                matrix[row, col] = 1.0 if weights is None else weights.get(anc, 0.0)
    return curies, list(vocabulary), matrix
