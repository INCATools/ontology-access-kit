from dataclasses import dataclass
from typing import Optional

import rdflib
from oaklib.implementations.sparql.abstract_sparql_implementation import AbstractSparqlImplementation
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface


@dataclass
class SparqlImplementation(AbstractSparqlImplementation, SearchInterface, MappingProviderInterface, OboGraphInterface):
    """
    Wraps any local or remote sparql endpoint
    """

    def __post_init__(self):
        if self.graph is None:
            resource = self.resource
            graph = rdflib.Graph()
            if resource is not None:
                graph.parse(str(resource.local_path), format=resource.format)
            self.graph = graph










