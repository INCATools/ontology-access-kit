import re
import uuid

import kgcl_schema.datamodel.kgcl as kgcl

from oaklib.datamodels.vocabulary import IS_A
from oaklib.types import CURIE

re_quoted = re.compile("^'(.*)'$")


def generate_change_id() -> CURIE:
    """
    Generates an identifier to be used on a change object
    :return:
    """
    return f"uuid:{uuid.uuid4()}"


def tidy_change_object(change: kgcl.Change):
    """
    Performs any necessary fixing on a Change object.

    Sometimes the main kgcl parser will leave quotes in place, URIs quoted, etc.
    As these are fixed in the main KCGL repo we can remove these here.

    :param change:
    :return:
    """

    def _fix(prop: str):
        v = getattr(change, prop)
        if v:
            m = re_quoted.match(v)
            if m:
                setattr(change, prop, m.group(1))

    if isinstance(change, kgcl.NodeCreation):
        _fix("name")
    if isinstance(change, kgcl.NodeRename):
        _fix("new_value")
    if isinstance(change, kgcl.EdgeCreation):
        if change.predicate == "is_a":
            change.predicate = IS_A
