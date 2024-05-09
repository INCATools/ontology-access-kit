import logging
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, Tuple

from oaklib.datamodels.obograph import (
    DisjointClassExpressionsAxiom,
    ExistentialRestrictionExpression,
)
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE

CACHE = Dict[PRED_CURIE, Dict[CURIE, List[CURIE]]]


@dataclass
class DisjointnessInducerConfig:
    min_descendants: int = field(default=3)
    exclude_existing: bool = field(default=True)
    exclude_if_subsumed: bool = field(default=True)
    genus_terms_are_candidates: bool = field(default=True)


def _descendants(
    adapter: OboGraphInterface,
    c: CURIE,
    predicates: Optional[List[PRED_CURIE]] = None,
    cache: Optional[CACHE] = None,
) -> List[CURIE]:
    """
    Return the descendants of a class.

    :param adapter:
    :param c:
    :param cache:
    :return:
    """
    if cache is None:
        cache = {}
    preds = tuple(predicates or [IS_A])
    if preds not in cache:
        cache[preds] = {}
    pcache = cache[preds]
    if c not in pcache:
        pcache[c] = list(adapter.descendants(c, predicates))
    return pcache[c]


def underlap(
    adapter: OboGraphInterface,
    class1: CURIE,
    class2: CURIE,
    predicates: Optional[List[PRED_CURIE]] = None,
    cache: Optional[CACHE] = None,
) -> Tuple[int, int, int]:
    """
    Compute the underlap between two classes.

    :param adapter:
    :param class1:
    :param class2:
    :param predicates:
    :param cache:
    :return: tuple of underlap, |C1|, |C2|
    """
    if predicates is None:
        predicates = [IS_A]
    desc1 = _descendants(adapter, class1, predicates=predicates, cache=cache)
    desc2 = _descendants(adapter, class2, predicates=predicates, cache=cache)
    return len(set(desc1).intersection(set(desc2))), len(desc1), len(desc2)


def generate_underlaps(
    adapter: OboGraphInterface,
    roots: Optional[List[CURIE]] = None,
    predicate_sets: Optional[List[List[PRED_CURIE]]] = None,
    config: Optional[DisjointnessInducerConfig] = None,
) -> Iterator[Tuple[List[PRED_CURIE], CURIE, CURIE, int, int]]:
    """
    Generate disjointness axioms for a set of roots.

    :param adapter:
    :param roots:
    :return:
    """
    cache = {}
    if config is None:
        config = DisjointnessInducerConfig()
    if predicate_sets is None:
        predicate_sets = [[IS_A]]
    if not roots:
        roots = []
        for predicates in predicate_sets:
            roots.extend(adapter.roots(predicates))
    stack = list(set(roots))
    logging.info(f"ROOTS: {stack}")
    visited = set()
    while len(stack) > 0:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for predicates in predicate_sets:
            children = [r[0] for r in adapter.relationships(objects=[node], predicates=predicates)]
            children = {
                c
                for c in children
                if len(_descendants(adapter, c, predicates=predicates, cache=cache))
                > config.min_descendants
            }
            logging.info(f"N: {node} CHILDREN {predicates}: {children}")
            for i1, c1 in enumerate(children):
                for i2, c2 in enumerate(children):
                    if i2 >= i1:
                        continue
                    u, s1, s2 = underlap(adapter, c1, c2, predicates, cache=cache)
                    if u > 0:
                        continue
                    if s1 < config.min_descendants or s2 < config.min_descendants:
                        continue
                    logging.debug(f"UNDERLAP: {c1} {c2} {u} {s1} {s2}")
                    yield predicates, c1, c2, s1, s2
                stack.append(c1)
    if config.genus_terms_are_candidates:
        ldas = adapter.logical_definitions()
        genus_ids = set()
        for lda in ldas:
            genus_ids.update(lda.genusIds)
        for i1, c1 in enumerate(genus_ids):
            for i2, c2 in enumerate(genus_ids):
                if i2 >= i1:
                    continue
                u, s1, s2 = underlap(adapter, c1, c2, [IS_A])
                if u > 0:
                    continue
                if s1 < config.min_descendants or s2 < config.min_descendants:
                    continue
                yield [IS_A], c1, c2, s1, s2


def equivalent(dxa1: DisjointClassExpressionsAxiom, dxa2: DisjointClassExpressionsAxiom) -> bool:
    """
    Determine if two disjointness axioms are equivalent.

    :param dxa1:
    :param dxa2:
    :return:
    """
    exprs1 = {str(x) for x in dxa1.classExpressions}
    exprs2 = {str(x) for x in dxa2.classExpressions}
    return set(dxa1.classIds) == set(dxa2.classIds) and exprs1 == exprs2


def subsumed_by(
    adapter: OboGraphInterface,
    dxa: DisjointClassExpressionsAxiom,
    existing: List[DisjointClassExpressionsAxiom],
) -> Iterator[DisjointClassExpressionsAxiom]:
    for other_dxa in existing:
        this_class_ids = set(other_dxa.classIds)
        this_class_expressions = set(
            [(x.propertyId, x.fillerId) for x in other_dxa.classExpressions]
        )
        if equivalent(dxa, other_dxa):
            yield other_dxa
            continue
        for c in dxa.classIds:
            ancs = list(adapter.ancestors(c, [IS_A]))
            this_class_ids = this_class_ids.difference(ancs)
        for cx in dxa.classExpressions:
            ancs = list(adapter.ancestors(cx.fillerId, [IS_A, cx.propertyId]))
            ancxs = [(cx.propertyId, a) for a in ancs]
            this_class_expressions = this_class_expressions.difference(ancxs)
        if len(this_class_ids) == 0 and len(this_class_expressions) == 0:
            yield other_dxa


def generate_disjoint_class_expressions_axioms(
    adapter: OboGraphInterface,
    roots: Optional[List[CURIE]] = None,
    predicate_sets: Optional[List[List[PRED_CURIE]]] = None,
    config: Optional[DisjointnessInducerConfig] = None,
) -> Iterator[DisjointClassExpressionsAxiom]:
    """
    Generate disjointness axioms for a set of roots.

    :param adapter:
    :param roots:
    :return:
    """
    if config is None:
        config = DisjointnessInducerConfig()
    if config.exclude_existing:
        existing = list(adapter.disjoint_class_expressions_axioms())
    else:
        existing = []
    for predicates, c1, c2, _s1, _s2 in generate_underlaps(adapter, roots, predicate_sets, config):
        non_is_a = [p for p in predicates if p != IS_A]
        if not non_is_a:
            yield DisjointClassExpressionsAxiom(
                classIds=[c1, c2],
            )
        else:
            if len(non_is_a) > 1:
                raise NotImplementedError(f"Cannot handle multiple non-is_a predicates: {non_is_a}")
            p = non_is_a[0]
            dxa = DisjointClassExpressionsAxiom(
                classExpressions=[
                    ExistentialRestrictionExpression(
                        propertyId=p,
                        fillerId=c1,
                    ),
                    ExistentialRestrictionExpression(
                        propertyId=p,
                        fillerId=c2,
                    ),
                ]
            )
            logging.debug(f"Checking candidate: {dxa} against existing: {len(existing)}")
            for e in existing:
                if equivalent(e, dxa):
                    break
                subsumers = list(subsumed_by(adapter, dxa, existing))
                if len(subsumers) > 0:
                    break
            else:
                yield dxa
                existing.append(dxa)
