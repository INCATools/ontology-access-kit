from math import exp, lgamma
from typing import Tuple


def log_binomial_coefficient(n: int, k: int) -> float:
    """
    Binomial coefficient (n choose k).

    n: number of successes in sample
    :param n:
    :param k:
    :return:
    """
    return lgamma(n + 1) - (lgamma(k + 1) + lgamma(n - k + 1))


def hypergeom_prob(n: int, k: int, N: int, K: int) -> float:
    """
    n: number of successes in sample
    k: number of successes in population
    N: size of sample
    K: size of population
    """
    return exp(
        log_binomial_coefficient(k, n)
        + log_binomial_coefficient(K - k, N - n)
        - log_binomial_coefficient(K, N)
    )


def hypergeometric_p_value(n: int, k: int, N: int, K: int) -> Tuple[float, float]:
    """
    Calculates the p-value for a hypergeometric test.

    Note on translation to scipy variable names:

    The scipy call: hypergeom(M, n, N)

    - K: scipy:M is the total number of objects
    - k: scipy:n is total number of Type I objects
    - n: scipy:N is the size of the sample

    :param n: number of successes in sample
    :param k: number of successes in population
    :param N: size of sample
    :param K: size of population
    :return: (p-value over-representation, p-value under-representation)
    """
    # failures in pop: K-k
    # minimum possible
    return (
        sum([hypergeom_prob(i, k, N, K) for i in range(n, min(k, N) + 1)]),
        sum([hypergeom_prob(i, k, N, K) for i in range(max(0, N - (K - k)), n + 1)]),
    )
