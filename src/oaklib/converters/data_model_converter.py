from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

import curies

from oaklib.datamodels.ontology_metadata import Any
from oaklib.types import CURIE


@dataclass(eq=False)
class DataModelConverter(ABC):
    """Base class for all inter-data model converters."""

    curie_converter: curies.Converter = None
    labeler: Callable[[CURIE], Optional[str]] = None

    def __hash__(self):
        return hash(str(self))

    @abstractmethod
    def convert(self, source: Any, target: Any = None) -> Any:
        """
        Converts from a source object to a target object.

        :param source:
        :param target: Optional. If passed, modified in place
        :return:
        """
        raise NotImplementedError
