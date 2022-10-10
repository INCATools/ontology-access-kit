"""Parser for GAF/HPOA and related association formats"""
from dataclasses import dataclass, field
from typing import Iterator, TextIO

from oaklib.datamodels.association import Association
from oaklib.parsers.association_parser import AssociationParser
from oaklib.parsers.parser_base import ColumnReference


@dataclass
class XafAssociationParser(AssociationParser):
    """Parsers for GAF and GAF-like formats."""

    comment_character: str = field(default_factory=lambda: "!")
    subject_prefix_column: ColumnReference = None
    subject_column: ColumnReference = None
    predicate_column: ColumnReference = None
    object_column: ColumnReference = None

    def parse(self, file: TextIO) -> Iterator[Association]:
        """
        Yields annotations from a GAF or GAF-like file

        :param file:
        :return:
        """
        lookup_subject_prefix = self.index_lookup_function(self.subject_prefix_column)
        lookup_subject = self.index_lookup_function(self.subject_column)
        lookup_predicate = self.index_lookup_function(self.predicate_column)
        lookup_object = self.index_lookup_function(self.object_column)
        for line in file.readlines():
            if line.startswith(self.comment_character):
                continue
            vals = line.split("\t")
            s = lookup_subject(vals)
            p = lookup_predicate(vals)
            o = lookup_object(vals)
            if self.subject_prefix_column:
                sp = lookup_subject_prefix(vals)
                s = f"{sp}:{s}"
            yield Association(s, p, o)
