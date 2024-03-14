"""Parser for GAF association formats"""

import csv
from dataclasses import dataclass
from typing import Iterator, Optional, TextIO

from oaklib.datamodels.association import Association, ParserConfiguration
from oaklib.parsers.xaf_association_parser import XafAssociationParser


@dataclass
class HpoaG2DAssociationParser(XafAssociationParser):
    """
    Parsers for Hpoa G2D format.

    Usage:

    >>> from oaklib.parsers.hpoa_g2d_association_parser import HpoaG2DAssociationParser
    >>> parser = HpoaG2DAssociationParser()
    >>> for assoc in parser.parse(open("tests/input/example-hpoa-g2d.csv")):
    ...     print(assoc.subject, assoc.subject_label, assoc.object, assoc.object_label)
    <BLANKLINE>
    ...
    HGNC:18806 CAMTA1 MONDO:0013886 nonprogressive cerebellar atxia with intellectual disability
    HGNC:16369 PARK7 MONDO:0011658 autosomal recessive early-onset Parkinson disease 7
    ...

    """

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
