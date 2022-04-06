# Auto generated from search_results.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-05T13:39:03
# Schema: search-results
#
# id: https://w3id.org/linkml/search_results
# description: A datamodel for representing the results of ontology search
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
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SR = CurieNamespace('sr', 'https://w3id.org/linkml/search_results/')
SSSOM = CurieNamespace('sssom', 'http://w3id.org/sssom/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = SR


# Types
class Position(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "Position"
    type_model_uri = SR.Position


# Class references



@dataclass
class SearchResultSet(YAMLRoot):
    """
    A collection of annotation results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SR.SearchResultSet
    class_class_curie: ClassVar[str] = "sr:SearchResultSet"
    class_name: ClassVar[str] = "SearchResultSet"
    class_model_uri: ClassVar[URIRef] = SR.SearchResultSet

    results: Optional[Union[Union[dict, "SearchResult"], List[Union[dict, "SearchResult"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, SearchResult) else SearchResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class SearchResult(YAMLRoot):
    """
    An individual text annotation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SR.SearchResult
    class_class_curie: ClassVar[str] = "sr:SearchResult"
    class_name: ClassVar[str] = "SearchResult"
    class_model_uri: ClassVar[URIRef] = SR.SearchResult

    object_id: Optional[str] = None
    object_label: Optional[str] = None
    object_source: Optional[str] = None
    matches_full_search_term: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.object_id is not None and not isinstance(self.object_id, str):
            self.object_id = str(self.object_id)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.object_source is not None and not isinstance(self.object_source, str):
            self.object_source = str(self.object_source)

        if self.matches_full_search_term is not None and not isinstance(self.matches_full_search_term, Bool):
            self.matches_full_search_term = Bool(self.matches_full_search_term)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.searchResultSet__results = Slot(uri=SR.results, name="searchResultSet__results", curie=SR.curie('results'),
                   model_uri=SR.searchResultSet__results, domain=None, range=Optional[Union[Union[dict, SearchResult], List[Union[dict, SearchResult]]]])

slots.searchResult__object_id = Slot(uri=SSSOM.object_id, name="searchResult__object_id", curie=SSSOM.curie('object_id'),
                   model_uri=SR.searchResult__object_id, domain=None, range=Optional[str])

slots.searchResult__object_label = Slot(uri=SSSOM.object_label, name="searchResult__object_label", curie=SSSOM.curie('object_label'),
                   model_uri=SR.searchResult__object_label, domain=None, range=Optional[str])

slots.searchResult__object_source = Slot(uri=SSSOM.object_source, name="searchResult__object_source", curie=SSSOM.curie('object_source'),
                   model_uri=SR.searchResult__object_source, domain=None, range=Optional[str])

slots.searchResult__matches_full_search_term = Slot(uri=SR.matches_full_search_term, name="searchResult__matches_full_search_term", curie=SR.curie('matches_full_search_term'),
                   model_uri=SR.searchResult__matches_full_search_term, domain=None, range=Optional[Union[bool, Bool]])
