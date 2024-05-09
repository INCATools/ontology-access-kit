"""Parser for GAF association formats"""

import csv
from dataclasses import dataclass, field
from typing import Iterator, Optional, TextIO, Union, Dict

from oaklib.datamodels.association import (
    Association,
    NegatedAssociation,
    ParserConfiguration,
)
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class MedgenMimG2DAssociationParser(XafAssociationParser):
    """
    Parsers for MIM2GENE NCBI TSV format.

    See `<ftp://ftp.ncbi.nih.gov/gene/DATA/mim2gene_medgen>`_ for more information.
    """

    conservative: bool = field(default_factory=lambda: True)

    def parse(
        self, file: TextIO, configuration: Optional[ParserConfiguration] = None, **kwargs,
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        reader = csv.DictReader(file, delimiter="\t")
        row: Dict[str, str]
        for row in reader:
            mim = row["#MIM number"]
            typ = row["type"]
            if typ != "phenotype":
                continue
            comments = [x for x in row["Comment"].split("; ") if x != "-"]
            if self.conservative:
                if comments:
                    continue
            predicate = "biolink:causes"
            if comments:
                if "susceptibility" in comments:
                    predicate = "biolink:gene_associated_with_condition"
                else:
                    continue
            gene_id = row["GeneID"]
            if gene_id == "-":
                continue
            assoc = Association(
                subject=f"NCBIGene:{gene_id}",
                predicate=predicate,
                object=f"OMIM:{mim}",
            )
            yield assoc
