from dataclasses import dataclass
from typing import Optional

from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface

ONTOBEE_MERGED_GRAPH_PREFIX = "http://purl.obolibrary.org/obo/merged/"


@dataclass
class OntobeeImplementation(
    AbstractSparqlImplementation, SearchInterface, MappingProviderInterface, OboGraphInterface
):
    """
    Wraps the Ontobee sparql endpoint

    An OntobeeImplementation can be initialed by:

        .. code:: python

           >>>  oi = OntobeeImplementation.create()

        The default ontobee endpoint will be assumed

    See: `<https://www.ontobee.org/>`_
    """

    def _default_url(self) -> str:
        return "http://sparql.hegroup.org/sparql"

    @property
    def named_graph(self) -> Optional[str]:
        if self.resource.slug is None:
            return None
        else:
            return f"{ONTOBEE_MERGED_GRAPH_PREFIX}{self.resource.slug.upper()}"
