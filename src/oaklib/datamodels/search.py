from dataclasses import dataclass
from typing import List

from deprecated.classic import deprecated

from oaklib.datamodels.search_datamodel import (
    SearchBaseConfiguration,
    SearchProperty,
    SearchTermSyntax,
)
from oaklib.datamodels.vocabulary import LABEL_PREDICATE, SYNONYM_PREDICATES
from oaklib.types import PRED_CURIE

DEFAULT_SEARCH_PROPERTIES = [SearchProperty.LABEL, SearchProperty.ALIAS]


def create_search_configuration(term: str) -> "SearchConfiguration":
    """
    Generates a search configuration based on search syntax

    term is either a plaintext search term, or a search term prefixed by

    - 1. a property code, one of t, ., l (for term, anything, label)
    - 2. a match type indicator, one of "~","/","=","^"

    For more documentation, see `Search docs <https://incatools.github.io/ontology-access-kit/interfaces/search.html>`_

    :param term:
    :return:
    """

    if len(term) > 1:
        prop = term[0]
        code = term[1]
        rest = term[2:]
        if code == "~":
            cfg = SearchBaseConfiguration([rest], is_partial=True)
        elif code == "/":
            cfg = SearchBaseConfiguration([rest], syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        elif code == "@":
            cfg = SearchBaseConfiguration([rest], syntax=SearchTermSyntax.SQL)
        elif code == "=":
            cfg = SearchBaseConfiguration([rest], is_partial=False)
        elif code == "^":
            cfg = SearchBaseConfiguration([rest], syntax=SearchTermSyntax.STARTS_WITH)
        else:
            cfg = SearchBaseConfiguration([term], properties=DEFAULT_SEARCH_PROPERTIES)
            prop = None
        if prop:
            if prop == "t":
                props = [SearchProperty.LABEL, SearchProperty.ALIAS]
            elif prop == ".":
                props = [SearchProperty.ANYTHING]
            elif prop == "l":
                props = [SearchProperty.LABEL]
            elif prop == "i":
                props = [SearchProperty.IDENTIFIER]
            else:
                raise ValueError(f"Unknown property code: {prop}")
            cfg.properties = [SearchProperty(p) for p in props]
        return cfg
    else:
        return SearchConfiguration([term], properties=DEFAULT_SEARCH_PROPERTIES)


def search_properties_to_predicates(props: List[SearchProperty]) -> List[PRED_CURIE]:
    preds = set()
    for p in props:
        if p == SearchProperty(SearchProperty.LABEL):
            preds.add(LABEL_PREDICATE)
        elif p == SearchProperty(SearchProperty.ALIAS):
            preds.update(SYNONYM_PREDICATES + [LABEL_PREDICATE])
        elif p == SearchProperty(SearchProperty.ANYTHING):
            preds.update(SYNONYM_PREDICATES + [LABEL_PREDICATE])
        else:
            raise ValueError(p)
    return list(preds)


@dataclass
class SearchConfiguration(SearchBaseConfiguration):
    """
    Parameters for altering behavior of search

    .. note ::

        many of these parameters are not yet implemented
    """
