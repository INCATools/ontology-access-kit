"""Simple in-memory cache for edges."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterator, List, Mapping, Optional, Tuple

from oaklib.types import CURIE

EDGE = Tuple[CURIE, CURIE, CURIE]

logger = logging.getLogger(__name__)


@dataclass
class EdgeIndex:
    """Simple in-memory cache for edges."""

    all_relationships_function: Optional[Callable] = None
    """Function that yields all relationships."""

    prepopulate: bool = False
    """Whether to prepopulate the index on instantiation."""

    _by_subject: Optional[Mapping[CURIE, List[EDGE]]] = None
    _by_object: Optional[Mapping[CURIE, List[EDGE]]] = None

    def __post_init__(self):
        if self.prepopulate:
            self._index()

    @property
    def by_subject(self) -> Mapping[CURIE, List[EDGE]]:
        """Index of relationships by subject."""
        if self._by_subject is None:
            self._index()
        return self._by_subject

    @property
    def by_object(self) -> Mapping[CURIE, List[EDGE]]:
        """Index of relationships by object."""
        if self._by_object is None:
            self._index()
        return self._by_object

    def _index(self):
        if not self.all_relationships_function:
            raise ValueError("No all_relationships_function provided")
        self._by_subject = defaultdict(list)
        self._by_object = defaultdict(list)
        for rel in self.all_relationships_function():
            s, _p, o = rel
            self._by_subject[s].append(rel)
            self._by_object[o].append(rel)

    def reindex(self):
        """Rebuild the index."""
        self._index()

    def edges(
        self,
        subjects: Optional[List[CURIE]] = None,
        predicates: Optional[List[CURIE]] = None,
        objects: Optional[List[CURIE]] = None,
    ) -> Iterator[EDGE]:
        """
        Yield all edges matching the specified criteria.

        :param subjects:
        :param predicates:
        :param objects:
        :return: relationship iterator
        """

        def _exclude(rel: EDGE) -> bool:
            if subjects is not None and rel[0] not in subjects:
                return True
            if predicates is not None and rel[1] not in predicates:
                return True
            if objects is not None and rel[2] not in objects:
                return True
            return False

        if subjects:
            logger.debug(f"Using relationship index keyed by {subjects}")
            for s in set(subjects):
                yield from [rel for rel in self.by_subject[s] if not _exclude(rel)]
        elif objects:
            logger.debug(f"Using relationship index keyed by {objects}")
            for o in set(objects):
                yield from [rel for rel in self.by_object[o] if not _exclude(rel)]
        else:
            logger.debug(f"No s/p specified, scanning all relationships filter by {predicates}")
            for rels in self.by_subject.values():
                yield from [rel for rel in rels if not _exclude(rel)]
