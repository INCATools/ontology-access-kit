"""Parser for GAF association formats"""
import csv
from dataclasses import dataclass
from typing import Iterator, Optional, TextIO, Union

from oaklib.datamodels.association import (
    Association,
    NegatedAssociation,
    ParserConfiguration,
)
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class GenCCAssociationParser(XafAssociationParser):
    """Parsers for GenCC CSV format.

    .. warning ::

        The CSV and TSV distributed by this group frequently has formatting errors.

    See `<https://search.thegencc.org/download>`_ for more information.
    """

    def parse(
        self, file: TextIO, configuration: Optional[ParserConfiguration] = None
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        reader = csv.DictReader(file)
        for row in reader:
            assoc = Association(
                object=row["disease_curie"],
                object_label=row["disease_title"],
                subject=row["gene_curie"],
                subject_label=row["gene_symbol"],
            )
            yield assoc
