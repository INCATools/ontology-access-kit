"""Parser for GAF association formats"""

from dataclasses import dataclass, field

from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class PairwiseAssociationParser(XafAssociationParser):
    """Parsers for simple subject-object 2 column association files."""

    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(1))
