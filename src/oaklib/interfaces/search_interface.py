from abc import ABC
from dataclasses import dataclass
from typing import List, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE


@dataclass
class SearchConfiguration:
    """
    Parameters for altering behavior of search

    .. note ::

        many of these parameters are not yet implemented
    """
    search_terms: List[str] = None
    include_id: bool = True
    include_label: bool = True
    include_aliases: bool = True
    include_definition: bool = False
    complete: bool = False
    is_regex: bool = False

    def use_label_only(self) -> "SearchConfiguration":
        self.include_label = False
        self.include_id = False
        self.include_definition = False
        self.include_aliases = False
        return self


class SearchInterface(BasicOntologyInterface, ABC):
    """
    An Ontology Interface that supports text-based search
    """

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        """
        Search over ontology using the specified search term.

        The search term may be a CURIE, label, or alias

        :param search_term:
        :param config:
        :return:
        """
        raise NotImplementedError

    def multiterm_search(self, search_terms: List[str], config: SearchConfiguration = None) -> Iterable[CURIE]:
        """
        As basic_search, using multiple terms

        :param search_terms:
        :param config:
        :return:
        """
        seen = set()
        for t in search_terms:
            if ':' in t:
                yield t
            for curie in self.basic_search(t):
                if curie in seen:
                    continue
                seen.add(curie)
                yield curie



