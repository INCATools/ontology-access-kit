# Auto generated from search_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-27T15:59:06
# Schema: search-datamodel
#
# id: https://w3id.org/linkml/search_datamodel
# description: A datamodel for representing a search configuration and results
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SEARCH = CurieNamespace('search', 'https://w3id.org/linkml/search_datamodel/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SSSOM = CurieNamespace('sssom', 'http://w3id.org/sssom/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
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
    A configuration for search
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.SearchBaseConfiguration
    class_class_curie: ClassVar[str] = "search:SearchBaseConfiguration"
    class_name: ClassVar[str] = "SearchBaseConfiguration"
    class_model_uri: ClassVar[URIRef] = SEARCH.SearchBaseConfiguration

    search_terms: Optional[Union[Union[str, SearchTerm], List[Union[str, SearchTerm]]]] = empty_list()
    syntax: Optional[Union[str, "SearchTermSyntax"]] = None
    properties: Optional[Union[Union[str, "SearchProperty"], List[Union[str, "SearchProperty"]]]] = empty_list()
    limit: Optional[int] = None
    cursor: Optional[int] = None
    is_regular_expression: Optional[Union[bool, Bool]] = None
    is_partial: Optional[Union[bool, Bool]] = None
    is_complete: Optional[Union[bool, Bool]] = None
    include_id: Optional[Union[bool, Bool]] = None
    include_label: Optional[Union[bool, Bool]] = None
    include_aliases: Optional[Union[bool, Bool]] = None
    include_definition: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.search_terms, list):
            self.search_terms = [self.search_terms] if self.search_terms is not None else []
        self.search_terms = [v if isinstance(v, SearchTerm) else SearchTerm(v) for v in self.search_terms]

        if self.syntax is not None and not isinstance(self.syntax, SearchTermSyntax):
            self.syntax = SearchTermSyntax(self.syntax)

        if not isinstance(self.properties, list):
            self.properties = [self.properties] if self.properties is not None else []
        self.properties = [v if isinstance(v, SearchProperty) else SearchProperty(v) for v in self.properties]

        if self.limit is not None and not isinstance(self.limit, int):
            self.limit = int(self.limit)

        if self.cursor is not None and not isinstance(self.cursor, int):
            self.cursor = int(self.cursor)

        if self.is_regular_expression is not None and not isinstance(self.is_regular_expression, Bool):
            self.is_regular_expression = Bool(self.is_regular_expression)

        if self.is_partial is not None and not isinstance(self.is_partial, Bool):
            self.is_partial = Bool(self.is_partial)

        if self.is_complete is not None and not isinstance(self.is_complete, Bool):
            self.is_complete = Bool(self.is_complete)

        if self.include_id is not None and not isinstance(self.include_id, Bool):
            self.include_id = Bool(self.include_id)

        if self.include_label is not None and not isinstance(self.include_label, Bool):
            self.include_label = Bool(self.include_label)

        if self.include_aliases is not None and not isinstance(self.include_aliases, Bool):
            self.include_aliases = Bool(self.include_aliases)

        if self.include_definition is not None and not isinstance(self.include_definition, Bool):
            self.include_definition = Bool(self.include_definition)

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

    rank: Optional[int] = None
    object_id: Optional[str] = None
    object_label: Optional[str] = None
    object_source: Optional[str] = None
    matches_full_search_term: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.rank is not None and not isinstance(self.rank, int):
            self.rank = int(self.rank)

        if self.object_id is not None and not isinstance(self.object_id, str):
            self.object_id = str(self.object_id)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.object_source is not None and not isinstance(self.object_source, str):
            self.object_source = str(self.object_source)

        if self.matches_full_search_term is not None and not isinstance(self.matches_full_search_term, Bool):
            self.matches_full_search_term = Bool(self.matches_full_search_term)

        super().__post_init__(**kwargs)


@dataclass
class SearchResultSet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SEARCH.SearchResultSet
    class_class_curie: ClassVar[str] = "search:SearchResultSet"
    class_name: ClassVar[str] = "SearchResultSet"
    class_model_uri: ClassVar[URIRef] = SEARCH.SearchResultSet

    configuration: Optional[Union[dict, SearchBaseConfiguration]] = None
    results: Optional[Union[Union[dict, SearchResult], List[Union[dict, SearchResult]]]] = empty_list()
    result_count: Optional[int] = None
    cursor: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.configuration is not None and not isinstance(self.configuration, SearchBaseConfiguration):
            self.configuration = SearchBaseConfiguration(**as_dict(self.configuration))

        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, SearchResult) else SearchResult(**as_dict(v)) for v in self.results]

        if self.result_count is not None and not isinstance(self.result_count, int):
            self.result_count = int(self.result_count)

        if self.cursor is not None and not isinstance(self.cursor, int):
            self.cursor = int(self.cursor)

        super().__post_init__(**kwargs)


# Enumerations
class SearchTermSyntax(EnumDefinitionImpl):

    PLAINTEXT = PermissibleValue(text="PLAINTEXT")
    REGULAR_EXPRESSION = PermissibleValue(text="REGULAR_EXPRESSION")
    SQL = PermissibleValue(text="SQL")
    LUCENE = PermissibleValue(text="LUCENE")
    STARTS_WITH = PermissibleValue(text="STARTS_WITH")

    _defn = EnumDefinition(
        name="SearchTermSyntax",
    )

class SearchProperty(EnumDefinitionImpl):
    """
    A property that can be searched on
    """
    IDENTIFIER = PermissibleValue(text="IDENTIFIER",
                                           meaning=SCHEMA.identifier)
    LABEL = PermissibleValue(text="LABEL",
                                 meaning=RDFS.label)
    ALIAS = PermissibleValue(text="ALIAS",
                                 meaning=SKOS.altLabel)
    COMMENT = PermissibleValue(text="COMMENT",
                                     meaning=RDFS.comment)
    DEFINITION = PermissibleValue(text="DEFINITION",
                                           meaning=SKOS.definition)
    ANYTHING = PermissibleValue(text="ANYTHING",
                                       meaning=RDF.Property)

    _defn = EnumDefinition(
        name="SearchProperty",
        description="A property that can be searched on",
    )

# Slots
class slots:
    pass

slots.searchBaseConfiguration__search_terms = Slot(uri=SEARCH.search_terms, name="searchBaseConfiguration__search_terms", curie=SEARCH.curie('search_terms'),
                   model_uri=SEARCH.searchBaseConfiguration__search_terms, domain=None, range=Optional[Union[Union[str, SearchTerm], List[Union[str, SearchTerm]]]])

slots.searchBaseConfiguration__syntax = Slot(uri=SEARCH.syntax, name="searchBaseConfiguration__syntax", curie=SEARCH.curie('syntax'),
                   model_uri=SEARCH.searchBaseConfiguration__syntax, domain=None, range=Optional[Union[str, "SearchTermSyntax"]])

slots.searchBaseConfiguration__properties = Slot(uri=SEARCH.properties, name="searchBaseConfiguration__properties", curie=SEARCH.curie('properties'),
                   model_uri=SEARCH.searchBaseConfiguration__properties, domain=None, range=Optional[Union[Union[str, "SearchProperty"], List[Union[str, "SearchProperty"]]]])

slots.searchBaseConfiguration__limit = Slot(uri=SEARCH.limit, name="searchBaseConfiguration__limit", curie=SEARCH.curie('limit'),
                   model_uri=SEARCH.searchBaseConfiguration__limit, domain=None, range=Optional[int])

slots.searchBaseConfiguration__cursor = Slot(uri=SEARCH.cursor, name="searchBaseConfiguration__cursor", curie=SEARCH.curie('cursor'),
                   model_uri=SEARCH.searchBaseConfiguration__cursor, domain=None, range=Optional[int])

slots.searchBaseConfiguration__is_regular_expression = Slot(uri=SEARCH.is_regular_expression, name="searchBaseConfiguration__is_regular_expression", curie=SEARCH.curie('is_regular_expression'),
                   model_uri=SEARCH.searchBaseConfiguration__is_regular_expression, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__is_partial = Slot(uri=SEARCH.is_partial, name="searchBaseConfiguration__is_partial", curie=SEARCH.curie('is_partial'),
                   model_uri=SEARCH.searchBaseConfiguration__is_partial, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__is_complete = Slot(uri=SEARCH.is_complete, name="searchBaseConfiguration__is_complete", curie=SEARCH.curie('is_complete'),
                   model_uri=SEARCH.searchBaseConfiguration__is_complete, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__include_id = Slot(uri=SEARCH.include_id, name="searchBaseConfiguration__include_id", curie=SEARCH.curie('include_id'),
                   model_uri=SEARCH.searchBaseConfiguration__include_id, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__include_label = Slot(uri=SEARCH.include_label, name="searchBaseConfiguration__include_label", curie=SEARCH.curie('include_label'),
                   model_uri=SEARCH.searchBaseConfiguration__include_label, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__include_aliases = Slot(uri=SEARCH.include_aliases, name="searchBaseConfiguration__include_aliases", curie=SEARCH.curie('include_aliases'),
                   model_uri=SEARCH.searchBaseConfiguration__include_aliases, domain=None, range=Optional[Union[bool, Bool]])

slots.searchBaseConfiguration__include_definition = Slot(uri=SEARCH.include_definition, name="searchBaseConfiguration__include_definition", curie=SEARCH.curie('include_definition'),
                   model_uri=SEARCH.searchBaseConfiguration__include_definition, domain=None, range=Optional[Union[bool, Bool]])

slots.searchResult__rank = Slot(uri=SEARCH.rank, name="searchResult__rank", curie=SEARCH.curie('rank'),
                   model_uri=SEARCH.searchResult__rank, domain=None, range=Optional[int])

slots.searchResult__object_id = Slot(uri=SSSOM.object_id, name="searchResult__object_id", curie=SSSOM.curie('object_id'),
                   model_uri=SEARCH.searchResult__object_id, domain=None, range=Optional[str])

slots.searchResult__object_label = Slot(uri=SSSOM.object_label, name="searchResult__object_label", curie=SSSOM.curie('object_label'),
                   model_uri=SEARCH.searchResult__object_label, domain=None, range=Optional[str])

slots.searchResult__object_source = Slot(uri=SSSOM.object_source, name="searchResult__object_source", curie=SSSOM.curie('object_source'),
                   model_uri=SEARCH.searchResult__object_source, domain=None, range=Optional[str])

slots.searchResult__matches_full_search_term = Slot(uri=SEARCH.matches_full_search_term, name="searchResult__matches_full_search_term", curie=SEARCH.curie('matches_full_search_term'),
                   model_uri=SEARCH.searchResult__matches_full_search_term, domain=None, range=Optional[Union[bool, Bool]])

slots.searchResultSet__configuration = Slot(uri=SEARCH.configuration, name="searchResultSet__configuration", curie=SEARCH.curie('configuration'),
                   model_uri=SEARCH.searchResultSet__configuration, domain=None, range=Optional[Union[dict, SearchBaseConfiguration]])

slots.searchResultSet__results = Slot(uri=SEARCH.results, name="searchResultSet__results", curie=SEARCH.curie('results'),
                   model_uri=SEARCH.searchResultSet__results, domain=None, range=Optional[Union[Union[dict, SearchResult], List[Union[dict, SearchResult]]]])

slots.searchResultSet__result_count = Slot(uri=SEARCH.result_count, name="searchResultSet__result_count", curie=SEARCH.curie('result_count'),
                   model_uri=SEARCH.searchResultSet__result_count, domain=None, range=Optional[int])

slots.searchResultSet__cursor = Slot(uri=SEARCH.cursor, name="searchResultSet__cursor", curie=SEARCH.curie('cursor'),
                   model_uri=SEARCH.searchResultSet__cursor, domain=None, range=Optional[int])
