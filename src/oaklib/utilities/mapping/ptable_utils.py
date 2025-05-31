from collections import defaultdict
from typing import Iterator, List

import sssom_schema as sssom

from oaklib.datamodels.vocabulary import (
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    IS_A,
    SKOS_BROAD_MATCH,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
    SKOS_NARROW_MATCH,
    SKOS_RELATED_MATCH,
)

DEFAULT_CONFIDENCE_BY_PREDICATE = {
    IS_A: 1.0,
    EQUIVALENT_CLASS: 1.0,
    HAS_DBXREF: 0.6,
    SKOS_RELATED_MATCH: 0.25,
    SKOS_EXACT_MATCH: 0.9,
    SKOS_CLOSE_MATCH: 0.8,
    SKOS_BROAD_MATCH: 0.9,
    SKOS_NARROW_MATCH: 0.9,
}


def mappings_to_ptable(
    mappings: List[sssom.Mapping],
) -> Iterator[List[float]]:
    """
    Convert a set of mappings to a ptable.

    :param mappings: list of mappings
    :return: An iterator that yields rows of the ptable as lists of floats.
    """
    tups_by_pair = defaultdict(list)
    for m in mappings:
        subj = m.subject_id
        obj = m.object_id
        pred = m.predicate_id
        inv = False
        if subj < obj:
            # reverse
            subj, obj = obj, subj
            inv = True
        conf = m.confidence
        if conf is None:
            if pred in DEFAULT_CONFIDENCE_BY_PREDICATE:
                conf = DEFAULT_CONFIDENCE_BY_PREDICATE[pred]
            else:
                continue
        tups_by_pair[(subj, obj)].append((conf, inv, pred))
    for (subj, obj), tuples in tups_by_pair.items():
        # sort by confidence
        sorted_tuples = sorted(tuples, key=lambda x: -x[0])
        conf, inv, pred = sorted_tuples[0]
        if pred in [SKOS_BROAD_MATCH, IS_A]:
            # subj SubClassOf obj
            pos = 0
        elif pred == SKOS_NARROW_MATCH:
            # subj SuperClassOf obj
            pos = 1
        # elif pred == SKOS_CLOSE_MATCH:
        #    # assumes that it was explicitly assigned as non-exact
        #    pos = 3
        else:
            pos = 2
        if inv:
            if pos == 1:
                pos = 0
            elif pos == 0:
                pos = 1
        residual = (1 - conf) / 3.0
        row = [subj, obj, residual, residual, residual, residual]
        row[pos + 2] = conf
        # Ensure the row sums to 1.0; but allow for floating point precision issues
        assert abs(sum(row[2:]) - 1.0) < 1e-6, f"Row sums to {sum(row[2:])}, expected 1.0"
        yield row
