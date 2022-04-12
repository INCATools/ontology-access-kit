from collections import defaultdict
from typing import Tuple, Any, Dict, List, Iterable


def pairs_as_dict(pairs: Iterable[Tuple[Any, Any]]) -> Dict[Any, List[Any]]:
    d = defaultdict(list)
    for p in pairs:
        d[p[0]].append(d[1])
    return d