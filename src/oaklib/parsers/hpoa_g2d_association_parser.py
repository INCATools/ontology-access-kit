"""Parser for GAF association formats"""
import csv
from dataclasses import dataclass, field
from typing import Iterator, Optional, TextIO

from oaklib.datamodels.association import Association, ParserConfiguration
from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class HpoaG2DAssociationParser(XafAssociationParser):
    """Parsers for Hpoa G2D format."""

    def parse(
        self,
        file: TextIO,
        configuration: Optional[ParserConfiguration] = None,
        mendelian_only=False,
        **kwargs,
    ) -> Iterator[Association]:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            typ = row["association_type"]
            if mendelian_only and typ != "MENDELIAN":
                continue
            assoc = Association(
                object=row["disease_id"].replace("ORPHA:", "Orphanet:"),
                subject=row["ncbi_gene_id"],
                subject_label=row["gene_symbol"],
                primary_knowledge_source=row["source"],
                aggregator_knowledge_source="infores:hpoa",
            )
            yield assoc
