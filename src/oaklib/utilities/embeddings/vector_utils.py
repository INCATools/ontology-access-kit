"""Vectorised operations over embedding matrices."""

from typing import Optional

import numpy as np

__all__ = [
    "cosine_similarity_matrix",
    "jaccard_similarity_matrix",
    "similarity_matrix",
]


def _l2_normalize(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return m / norms


def cosine_similarity_matrix(a: np.ndarray, b: Optional[np.ndarray] = None) -> np.ndarray:
    """
    All-by-all cosine similarity between the rows of two matrices.

    >>> a = np.array([[1.0, 0.0], [1.0, 1.0]])
    >>> cosine_similarity_matrix(a).round(3).tolist()
    [[1.0, 0.707], [0.707, 1.0]]

    Zero vectors have a similarity of zero to everything:

    >>> cosine_similarity_matrix(np.array([[0.0, 0.0]]), a).tolist()
    [[0.0, 0.0]]

    :param a: an (m x d) matrix
    :param b: an (n x d) matrix; defaults to ``a``
    :return: an (m x n) matrix of cosine similarities
    """
    a = np.asarray(a, dtype=float)
    b = a if b is None else np.asarray(b, dtype=float)
    return np.clip(_l2_normalize(a) @ _l2_normalize(b).T, -1.0, 1.0)


def jaccard_similarity_matrix(a: np.ndarray, b: Optional[np.ndarray] = None) -> np.ndarray:
    """
    All-by-all Jaccard similarity between the rows of two binary matrices.

    Any non-zero value is treated as set membership.

    >>> a = np.array([[1, 1, 0, 0], [0, 1, 1, 0]])
    >>> jaccard_similarity_matrix(a).round(3).tolist()
    [[1.0, 0.333], [0.333, 1.0]]

    :param a: an (m x d) matrix
    :param b: an (n x d) matrix; defaults to ``a``
    :return: an (m x n) matrix of Jaccard similarities
    """
    a = (np.asarray(a) != 0).astype(float)
    b = a if b is None else (np.asarray(b) != 0).astype(float)
    intersection = a @ b.T
    union = a.sum(axis=1)[:, None] + b.sum(axis=1)[None, :] - intersection
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(union > 0, intersection / union, 0.0)


METRICS = {
    "cosine": cosine_similarity_matrix,
    "jaccard": jaccard_similarity_matrix,
}


def similarity_matrix(
    a: np.ndarray, b: Optional[np.ndarray] = None, metric: str = "cosine"
) -> np.ndarray:
    """
    All-by-all similarity between the rows of two matrices using a named metric.

    :param a: an (m x d) matrix
    :param b: an (n x d) matrix; defaults to ``a``
    :param metric: one of ``cosine`` or ``jaccard``
    :return: an (m x n) matrix
    """
    if metric not in METRICS:
        raise ValueError(f"Unknown metric: {metric}; must be one of {list(METRICS)}")
    return METRICS[metric](a, b)
