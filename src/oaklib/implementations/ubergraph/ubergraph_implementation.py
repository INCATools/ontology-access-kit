from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple

from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.types import CURIE


class RelationGraphEnum(Enum):
    """
    triples in UG are organized into different graphs
    """
    ontology = "http://reasoner.renci.org/ontology"
    redundant = "http://reasoner.renci.org/redundant"
    nonredundant = "http://reasoner.renci.org/nonredundant"


@dataclass
class UbergraphImplementation(SparqlImplementation, RelationGraphInterface, SearchInterface):
    """
    Wraps the Ubergraph sparql endpoint

    See: `<https://github.com/INCATools/ubergraph>`_

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in Ubergraph

    An UbergraphImplementation can be initialed by:

        .. code:: python

           >>>  oi = UbergraphImplementation.create()

        The default ubergraph endpoint will be assumed

    """
    #sparql_wrapper: SPARQLWrapper

    def _default_url(self) -> str:
        return "https://ubergraph.apps.renci.org/sparql"

    def _is_blazegraph(self) -> bool:
        """
        Currently Ubergraph uses blazegraph
        """
        return True



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





