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
    """
    Parsers for GenCC CSV format.

    .. warning ::

        The CSV and TSV distributed by this group frequently has formatting errors.

    See `<https://search.thegencc.org/download>`_ for more information.

    Usage:

    >>> from oaklib.parsers.gencc_association_parser import GenCCAssociationParser
    >>> parser = GenCCAssociationParser()
    >>> for assoc in parser.parse(open("tests/input/example-g2d.gencc.csv")):
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
        use_original_as_backup=False,
        **kwargs,
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        reader = csv.DictReader(file)
        for row in reader:
            disease_curie = row["disease_curie"]
            disease_title = row["disease_title"]
            if not disease_curie:
                if use_original_as_backup:
                    disease_curie = row["original_disease_curie"]
                    disease_title = row["original_disease_title"]
                else:
                    continue
            assoc = Association(
                object=disease_curie,
                object_label=disease_title,
                subject=row["gene_curie"],
                subject_label=row["gene_symbol"],
                primary_knowledge_source=row["submitter_curie"],
            )
            yield assoc
