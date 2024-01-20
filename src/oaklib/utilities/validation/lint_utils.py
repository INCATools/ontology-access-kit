import re
from typing import Iterable, Tuple, Type

from kgcl_schema.datamodel.kgcl import (
    Change,
    NodeRename,
    NodeTextDefinitionChange,
    SynonymReplacement,
)

from oaklib import BasicOntologyInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.types import CURIE

ISSUE = Tuple[bool, Change]


def repair(entity: CURIE, v: str, change_class: Type[Change]) -> Iterable[ISSUE]:
    if v is None:
        return
    orig_v = v
    v = re.sub(r" +", " ", v)
    v = re.sub(r"^\s+", "", v)
    v = re.sub(r"\s+$", "", v)
    if v != orig_v:
        chg = change_class(id="x", about_node=entity, old_value=orig_v, new_value=v)
        yield True, chg


def lint_ontology(
    oi: BasicOntologyInterface, dry_run=False, entities: Iterable[CURIE] = None
) -> Iterable[ISSUE]:
    """
    Perform a style check on an ontology

    By default repairs will be performed if necessary

    :param oi:
    :return:
    """
    for actionable, change in _lint_ontology_dry_run(oi, entities):
        if actionable and not dry_run:
            if isinstance(oi, PatcherInterface):
                oi.apply_patch(change)
        yield actionable, change


def _lint_ontology_dry_run(
    oi: BasicOntologyInterface, entities: Iterable[CURIE] = None
) -> Iterable[ISSUE]:
    if entities is None:
        entities = oi.entities()
    for e in entities:
        label = oi.label(e)
        for r in repair(e, label, NodeRename):
            yield r
        defn = oi.definition(e)
        for r in repair(e, defn, NodeTextDefinitionChange):
            yield r
        for _pred, syn in oi.alias_relationships(e):
            for r in repair(e, syn, SynonymReplacement):
                yield r
