from abc import ABC, abstractmethod
from dataclasses import dataclass

from oaklib.datamodels.ontology_metadata import Any


@dataclass
class DataModelConverter(ABC):
    """Base class for all inter-data model converters."""

    @abstractmethod
    def convert(self, source: Any, target: Any = None) -> Any:
        """
        Converts from a source object to a target object.

        :param source:
        :param target: Optional. If passed, modified in place
        :return:
        """
        raise NotImplementedError
