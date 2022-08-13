from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

from oaklib.types import CURIE


def pairs_as_dict(pairs: Iterable[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    """
    Translates a collection of key-value pairs into a key-values dictionary

    :param pairs:
    :return:
    """
    d = defaultdict(list)
    for p in pairs:
        d[p[0]].append(d[1])
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


OBO_CONTEXT_URL = "https://raw.githubusercontent.com/OBOFoundry/OBOFoundry.github.io/master/registry/obo_context.jsonld"


@lru_cache(1)
def get_obo_prefix_map():
    return requests.get(OBO_CONTEXT_URL).json()["@context"]
