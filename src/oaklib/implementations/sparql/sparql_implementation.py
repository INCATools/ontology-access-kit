from dataclasses import dataclass

import rdflib

from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.search_interface import SearchInterface


@dataclass
class SparqlImplementation(
    AbstractSparqlImplementation,
    DifferInterface,
    SearchInterface,
    MappingProviderInterface,
    OboGraphInterface,
    PatcherInterface,
):
    """
    Wraps any local or remote sparql endpoint
    """

    def __post_init__(self):
        if self.graph is None:
            resource = self.resource
            # print(resource)
            if resource.url:
                super(SparqlImplementation, self).__post_init__()
            else:
                graph = rdflib.Graph()
                if resource is not None:
                    graph.parse(str(resource.local_path), format=resource.format)
                    self.graph = graph
