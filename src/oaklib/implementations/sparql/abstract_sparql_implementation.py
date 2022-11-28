import logging
import typing
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import kgcl_rdflib.apply.graph_transformer as kgcl_patcher
import rdflib
import SPARQLWrapper
from kgcl_schema.datamodel import kgcl
from rdflib import RDFS, BNode, Literal, URIRef
from rdflib.term import Identifier
from SPARQLWrapper import JSON
from sssom_schema import Mapping

from oaklib.datamodels import obograph
from oaklib.datamodels.search import (
    SearchConfiguration,
    search_properties_to_predicates,
)
from oaklib.datamodels.search_datamodel import SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    ALL_MATCH_PREDICATES,
    DEFAULT_PREFIX_MAP,
    HAS_DEFINITION_URI,
    IDENTIFIER_PREDICATE,
    IS_A,
    IS_DEFINED_BY,
    LABEL_PREDICATE,
    OBO_PURL,
    RDF_TYPE,
    SEMAPV,
    SYNONYM_PREDICATES,
)
from oaklib.implementations.sparql import SEARCH_CONFIG
from oaklib.implementations.sparql.sparql_query import SparqlQuery, SparqlUpdate
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    METADATA_MAP,
    PRED_CURIE,
    PREFIX_MAP,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
)
from oaklib.interfaces.rdf_interface import TRIPLE, RdfInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, URI
from oaklib.utilities.basic_utils import pairs_as_dict
from oaklib.utilities.mapping.sssom_utils import create_sssom_mapping
from oaklib.utilities.rate_limiter import check_limit

VAL_VAR = "v"


def _sparql_values(var_name: str, vals: List[str]):
    if vals is None:
        return None
    return f'VALUES ?{var_name} {{ {" ".join(vals)} }}'


def _stringify(v: str, as_string_literal: bool = False) -> str:
    """
    Quotes a string for SPARQL queries, escaping internal quotes

    Optionally will cast into an xsd:string - note that SPARQL draws a distinction
    between "foo" and "foo"^^xsd:string, and with no consensus on how to store
    simple strings, it is often necessary to query for both

    :param v: unescaped input string
    :param as_string_literal: if true then yield "foo"^^xsd:string
    :return: escaped string
    """
    v = v.replace('"', '\\"')
    v = f'"{v}"'
    if as_string_literal:
        v = f"{v}^^xsd:string"
    return v


def _as_rdf_obj(v) -> URIRef:
    val = v["value"]
    if v["type"] == "uri":
        return URIRef(val)
    elif v["type"] == "bnode":
        return BNode(val)
    else:
        return Literal(val, lang=v.get("lang", None), datatype=v.get("datatype", None))


def _quote_uri(uri: str) -> str:
    return f"<{uri}>"


@dataclass
class AbstractSparqlImplementation(RdfInterface, ABC):
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
    _list_of_named_graphs: List[str] = None

    def __post_init__(self):
        if self.sparql_wrapper is None:
            resource = self.resource
            if resource is None:
                resource = OntologyResource()
            if resource.url is None:
                resource.url = self._default_url()
            if resource.format is None:
                resource.format = "turtle"
            if resource.local:
                self.graph = rdflib.Graph()
                self.graph.parse(resource.local_path, format=resource.format)
            else:
                self.sparql_wrapper = SPARQLWrapper.SPARQLWrapper(resource.url)

    def _curie_dict_to_values(self, key_var: str, val_var: str, d: Dict[CURIE, CURIE]):
        d = {self.curie_to_sparql(k): self.curie_to_sparql(v) for k, v in d.items()}
        return self._tuples_to_values((key_var, val_var), d.items())

    def _tuples_to_values(self, var_names: Tuple, tuples: List[Tuple]):
        def t2s(t):
            return f'({" ".join(t)})'

        var_tuple = [f"?{n}" for n in var_names]
        vals = [f"{t2s(t)}" for t in tuples]
        return f'VALUES {t2s(var_tuple)} {{ {" ".join(vals)} }}'

    @property
    def named_graph(self) -> Optional[str]:
        return None

    def _default_url(self) -> str:
        raise NotImplementedError

    def _is_blazegraph(self) -> bool:
        return False

    # def store(self, resource: OntologyResource) -> None:
    #    SparqlBasicImpl.dump(self.engine, resource)

    def _label_uri(self):
        return (
            self.ontology_metamodel_mapper.label_uri()
            if self.ontology_metamodel_mapper
            else RDFS.label
        )

    def _mapping_predicates(self):
        preds = ALL_MATCH_PREDICATES
        omm = self.ontology_metamodel_mapper
        if omm:
            return [omm.map_curie(pred, unmapped_reflexive=True) for pred in preds]
        else:
            return preds

    def _definition_uri(self):
        return (
            self.ontology_metamodel_mapper.definition_uri()
            if self.ontology_metamodel_mapper
            else HAS_DEFINITION_URI
        )

    def curie_to_uri(self, curie: CURIE, strict: bool = False) -> URI:
        if curie.startswith("http"):
            return curie
        # FIXME replace with super() call
        pm = self.prefix_map()
        if ":" in curie:
            toks = curie.split(":")
            if len(toks) > 2:
                logging.warning(f"CURIE should not contain double colons: {toks}")
                pfx = toks[0]
                local_id = "_".join(toks[1:])
            else:
                pfx, local_id = toks
            if pfx in pm:
                return f"{pm[pfx]}{local_id}"
            else:
                return f"http://purl.obolibrary.org/obo/{pfx}_{local_id}"
        else:
            logging.warning(f"Not a curie: {curie}")
            return curie

    def curie_to_sparql(self, curie: CURIE, strict: bool = False) -> URI:
        if curie.startswith("<"):
            return curie
        return f"<{self.curie_to_uri(curie, strict=strict)}>"

    def uri_to_curie(self, uri: URI, strict=True) -> Optional[CURIE]:
        # TODO: do not hardcode OBO
        pm = self.prefix_map()
        for k, v in pm.items():
            if uri.startswith(v):
                return uri.replace(v, f"{k}:")
        if uri.startswith(OBO_PURL):
            uri = uri.replace(OBO_PURL, "")
            return uri.replace("_", ":")
        return uri

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        query = SparqlQuery(select=["?s"], distinct=True, where=["?s a ?cls", "FILTER (isIRI(?s))"])
        if owl_type:
            query.where.append(f"?s a {self.curie_to_sparql(owl_type)}")
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    def obsoletes(self) -> Iterable[CURIE]:
        query = SparqlQuery(select=["?s"], distinct=True, where=["?s owl:deprecated true"])
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        mapping_preds = self._mapping_predicates()
        uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=["?p ?o"], distinct=True, where=[f"{uri} ?p ?o"])
        query.add_values("p", [self.curie_to_sparql(p) for p in mapping_preds])
        bindings = self._query(query.query_str())
        for row in bindings:
            yield (self.uri_to_curie(row["p"]["value"]), self.uri_to_curie(row["o"]["value"]))

    def ontologies(self) -> Iterable[CURIE]:
        query = SparqlQuery(select=["?s"], where=["?s rdf:type owl:Ontology"])
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    def list_of_named_graphs(self) -> List[URI]:
        if self._list_of_named_graphs:
            return self._list_of_named_graphs
        query = "select DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o }}"
        sw = self.sparql_wrapper
        sw.setQuery(query)
        sw.setReturnFormat(JSON)
        check_limit()
        ret = sw.queryAndConvert()
        logging.debug(f"RET={ret}")
        self._list_of_named_graphs = [row["g"]["value"] for row in ret["results"]["bindings"]]
        return self._list_of_named_graphs

    def _query(self, query: Union[str, SparqlQuery], prefixes: PREFIX_MAP = None):
        if prefixes is None:
            prefixes = DEFAULT_PREFIX_MAP
        ng = self.named_graph
        if isinstance(query, SparqlQuery) and ng:
            if query.graph is not None:
                if isinstance(query.graph, list):
                    query.graph.append(ng)
                else:
                    query.graph = [query.graph, ng]
            else:
                query.graph = ng
        if isinstance(query, SparqlQuery):
            query = query.query_str()
        sw = self.sparql_wrapper
        for k, v in prefixes.items():
            query = f"PREFIX {k}: <{v}>\n" + query
        if self.graph:
            rows = []

            def tr(v: Identifier):
                val = str(v)
                dt = None
                t = None
                if isinstance(v, BNode):
                    t = "bnode"
                elif isinstance(v, Literal):
                    t = "typed-literal"
                    dt = v.datatype
                else:
                    t = "uri"
                return dict(value=val, datatype=dt, type=t)

            logging.debug(f"Query={query}")
            for row in self.graph.query(query):
                rows.append({k: tr(row[k]) for k in row.labels})
            return rows
        else:
            logging.info(f"QUERY={query} // sw={sw}")
            sw.setQuery(query)
            sw.setReturnFormat(JSON)
            check_limit()
            ret = sw.queryAndConvert()
            logging.debug(f"queryResults={ret}")
            return ret["results"]["bindings"]

    def _triples(
        self,
        subject: CURIE = None,
        predicate: PRED_CURIE = None,
        object: PRED_CURIE = None,
        graph: CURIE = None,
    ) -> Iterable[Tuple]:
        vars = []

        def _urify_arg(arg: CURIE, name: str):
            if arg is None:
                vars.append(name)
                return f"?{name}"
            else:
                return f"<{self.curie_to_uri(arg)}>"

        subject_uri = _urify_arg(subject, "s")
        predicate_uri = _urify_arg(predicate, "p")
        object_uri = _urify_arg(object, "o")
        if graph is None:
            # do not include graph in select
            graph_uri = "?g"
        else:
            graph_uri = _urify_arg(graph, "g")
        vars_str = " ".join([f"?{v}" for v in vars])
        bindings = self._query(
            f"SELECT DISTINCT {vars_str} WHERE {{ GRAPH {graph_uri} {{ {subject_uri} {predicate_uri} {object_uri} }}}}"
        )
        for row in bindings:
            yield tuple([row[v]["value"] for v in vars])

    def hierararchical_parents(self, curie: CURIE, isa_only: bool = False) -> List[CURIE]:
        uri = self.curie_to_uri(curie)
        is_a_pred = (
            self.ontology_metamodel_mapper.is_a_uri()
            if self.ontology_metamodel_mapper
            else RDFS.subClassOf
        )
        query = SparqlQuery(
            select=["?o"], where=[f"<{uri}> <{is_a_pred}> ?o", "FILTER (isIRI(?o))"]
        )
        bindings = self._query(query)
        return list(set([self.uri_to_curie(row["o"]["value"]) for row in bindings]))

    def get_hierararchical_children_by_curie(
        self, curie: CURIE, isa_only: bool = False
    ) -> List[CURIE]:
        uri = self.curie_to_uri(curie)
        query = SparqlQuery(
            select=["?s"], where=[f"?s <{RDFS.subClassOf}> <{uri}>", "FILTER (isIRI(?s))"]
        )
        bindings = self._query(query)
        return list(set([self.uri_to_curie(row["s"]["value"]) for row in bindings]))

    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        if predicates:
            predicates = list(set(predicates))
        pred_quris = [self.curie_to_sparql(p) for p in predicates] if predicates else None
        if self.ontology_metamodel_mapper and pred_quris is not None:
            pred_quris = [self.ontology_metamodel_mapper.direct_map_uri(p) for p in pred_quris]
        uri = self.curie_to_uri(curie)
        is_a_pred = (
            self.ontology_metamodel_mapper.is_a_curie() if self.ontology_metamodel_mapper else IS_A
        )
        if not predicates or is_a_pred in predicates:
            # all simple is-a relationships
            for p in self.hierararchical_parents(curie):
                yield IS_A, p
        if not predicates or predicates != [is_a_pred]:
            # subclassof existential restrictions
            query = SparqlQuery(
                select=["?p", "?o"],
                where=[
                    f"<{uri}> <{RDFS.subClassOf}> [owl:onProperty ?p ; owl:someValuesFrom ?o]",
                    "FILTER (isIRI(?o))",
                ],
            )
            query.add_values("p", pred_quris)
            bindings = self._query(query)
            for row in bindings:
                pred = self.uri_to_curie(row["p"]["value"])
                obj = self.uri_to_curie(row["o"]["value"])
                yield pred, obj
            # direct triples where the predicate is an ObjectProperty
            query = SparqlQuery(
                select=["?p", "?o"],
                where=[
                    f"<{uri}> ?p ?o",
                    "?p rdf:type owl:ObjectProperty",
                ],
            )
            query.add_values("p", pred_quris)
            bindings = self._query(query)
            for row in bindings:
                pred = self.uri_to_curie(row["p"]["value"])
                obj = self.uri_to_curie(row["o"]["value"])
                yield pred, obj
            # simple RDF type triples
            if not predicates or RDF_TYPE in predicates:
                query = SparqlQuery(
                    select=["?o"],
                    where=[
                        f"<{uri}> rdf:type ?o",
                        "?o a owl:Class",
                    ],
                )
                bindings = self._query(query)
                for row in bindings:
                    obj = self.uri_to_curie(row["o"]["value"])
                    yield RDF_TYPE, obj

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        """
        Returns all matching relationships

        :param subjects: constrain search to these subjects (i.e outgoing edges)
        :param predicates: constrain search to these predicates
        :param objects: constrain search to these objects (i.e incoming edges)
        :param include_tbox: if true, include class-class relationships (default True)
        :param include_abox: if true, include instance-instance/class relationships (default True)
        :param include_entailed:
        :return:
        """
        if not subjects:
            subjects = list(self.entities())
        logging.info(f"Subjects: {len(subjects)}")
        for subject in subjects:
            for this_predicate, this_objects in self.outgoing_relationship_map(subject).items():
                if predicates and this_predicate not in predicates:
                    continue
                for this_object in this_objects:
                    if objects and this_object not in objects:
                        continue
                    yield subject, this_predicate, this_object

    def outgoing_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.outgoing_relationships(*args, **kwargs))

    def incoming_relationship_map(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        uri = self.curie_to_uri(curie)
        rels = defaultdict(list)
        logging.info(f"Getting incoming for: {curie}")
        rels[IS_A] = self.get_hierararchical_children_by_curie(curie)
        query = SparqlQuery(
            select=["?s", "?p"],
            where=[
                f"?s <{RDFS.subClassOf}> [owl:onProperty ?p ; owl:someValuesFrom <{uri}>]",
                "FILTER (isIRI(?s))",
            ],
        )
        bindings = self._query(query)
        for row in bindings:
            pred = self.uri_to_curie(row["p"]["value"])
            subj = self.uri_to_curie(row["s"]["value"])
            if subj not in rels[pred]:
                rels[pred].append(subj)
        logging.info(f"Incoming for: {curie} => {rels}")
        return rels

    def _get_anns(self, curie: CURIE, pred: Union[URIRef, CURIE]):
        uri = self.curie_to_sparql(curie)
        pred = self.curie_to_sparql(pred)
        query = SparqlQuery(select=["?v"], where=[f"{uri} {pred} ?v"])
        if self.multilingual:
            query.where.append(f'FILTER (LANG(?v) = "{self.preferred_language}")')
        bindings = self._query(query)
        return list(set([row[VAL_VAR]["value"] for row in bindings]))

    def label(self, curie: CURIE):
        labels = list(self.labels([curie]))
        if labels:
            if len(labels) > 1:
                logging.warning(f"Multiple labels for {curie} = {labels}")
            return labels[0][1]
        else:
            return None

    def labels(self, curies: Iterable[CURIE], allow_none=True) -> Iterable[Tuple[CURIE, str]]:
        label_uri = self._label_uri()
        uris = [self.curie_to_sparql(x) for x in curies]
        query = SparqlQuery(
            select=["?s ?label"], where=[f"?s <{label_uri}> ?label", _sparql_values("s", uris)]
        )
        if self.multilingual:
            query.where.append(f'FILTER (LANG(?label) = "{self.preferred_language}")')
        bindings = self._query(query)
        label_map = {}
        for row in bindings:
            curie, label = self.uri_to_curie(row["s"]["value"]), row["label"]["value"]
            if curie in label_map:
                if label_map[curie] != label:
                    logging.warning(f"Multiple labels for {curie} = {label_map[curie]} != {label}")
            else:
                label_map[curie] = label
                yield curie, label
        if allow_none:
            for curie in curies:
                if curie not in label_map:
                    yield curie, None

    def defined_bys(self, entities: Iterable[CURIE]) -> Iterable[str]:
        entities = list(entities)
        uris = [self.curie_to_sparql(x) for x in entities]
        query = SparqlQuery(
            select=["?s ?o"], where=[f"?s {IS_DEFINED_BY} ?o", _sparql_values("s", uris)]
        )
        bindings = self._query(query)
        for row in bindings:
            curie, db = self.uri_to_curie(row["s"]["value"]), row["o"]["value"]
            yield curie, db
            entities.remove(curie)
        return super().defined_bys(entities)

    def _alias_predicates(self) -> List[PRED_CURIE]:
        # different implementations can override this; e.g Wikidata uses skos:altLabel
        return SYNONYM_PREDICATES

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        uri = self.curie_to_sparql(curie)
        label_uri = self._label_uri()
        alias_pred_uris = [
            self.curie_to_sparql(p) for p in self._alias_predicates() + [_quote_uri(label_uri)]
        ]
        query = SparqlQuery(
            select=["?p", "?o"], where=[f"{uri} ?p ?o", _sparql_values("p", alias_pred_uris)]
        )
        if self.multilingual:
            query.where.append(f'FILTER (LANG(?o) = "{self.preferred_language}")')
        logging.info(f"{query.query_str()}")
        bindings = self._query(
            query.query_str(), {"oboInOwl": "http://www.geneontology.org/formats/oboInOwl#"}
        )
        m = defaultdict(list)
        for row in bindings:
            m[self.uri_to_curie(row["p"]["value"])].append(row["o"]["value"])
        return m

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=["?p", "?o"], where=[f"{uri} ?p ?o"])
        bindings = self._query(
            query.query_str(), {"oboInOwl": "http://www.geneontology.org/formats/oboInOwl#"}
        )
        m = defaultdict(list)
        for row in bindings:
            m[self.uri_to_curie(row["p"]["value"])].append(row["o"]["value"])
        self.add_missing_property_values(curie, m)
        return dict(m)

    def curies_by_label(self, label: str) -> List[CURIE]:
        label_uri = self._label_uri()
        # Note there are multiple ways to store a label in RDF:
        #  - plain literal
        #  - xsd:string
        #  - with language tag
        clauses = [f'?s rdfs:label "{label}"', f'?s <{label_uri}> "{label}"^^xsd:string']
        if self.multilingual:
            clauses.append(f'?s rdfs:label "{label}"@{self.preferred_language}')
        clauses_j = " UNION ".join([f"{{ {c} }}" for c in clauses])
        query = SparqlQuery(select=["?s"], where=[f"{{ {clauses_j} }}"])
        logging.info(f"Query = {query.query_str()}")
        bindings = self._query(query)
        return [self.uri_to_curie(row["s"]["value"]) for row in bindings]

    def create_entity(
        self, curie: CURIE, label: str = None, relationships: RELATIONSHIP_MAP = None
    ) -> CURIE:
        raise NotImplementedError

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE):
        raise NotImplementedError

    def definition(self, curie: CURIE) -> Optional[str]:
        # TODO: allow this to be configured to use different predicates
        defn_uri = self._definition_uri()
        labels = self._get_anns(curie, defn_uri)
        if labels:
            if len(labels) > 1:
                logging.error(f"Multiple labels for {curie} = {labels}")
            return labels[0]
        else:
            return None

    def dump(self, path: str = None, syntax: str = "turtle"):
        if self.named_graph is None and not self.graph:
            raise ValueError("Must specify a named graph to dump for a remote triplestore")
        query = SparqlQuery(select=["?s", "?p", "?o"], where=["?s ?p ?o"])
        bindings = self._query(query)
        g = rdflib.Graph()

        bnodes = {}

        def tr(v: dict):
            vv = v["value"]
            if v["type"] == "bnode":
                if vv not in bnodes:
                    bnodes[vv] = BNode()
                return bnodes[vv]
            elif v["type"] == "uri":
                return URIRef(vv)
            else:
                return Literal(vv)

        for row in bindings:
            triple = (tr(row["s"]), tr(row["p"]), tr(row["o"]))
            g.add(triple)
        g.serialize(path, format=syntax)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(
        self, search_term: str, config: SearchConfiguration = SEARCH_CONFIG
    ) -> Iterable[CURIE]:
        if ":" in search_term and " " not in search_term:
            # logging.error(f"Not performing search on what looks like a CURIE: {search_term}")
            # return
            search_term = self.curie_to_uri(search_term)

        if self._is_blazegraph():
            filter_clause = f'?v bds:search "{search_term}"'
        else:
            if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
                filter_clause = f'strStarts(str(?v), "{search_term}")'
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
                filter_clause = f'regex(str(?v), "{search_term}", "i")'
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.LUCENE):
                raise NotImplementedError("Lucene not implemented")
            elif config.is_partial:
                filter_clause = f'contains(str(?v), "{search_term}")'
            else:
                filter_clause = f'str(?v) = "{search_term}"'
            filter_clause = f"FILTER({filter_clause})"
        if config.properties:
            preds = search_properties_to_predicates(config.properties)
        else:
            preds = [LABEL_PREDICATE]
        if self.ontology_metamodel_mapper:
            preds = [
                self.ontology_metamodel_mapper.map_curie(pred, unmapped_reflexive=True)[0]
                for pred in preds
            ]
        if preds == [IDENTIFIER_PREDICATE]:
            where = ["?v a ?s_cls", "BIND(?v AS ?s)"]
            query = SparqlQuery(select=["?s"], where=where + [filter_clause])
        else:
            non_id_preds = [pred for pred in preds if pred != IDENTIFIER_PREDICATE]
            non_id_preds = [self.curie_to_sparql(p) for p in non_id_preds]
            if len(non_id_preds) == 1:
                where = [f"?s {preds[0]} ?v "]
            elif len(non_id_preds) == 1:
                raise ValueError("Logic error; this should be handled by above clause")
            else:
                where = ["?s ?p ?v ", f'VALUES ?p {{ {" ".join(non_id_preds)} }}']
            if IDENTIFIER_PREDICATE in preds:
                raise NotImplementedError(
                    f"Cannot mix identifier and non-identifier preds: {preds}"
                )
            query = SparqlQuery(select=["?s"], where=where + [filter_clause])
        logging.info(f"Search query: {query.query_str()}")
        bindings = self._query(query, prefixes=DEFAULT_PREFIX_MAP)
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])
        # if SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
        #    raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE) -> obograph.Node:
        params = dict(id=curie, lbl=self.label(curie))
        return obograph.Node(**params)

    def hierarchical_descendants(self, start_curies: Union[CURIE, List[CURIE]]) -> Iterable[CURIE]:
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = ["?s rdfs:subClassOf* ?o", _sparql_values("o", query_uris)]
        query = SparqlQuery(select=["?s"], distinct=True, where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingProviderInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        pred_uris = [self.curie_to_sparql(pred) for pred in self._mapping_predicates()]
        # input curie is subject
        query = SparqlQuery(
            select=["?p", "?o"],
            where=[f"{self.curie_to_sparql(curie)} ?p ?o", _sparql_values("p", pred_uris)],
        )
        bindings = self._query(query)
        for row in bindings:
            m = create_sssom_mapping(
                subject_id=curie,
                predicate_id=self.uri_to_curie(row["p"]["value"]),
                object_id=self.uri_to_curie(row["o"]["value"]),
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            if m is not None:
                yield m
        # input curie is object
        query = SparqlQuery(
            select=["?s", "?p"],
            where=[
                "?s ?p ?o",
                _sparql_values(
                    "o",
                    [
                        _stringify(curie),
                        _stringify(curie, as_string_literal=True),
                        self.curie_to_sparql(curie),
                    ],
                ),
                _sparql_values("p", pred_uris),
            ],
        )
        bindings = self._query(query)
        for row in bindings:
            m = create_sssom_mapping(
                subject_id=self.uri_to_curie(row["s"]["value"]),
                predicate_id=self.uri_to_curie(row["p"]["value"]),
                object_id=curie,
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            if m is not None:
                yield m

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RdfInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def extract_triples(
        self,
        seed_curies: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        strategy=None,
        map_to_curies=True,
    ) -> Iterator[TRIPLE]:
        seed_uris = [self.curie_to_sparql(c) for c in seed_curies]
        # Note that some triplestores will have performance issues with this query
        traverse_preds = [
            "rdfs:subClassOf",
            "owl:onProperty",
            "owl:someValuesFrom",
            "owl:annotatedSource",
            "owl:equivalentClass",
        ]
        if predicates:
            # note that predicates are only used in the ABox - for a RelationGraph-implementing
            # triplestore this will also include TBox existentials
            traverse_preds = list(set(traverse_preds + predicates))
        query = SparqlQuery(
            select=["?s", "?p", "?o"],
            where=[
                "?s ?p ?o ." f'?seed ({"|".join(traverse_preds)})* ?s',
                _sparql_values("seed", seed_uris),
            ],
        )
        bindings = self._query(query)
        n = 0
        for row in bindings:
            n += 1
            triple = (row["s"], row["p"], row["o"])
            if map_to_curies:
                yield tuple([self.uri_to_curie(v["value"]) for v in list(triple)])
            else:
                yield tuple([_as_rdf_obj(v) for v in list(triple)])
        logging.info(f"Total triples: {n}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _sparql_update(self, query: SparqlUpdate, prefixes: PREFIX_MAP = None):
        if prefixes is None:
            prefixes = {}
        ng = self.named_graph
        if ng:
            if query.graph is not None:
                if isinstance(query.graph, list):
                    query.graph.append(ng)
                else:
                    query.graph = [query.graph, ng]
            else:
                query.graph = ng
        query = query.query_str()
        sw = self.sparql_wrapper
        for k, v in prefixes.items():
            query = f"PREFIX {k}: <{v}>\n" + query
        if self.graph:
            self.graph.update(query)
        else:
            logging.info(f"QUERY={query} // sw={sw}")
            sw.setQuery(query)
            sw.setReturnFormat(JSON)
            check_limit()
            ret = sw.query()
            logging.info(f"RET={ret}")

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        q = SparqlUpdate(
            delete=["?s ?p ?o"],
            insert=["?s_new ?p ?o"],
            where=["?s ?p ?o", self._curie_dict_to_values("s", "s_new", curie_map)],
        )
        self._sparql_update(q)
        q = SparqlUpdate(
            delete=["?s ?p ?o"],
            insert=["?s ?p ?o_new"],
            where=["?s ?p ?o", self._curie_dict_to_values("o", "o_new", curie_map)],
        )
        self._sparql_update(q)
        q = SparqlUpdate(
            delete=["?s ?p ?o"],
            insert=["?s ?p_new ?o"],
            where=["?s ?p ?o", self._curie_dict_to_values("p", "p_new", curie_map)],
        )
        self._sparql_update(q)

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: typing.Mapping[PRED_CURIE, Any] = None,
    ) -> Optional[kgcl.Change]:
        if self.graph:
            logging.info(f"Applying: {patch} to {self.graph}")
            kgcl_patcher.apply_patch([patch], self.graph)
            return patch
        else:
            raise NotImplementedError("Apply patch is only implemented for local graphs")

    def save(self):
        if self.graph:
            if self.resource.format:
                format = self.resource.format
            else:
                format = "turtle"
            self.graph.serialize(destination=self.resource.local_path, format=format)
        else:
            logging.debug("Save has no effect on remote triplestore")
