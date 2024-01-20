from collections import defaultdict
from itertools import chain, combinations
from typing import Any, Dict, Iterable, List, Optional, Tuple

from oaklib.types import CURIE


def powerset(iterable):
    """
    Calculate the powerset of an iterable.

    >>> list(powerset([1,2,3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

    :param iterable:
    :return:
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def pairs_as_dict(pairs: Iterable[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    """
    Translates a collection of key-value pairs into a key-values dictionary

    :param pairs:
    :return:
    """
    d = defaultdict(list)
    for p in pairs:
        d[p[0]].append(p[1])
    return d


def triples_as_dict(tuples: Iterable[Tuple[Any, Any, Any]]) -> Dict[Any, List[Tuple[Any, Any]]]:
    """
    Translates a collection of s-p-o pairs tuples a key-value dictionary keyed by subject

    :param tuples:
    :return:
    """
    d = defaultdict(list)
    for t in tuples:
        d[t[0]].append((t[1], t[2]))
    return d


def get_curie_prefix(curie: CURIE) -> Optional[str]:
    """
    Extract the prefix from a CURIE.

    A CURIE is a string typically of the form PREFIX : LOCALNAME

    We allow simple strings as CURIEs, if the input does not conform to the prefix-localname
    syntax then None is returned

    :param curie:
    :return: prefix
    """
    if ":" in curie:
        return curie.split(":")[0]
    else:
        return None
