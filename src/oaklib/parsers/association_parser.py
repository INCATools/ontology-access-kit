"""Parser for GAF/HPOA and related association formats"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, TextIO

from oaklib.datamodels.association import Association
from oaklib.parsers.parser_base import Parser


@dataclass
class AssociationParser(Parser, ABC):
    """Base class for all association parsers."""

    @abstractmethod
    def parse(self, file: TextIO) -> Iterator[Association]:
        raise NotImplementedError
