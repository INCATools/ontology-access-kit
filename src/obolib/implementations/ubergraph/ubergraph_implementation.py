from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import List, Iterable, Tuple

import SPARQLWrapper
from obolib.implementations.sparql.sparql_implementation import SparqlImplementation, SparqlQuery
from obolib.implementations.ubergraph.ubergraph import UbergraphProvider
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP
from obolib.interfaces.relation_graph_interface import RelationGraphInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE


class RelationGraphEnum(Enum):
    ontology = "http://reasoner.renci.org/ontology"
    redundant = "http://reasoner.renci.org/redundant"
    nonredundant = "http://reasoner.renci.org/nonredundant"


@dataclass
class UbergraphImplementation(SparqlImplementation, RelationGraphInterface):
    """
    Wraps the Ubergraph sparql endpoint

    See: `<https://github.com/INCATools/ubergraph>`_
    """
    engine: SPARQLWrapper

    @classmethod
    def create(cls, resource: OntologyResource = None) -> "UbergraphImplementation":
        """
        An UbergraphImplementation can be initialed by:

        .. code:: python

           >>>  oi = UbergraphImplementation.create()

        The default ubergraph endpoint will be assumed

        :param resource: optional
        :return:
        """
        engine = UbergraphProvider.create_engine(resource)
        return UbergraphImplementation(engine)

    def store(self, resource: OntologyResource) -> None:
        UbergraphProvider.dump(self.engine, resource)

    def _get_outgoing_edges_by_curie(self, curie: CURIE, graph: RelationGraphEnum) -> Iterable[Tuple[CURIE, CURIE]]:
        rmap = defaultdict(list)
        subj = self.curie_to_uri(curie)
        query = SparqlQuery(select=['?p', '?o'],
                            where=[f'GRAPH <{graph.value}> {{ <{subj}> ?p ?o }}',
                                   f'?o a owl:Class'])
        bindings = self._query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row['p']['value'])
            obj = self.uri_to_curie(row['o']['value'])
            yield pred, obj

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, obj in self._get_outgoing_edges_by_curie(curie, graph=RelationGraphEnum.nonredundant):
            rmap[pred].append(obj)
        return rmap





