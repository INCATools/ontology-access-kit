from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import List

import SPARQLWrapper
from obolib.implementations.sparql.sparql_implementation import SparqlImplementation
from obolib.implementations.ubergraph.ubergraph import UbergraphProvider
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP
from obolib.interfaces.relation_graph_interface import RelationGraphInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE


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

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred_uri, obj_uri in self._triples(curie, None, None, None):
            pred = self.uri_to_curie(pred_uri)
            obj = self.uri_to_curie(obj_uri)
            rmap[pred].append(obj)
        return rmap





