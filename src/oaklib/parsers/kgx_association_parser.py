"""Parser for KGX"""

from csv import DictReader
from dataclasses import dataclass
from typing import Iterator, TextIO

from oaklib.datamodels.association import Association
from oaklib.parsers.association_parser import AssociationParser


@dataclass
class KgxAssociationParser(AssociationParser):
    """Parsers for KGX."""

    def parse(self, file: TextIO) -> Iterator[Association]:
        """
        Yields annotations from a KGX edges file

        :param file:
        :return:
        """
        reader = DictReader(file, delimiter="\t")
        for row in reader:
            yield Association(row["subject"], row["predicate"], row["object"])
