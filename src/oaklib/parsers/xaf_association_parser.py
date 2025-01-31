"""Parser for GAF/HPOA and related association formats"""

import logging
import re
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional, TextIO, Union

from oaklib.datamodels.association import (
    Association,
    NegatedAssociation,
    ParserConfiguration,
    PropertyValue,
)
from oaklib.parsers.association_parser import AssociationParser
from oaklib.parsers.parser_base import ColumnReference


def _check_identifier(s: str, expected_prefixes: List[str], must_be_curie: bool):
    if ":" not in s:
        message = f"Expected CURIE, got {s}"
        if must_be_curie:
            raise ValueError(message)
        logging.debug(message)
        return
    if re.match(r"\s", s):
        raise ValueError(f"Unexpected whitespace in {s}")
    prefix, _ = s.split(":", 1)
    if expected_prefixes and prefix not in expected_prefixes:
        raise ValueError(f"Unexpected prefix {prefix} in {s}")


@dataclass
class XafAssociationParser(AssociationParser):
    """
    Parsers for GAF and GAF-like formats.

    Note that implementations should use a subclass of this, and override ClassVars to
    determine behavior.
    """

    comment_character: str = field(default_factory=lambda: "!")
    """
    Character that indicates a comment line.
    Comment lines should be at the beginning of the file. They may include metadata that can be parsed
    """

    delimiter: str = field(default_factory=lambda: "\t")
    """
    Delimiter
    """

    subject_prefix = None
    """
    Prefix to use for subjects that do not have a prefix. This is prepended onto the subject_prefix_column
    If not specified, then EITHER subject_prefix_column MUST be specified, OR subject_column MUST be a CURIE
    """

    subject_prefix_column: Optional[ColumnReference] = None
    """
    Column that contains the prefix for the subject. If this is specified, then subject_column MUST NOT be a CURIE
    """

    subject_column: Optional[ColumnReference] = None
    """
    Column that contains the subject (e.g. gene ID).
    """

    subject_label_column: Optional[ColumnReference] = None
    """
    Column that contains the subject label (e.g. gene symbol)
    """

    predicate_column: Optional[ColumnReference] = None
    """
    Column that contains the predicate (e.g. RO:0002200)
    """

    object_column: Optional[ColumnReference] = None
    """
    Column that contains the object (e.g. GO or Phenotype term ID)
    """

    object_label_column: Optional[ColumnReference] = None
    """
    Column that contains the object label (e.g. term name)
    """

    subject_must_be_curie = False
    """
    If True, then the subject column is validated to ensure it is a CURIE
    """

    object_must_be_curie = False
    """
    If True, then the object column is validated to ensure it is a CURIE
    """

    expected_subject_prefixes: Optional[List[str]] = None
    """
    List of prefixes that are expected for subjects. If specified,
    then the subject prefix is validated against this list
    """

    expected_object_prefixes: Optional[List[str]] = None
    """
    List of prefixes that are expected for objects. If specified,
    then the object prefix is validated against this list
    """

    expected_predicates: Optional[List[str]] = None
    """
    List of predicates that are expected. If specified, then the predicate is validated against this list
    """

    default_predicate_value: Optional[str] = None
    """
    If specified, then this value is used as the predicate if the predicate_column is not specified
    """

    evidence_type_column: Optional[ColumnReference] = None
    """
    Column that contains the evidence type (e.g. GAF code like IEA)
    """

    publications_column: Optional[ColumnReference] = None
    """
    Column that contains the publications (e.g. PMID, DOI).
    """

    primary_knowledge_source_column: Optional[ColumnReference] = None
    """
    Column that contains the primary association provider
    """

    other_column_mappings: Optional[Dict[int, str]] = None
    """
    Mapping of column indices to attribute names.
    """

    def post_process(
        self, association: Association
    ) -> List[Union[Association, NegatedAssociation]]:
        return [association]

    def parse(
        self,
        file: TextIO,
        configuration: Optional[ParserConfiguration] = None,
        **kwargs,
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        """
        Yields annotations from a GAF or GAF-like file

        :param file: File to parse
        :param configuration: Configuration for the parser
        :param kwargs: Additional arguments
        :return:
        """
        lookup_subject_prefix = self.index_lookup_function(self.subject_prefix_column)
        lookup_subject = self.index_lookup_function(self.subject_column)
        lookup_subject_label = self.index_lookup_function(self.subject_label_column)
        lookup_predicate = self.index_lookup_function(self.predicate_column)
        lookup_object = self.index_lookup_function(self.object_column)
        lookup_publications = self.index_lookup_function(self.publications_column)
        lookup_evidence_type = self.index_lookup_function(self.evidence_type_column)
        lookup_primary_knowledge_source = self.index_lookup_function(
            self.primary_knowledge_source_column
        )
        if (
            self.subject_prefix_column
            and self.expected_subject_prefixes
            and self.subject_prefix not in self.expected_subject_prefixes
        ):
            raise ValueError(f"Unexpected subject prefix {self.subject_prefix} in file")
        if (
            self.default_predicate_value
            and self.expected_predicates
            and self.default_predicate_value not in self.expected_predicates
        ):
            raise ValueError(f"Unexpected default predicate {self.default_predicate_value} in file")
        for line in file.readlines():
            is_negated = False
            if line.startswith(self.comment_character):
                continue
            line = line.rstrip()
            vals = line.split("\t")
            # logging.debug(f"Processing line: {line} // {vals}")
            s = lookup_subject(vals)
            p = lookup_predicate(vals)
            o = lookup_object(vals)
            if p:
                ps = p.split("|")
                p = None
                for candidate in ps:
                    if candidate.lower() == "not":
                        is_negated = True
                    else:
                        if p:
                            raise ValueError(
                                f"Unexpected predicate {candidate} for {p} in line: {line}"
                            )
                        p = candidate
            if not p:
                p = self.default_predicate_value
            if self.subject_prefix_column:
                sp = lookup_subject_prefix(vals)
                s = f"{sp}:{s}"
            elif self.subject_prefix:
                s = f"{self.subject_prefix}:{s}"
            else:
                _check_identifier(s, self.expected_subject_prefixes, self.subject_must_be_curie)
            _check_identifier(o, self.expected_object_prefixes, self.object_must_be_curie)
            if self.expected_predicates and p not in self.expected_predicates:
                raise ValueError(f"Unexpected predicate {p} in line: {line}")
            if s.startswith("MGI:MGI:"):
                # TODO: make this more configurable
                s = s.replace("MGI:MGI:", "MGI:")
            if is_negated:
                association = NegatedAssociation(s, p, o, negated=True)
            else:
                association = Association(s, p, o)
            if lookup_publications:
                pub = lookup_publications(vals)
                if pub:
                    association.publications = pub.split("|")
            if lookup_evidence_type:
                ev = lookup_evidence_type(vals)
                if ev:
                    association.evidence_type = ev
            if lookup_primary_knowledge_source:
                src = lookup_primary_knowledge_source(vals)
                if src:
                    if ":" not in src:
                        src = f"infores:{src}"
                    association.primary_knowledge_source = src
            if lookup_subject_label:
                sl = lookup_subject_label(vals)
                if sl:
                    association.subject_label = sl
            if self.other_column_mappings:
                for i, attr in self.other_column_mappings.items():
                    association.property_values[attr] = PropertyValue(attr, vals[i])
            for processed_association in self.post_process(association):
                if isinstance(processed_association, NegatedAssociation):
                    if configuration and configuration.preserve_negated_associations:
                        yield processed_association
                else:
                    yield processed_association
