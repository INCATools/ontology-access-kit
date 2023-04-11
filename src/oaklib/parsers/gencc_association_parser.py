"""Parser for GAF association formats"""
import csv
from dataclasses import dataclass, field
from typing import Iterator, Optional, TextIO, Union

from oaklib.datamodels.association import (
    Association,
    NegatedAssociation,
    ParserConfiguration,
)
from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class GenCCAssociationParser(XafAssociationParser):
    """Parsers for GenCC CSV format.

    See `<https://search.thegencc.org/download>`_ for more information.
    """

    def parse(
        self, file: TextIO, configuration: Optional[ParserConfiguration] = None
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        reader = csv.DictReader(file)
        for row in reader:
            assoc = Association(
                subject=row["disease_curie"],
                subject_label=row["disease_title"],
                object=row["gene_curie"],
                object_label=row["gene_symbol"],
            )
            yield assoc
