from abc import ABC
from typing import Iterable, List, Optional

from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = ["SearchConfiguration", "SearchInterface"]


class SearchInterface(BasicOntologyInterface, ABC):
    """
    An Ontology Interface that supports text-based search.

    The search interface provides a largely implementation-neutral way to query an ontology. It allows for

    - exact or partial matches
    - matching the beginning of a term
    - regular expression search

    It also allows you to control which metadata elements are searched over (typically labels and aliases)

    Implementations may differ in their behavior. Some implementations may not be able to honor specific requests.
    For example, the :ref:`SqlDatabaseImplementation` implementation may not be able to fulfil regular
    expression queries.

    Some endpoints may return results that are ranked by relevance, others may be arbitrary

    Command Line
    ------------

    A good way to explore this interface is via the search subcommand:

    Ubergraph uses relevancy ranking:

    .. code::

        runoak -i ubergraph:uberon search limb

    Exact match for a label using sqlite:

    .. code::

        runoak -i db/cl.db search l=neuron

    Inexact match for a label or synonym using sqlite:

    .. code::

        poetry run runoak -i db/cl.db search .~neuron

    Datamodels
    ----------

    Search uses `<https://w3id.org/oak/search>`_ to specify both an input query and search results,
     see :ref:`datamodels`
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
