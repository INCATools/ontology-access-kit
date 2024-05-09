import base64
import logging
from copy import deepcopy
from itertools import product
from random import shuffle
from typing import Iterator, List, Set, Tuple

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE
from oaklib.utilities.lexical.patternizer import LexicalPattern


def logical_definition_to_set(ldef: LogicalDefinitionAxiom) -> Set[CURIE]:
    return set(
        ldef.genusIds
        + [r.propertyId for r in ldef.restrictions]
        + [r.fillerId for r in ldef.restrictions]
    )


def set_delta(s1: Set[CURIE], s2: Set[CURIE]) -> Tuple[Tuple[CURIE], Tuple[CURIE]]:
    return tuple(s1.difference(s2)), tuple(s2.difference(s1))


def reflexive_logical_definition(curie: CURIE) -> LogicalDefinitionAxiom:
    return LogicalDefinitionAxiom(definedClassId=curie, genusIds=[curie], restrictions=[])


def logical_definition_signature(ldef: LogicalDefinitionAxiom) -> List[CURIE]:
    return (
        [ldef.definedClassId]
        + ldef.genusIds
        + [r.propertyId for r in ldef.restrictions]
        + [r.fillerId for r in ldef.restrictions]
    )


def analyze_logical_definitions(
    adapter: BasicOntologyInterface, ldefs: List[LogicalDefinitionAxiom], reflexive=False
) -> Iterator:
    if reflexive:
        ldefs = deepcopy(ldefs)
        signature = []
        for ldef in ldefs:
            signature.extend(logical_definition_signature(ldef))
        for curie in signature:
            ldefs.append(reflexive_logical_definition(curie))
    lmap = {ldef.definedClassId: logical_definition_to_set(ldef) for ldef in ldefs}
    curies = list(lmap.keys())
    rels = [rel for rel in adapter.relationships(curies) if rel[2] in curies]
    logging.info(f"Found {len(rels)} relationships")
    abduced = []
    amap = {}
    for rel in rels:
        sx = lmap[rel[0]]
        ox = lmap[rel[2]]
        d = set_delta(sx, ox)
        abduced.append((rel[1], d))
        amap[d] = rel
        logging.debug(f"Indexing amap[{d}] = {rel}")
    for i, ix in lmap.items():
        irels = [rel for rel in rels if rel[0] == i]
        for j, jx in lmap.items():
            ijrels = [rel for rel in irels if rel[2] == j]
            if i != j:
                d = set_delta(ix, jx)
                logging.debug(f"Checking if {i}, {j} = {d} in amap")
                if d in amap:
                    if not ijrels:
                        print(i, j, d, amap[d])
                        yield ("abduced", i, j, amap[d])


def generate_descendant_logical_definitions(
    adapter: OboGraphInterface,
    ldef: LogicalDefinitionAxiom,
    pattern: LexicalPattern = None,
    random_sample=False,
) -> Iterator[LogicalDefinitionAxiom]:
    existing = list(adapter.logical_definitions())
    dc_to_ldef = {ldef.definedClassId: ldef for ldef in existing}
    ldef_to_dc = {str(ldef): dc for dc, ldef in dc_to_ldef.items()}
    terms = ldef.genusIds + [r.fillerId for r in ldef.restrictions]
    num_genus_ids = len(ldef.genusIds)
    props = [r.propertyId for r in ldef.restrictions]
    candidates_list = [adapter.descendants([t], [IS_A], reflexive=True) for t in terms]
    if random_sample:
        candidates_list = [shuffle(cs) for cs in candidates_list]
    for tpl in product(*candidates_list):
        if tpl == tuple(terms):
            continue
        restrictions = [
            ExistentialRestrictionExpression(propertyId=pred, fillerId=filler)
            for pred, filler in zip(props, tpl[num_genus_ids:], strict=False)
        ]
        curie = base64.b64encode(str(tpl).encode("ascii")).decode("utf-8")
        new_ldef = LogicalDefinitionAxiom(
            definedClassId=curie,
            genusIds=list(tpl[0:num_genus_ids]),
            restrictions=restrictions,
        )
        if str(new_ldef) in ldef_to_dc:
            logging.debug(f"Skipping {new_ldef} because it already exists")
            continue
        yield new_ldef
