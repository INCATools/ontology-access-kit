import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple, List, Union, Optional, Iterator

from oaklib.datamodels import obograph
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation, _sparql_values
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP, RELATIONSHIP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate
from rdflib import RDFS, RDF, OWL


class RelationGraphEnum(Enum):
    """
    triples in UG are organized into different graphs
    """
    ontology = "http://reasoner.renci.org/ontology"
    redundant = "http://reasoner.renci.org/redundant"
    nonredundant = "http://reasoner.renci.org/nonredundant"


@dataclass
class UbergraphImplementation(SparqlImplementation, RelationGraphInterface, SearchInterface, OboGraphInterface,
                              MappingProviderInterface, SubsetterInterface):
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

    @property
    def named_graph(self) -> Optional[str]:
        if not self.resource or self.resource.slug is None:
            return None
        else:
            ont = self.resource.slug
            for g in self.list_of_named_graphs():
                if f'/{ont}.' in g or f'/{ont}-base' in g:
                    return g

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RelationGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _get_outgoing_edges_by_curie(self, curie: CURIE, graph: RelationGraphEnum,
                                     predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=['?p', '?o'],
                            where=[f'GRAPH <{graph.value}> {{ {query_uri} ?p ?o }}',
                                   f'?o a owl:Class'])
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        bindings = self._query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row['p']['value'])
            obj = self.uri_to_curie(row['o']['value'])
            yield pred, obj

    def _get_incoming_edges_by_curie(self, curie: CURIE, graph: RelationGraphEnum,
                                     predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=['?s', '?p'],
                            where=[f'GRAPH <{graph.value}> {{ ?s ?p {query_uri}  }}',
                                   f'?s a owl:Class'])
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        bindings = self._query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row['p']['value'])
            subj = self.uri_to_curie(row['s']['value'])
            yield pred, subj


    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, obj in self._get_outgoing_edges_by_curie(curie, graph=RelationGraphEnum.nonredundant):
            rmap[pred].append(obj)
        return rmap

    def get_incoming_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, s in self._get_incoming_edges_by_curie(curie, graph=RelationGraphEnum.nonredundant):
            rmap[pred].append(s)
        return rmap

    def entailed_outgoing_relationships_by_curie(self, curie: CURIE,
                                                 predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._get_outgoing_edges_by_curie(curie, graph=RelationGraphEnum.redundant, predicates=predicates)

    def entailed_incoming_relationships_by_curie(self, curie: CURIE,
                                                 predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._get_incoming_edges_by_curie(curie, graph=RelationGraphEnum.redundant, predicates=predicates)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _values(self, var: str, in_list: Optional[List[str]]) -> str:
        if in_list is None:
            return ""
        else:
            return f'VALUES ?{var} {{ {" ".join(in_list)} }}'

    def _from_subjects_chunked(self, subjects: List[CURIE], predicates: List[PRED_CURIE] = None, **kwargs):
        SIZE = 10
        while len(subjects) > 0:
            next_subjects = subjects[0:SIZE]
            subjects = subjects[SIZE:]
            for r in self._from_subjects(next_subjects, predicates, **kwargs):
                yield r


    def _from_subjects(self, subjects: List[CURIE], predicates: List[PRED_CURIE] = None,
                       graph: str = None, object_is_literal=False, where=[]) -> Iterable[Tuple[CURIE, PRED_CURIE, CURIE]]:
        subject_uris = [self.curie_to_sparql(curie) for curie in subjects]
        if predicates:
            predicate_uris = [self.curie_to_sparql(curie) for curie in predicates]
        else:
            predicate_uris = None
        query = SparqlQuery(select=['?s ?p ?o'],
                            distinct=True,
                            graph=graph,
                            where=['?s ?p ?o',
                                   self._values('s', subject_uris),
                                   self._values('p', predicate_uris),
                                   ] + where)
        #print(f'G={graph} Q={query.query_str()}')
        bindings = self._query(query.query_str())
        for row in bindings:
            v = row['o']['value']
            if not object_is_literal:
                v = self.uri_to_curie(v)
            yield (self.uri_to_curie(row['s']['value']),
                   self.uri_to_curie(row['p']['value']),
                   v)

    def _object_properties(self) -> List[PRED_CURIE]:
        return list(set([t[0] for t in self._triples(None, RDF.type, OWL.ObjectProperty)]))

    def node(self, curie: CURIE) -> obograph.Node:
        params = dict(id=curie,
                      label=self.get_label_by_curie(curie))
        return obograph.Node(**params)

    def ancestor_graph(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> obograph.Graph:
        ancs = list(self.ancestors(start_curies, predicates))
        logging.info(f'NUM ANCS: {len(ancs)}')
        edges = []
        nodes = {}
        for rel in self._from_subjects_chunked(ancs, predicates, graph=RelationGraphEnum.nonredundant.value, where=[]):
            edges.append(obograph.Edge(sub=rel[0], pred=rel[1], obj=rel[2]))
        logging.info(f'NUM EDGES: {len(edges)}')
        for rel in self._from_subjects_chunked(ancs, [RDFS.label], object_is_literal=True):
            id = rel[0]
            nodes[id] = obograph.Node(id=id, label=rel[2])
        logging.info(f'NUM NODES: {len(nodes)}')
        return obograph.Graph(id='query',
                              nodes=list(nodes.values()), edges=edges)

    def relationships_to_graph(self, relationships: Iterable[RELATIONSHIP]) -> obograph.Graph:
        relationships = list(relationships)
        edges = [obograph.Edge(sub=s, pred=p, obj=o) for s, p, o in relationships]
        node_ids = set()
        for rel in relationships:
            node_ids.update(list(rel))
        nodes = {}
        for s, p, o in self._from_subjects_chunked(list(node_ids), [RDFS.label], object_is_literal=True):
            nodes[s] = obograph.Node(id=s, label=o)
        logging.info(f'NUM EDGES: {len(edges)}')
        return obograph.Graph(id='query',
                              nodes=list(nodes.values()), edges=edges)

    def ancestors(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        # TODO: DRY
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [f'?s ?p ?o',
                 f'?o a owl:Class',
                 #f'?p a owl:ObjectProperty',
                 f'VALUES ?s {{ {" ".join(query_uris)} }}']
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        query = SparqlQuery(select=['?o'],
                            distinct=True,
                            where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row['o']['value'])

    def descendants(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        # TODO: DRY
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [f'?s ?p ?o',
                 f'?s a owl:Class',
                 f'VALUES ?o {{ {" ".join(query_uris)} }}']
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        query = SparqlQuery(select=['?s'],
                            distinct=True,
                            where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row['s']['value'])

    def gap_fill_relationships(self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None) -> Iterator[RELATIONSHIP]:
        # TODO: compare with https://api.triplydb.com/s/_mZ9q_-rg
        query_uris = [self.curie_to_sparql(curie) for curie in seed_curies]
        where = [f'?s ?p ?o',
                 _sparql_values('s', query_uris),
                 _sparql_values('o', query_uris)]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values('p', pred_uris))
        query = SparqlQuery(select=['?s ?p ?o'],
                            where=where)
        bindings = self._query(query.query_str())
        # TODO: remove redundancy
        rels = []
        for row in bindings:
            rels.append( (self.uri_to_curie(row['s']['value']),
                          self.uri_to_curie(row['p']['value']),
                          self.uri_to_curie(row['o']['value'])))
        for rel in transitive_reduction_by_predicate(rels):
            yield rel




