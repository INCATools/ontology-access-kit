"""Parser for PomBase PHAF association formats"""

from dataclasses import dataclass, field

from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class PhafAssociationParser(XafAssociationParser):
    """Parsers for PHAF format."""

    comment_character: str = "#"

    subject_prefix_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(1))
    predicate_column: ColumnReference = None
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(2))
    expected_object_prefixes = ["FYPO"]
