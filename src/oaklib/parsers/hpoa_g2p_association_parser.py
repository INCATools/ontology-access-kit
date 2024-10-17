"""Parser for GAF association formats"""

from dataclasses import dataclass, field

from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class HpoaG2PAssociationParser(XafAssociationParser):
    """Parsers for Hpoa G2P format."""

    comment_character: str = "#"

    subject_prefix = "NCBIGene"
    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    subject_label_column: ColumnReference = field(default_factory=lambda: ColumnReference(1))
    predicate_column: ColumnReference = None
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(2))
