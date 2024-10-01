import base64
import json
import re
import sys
import uuid
from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Iterator, List, Optional, TextIO, Union

import kgcl_schema.datamodel.kgcl as kgcl
import kgcl_schema.grammar.parser as kgcl_parser
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.dumpers import json_dumper, yaml_dumper

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


CURIE_SLOTS = {
    "subject": "subject_type",
    "object": "object_type",
    "predicate": "predicate_type",
    "about_node": "about_node_representation",
}


def substitute_curies_for_labels(
    changes: Union[List[kgcl.Change], kgcl.Change], label_function: Callable
):
    if isinstance(changes, list):
        for change in changes:
            substitute_curies_for_labels(change, label_function)
        return
    change = changes
    for k, v in vars(change).items():
        if k in CURIE_SLOTS:
            new_v = label_function(v)
            if new_v:
                new_v = f"'{new_v}'"
                setattr(change, k, new_v)
                setattr(change, CURIE_SLOTS[k], "label")


def substitute_labels_for_curies(
    changes: Union[List[kgcl.Change], kgcl.Change], curie_function: Callable
):
    if isinstance(changes, list):
        for change in changes:
            substitute_labels_for_curies(change, curie_function)
        return
    change = changes
    for k, v in vars(change).items():
        if k in CURIE_SLOTS:
            k_type = CURIE_SLOTS[k]
            try:
                k_type_value = getattr(change, k_type)
            except AttributeError:
                continue
            if k_type_value == "label" or k_type_value == "literal":
                new_v = curie_function(v)
                if new_v:
                    setattr(change, k, new_v)
                    setattr(change, CURIE_SLOTS[k], "curie")


def write_kgcl(
    changes: List[kgcl.Change], file: Optional[Union[str, Path, TextIO]], changes_format="json"
):
    """
    Writes a list of changes to a file

    :param changes:
    :param file:
    :param changes_format:
    :return:
    """
    if file is None:
        file = sys.stdout
    elif not isinstance(file, TextIOWrapper):
        file = open(str(file), "w")
    if changes_format == "json":
        out = json_dumper.dumps(changes)
    elif changes_format == "yaml":
        out = yaml_dumper.dumps(changes)
    else:
        out = "\n".join([render(c) for c in changes])
    file.write(out)


def tidy_change_object(change: kgcl.Change):
    """
    Performs any necessary fixing on a Change object.

    Sometimes the main kgcl parser will leave quotes in place, URIs quoted, etc.
    As these are fixed in the main KCGL repo we can remove these here.

    See `<https://github.com/INCATools/kgcl/issues/66>`_ for more information.

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
