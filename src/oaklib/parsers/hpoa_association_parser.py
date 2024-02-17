"""Parser for GAF association formats"""

from dataclasses import dataclass, field
from typing import List, Union

from oaklib.datamodels.association import Association, NegatedAssociation
from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class HpoaAssociationParser(XafAssociationParser):
    """Parsers for Hpoa format."""

    comment_character: str = "#"

    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    subject_label_column: ColumnReference = field(default_factory=lambda: ColumnReference(1))
    predicate_column: ColumnReference = None
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(3))

    def post_process(
        self, association: Association
    ) -> List[Union[Association, NegatedAssociation]]:
        if association.predicate and "not" in association.predicate.lower():
            # in future this may return a NegatedAssociation
            return [NegatedAssociation(**association.__dict__)]
        return super().post_process(association)
