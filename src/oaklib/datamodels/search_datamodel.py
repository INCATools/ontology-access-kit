# Auto generated from search_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-12-15T18:41:02
# Schema: search-datamodel
#
# id: https://w3id.org/linkml/search_datamodel
# description: A datamodel for representing a search configuration and results. This is intended to provide a
#              unified layer over both: - (a) how searches are *parameterized* - (b) the structure of search
#              *results*. The scope is any kind of service that provides search over *named entities*, including
#              ontology concepts. It is not intended to cover generic search results, e.g. google search, although
#              parts could be generalized for this purpose.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions,
)
from linkml_runtime.linkml_model.types import Boolean, Integer, String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    Bool,
    URIorCURIE,
    bnode,
    empty_dict,
    empty_list,
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str,
)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SEARCH = CurieNamespace("search", "https://w3id.org/linkml/search_datamodel/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
SSSOM = CurieNamespace("sssom", "http://w3id.org/sssom/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = SEARCH


# Types
class SearchTerm(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "SearchTerm"
    type_model_uri = SEARCH.SearchTerm


# Class references


@dataclass
class SearchBaseConfiguration(YAMLRoot):
    """
    A user-specified configuration that determines how a particular search operation works
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.SearchBaseConfiguration
    class_class_curie: ClassVar[str] = "search:SearchBaseConfiguration"
    class_name: ClassVar[str] = "SearchBaseConfiguration"
    class_model_uri: ClassVar[URIRef] = SEARCH.SearchBaseConfiguration

    search_terms: Optional[
        Union[Union[str, SearchTerm], List[Union[str, SearchTerm]]]
    ] = empty_list()
    syntax: Optional[Union[str, "SearchTermSyntax"]] = None
    properties: Optional[
        Union[Union[str, "SearchProperty"], List[Union[str, "SearchProperty"]]]
    ] = empty_list()
    limit: Optional[int] = None
    cursor: Optional[int] = None
    is_partial: Optional[Union[bool, Bool]] = None
    is_complete: Optional[Union[bool, Bool]] = None
    include_obsoletes_in_results: Optional[Union[bool, Bool]] = None
    is_fuzzy: Optional[Union[bool, Bool]] = None
    categories: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    force_case_insensitive: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.search_terms, list):
            self.search_terms = [self.search_terms] if self.search_terms is not None else []
        self.search_terms = [
            v if isinstance(v, SearchTerm) else SearchTerm(v) for v in self.search_terms
        ]

        if self.syntax is not None and not isinstance(self.syntax, SearchTermSyntax):
            self.syntax = SearchTermSyntax(self.syntax)

        if not isinstance(self.properties, list):
            self.properties = [self.properties] if self.properties is not None else []
        self.properties = [
            v if isinstance(v, SearchProperty) else SearchProperty(v) for v in self.properties
        ]

        if self.limit is not None and not isinstance(self.limit, int):
            self.limit = int(self.limit)

        if self.cursor is not None and not isinstance(self.cursor, int):
            self.cursor = int(self.cursor)

        if self.is_partial is not None and not isinstance(self.is_partial, Bool):
            self.is_partial = Bool(self.is_partial)

        if self.is_complete is not None and not isinstance(self.is_complete, Bool):
            self.is_complete = Bool(self.is_complete)

        if self.include_obsoletes_in_results is not None and not isinstance(
            self.include_obsoletes_in_results, Bool
        ):
            self.include_obsoletes_in_results = Bool(self.include_obsoletes_in_results)

        if self.is_fuzzy is not None and not isinstance(self.is_fuzzy, Bool):
            self.is_fuzzy = Bool(self.is_fuzzy)

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories
        ]

        if self.force_case_insensitive is not None and not isinstance(
            self.force_case_insensitive, Bool
        ):
            self.force_case_insensitive = Bool(self.force_case_insensitive)

        super().__post_init__(**kwargs)


@dataclass
class ComplexQuery(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.ComplexQuery
    class_class_curie: ClassVar[str] = "search:ComplexQuery"
    class_name: ClassVar[str] = "ComplexQuery"
    class_model_uri: ClassVar[URIRef] = SEARCH.ComplexQuery

    all_of: Optional[
        Union[Union[dict, "ComplexQuery"], List[Union[dict, "ComplexQuery"]]]
    ] = empty_list()
    any_of: Optional[
        Union[Union[dict, "ComplexQuery"], List[Union[dict, "ComplexQuery"]]]
    ] = empty_list()
    none_of: Optional[
        Union[Union[dict, "ComplexQuery"], List[Union[dict, "ComplexQuery"]]]
    ] = empty_list()
    path_to: Optional[str] = None
    atom: Optional[Union[dict, SearchBaseConfiguration]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.all_of, list):
            self.all_of = [self.all_of] if self.all_of is not None else []
        self.all_of = [
            v if isinstance(v, ComplexQuery) else ComplexQuery(**as_dict(v)) for v in self.all_of
        ]

        if not isinstance(self.any_of, list):
            self.any_of = [self.any_of] if self.any_of is not None else []
        self.any_of = [
            v if isinstance(v, ComplexQuery) else ComplexQuery(**as_dict(v)) for v in self.any_of
        ]

        if not isinstance(self.none_of, list):
            self.none_of = [self.none_of] if self.none_of is not None else []
        self.none_of = [
            v if isinstance(v, ComplexQuery) else ComplexQuery(**as_dict(v)) for v in self.none_of
        ]

        if self.path_to is not None and not isinstance(self.path_to, str):
            self.path_to = str(self.path_to)

        if self.atom is not None and not isinstance(self.atom, SearchBaseConfiguration):
            self.atom = SearchBaseConfiguration(**as_dict(self.atom))

        super().__post_init__(**kwargs)


@dataclass
class PathExpression(YAMLRoot):
    """
    A path query
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.PathExpression
    class_class_curie: ClassVar[str] = "search:PathExpression"
    class_name: ClassVar[str] = "PathExpression"
    class_model_uri: ClassVar[URIRef] = SEARCH.PathExpression

    traversal: Optional[Union[str, "GraphFunction"]] = None
    graph_predicates: Optional[
        Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]
    ] = empty_list()
    search_term: Optional[Union[dict, SearchBaseConfiguration]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.traversal is not None and not isinstance(self.traversal, GraphFunction):
            self.traversal = GraphFunction(self.traversal)

        if not isinstance(self.graph_predicates, list):
            self.graph_predicates = (
                [self.graph_predicates] if self.graph_predicates is not None else []
            )
        self.graph_predicates = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.graph_predicates
        ]

        if self.search_term is not None and not isinstance(
            self.search_term, SearchBaseConfiguration
        ):
            self.search_term = SearchBaseConfiguration(**as_dict(self.search_term))

        super().__post_init__(**kwargs)


@dataclass
class SearchResult(YAMLRoot):
    """
    An individual search result
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.SearchResult
    class_class_curie: ClassVar[str] = "search:SearchResult"
    class_name: ClassVar[str] = "SearchResult"
    class_model_uri: ClassVar[URIRef] = SEARCH.SearchResult

    object_id: str = None
    rank: Optional[int] = None
    object_label: Optional[str] = None
    object_source: Optional[str] = None
    object_source_version: Optional[str] = None
    object_match_field: Optional[str] = None
    matches_full_search_term: Optional[Union[bool, Bool]] = None
    snippet: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object_id):
            self.MissingRequiredField("object_id")
        if not isinstance(self.object_id, str):
            self.object_id = str(self.object_id)

        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.object_source is not None and not isinstance(self.object_source, str):
            self.object_source = str(self.object_source)

        if self.object_source_version is not None and not isinstance(
            self.object_source_version, str
        ):
            self.object_source_version = str(self.object_source_version)

        if self.object_match_field is not None and not isinstance(self.object_match_field, str):
            self.object_match_field = str(self.object_match_field)

        if self.matches_full_search_term is not None and not isinstance(
            self.matches_full_search_term, Bool
        ):
            self.matches_full_search_term = Bool(self.matches_full_search_term)

        if self.snippet is not None and not isinstance(self.snippet, str):
            self.snippet = str(self.snippet)

        super().__post_init__(**kwargs)


@dataclass
class SearchResultSet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.SearchResultSet
    class_class_curie: ClassVar[str] = "search:SearchResultSet"
    class_name: ClassVar[str] = "SearchResultSet"
    class_model_uri: ClassVar[URIRef] = SEARCH.SearchResultSet

    configuration: Optional[Union[dict, SearchBaseConfiguration]] = None
    results: Optional[
        Union[Union[dict, SearchResult], List[Union[dict, SearchResult]]]
    ] = empty_list()
    result_count: Optional[int] = None
    cursor: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.configuration is not None and not isinstance(
            self.configuration, SearchBaseConfiguration
        ):
            self.configuration = SearchBaseConfiguration(**as_dict(self.configuration))

        self._normalize_inlined_as_dict(
            slot_name="results", slot_type=SearchResult, key_name="object_id", keyed=False
        )

        if self.result_count is not None and not isinstance(self.result_count, int):
            self.result_count = int(self.result_count)

        if self.cursor is not None and not isinstance(self.cursor, int):
            self.cursor = int(self.cursor)

        super().__post_init__(**kwargs)


# Enumerations
class SearchTermSyntax(EnumDefinitionImpl):

    PLAINTEXT = PermissibleValue(
        text="PLAINTEXT", description="The search term is plain text with no special syntax"
    )
    REGULAR_EXPRESSION = PermissibleValue(
        text="REGULAR_EXPRESSION",
        description="The search term is a regular expression, ECMAscript style assumed",
    )
    SQL = PermissibleValue(
        text="SQL",
        description="The search term is SQL LIKE syntax, with percent symbols acting as wildcards",
    )
    LUCENE = PermissibleValue(text="LUCENE", description="The search term is in Lucene/Solr syntax")
    STARTS_WITH = PermissibleValue(
        text="STARTS_WITH",
        description="The search term is plain text but the matched field must start with the search term",
    )

    _defn = EnumDefinition(
        name="SearchTermSyntax",
    )


class SearchProperty(EnumDefinitionImpl):
    """
    A property that can be searched on
    """

    IDENTIFIER = PermissibleValue(
        text="IDENTIFIER",
        description="The identifier or URI of the entity",
        meaning=SCHEMA.identifier,
    )
    REPLACEMENT_IDENTIFIER = PermissibleValue(
        text="REPLACEMENT_IDENTIFIER",
        description="A replacement identifier or URI for the entity",
        meaning=SCHEMA.identifier,
    )
    MAPPED_IDENTIFIER = PermissibleValue(
        text="MAPPED_IDENTIFIER",
        description="An identifier or URI for a mapping",
        meaning=SKOS.closeMatch,
    )
    LABEL = PermissibleValue(
        text="LABEL",
        description="The preferred label / human readable name of the entity",
        meaning=RDFS.label,
    )
    ALIAS = PermissibleValue(
        text="ALIAS", description="An alias or synonym of the entity", meaning=SKOS.altLabel
    )
    COMMENT = PermissibleValue(
        text="COMMENT", description="A comment on the entity", meaning=RDFS.comment
    )
    DEFINITION = PermissibleValue(
        text="DEFINITION", description="The definition of the entity", meaning=SKOS.definition
    )
    INFORMATIVE_TEXT = PermissibleValue(
        text="INFORMATIVE_TEXT",
        description="Any informative text attached to the entity including comments, definitions, descriptions, examples",
    )
    ANYTHING = PermissibleValue(text="ANYTHING", meaning=RDF.Property)

    _defn = EnumDefinition(
        name="SearchProperty",
        description="A property that can be searched on",
    )


class BooleanOperator(EnumDefinitionImpl):

    AND = PermissibleValue(text="AND")
    OR = PermissibleValue(text="OR")
    NOT = PermissibleValue(text="NOT")
    XOR = PermissibleValue(text="XOR")

    _defn = EnumDefinition(
        name="BooleanOperator",
    )


class GraphFunction(EnumDefinitionImpl):

    DESCENDANT_OF = PermissibleValue(text="DESCENDANT_OF")
    ANCESTOR_OF = PermissibleValue(text="ANCESTOR_OF")
    PROPER_DESCENDANT_OF = PermissibleValue(text="PROPER_DESCENDANT_OF")
    PROPER_ANCESTOR_OF = PermissibleValue(text="PROPER_ANCESTOR_OF")
    PARENT_OF = PermissibleValue(text="PARENT_OF")
    CHILD_OF = PermissibleValue(text="CHILD_OF")

    _defn = EnumDefinition(
        name="GraphFunction",
    )


# Slots
class slots:
    pass


slots.searchBaseConfiguration__search_terms = Slot(
    uri=SEARCH.search_terms,
    name="searchBaseConfiguration__search_terms",
    curie=SEARCH.curie("search_terms"),
    model_uri=SEARCH.searchBaseConfiguration__search_terms,
    domain=None,
    range=Optional[Union[Union[str, SearchTerm], List[Union[str, SearchTerm]]]],
)

slots.searchBaseConfiguration__syntax = Slot(
    uri=SEARCH.syntax,
    name="searchBaseConfiguration__syntax",
    curie=SEARCH.curie("syntax"),
    model_uri=SEARCH.searchBaseConfiguration__syntax,
    domain=None,
    range=Optional[Union[str, "SearchTermSyntax"]],
)

slots.searchBaseConfiguration__properties = Slot(
    uri=SEARCH.properties,
    name="searchBaseConfiguration__properties",
    curie=SEARCH.curie("properties"),
    model_uri=SEARCH.searchBaseConfiguration__properties,
    domain=None,
    range=Optional[Union[Union[str, "SearchProperty"], List[Union[str, "SearchProperty"]]]],
)

slots.searchBaseConfiguration__limit = Slot(
    uri=SEARCH.limit,
    name="searchBaseConfiguration__limit",
    curie=SEARCH.curie("limit"),
    model_uri=SEARCH.searchBaseConfiguration__limit,
    domain=None,
    range=Optional[int],
)

slots.searchBaseConfiguration__cursor = Slot(
    uri=SEARCH.cursor,
    name="searchBaseConfiguration__cursor",
    curie=SEARCH.curie("cursor"),
    model_uri=SEARCH.searchBaseConfiguration__cursor,
    domain=None,
    range=Optional[int],
)

slots.searchBaseConfiguration__is_partial = Slot(
    uri=SEARCH.is_partial,
    name="searchBaseConfiguration__is_partial",
    curie=SEARCH.curie("is_partial"),
    model_uri=SEARCH.searchBaseConfiguration__is_partial,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.searchBaseConfiguration__is_complete = Slot(
    uri=SEARCH.is_complete,
    name="searchBaseConfiguration__is_complete",
    curie=SEARCH.curie("is_complete"),
    model_uri=SEARCH.searchBaseConfiguration__is_complete,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.searchBaseConfiguration__include_obsoletes_in_results = Slot(
    uri=SEARCH.include_obsoletes_in_results,
    name="searchBaseConfiguration__include_obsoletes_in_results",
    curie=SEARCH.curie("include_obsoletes_in_results"),
    model_uri=SEARCH.searchBaseConfiguration__include_obsoletes_in_results,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.searchBaseConfiguration__is_fuzzy = Slot(
    uri=SEARCH.is_fuzzy,
    name="searchBaseConfiguration__is_fuzzy",
    curie=SEARCH.curie("is_fuzzy"),
    model_uri=SEARCH.searchBaseConfiguration__is_fuzzy,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.searchBaseConfiguration__categories = Slot(
    uri=SEARCH.categories,
    name="searchBaseConfiguration__categories",
    curie=SEARCH.curie("categories"),
    model_uri=SEARCH.searchBaseConfiguration__categories,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.searchBaseConfiguration__force_case_insensitive = Slot(
    uri=SEARCH.force_case_insensitive,
    name="searchBaseConfiguration__force_case_insensitive",
    curie=SEARCH.curie("force_case_insensitive"),
    model_uri=SEARCH.searchBaseConfiguration__force_case_insensitive,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.complexQuery__all_of = Slot(
    uri=SEARCH.all_of,
    name="complexQuery__all_of",
    curie=SEARCH.curie("all_of"),
    model_uri=SEARCH.complexQuery__all_of,
    domain=None,
    range=Optional[Union[Union[dict, ComplexQuery], List[Union[dict, ComplexQuery]]]],
)

slots.complexQuery__any_of = Slot(
    uri=SEARCH.any_of,
    name="complexQuery__any_of",
    curie=SEARCH.curie("any_of"),
    model_uri=SEARCH.complexQuery__any_of,
    domain=None,
    range=Optional[Union[Union[dict, ComplexQuery], List[Union[dict, ComplexQuery]]]],
)

slots.complexQuery__none_of = Slot(
    uri=SEARCH.none_of,
    name="complexQuery__none_of",
    curie=SEARCH.curie("none_of"),
    model_uri=SEARCH.complexQuery__none_of,
    domain=None,
    range=Optional[Union[Union[dict, ComplexQuery], List[Union[dict, ComplexQuery]]]],
)

slots.complexQuery__path_to = Slot(
    uri=SEARCH.path_to,
    name="complexQuery__path_to",
    curie=SEARCH.curie("path_to"),
    model_uri=SEARCH.complexQuery__path_to,
    domain=None,
    range=Optional[str],
)

slots.complexQuery__atom = Slot(
    uri=SEARCH.atom,
    name="complexQuery__atom",
    curie=SEARCH.curie("atom"),
    model_uri=SEARCH.complexQuery__atom,
    domain=None,
    range=Optional[Union[dict, SearchBaseConfiguration]],
)

slots.pathExpression__traversal = Slot(
    uri=SEARCH.traversal,
    name="pathExpression__traversal",
    curie=SEARCH.curie("traversal"),
    model_uri=SEARCH.pathExpression__traversal,
    domain=None,
    range=Optional[Union[str, "GraphFunction"]],
)

slots.pathExpression__graph_predicates = Slot(
    uri=SEARCH.graph_predicates,
    name="pathExpression__graph_predicates",
    curie=SEARCH.curie("graph_predicates"),
    model_uri=SEARCH.pathExpression__graph_predicates,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.pathExpression__search_term = Slot(
    uri=SEARCH.search_term,
    name="pathExpression__search_term",
    curie=SEARCH.curie("search_term"),
    model_uri=SEARCH.pathExpression__search_term,
    domain=None,
    range=Optional[Union[dict, SearchBaseConfiguration]],
)

slots.searchResult__rank = Slot(
    uri=SEARCH.rank,
    name="searchResult__rank",
    curie=SEARCH.curie("rank"),
    model_uri=SEARCH.searchResult__rank,
    domain=None,
    range=Optional[int],
)

slots.searchResult__object_id = Slot(
    uri=SSSOM.object_id,
    name="searchResult__object_id",
    curie=SSSOM.curie("object_id"),
    model_uri=SEARCH.searchResult__object_id,
    domain=None,
    range=str,
)

slots.searchResult__object_label = Slot(
    uri=SSSOM.object_label,
    name="searchResult__object_label",
    curie=SSSOM.curie("object_label"),
    model_uri=SEARCH.searchResult__object_label,
    domain=None,
    range=Optional[str],
)

slots.searchResult__object_source = Slot(
    uri=SSSOM.object_source,
    name="searchResult__object_source",
    curie=SSSOM.curie("object_source"),
    model_uri=SEARCH.searchResult__object_source,
    domain=None,
    range=Optional[str],
)

slots.searchResult__object_source_version = Slot(
    uri=SSSOM.object_source_version,
    name="searchResult__object_source_version",
    curie=SSSOM.curie("object_source_version"),
    model_uri=SEARCH.searchResult__object_source_version,
    domain=None,
    range=Optional[str],
)

slots.searchResult__object_match_field = Slot(
    uri=SSSOM.object_match_field,
    name="searchResult__object_match_field",
    curie=SSSOM.curie("object_match_field"),
    model_uri=SEARCH.searchResult__object_match_field,
    domain=None,
    range=Optional[str],
)

slots.searchResult__matches_full_search_term = Slot(
    uri=SEARCH.matches_full_search_term,
    name="searchResult__matches_full_search_term",
    curie=SEARCH.curie("matches_full_search_term"),
    model_uri=SEARCH.searchResult__matches_full_search_term,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.searchResult__snippet = Slot(
    uri=SEARCH.snippet,
    name="searchResult__snippet",
    curie=SEARCH.curie("snippet"),
    model_uri=SEARCH.searchResult__snippet,
    domain=None,
    range=Optional[str],
)

slots.searchResultSet__configuration = Slot(
    uri=SEARCH.configuration,
    name="searchResultSet__configuration",
    curie=SEARCH.curie("configuration"),
    model_uri=SEARCH.searchResultSet__configuration,
    domain=None,
    range=Optional[Union[dict, SearchBaseConfiguration]],
)

slots.searchResultSet__results = Slot(
    uri=SEARCH.results,
    name="searchResultSet__results",
    curie=SEARCH.curie("results"),
    model_uri=SEARCH.searchResultSet__results,
    domain=None,
    range=Optional[Union[Union[dict, SearchResult], List[Union[dict, SearchResult]]]],
)

slots.searchResultSet__result_count = Slot(
    uri=SEARCH.result_count,
    name="searchResultSet__result_count",
    curie=SEARCH.curie("result_count"),
    model_uri=SEARCH.searchResultSet__result_count,
    domain=None,
    range=Optional[int],
)

slots.searchResultSet__cursor = Slot(
    uri=SEARCH.cursor,
    name="searchResultSet__cursor",
    curie=SEARCH.curie("cursor"),
    model_uri=SEARCH.searchResultSet__cursor,
    domain=None,
    range=Optional[int],
)
