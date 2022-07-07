from dataclasses import dataclass
from typing import Optional

from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface


@dataclass
class LovImplementation(
    AbstractSparqlImplementation, SearchInterface, MappingProviderInterface, OboGraphInterface
):
    """
    Wraps the LOV SPARQL endpoint

    See `<https://lov.linkeddata.es>`_

    """

    def _default_url(self) -> str:
        return "https://lov.linkeddata.es/dataset/lov/sparql"

    @property
    def named_graph(self) -> Optional[str]:
        if self.resource.slug is None:
            return None
        else:
            return self.resource.slug
