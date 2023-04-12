from dataclasses import dataclass
from typing import List, Optional

import rdflib

from oaklib import BasicOntologyInterface
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.merge_interface import MergeConfiguration, MergeInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface


@dataclass
class SparqlImplementation(
    AbstractSparqlImplementation,
    AssociationProviderInterface,
    RdfInterface,
    DifferInterface,
    SearchInterface,
    MappingProviderInterface,
    OboGraphInterface,
    PatcherInterface,
    SemanticSimilarityInterface,
    TextAnnotatorInterface,
    TaxonConstraintInterface,
    MergeInterface,
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

    def merge(
        self,
        sources: List[BasicOntologyInterface],
        configuration: Optional[MergeConfiguration] = None,
        **kwargs,
    ):
        """
        Merges from multiple sources into current adapter.

        :param sources:
        :param configuration:
        :param kwargs:
        :return:
        """
        if not configuration:
            configuration = MergeConfiguration()
        if not self.graph:
            raise NotImplementedError("Cannot merge into a read-only graph")
        for source in sources:
            if not isinstance(source, RdfInterface):
                raise NotImplementedError("Cannot merge from non-sparql source")
            for t in source.all_rdflib_triples():
                self.graph.add(t)
