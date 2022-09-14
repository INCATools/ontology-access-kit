"""
A simple OBO Format parser.

This implements a "delayed parsing" strategy for OBO. The OBO file is treated as a loosely
specified toml-like structure, consisting of stanzas of tag-val pairs.

The precise parsing of each tag-val pair is delayed until precise semantics are required
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Mapping, Optional, TextIO, Tuple, Union

from oaklib.datamodels.vocabulary import SCOPE_TO_SYNONYM_PRED_MAP
from oaklib.types import CURIE, PRED_CURIE

re_tag_value = re.compile(r"^(\S+):\s*(.*)$")
re_stanza_type = re.compile(r"^\[(\w+)\]$")
re_empty = re.compile(r"^\S*$")
re_synonym1 = re.compile(r'^"(.*)"\s+(\w+)\s+\[(.*)\](?:\s+\{(.*)\})?$')
re_synonym2 = re.compile(r'^"(.*)"\s+(\w+)\s+(\w+)\s+\[(.*)\](?:\s+\{(.*)\})?$')
re_quoted_simple = re.compile(r'^"(.*)"\s+\[')


def _synonym_scope_pred(s: str) -> str:
    scope = s.upper()
    if scope in SCOPE_TO_SYNONYM_PRED_MAP:
        return SCOPE_TO_SYNONYM_PRED_MAP[scope]
    else:
        raise ValueError(f"Unknown scope: {scope}")


STANZA_TERM = "Term"
STANZA_TYPEDEF = "Typedef"

TAG = str
TAG_SUBSETDEF = "subsetdef"
TAG_SUBSET = "subset"
TAG_OBSOLETE = "is_obsolete"
TAG_NAME = "name"
TAG_DEF = "def"
TAG_XREF = "xref"
TAG_COMMENT = "comment"
TAG_SYNONYM = "synonym"
TAG_DEFINITION = "def"
TAG_IS_A = "is_a"
TAG_EQUIVALENT_TO = "equivalent_to"
TAG_RELATIONSHIP = "relationship"
TAG_INTERSECTION_OF = "intersection_of"
SYNONYM_TUPLE = Tuple[PRED_CURIE, str, Optional[str], List[CURIE]]


def _parse_list(as_str: str) -> List[str]:
    if as_str == "":
        return []
    return as_str.split(", ")


@dataclass
class TagValue:
    """Simple unparsed tag-value pair"""

    tag: TAG
    """OBO Format Tag, e.g. id, name, synonym"""

    value: str
    """Raw unparsed value.
    This can later be 'cast' to precise structures using methods like as_synonym"""

    def as_synonym(self) -> Optional[SYNONYM_TUPLE]:
        """
        Cast a tag-value pair as a synonym

        Returns None if this is not a synonym TV

        :return: synonym tuple structure
        """
        if self.tag != TAG_SYNONYM:
            return
        m = re_synonym2.match(self.value)
        if m:
            syn = m.groups()
        else:
            m = re_synonym1.match(self.value)
            if m:
                syn = m.group(1), m.group(2), None, m.group(3)
            else:
                raise ValueError(f"Bad synonym: {self.value}")
        return syn[0], syn[1], syn[2], _parse_list(syn[3])

    def replace_quoted_part(self, v: str):
        """
        Replace the quoted part of a value leaving the rest unmodified

        :param v: new value
        :return:
        """
        v = v.replace('"', '\\"')
        self.value = re.sub(r'^"(.*)"\s+', f'"{v}" ', self.value)


@dataclass
class Structure:
    """
    Abstract grouping for Stanzas and Headers
    """

    tag_values: List[TagValue] = field(default_factory=lambda: [])
    """List of all tag-value pairs for this stanza or header"""

    def _simple_value(self, v) -> str:
        return v.split(" ")[0]

    def _values(self, tag: TAG) -> List[str]:
        return [tv.value for tv in self.tag_values if tv.tag == tag]

    def simple_values(self, tag: TAG) -> List[CURIE]:
        """
        Get values for a tag where the tag follows the structure of an OBO
        subset tag or similar

        :param tag:
        :return:
        """
        return [self._simple_value(v) for v in self._values(tag)]

    def pair_values(self, tag: TAG) -> List[Tuple[str, str]]:
        """
        Get values for a tag as a pair-tuple, consistent with the relationship tag

        :param tag:
        :return:
        """
        pairs = []
        for v in self._values(tag):
            toks = v.split(" ")
            pairs.append((toks[0], toks[1]))
        return pairs

    def intersection_of_tuples(self) -> List[Tuple[CURIE, Optional[CURIE]]]:
        pairs = []
        for v in self._values(TAG_INTERSECTION_OF):
            toks = [x for x in v.split(" ") if x]
            if toks[1].startswith("!"):
                pairs.append((toks[0], None))
            else:
                pairs.append((toks[0], toks[1]))
        return pairs

    def singular_value(self, tag: TAG, strict=False) -> Optional[str]:
        """
        Get value for a tag where the tag follows the structure of an OBO
        name, comment tag or similar; the tag must have cardinality zero or one,
        and the value is raw

        :param tag:
        :param strict:
        :return:
        """
        vals = self._values(tag)
        if vals:
            if strict and len(vals) > 1:
                raise ValueError(f"Multiple vals {vals} for {tag} in {self.id}")
            return vals[0]
        else:
            if strict:
                raise ValueError(f"No value for {tag} in {self.id}")

    def quoted_value(self, tag: TAG, strict=False) -> Optional[str]:
        """
        Get value for a tag where the tag follows the structure of an OBO
        def, synonym tag or similar

        :param tag:
        :param strict:
        :return:
        """
        vals = self._values(tag)
        if vals:
            if strict and len(vals) > 1:
                raise ValueError(f"Multiple vals {vals} for {tag} in {self.id}")
            m = re_quoted_simple.match(vals[0])
            if m:
                return m.group(1)
            else:
                raise ValueError(f"Could not parse quoted string from {vals}")

    def synonyms(self) -> List[SYNONYM_TUPLE]:
        """
        All synonyms for a stanza

        :return: list of synonyms
        """
        return [tv.as_synonym() for tv in self.tag_values if tv.tag == TAG_SYNONYM]

    def set_singular_tag(self, tag: TAG, val: str) -> None:
        """
        Sets the value of a singular tag such as name

        :param tag:
        :param val:
        :return:
        """
        is_set = False
        for tv in self.tag_values:
            if tv.tag == tag:
                tv.value = val
                is_set = True
        if not is_set:
            self.add_tag_value(tag, val)

    def remove_simple_tag_value(self, tag: TAG, val: str) -> None:
        """
        removes a simple tag-value such as is_a

        :param tag:
        :param val:
        :return:
        """
        n = 0
        tvs = []
        for tv in self.tag_values:
            if tv.tag == tag:
                if self._simple_value(tv.value) == val:
                    n += 1
                    continue
            tvs.append(tv)
        if not n:
            raise ValueError(f"No values to set for {tag} = {val}")
        self.tag_values = tvs

    def remove_pairwise_tag_value(self, tag: TAG, val1: str, val2: str) -> None:
        """
        removes a simple tag-value such as is_a

        :param tag:
        :param val:
        :return:
        """
        n = 0
        tvs = []
        for tv in self.tag_values:
            if tv.tag == tag:
                vals = tv.value.split(" ")
                if vals[0:2] == [val1, val2]:
                    n += 1
                    continue
            tvs.append(tv)
        if not n:
            raise ValueError(f"No values to set for {tag} = {val1} {val2}")
        self.tag_values = tvs

    def add_tag_value(self, tag: TAG, val: str) -> None:
        """
        Adds a tag-value pair

        :param tag:
        :param val:
        :return:
        """
        self.tag_values.append(TagValue(tag, val))

    def get_boolean_value(self, tag: TAG, strict=False) -> bool:
        """
        Gets the value of a tag such as is_obsolete

        :param tag:
        :param strict:
        :return:
        """
        vals = self._values(tag)
        if strict and len(vals) > 1:
            raise ValueError(f"Multiple vals for {tag} = {vals} in {self.id}")
        return any(v for v in vals if v == "true")


@dataclass
class Header(Structure):
    """
    Header portion of an OBO Document
    """

    def ontology(self) -> str:
        raise NotImplementedError


@dataclass
class Stanza(Structure):
    """A Term or Typedef stanza"""

    id: Optional[str] = None
    """Unique identifier"""

    type: Optional[str] = None
    """Stanza type, either Term or Typedef"""


@dataclass
class OboDocument:
    """An OBO Document is a header plus zero or more stanzas"""

    header: Header = field(default_factory=lambda: Header())
    stanzas: Mapping[CURIE, Stanza] = field(default_factory=lambda: {})

    def add_stanza(self, stanza: Stanza) -> None:
        self.stanzas[stanza.id] = stanza

    def dump(self, file: TextIO) -> None:
        """Export to a file

        :param file:
        """
        self._dump_tag_values(self.header.tag_values, file)
        for s in self.stanzas.values():
            file.write(f"[{s.type}]\n")
            self._dump_tag_values(s.tag_values, file)

    def _dump_tag_values(self, tag_values: List[TagValue], file: TextIO):
        for tv in tag_values:
            file.write(f"{tv.tag}: {tv.value}\n")
        file.write("\n")


def parse_obo_document(path: Union[str, Path]) -> OboDocument:
    """
    Parse a path to an OBO Document

    :param path:
    :return:
    """
    tag_values: List[TagValue] = []
    obo_document: Optional[OboDocument] = None
    stanzas = []
    with open(path) as stream:
        for line in stream.readlines():
            line = line.rstrip()
            if line.startswith("!"):
                continue
            elif line.startswith("["):
                m = re_stanza_type.match(line)
                if not m:
                    raise ValueError(f"Cannot parse {line}")
                typ = m.group(1)
                if typ != STANZA_TERM and typ != STANZA_TYPEDEF:
                    raise ValueError(f"Bad type: {typ}")
                if obo_document is None:
                    obo_document = OboDocument(header=Header(tag_values=tag_values))
                else:
                    stanzas[-1].tag_values = tag_values
                tag_values = []
                stanza = Stanza(id=None, type=typ, tag_values=[])
                stanzas.append(stanza)
            elif re_tag_value.match(line):
                (tag, val) = re_tag_value.match(line).groups()
                tag_values.append(TagValue(tag, val))
                if tag == "id":
                    stanzas[-1].id = val
            elif re_empty.match(line):
                continue
            else:
                raise ValueError(f"Cannot parse: {line}")
        stanzas[-1].tag_values = tag_values
    obo_document.stanzas = {stanza.id: stanza for stanza in stanzas}
    return obo_document
