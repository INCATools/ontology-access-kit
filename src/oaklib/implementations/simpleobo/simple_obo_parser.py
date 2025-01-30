"""
A simple OBO Format parser.

This implements a "delayed parsing" strategy for OBO. The OBO file is treated as a loosely
specified toml-like structure, consisting of stanzas of tag-val pairs.

The precise parsing of each tag-val pair is delayed until precise semantics are required
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Mapping, Optional, TextIO, Tuple, Union

from oaklib.datamodels.vocabulary import SCOPE_TO_SYNONYM_PRED_MAP
from oaklib.types import CURIE, PRED_CURIE

re_tag_value = re.compile(r"^(\S+):\s*(.*)$")
re_stanza_type = re.compile(r"^\[(\w+)\]$")
re_empty = re.compile(r"^\S*$")
re_def = re.compile(r"^\"(.*)\"\s+\[(.*)\](?:\s+\{(.*)\})?$")
re_synonym1 = re.compile(r"^\"(.*)\"\s+(\w+)\s+\[(.*)\](?:\s+\{(.*)\})?$")
re_synonym2 = re.compile(r"^\"(.*)\"\s+(\w+)\s+(\S)+\s\[(.*)\](?:\s+\{(.*)\})?$")
re_quoted_simple = re.compile(r'^"(.*)"\s+\[')
re_property_value1 = re.compile(r"^(\S+)\s+(.*)\s+(\S+)(?:\s+\{(.*)\})?$")
re_property_value2 = re.compile(r"^(\S+)\s+(\S+)(?:\s+\{(.*)\})?$")


def _synonym_scope_pred(s: str) -> str:
    scope = s.upper()
    if scope in SCOPE_TO_SYNONYM_PRED_MAP:
        return SCOPE_TO_SYNONYM_PRED_MAP[scope]
    else:
        raise ValueError(f"Unknown scope: {scope}")


STANZA_TERM = "Term"
STANZA_TYPEDEF = "Typedef"

TAG = str
TAG_ID = "id"
TAG_ONTOLOGY = "ontology"
TAG_ID_SPACE = "idspace"
TAG_DATA_VERSION = "data-version"
TAG_SUBSETDEF = "subsetdef"
TAG_SYNONYMTYPEDEF = "synonymtypedef"
TAG_SUBSET = "subset"
TAG_IS_OBSOLETE = "is_obsolete"
TAG_REPLACED_BY = "replaced_by"
TAG_CONSIDER = "consider"
TAG_ALT_ID = "alt_id"
TAG_PROPERTY_VALUE = "property_value"
TAG_NAME = "name"
TAG_DEF = "def"
TAG_NAMESPACE = "namespace"
TAG_XREF = "xref"
TAG_COMMENT = "comment"
TAG_SYNONYM = "synonym"
TAG_DEFINITION = "def"
TAG_IS_A = "is_a"
TAG_INVERSE_OF = "inverse_of"
TAG_EQUIVALENT_TO = "equivalent_to"
TAG_RELATIONSHIP = "relationship"
TAG_INTERSECTION_OF = "intersection_of"
TAG_UNION_OF = "union_of"
TAG_DISJOINT_FROM = "disjoint_from"
TAG_CREATED_BY = "created_by"
TAG_CREATION_DATE = "creation_date"
SYNONYM_TUPLE = Tuple[PRED_CURIE, str, Optional[str], List[CURIE]]
PROPERTY_VALUE_TUPLE = Tuple[PRED_CURIE, str, Optional[CURIE], Optional[List[CURIE]]]

TAG_IS_TRANSITIVE = "is_transitive"
TAG_IS_SYMMETRIC = "is_symmetric"
TAG_IS_ANTI_SYMMETRIC = "is_anti_symmetric"
TAG_IS_REFLEXIVE = "is_reflexive"
TAG_IS_ASYMMETRIC = "is_asymmetric"
TAG_IS_FUNCTIONAL = "is_functional"
TAG_IS_INVERSE_FUNCTIONAL = "is_inverse_functional"
TAG_HOLDS_OVER_CHAIN = "holds_over_chain"
TAG_DOMAIN = "domain"
TAG_RANGE = "range"

TERM_TAGS = [
    TAG_ID,
    # TAG_IS_ANONYMOUS,
    TAG_NAME,
    TAG_NAMESPACE,
    TAG_ALT_ID,
    TAG_DEF,
    TAG_COMMENT,
    TAG_SUBSET,
    TAG_SYNONYM,
    TAG_XREF,
    # TAG_BUILTIN,
    TAG_IS_A,
    TAG_INTERSECTION_OF,
    TAG_UNION_OF,
    TAG_EQUIVALENT_TO,
    TAG_DISJOINT_FROM,
    TAG_RELATIONSHIP,
    TAG_PROPERTY_VALUE,
    TAG_IS_OBSOLETE,
    TAG_REPLACED_BY,
    TAG_CONSIDER,
    TAG_CREATED_BY,
    TAG_CREATION_DATE,
]

OBO_TERM = "Term"
OBO_TYPEDEF = "Typedef"


def _parse_list(as_str: str) -> List[str]:
    if as_str == "":
        return []
    return as_str.split(", ")


@dataclass
class ValueComponent:
    pass

    def order(self) -> Tuple:
        pass


@dataclass
class QuotedText(ValueComponent):
    value: str

    def order(self) -> Tuple[str, str]:
        return self.value.lower(), self.value


@dataclass
class SimpleValue(ValueComponent):
    value: str

    def order(self) -> Tuple[str, str]:
        return (self.value,)
        # return self.value.lower(), self.value


@dataclass
class XrefList(ValueComponent):
    values: List[str]

    def order(self) -> Tuple:
        return tuple(self.values)


@dataclass
class Comment(ValueComponent):
    value: str

    def order(self) -> Tuple:
        return (0,)


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

    def as_definition(self) -> Optional[Tuple[str, List[str]]]:
        """
        Cast a tag-value pair as a definition

        Returns None if this is not a definition TV

        :return: definition tuple structure
        """
        if self.tag != TAG_DEF:
            return
        m = re_def.match(self.value)
        if m:
            xrefs = _parse_list(m.group(2)) if m.group(2) else []
            return m.group(1), xrefs
        else:
            raise ValueError(f"Bad definition: {self.value}")

    def as_property_value(self) -> Optional[PROPERTY_VALUE_TUPLE]:
        """
        Cast a tag-value pair as a property value

        Returns None if this is not a property value TV

        :return: property value tuple structure
        """
        if self.tag != TAG_PROPERTY_VALUE:
            return
        m = re_property_value1.match(self.value)
        if m:
            # includes datatype (literal annotation)
            pv = m.groups()
        else:
            # no datatype
            m = re_property_value2.match(self.value)
            if m:
                pv = m.group(1), m.group(2), None, None
            else:
                raise ValueError(f"Bad property value: {self.value}")
        return pv[0], pv[1], pv[2], None

    def replace_quoted_part(self, v: str):
        """
        Replace the quoted part of a value leaving the rest unmodified

        :param v: new value
        :return:
        """
        v = v.replace('"', '\\"')
        self.value = re.sub(r'^"(.*)"\s+', f'"{v}" ', self.value)

    def replace_token(self, curie_map: Mapping[CURIE, CURIE]):
        toks = self.value.split(" ")
        toks = [curie_map.get(x, x) for x in toks]
        self.value = " ".join(toks)

    def values_as_tuple(self) -> Tuple:
        """
        Return a tuple of values for sorting

        :return:
        """
        toks = [x for x in self.value.split(" ") if x]
        tpl = []
        for t in toks:
            if t.startswith("!"):
                break
            tpl.append(t)
        return tuple(tpl)

    def tokenize(self) -> List[ValueComponent]:
        """
        Tokenize the value

        :return:
        """
        if self.tag in [TAG_NAME, TAG_NAMESPACE, TAG_COMMENT]:
            return [SimpleValue(self.value)]
        toks = [x for x in self.value.split(" ") if x]
        cmt = ""
        components = []
        while toks:
            t = toks.pop(0)
            if t.startswith("!"):
                cmt = " ".join(toks)
                break
            if t.startswith('"'):
                toks.insert(0, t)
                s = ""
                while True:
                    if not toks:
                        raise ValueError(f"Badly quoted value: {self.value}")
                    if s:
                        s += " "
                    s += toks.pop(0)
                    closed = False
                    if '"' in s:
                        for i, char in enumerate(s):
                            # Check if the current character is a quote and not escaped
                            if char == '"' and i > 0 and s[i - 1] != "\\":
                                s = s[0:i]
                                rest = s[i + 1 :]
                                if len(rest) > 0:
                                    toks.insert(0, rest)
                                closed = True
                                break
                    if closed:
                        break
                components.append(QuotedText(s))
            elif t.startswith("["):
                toks.insert(0, t[1:])
                xrefs = []
                while True:
                    if not toks:
                        # components.append(SimpleValue("[" + " ".join(xrefs)))
                        # break
                        raise ValueError(f"Xref list does not terminate: {self.value}")
                    next_tok = toks.pop(0)
                    if next_tok.endswith("]"):
                        xrefs.append(next_tok[:-1])
                        break
                    xrefs.append(next_tok)
                # TODO
                components.append(XrefList(xrefs))
            else:
                components.append(SimpleValue(t))
        if cmt:
            components.append(Comment(cmt))
        return components

    def order(self) -> Tuple:
        """
        Order for sorting tag-value pairs.

        Note: we aim for consistency with OWLAPI, which differs partially from
        https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html
        :return:
        """
        t = self.tag
        v1 = TERM_TAGS.index(t) if t in TERM_TAGS else 99
        toks = self.tokenize()
        if self.tag == TAG_SYNONYM:
            # normalize a synonym by placing a blank type if not present
            if isinstance(toks[2], XrefList):
                # necessary to preserve owlapi order
                toks.insert(2, SimpleValue("zzzzz"))
        order_values = []
        for x in toks:
            order_values.append(x.order())
        if self.tag == TAG_INTERSECTION_OF:
            tpl = self.values_as_tuple()
            order_values = [chr(96 + len(list(tpl)))] + order_values
        return tuple([v1] + order_values)


@dataclass
class Structure:
    """
    Abstract grouping for Stanzas and Headers
    """

    tag_values: List[TagValue] = field(default_factory=lambda: [])
    """List of all tag-value pairs for this stanza or header"""

    def _simple_value(self, v) -> str:
        return v.split(" ")[0]

    def _quoted_value(self, v) -> str:
        return re.findall('"([^"]*)"', v)[0]

    def _values(self, tag: TAG) -> List[str]:
        return [tv.value for tv in self.tag_values if tv.tag == tag]

    def normalize_order(self):
        self.tag_values = sorted(self.tag_values, key=lambda x: x.order())

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
            if len(toks) == 1 or toks[1].startswith("!"):
                pairs.append((toks[0], None))
            else:
                pairs.append((toks[0], toks[1]))
        return pairs

    def property_value_tuples(self) -> List[Tuple[CURIE, Optional[CURIE]]]:
        pairs = []
        for v in self._values(TAG_PROPERTY_VALUE):
            toks = [x for x in v.split(" ") if x]
            if len(toks) == 1 or toks[1].startswith("!"):
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
            if "[" in vals[0]:
                m = re_quoted_simple.match(vals[0])
                if m:
                    return m.group(1)
                else:
                    raise ValueError(f"Could not parse quoted string from {vals}")
            else:
                return vals[0]

    def synonyms(self) -> List[SYNONYM_TUPLE]:
        """
        All synonyms for a stanza

        :return: list of synonyms
        """
        return [tv.as_synonym() for tv in self.tag_values if tv.tag == TAG_SYNONYM]

    def property_values(self) -> List[PROPERTY_VALUE_TUPLE]:
        """
        All property values for a stanza

        :return: list of property values
        """
        return [tv.as_property_value() for tv in self.tag_values if tv.tag == TAG_PROPERTY_VALUE]

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
        :param val: ID value.
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
            logging.warning(f"No values to remove for {tag} = {val} // {self}")
        self.tag_values = tvs

    def remove_tag_quoted_value(self, tag: TAG, val: str) -> None:
        """
        removes a simple tag-value such as synonym or definition.

        :param tag:
        :param val: Quoted value.
        :return:
        """
        n = 0
        tvs = []
        for tv in self.tag_values:
            if tv.tag == tag:
                if self._quoted_value(tv.value) == val:
                    n += 1
                    continue
            tvs.append(tv)
        if not n:
            logging.warning(f"No values to remove for {tag} = {val} // {self}")
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
            logging.warning(f"No values to remove for {tag} = {val1} {val2} // {self}")
        self.tag_values = tvs

    def _kwargs_to_qualifiers_string(self, **kwargs) -> str:
        """
        Converts a set of kwargs to a qualifier string

        :param kwargs:
        :return:
        """
        if not kwargs:
            return ""
        quals = [f'{k}="{v}"' for k, v in kwargs.items()]
        quals_str = ", ".join(quals)
        return f" {{{quals_str}}}"

    def add_tag_value(self, tag: TAG, val: str, **kwargs) -> None:
        """
        Adds a tag-value pair

        :param tag:
        :param val:
        :return:
        """
        if kwargs:
            val += " " + self._kwargs_to_qualifiers_string(**kwargs)
        self.tag_values.append(TagValue(tag, val))

    def add_quoted_tag_value(self, tag: TAG, val: str, xrefs: List[str]) -> None:
        """
        Adds a tag-value pair

        :param tag:
        :param val:
        :return:
        """
        self.tag_values.append(TagValue(tag, f"\"{val}\" [{','.join(xrefs)}]"))

    def add_tag_value_pair(self, tag: TAG, val1: str, val2: str, **kwargs) -> None:
        """
        Adds a tag-value pair where the value is a pair

        :param tag:
        :param val1:
        :param val2:
        :return:
        """
        v = f"{val1} {val2}"
        if kwargs:
            v += " " + self._kwargs_to_qualifiers_string(**kwargs)
        self.tag_values.append(TagValue(tag, v))

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

    def replace_token(self, curie_map: Mapping[CURIE, CURIE]):
        if self.id in curie_map:
            self.id = curie_map[self.id]
        for tv in self.tag_values:
            tv.replace_token(curie_map)


@dataclass
class OboDocument:
    """An OBO Document is a header plus zero or more stanzas"""

    header: Header = field(default_factory=lambda: Header())
    stanzas: Mapping[CURIE, Stanza] = field(default_factory=lambda: {})
    curie_to_shorthand_map: Mapping[CURIE, CURIE] = field(default_factory=lambda: {})

    def add_stanza(self, stanza: Stanza) -> None:
        """
        Adds a stanza to the document.

        Ensures stanza added in order.
        :param stanza:
        :return:
        """
        self.stanzas[stanza.id] = stanza
        self.order_stanzas()

    def reindex(self) -> None:
        self.stanzas = {s.id: s for s in self.stanzas.values()}

    def order_stanzas(self) -> None:
        """
        Orders stanzas by ID

        Does not change tag-value ordering within stanzas
        """
        term_stanzas = {
            curie: stanza
            for curie, stanza in self.stanzas.items()
            if self.stanzas[curie].type == OBO_TERM
        }
        typedef_stanzas = {
            curie: stanza
            for curie, stanza in self.stanzas.items()
            if self.stanzas[curie].type == OBO_TYPEDEF
        }
        sorted_term_stanzas = self._sort_stanzas(term_stanzas)
        sorted_typedef_stanzas = self._sort_stanzas(typedef_stanzas)

        self.stanzas = {s.id: s for s in sorted_term_stanzas}
        self.stanzas.update({s.id: s for s in sorted_typedef_stanzas})

    def _sort_stanzas(self, stanzas: Mapping[CURIE, Stanza]) -> Mapping[CURIE, Stanza]:
        values = stanzas.values()
        return sorted(values, key=lambda x: x.id)

    def normalize_line_order(self) -> None:
        """
        Normalizes line order within stanzas
        """
        for s in self.stanzas.values():
            s.normalize_order()

    def dump(self, file: TextIO, ensure_sorted=False, normalize_line_order=False) -> None:
        """
        Export to a file

        :param file:
        :param ensure_sorted: Sort stanzas
        :param normalize_line_order: Sort tags within stanzas
        """
        if ensure_sorted:
            self.order_stanzas()
        if normalize_line_order:
            self.normalize_line_order()

        self._dump_tag_values(self.header.tag_values, file)
        for s in self.stanzas.values():
            self._dump_stanza(s, file)

    def _dump_stanza(self, stanza: Stanza, file: TextIO):
        file.write(f"[{stanza.type}]\n")
        file.write(f"id: {stanza.id}\n")
        self._dump_tag_values(stanza.tag_values, file)

    def _dump_tag_values(self, tag_values: List[TagValue], file: TextIO):
        for tv in tag_values:
            if tv.tag != "id":
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
    with open(path, encoding="utf-8") as stream:
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
                    raise ValueError(f"Bad type: {typ} in line {line}")
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
        if stanzas:
            stanzas[-1].tag_values = tag_values
        else:
            if tag_values:
                if obo_document is not None:
                    raise AssertionError(
                        f"Should not have tag values: {tag_values} without stanzas"
                    )
                obo_document = OboDocument(header=Header(tag_values=tag_values))
    obo_document.stanzas = {stanza.id: stanza for stanza in stanzas}
    return obo_document
