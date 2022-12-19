from dataclasses import dataclass

import rdflib

import oaklib.datamodels as dm
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface

__all__ = [
    "OakMetaModelImplementation",
]

from oaklib.mappers.ontology_metadata_mapper import load_default_sssom


@dataclass
class OakMetaModelImplementation(
    AbstractSparqlImplementation,
    DifferInterface,
    SearchInterface,
    MappingProviderInterface,
    OboGraphInterface,
    PatcherInterface,
    SemanticSimilarityInterface,
):
    """
    Wraps the internal OAK data models.

    OAK uses a number of different data models, see:

    `<https://incatools.github.io/ontology-access-kit/datamodels>`_

    Each of these datamodels is also stored as RDF/OWL, which allows
    for introspection as ontologies.
    """

    def __post_init__(self):
        if self.resource is None:
            raise ValueError("resource must be set")
        graph = rdflib.Graph()
        graph.parse(str(dm.this_path / f"{self.resource.slug}.owl.ttl"), format="turtle")
        self.graph = graph
        mappings = load_default_sssom("omo-to-skos")
        self.set_metamodel_mappings(mappings)
        # TODO: register this with w3id.org
        self.prefix_map()["oaklib"] = "https://w3id.org/oaklib/"
