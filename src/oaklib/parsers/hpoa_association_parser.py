"""Parser for GAF association formats"""
from dataclasses import dataclass, field

from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class HpoaAssociationParser(XafAssociationParser):
    """Parsers for Hpoa format."""

    comment_character: str = "#"

    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    predicate_column: ColumnReference = None
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(3))
