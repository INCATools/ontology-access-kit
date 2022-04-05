from typing import List, Dict

from oaklib.interfaces import RelationGraphInterface
from oaklib.types import CURIE, PRED_CURIE

def filter_redundant(oi: RelationGraphInterface, curies: List[CURIE], predicates: List[PRED_CURIE] = None) -> List[CURIE]:
    return [curie for curie in curies if not is_redundant(oi, curie, curies, predicates)]

def is_redundant(oi: RelationGraphInterface, curie: CURIE, curies: List[CURIE], predicates: List[PRED_CURIE] = None) -> bool:
    for candidate in curies:
        if candidate != curie:
            if curie in list(oi.ancestors(candidate, predicates=predicates)):
                return True
    return False

def roll_up_to_named_subset(oi: RelationGraphInterface, subset: CURIE, curies: List[CURIE],
                            predicates: List[PRED_CURIE] = None) -> Dict[CURIE, List[CURIE]]:
    # see https://metacpan.org/dist/go-perl/view/scripts/map2slim
    terms_in_subset = set(oi.curies_by_subset(subset))
    print(f'SUBSET={list(terms_in_subset)}')
    subset_ancs = {t: [a for a in oi.ancestors(t, predicates) if a != t] for t in terms_in_subset}
    m = {}
    for curie in curies:
        ancs = list(oi.ancestors(curie, predicates=predicates))
        print(f'{curie} ANCS={list(ancs)}')
        ancs_in_subset = terms_in_subset.intersection(ancs)
        print(f'    xx ANCS={list(ancs_in_subset)}')
        nr_ancs_in_subset = filter_redundant(oi, ancs_in_subset, predicates)
        #exclude = set()
        #for a in ancs_in_subset:
        #    exclude.update(subset_ancs[a])
        #    print(f'+{a} ==> EXC {exclude}')
        m[curie] = nr_ancs_in_subset
    return m




