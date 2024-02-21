"""Parser for GAF/HPOA and related association formats"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Iterator, Optional, TextIO, Union

from oaklib.datamodels.association import (
    Association,
    NegatedAssociation,
    ParserConfiguration,
)
from oaklib.parsers.parser_base import Parser


@dataclass
class AssociationParser(Parser, ABC):
    """Base class for all association parsers."""

    @abstractmethod
    def parse(
        self, file: TextIO, configuration: Optional[ParserConfiguration] = None, **kwargs
    ) -> Iterator[Union[NegatedAssociation, Association]]:
        raise NotImplementedError

    def add_metadata(
        self,
        associations: Iterable[Union[NegatedAssociation, Association]],
        primary_knowledge_source: Optional[str] = None,
        aggregator_knowledge_source: Optional[str] = None,
    ):
        """
        Add metadata to associations.

        :param associations:
        :param primary_knowledge_source:
        :return:
        """
        if primary_knowledge_source or aggregator_knowledge_source:
            for association in associations:
                if primary_knowledge_source and not association.primary_knowledge_source:
                    association.primary_knowledge_source = primary_knowledge_source
                if aggregator_knowledge_source and not association.aggregator_knowledge_source:
                    association.aggregator_knowledge_source = aggregator_knowledge_source
