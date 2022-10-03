"""Base class for all parsers."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Iterator, List, Optional, TextIO, Tuple


@dataclass
class ColumnReference:
    """A way of indexing a column."""

    index: Optional[int] = None
    """Number of the column (zero-based)."""

    name: Optional[str] = None
    """Name of the column."""

    column_pair: Optional[Tuple["ColumnReference", "ColumnReference"]] = None
    """For CURIEs split over two columns"""


@dataclass
class Parser(ABC):
    """Base class for all parsers."""

    @abstractmethod
    def parse(self, file: TextIO) -> Iterator:
        """
        Abstract method for all parsers.

        :param file:
        :return:
        """
        raise NotImplementedError

    def index_lookup_function(self, column_reference: Optional[ColumnReference]) -> Callable:
        """
        Returns a function that can be used to lookup a row by reference.

        :param column_reference:
        :return:
        """
        if column_reference is None:
            return lambda _: None
        ix = column_reference.index
        if ix is None:
            raise ValueError("Column reference must have index")

        def _lookup(vals: List[Any]) -> Any:
            return vals[ix]

        return _lookup
