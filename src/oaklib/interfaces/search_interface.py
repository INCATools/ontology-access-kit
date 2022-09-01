from abc import ABC
from typing import Iterable, List, Optional

from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = ["SearchConfiguration", "SearchInterface"]


class SearchInterface(BasicOntologyInterface, ABC):
    """
    An Ontology Interface that supports text-based search
    """

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        """
        Search over ontology using the specified search term.

        The search term may be a CURIE, label, or alias

        :param search_term:
        :param config:
        :return:
        """
        raise NotImplementedError

    def multiterm_search(
        self, search_terms: List[str], config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        """
        As basic_search, using multiple terms

        :param search_terms:
        :param config:
        :return:
        """
        seen = set()
        for t in search_terms:
            if ":" in t:
                yield t
            else:
                for curie in self.basic_search(t, config=config):
                    if curie in seen:
                        continue
                    seen.add(curie)
                    yield curie
