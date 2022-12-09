from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

import curies

from oaklib.datamodels.ontology_metadata import Any
from oaklib.types import CURIE


@dataclass(eq=False)
class DataModelConverter(ABC):
    """Base class for all inter-data model converters.

    Do not use this directly: use one of the subclasses.
    """

    curie_converter: curies.Converter = None
    """Converts between CURIEs and URIs"""

    labeler: Callable[[CURIE], Optional[str]] = None
    """A function that returns a label for a given CURIE"""

    def __hash__(self):
        return hash(str(self))

    @abstractmethod
    def convert(self, source: Any, target: Any = None, **kwargs) -> Any:
        """
        Converts from a source object to a target object.

        Individual subclasses will map this to a specific subtype.

        :param source:
        :param target: Optional. If passed, modified in place
        :param kwargs: Additional arguments
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def dump(self, source: Any, target: str = None, **kwargs) -> None:
        """
        Dumps a source object to a target file.

        :param source:
        :param target:
        :return:
        """
        raise NotImplementedError
