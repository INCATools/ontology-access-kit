"""Parser for GAF association formats"""

from dataclasses import dataclass, field
from enum import Enum

from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


class GafAssociationColumns(Enum):
    db = "db"
    local_id = "local_id"
    db_object_symbol = "db_object_symbol"
    qualifiers = "qualifiers"
    ontology_class_ref = "ontology_class_ref"
    supporting_references = "supporting_references"
    evidence_type = "evidence_type"
    with_or_from = "with_or_from"
    aspect = "aspect"
    db_object_name = "db_object_name"
    db_object_synonyms = "db_object_synonyms"
    db_object_type = "db_object_type"
    db_object_taxon = "db_object_taxon"
    annotation_date = "annotation_date"
    assigned_by = "assigned_by"
    annotation_extensions = "annotation_extensions"
    gene_product_form = "gene_product_form"


@dataclass
class GafAssociationParser(XafAssociationParser):
    """Parsers for GAF format."""

    subject_prefix_column: ColumnReference = field(default_factory=lambda: ColumnReference(0))
    subject_column: ColumnReference = field(default_factory=lambda: ColumnReference(1))
    subject_label_column: ColumnReference = field(default_factory=lambda: ColumnReference(2))
    predicate_column: ColumnReference = field(default_factory=lambda: ColumnReference(3))
    object_column: ColumnReference = field(default_factory=lambda: ColumnReference(4))
    evidence_type_column: ColumnReference = field(default_factory=lambda: ColumnReference(6))
    publications_column: ColumnReference = field(default_factory=lambda: ColumnReference(5))
    primary_knowledge_source_column: ColumnReference = field(
        default_factory=lambda: ColumnReference(14)
    )
    expected_object_prefixes = ["GO"]

    other_column_mappings = {}
