import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Iterable, Tuple, Optional

import SPARQLWrapper
import rdflib
from SPARQLWrapper import JSON
from obolib.implementations.sparql.sparql_query import SparqlQuery
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    PREFIX_MAP
from obolib.resource import OntologyResource
from obolib.types import CURIE, URI
from obolib.vocabulary.vocabulary import IS_A, HAS_DEFINITION_URI
from rdflib import URIRef, RDFS

VAL_VAR = 'v'


@dataclass
class SparqlImplementation(BasicOntologyInterface):
    """
    An OntologyInterface implementation that wraps a (typically remote) SPARQL endpoint.

    Note: Each sparql endpoint typically implements its own bespoke transformations, leading
    to lack of interoperability. For some purposes it may be better to use a more specific
    implementation:

    - :class:`.OntobeeImplementation`
    - :class:`.UbergraphImplementation`
    """
    sparql_wrapper: SPARQLWrapper = None
    graph: rdflib.Graph = None

    def __post_init__(self):
        if self.sparql_wrapper is None:
            resource = self.resource
            if resource is None:
                resource = OntologyResource(url=self._default_url())
            if resource.local:
                self.graph = rdflib.Graph()
                self.graph.parse(resource.local_path)
            else:
                self.sparql_wrapper = SPARQLWrapper.SPARQLWrapper(resource.url)

    def _default_url(self) -> str:
        raise NotImplementedError


    def get_prefix_map(self) -> PREFIX_MAP:
        # TODO
        return {'rdfs': str(RDFS)}

    #def store(self, resource: OntologyResource) -> None:
    #    SparqlBasicImpl.dump(self.engine, resource)

    def curie_to_uri(self, curie: CURIE, strict: bool = False) -> URI:
        if curie.startswith('http'):
            return curie
        pm = self.get_prefix_map()
        pfx, local_id = curie.split(':')
        if pfx in pm:
            return f'{pm[pfx]}{local_id}'
        else:
            return f'http://purl.obolibrary.org/obo/{pfx}_{local_id}'

    def uri_to_curie(self, uri: URI, strict=True) -> Optional[CURIE]:
        # TODO: do not hardcode OBO
        pm = self.get_prefix_map()
        for k, v in pm.items():
            if uri.startswith(v):
                return uri.replace(v, f'{k}:')
        if uri.startswith('http://purl.obolibrary.org/obo/'):
            uri = uri.replace('http://purl.obolibrary.org/obo/', "")
            return uri.replace('_', ':')
        return uri

    def _query(self, query: str, prefixes: PREFIX_MAP = {}):
        sw = self.sparql_wrapper
        for k, v in prefixes.items():
            query = f'PREFIX {k}: <{v}>\n' + query
        logging.info(f'QUERY={query}')
        sw.setQuery(query)
        sw.setReturnFormat(JSON)
        ret = sw.queryAndConvert()
        return ret["results"]["bindings"]

    def _triples(self, subject: CURIE = None, predicate: PRED_CURIE = None, object: PRED_CURIE = None, graph: CURIE = None) -> Iterable[Tuple]:
        vars = []
        def _urify_arg(arg: CURIE, name: str):
            if arg is None:
                vars.append(name)
                return f'?{name}'
            else:
                return f'<{self.curie_to_uri(arg)}>'
        subject_uri = _urify_arg(subject, 's')
        predicate_uri = _urify_arg(predicate, 'p')
        object_uri = _urify_arg(object, 'o')
        if graph is None:
            # do not include graph in select
            graph_uri = '?g'
        else:
            graph_uri = _urify_arg(graph, 'g')
        vars_str = ' '.join([f'?{v}' for v in vars])
        bindings = self._query(f"SELECT DISTINCT {vars_str} WHERE {{ GRAPH {graph_uri} {{ {subject_uri} {predicate_uri} {object_uri} }}}}")
        for row in bindings:
            yield tuple([row[v]['value'] for v in vars])

    def get_parents_by_curie(self, curie: CURIE, isa_only: bool = False) -> List[CURIE]:
        uri = self.curie_to_uri(curie)
        query = SparqlQuery(select=['?o'],
                            where=[f'<{uri}> <{RDFS.subClassOf}> ?o',
                                   'FILTER (isIRI(?o))'])
        bindings = self._query(query.query_str())
        return list(set([self.uri_to_curie(row['o']['value']) for row in bindings]))

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        uri = self.curie_to_uri(curie)
        rels = defaultdict(list)
        rels[IS_A] = self.get_parents_by_curie(curie)
        query = SparqlQuery(select=['?p', '?o'],
                            where=[f'<{uri}> <{RDFS.subClassOf}> [owl:onProperty ?p ; owl:someValuesFrom ?o]',
                                   'FILTER (isIRI(?o))'])
        bindings = self._query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row['p']['value'])
            obj = self.uri_to_curie(row['o']['value'])
            if obj not in rels[pred]:
                rels[pred].append(obj)
        return rels


    def _get_anns(self, curie: CURIE, pred: URIRef):
        uri = self.curie_to_uri(curie)
        bindings = self._query(f"SELECT ?{VAL_VAR} WHERE {{ <{uri}> <{pred}> ?v }}")
        return list(set([row[VAL_VAR]['value'] for row in bindings]))

    def get_label_by_curie(self, curie: CURIE):
        labels = self._get_anns(curie, RDFS.label)
        if labels:
            if len(labels) > 1:
                logging.error(f'Multiple labels for {curie} = {labels}')
            return labels[0]
        else:
            return None

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        uri = self.curie_to_uri(curie)
        valstr = "VALUES ?pred {oboInOwl:hasExactSynonym}"
        bindings = self._query(f"SELECT ?pred ?{VAL_VAR} WHERE {{ <{uri}> ?pred ?v . {valstr} }}",
                               {'oboInOwl': 'http://www.geneontology.org/formats/oboInOwl#'})
        m = defaultdict(list)
        for row in bindings:
            #print(f'BINDINGS={row}')
            m[row['pred']['value']].append(row[VAL_VAR]['value'])
        return m


    def get_curies_by_label(self, label: str) -> List[CURIE]:
        return [t.id for t in self.sparql_wrapper.terms()]


    def create_entity(self, curie: CURIE, label: str = None, relationships: RELATIONSHIP_MAP = None) -> CURIE:
        raise NotImplementedError

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE):
        raise NotImplementedError

    def get_definition_by_curie(self, curie: CURIE) -> str:
        """

        :param curie:
        :return:
        """
        labels = self._get_anns(curie, HAS_DEFINITION_URI)
        if labels:
            if len(labels) > 1:
                logging.error(f'Multiple labels for {curie} = {labels}')
            return labels[0]
        else:
            return None






