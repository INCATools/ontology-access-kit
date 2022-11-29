import base64
import json
import re
import uuid
from io import TextIOWrapper
from pathlib import Path
from typing import Iterator, List, TextIO, Union

import kgcl_schema.datamodel.kgcl as kgcl
import kgcl_schema.grammar.parser as kgcl_parser

from oaklib.datamodels.vocabulary import IS_A
from oaklib.types import CURIE

re_quoted = re.compile("^'(.*)'$")


def generate_change_id() -> CURIE:
    """
    Generates an identifier to be used on a change object
    :return:
    """
    return f"uuid:{uuid.uuid4()}"


def assign_id(change: kgcl.Change):
    """
    Assigns an ID to a change object
    :param change:
    :return:
    """
    message_bytes = str(change).encode("ascii")
    return base64.b64encode(message_bytes)


def parse_kgcl_files(
    files: List[Union[str, Path, TextIO]], changes_format="json"
) -> Iterator[kgcl.Change]:
    """
    Parses a list of KGCL files yielding Change objects

    :param files:
    :param changes_format: default is "json"
    :return: change iterator
    """
    changes = []
    for file in files:
        if not isinstance(file, TextIOWrapper):
            file = open(str(file), "r")
        if changes_format == "json":
            import kgcl_schema.utils as kgcl_utilities

            objs = json.load(file)
            for obj in objs:
                obj["type"] = obj["@type"]
                del obj["@type"]
            changes = kgcl_utilities.from_dict({"change_set": objs}).change_set
        else:
            for line in file.readlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                change = kgcl_parser.parse_statement(line)
                changes.append(change)
    for change in changes:
        # tidy_change_object(change)
        yield change


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
