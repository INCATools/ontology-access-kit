# Auto generated from text_annotator.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-05T10:01:24
# Schema: text-annotator
#
# id: https://w3id.org/linkml/text_annotator
# description: A datamodel for representing the results of textual named entity recognition annotation results
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
from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ANN = CurieNamespace('ann', 'https://w3id.org/linkml/text_annotator/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = ANN


# Types
class Position(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "Position"
    type_model_uri = ANN.Position


# Class references
class TextAnnotationTerm(extended_str):
    pass


@dataclass
class TextAnnotationResultSet(YAMLRoot):
    """
    A collection of annotation results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.TextAnnotationResultSet
    class_class_curie: ClassVar[str] = "ann:TextAnnotationResultSet"
    class_name: ClassVar[str] = "TextAnnotationResultSet"
    class_model_uri: ClassVar[URIRef] = ANN.TextAnnotationResultSet

    annotations: Optional[Union[Dict[Union[str, TextAnnotationTerm], Union[dict, "TextAnnotation"]], List[Union[dict, "TextAnnotation"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="annotations", slot_type=TextAnnotation, key_name="term", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class HasSpan(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.HasSpan
    class_class_curie: ClassVar[str] = "ann:HasSpan"
    class_name: ClassVar[str] = "HasSpan"
    class_model_uri: ClassVar[URIRef] = ANN.HasSpan

    start_position: Optional[Union[int, Position]] = None
    end_position: Optional[Union[int, Position]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.start_position is not None and not isinstance(self.start_position, Position):
            self.start_position = Position(self.start_position)

        if self.end_position is not None and not isinstance(self.end_position, Position):
            self.end_position = Position(self.end_position)

        super().__post_init__(**kwargs)


@dataclass
class TextAnnotation(YAMLRoot):
    """
    An individual text annotation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.TextAnnotation
    class_class_curie: ClassVar[str] = "ann:TextAnnotation"
    class_name: ClassVar[str] = "TextAnnotation"
    class_model_uri: ClassVar[URIRef] = ANN.TextAnnotation

    term: Union[str, TextAnnotationTerm] = None
    start_position: Optional[Union[int, Position]] = None
    end_position: Optional[Union[int, Position]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.term):
            self.MissingRequiredField("term")
        if not isinstance(self.term, TextAnnotationTerm):
            self.term = TextAnnotationTerm(self.term)

        if self.start_position is not None and not isinstance(self.start_position, Position):
            self.start_position = Position(self.start_position)

        if self.end_position is not None and not isinstance(self.end_position, Position):
            self.end_position = Position(self.end_position)

        super().__post_init__(**kwargs)


# Enumerations
class TransformationType(EnumDefinitionImpl):
    """
    A controlled datamodels of the types of transformation that can be applied to
    """
    Stemming = PermissibleValue(text="Stemming",
                                       description="Removal of the last few characters of a word to yield a stem term for each word in the term")
    Lemmatization = PermissibleValue(text="Lemmatization",
                                                 description="Contextual reduction of a word to its base form for each word in the term")
    WordOrderNormalization = PermissibleValue(text="WordOrderNormalization",
                                                                   description="reorder words in the term to a standard order such that comparisons are order-independent")
    Depluralization = PermissibleValue(text="Depluralization",
                                                     description="Transform plural form to singular form for each word in a term")
    CaseNormalization = PermissibleValue(text="CaseNormalization",
                                                         description="Transform term to a standard case, typically lowercase")
    WhitespaceNormalization = PermissibleValue(text="WhitespaceNormalization",
                                                                     description="Trim whitespace, condense whitespace runs, and transform all non-space whitespace to spaces")
    TermExpanson = PermissibleValue(text="TermExpanson",
                                               description="Expand terms using a dictionary")

    _defn = EnumDefinition(
        name="TransformationType",
        description="A controlled datamodels of the types of transformation that can be applied to",
    )

# Slots
class slots:
    pass

slots.textAnnotationResultSet__annotations = Slot(uri=ANN.annotations, name="textAnnotationResultSet__annotations", curie=ANN.curie('annotations'),
                   model_uri=ANN.textAnnotationResultSet__annotations, domain=None, range=Optional[Union[Dict[Union[str, TextAnnotationTerm], Union[dict, TextAnnotation]], List[Union[dict, TextAnnotation]]]])

slots.hasSpan__start_position = Slot(uri=ANN.start_position, name="hasSpan__start_position", curie=ANN.curie('start_position'),
                   model_uri=ANN.hasSpan__start_position, domain=None, range=Optional[Union[int, Position]])

slots.hasSpan__end_position = Slot(uri=ANN.end_position, name="hasSpan__end_position", curie=ANN.curie('end_position'),
                   model_uri=ANN.hasSpan__end_position, domain=None, range=Optional[Union[int, Position]])

slots.textAnnotation__term = Slot(uri=ANN.term, name="textAnnotation__term", curie=ANN.curie('term'),
                   model_uri=ANN.textAnnotation__term, domain=None, range=URIRef)
