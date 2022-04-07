import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Iterable, Tuple, Optional

import SPARQLWrapper
import rdflib
from SPARQLWrapper import JSON
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    PREFIX_MAP
from oaklib.interfaces.search_interface import SearchConfiguration
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, URI
from oaklib.datamodels.vocabulary import IS_A, HAS_DEFINITION_URI, LABEL_PREDICATE, OBO_PURL
from oaklib.utilities.rate_limiter import check_limit
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

    def _is_blazegraph(self) -> bool:
        return False


    def get_prefix_map(self) -> PREFIX_MAP:
        # TODO
        return {'rdfs': str(RDFS)}

    #def store(self, resource: OntologyResource) -> None:
    #    SparqlBasicImpl.dump(self.engine, resource)

    def curie_to_uri(self, curie: CURIE, strict: bool = False) -> URI:
        if curie.startswith('http'):
            return curie
        pm = self.get_prefix_map()
        if ':' in curie:
            pfx, local_id = curie.split(':')
            if pfx in pm:
                return f'{pm[pfx]}{local_id}'
            else:
                return f'http://purl.obolibrary.org/obo/{pfx}_{local_id}'
        else:
            logging.warning(f'Not a curie: {curie}')
            return curie

    def curie_to_sparql(self, curie: CURIE, strict: bool = False) -> URI:
        return f'<{self.curie_to_uri(curie, strict=strict)}>'

    def uri_to_curie(self, uri: URI, strict=True) -> Optional[CURIE]:
        # TODO: do not hardcode OBO
        pm = self.get_prefix_map()
        for k, v in pm.items():
            if uri.startswith(v):
                return uri.replace(v, f'{k}:')
        if uri.startswith(OBO_PURL):
            uri = uri.replace(OBO_PURL, "")
            return uri.replace('_', ':')
        return uri

    def _query(self, query: str, prefixes: PREFIX_MAP = {}):
        sw = self.sparql_wrapper
        for k, v in prefixes.items():
            query = f'PREFIX {k}: <{v}>\n' + query
        logging.info(f'QUERY={query}')
        sw.setQuery(query)
        sw.setReturnFormat(JSON)
        check_limit()
        ret = sw.queryAndConvert()
        logging.info(f'RET={ret}')
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
                logging.warning(f'Multiple labels for {curie} = {labels}')
            return labels[0]
        else:
            return None

    def get_labels_for_curies(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        uri_map = {self.curie_to_uri(curie): curie for curie in curies}
        uris = [f'<{uri}>' for uri in uri_map.keys()]
        query = SparqlQuery(select=['?s ?label'],
                            where=[f'?s <{RDFS.label}> ?label',
                                   f'VALUES ?s {{ {" ".join(uris)} }}'])
        bindings = self._query(query.query_str())
        label_map = {}
        for row in bindings:
            curie, label = self.uri_to_curie(row['s']['value']), row['label']['value']
            if curie in label_map:
                if label_map[curie] != label:
                    logging.warning(f'Multiple labels for {curie} = {label_map[curie]} != {label}')
            else:
                yield curie, label
        for curie in curies:
            if curie not in label_map:
                yield curie, None

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
        query = SparqlQuery(select=['?s'],
                            where=[f'{{ {{ ?s rdfs:label "{label}" }} UNION {{ ?s rdfs:label "{label}"^^xsd:string }}  }}'])
        bindings = self._query(query.query_str())
        return [self.uri_to_curie(row['s']['value']) for row in bindings]


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

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        if ':' in search_term and ' ' not in search_term:
            logging.debug(f'Not performing search on what looks like a CURIE: {search_term}')
            return
        if self._is_blazegraph():
            filter_clause = f'?v bds:search "{search_term}"'
        else:
            if config.complete:
                filter_clause = f'?v = "{search_term}"'
            else:
                filter_clause = f'strStarts(str(?v), "{search_term}")'
            filter_clause = f'FILTER({filter_clause})'
        preds = [LABEL_PREDICATE]
        if len(preds) == 1:
            where = [f'?s {preds[0]} ?v ']
        else:
            where = [f'?s ?p ?v ',
                     f'VALUES ?p {{ {" ".join(preds)} }}']
        query = SparqlQuery(select=['?s'],
                            where=where + [filter_clause])
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row['s']['value'])






