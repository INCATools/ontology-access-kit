# Auto generated from association.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-03-15T10:56:08
# Schema: association
#
# id: https://w3id.org/oak/association
# description: A datamodel for representing generic associations. The core datamodel is broad, encompassing the W3
#              Open Annotation data model as well as common ontology annotation data models using in the
#              biosciences.
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
from linkml_runtime.linkml_model.types import Boolean, Uriorcurie
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
OA = CurieNamespace("oa", "http://www.w3.org/ns/oa#")
ONTOASSOC = CurieNamespace("ontoassoc", "https://w3id.org/oak/association/")
RDF = CurieNamespace("rdf", "http://example.org/UNKNOWN/rdf/")
DEFAULT_ = ONTOASSOC


# Types

# Class references


@dataclass
class Association(YAMLRoot):
    """
    A generic association between a thing (subject) and another thing (object).
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OA.Annotation
    class_class_curie: ClassVar[str] = "oa:Annotation"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.Association

    subject: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None
    property_values: Optional[
        Union[Union[dict, "PropertyValue"], List[Union[dict, "PropertyValue"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        if not isinstance(self.property_values, list):
            self.property_values = (
                [self.property_values] if self.property_values is not None else []
            )
        self.property_values = [
            v if isinstance(v, PropertyValue) else PropertyValue(**as_dict(v))
            for v in self.property_values
        ]

        super().__post_init__(**kwargs)


@dataclass
class NegatedAssociation(YAMLRoot):
    """
    A negated association between a thing (subject) and another thing (object).
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC.NegatedAssociation
    class_class_curie: ClassVar[str] = "ontoassoc:NegatedAssociation"
    class_name: ClassVar[str] = "NegatedAssociation"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.NegatedAssociation

    subject: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None
    property_values: Optional[
        Union[Union[dict, "PropertyValue"], List[Union[dict, "PropertyValue"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        if not isinstance(self.property_values, list):
            self.property_values = (
                [self.property_values] if self.property_values is not None else []
            )
        self.property_values = [
            v if isinstance(v, PropertyValue) else PropertyValue(**as_dict(v))
            for v in self.property_values
        ]

        super().__post_init__(**kwargs)


@dataclass
class PropertyValue(YAMLRoot):
    """
    A generic tag-value that can be associated with an association.
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC.PropertyValue
    class_class_curie: ClassVar[str] = "ontoassoc:PropertyValue"
    class_name: ClassVar[str] = "PropertyValue"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.PropertyValue

    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        super().__post_init__(**kwargs)


@dataclass
class RollupGroup(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC.RollupGroup
    class_class_curie: ClassVar[str] = "ontoassoc:RollupGroup"
    class_name: ClassVar[str] = "RollupGroup"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.RollupGroup

    group_object: Optional[Union[str, URIorCURIE]] = None
    sub_groups: Optional[
        Union[Union[dict, "RollupGroup"], List[Union[dict, "RollupGroup"]]]
    ] = empty_list()
    associations: Optional[
        Union[Union[dict, Association], List[Union[dict, Association]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.group_object is not None and not isinstance(self.group_object, URIorCURIE):
            self.group_object = URIorCURIE(self.group_object)

        if not isinstance(self.sub_groups, list):
            self.sub_groups = [self.sub_groups] if self.sub_groups is not None else []
        self.sub_groups = [
            v if isinstance(v, RollupGroup) else RollupGroup(**as_dict(v)) for v in self.sub_groups
        ]

        if not isinstance(self.associations, list):
            self.associations = [self.associations] if self.associations is not None else []
        self.associations = [
            v if isinstance(v, Association) else Association(**as_dict(v))
            for v in self.associations
        ]

        super().__post_init__(**kwargs)


@dataclass
class ParserConfiguration(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC.ParserConfiguration
    class_class_curie: ClassVar[str] = "ontoassoc:ParserConfiguration"
    class_name: ClassVar[str] = "ParserConfiguration"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.ParserConfiguration

    preserve_negated_associations: Optional[Union[bool, Bool]] = None
    include_association_attributes: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.preserve_negated_associations is not None and not isinstance(
            self.preserve_negated_associations, Bool
        ):
            self.preserve_negated_associations = Bool(self.preserve_negated_associations)

        if self.include_association_attributes is not None and not isinstance(
            self.include_association_attributes, Bool
        ):
            self.include_association_attributes = Bool(self.include_association_attributes)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.subject = Slot(
    uri=RDF.subject,
    name="subject",
    curie=RDF.curie("subject"),
    model_uri=ONTOASSOC.subject,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.predicate = Slot(
    uri=RDF.predicate,
    name="predicate",
    curie=RDF.curie("predicate"),
    model_uri=ONTOASSOC.predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.object = Slot(
    uri=RDF.object,
    name="object",
    curie=RDF.curie("object"),
    model_uri=ONTOASSOC.object,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.property_values = Slot(
    uri=ONTOASSOC.property_values,
    name="property_values",
    curie=ONTOASSOC.curie("property_values"),
    model_uri=ONTOASSOC.property_values,
    domain=None,
    range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]],
)

slots.group_object = Slot(
    uri=RDF.object,
    name="group_object",
    curie=RDF.curie("object"),
    model_uri=ONTOASSOC.group_object,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.sub_groups = Slot(
    uri=ONTOASSOC.sub_groups,
    name="sub_groups",
    curie=ONTOASSOC.curie("sub_groups"),
    model_uri=ONTOASSOC.sub_groups,
    domain=None,
    range=Optional[Union[Union[dict, RollupGroup], List[Union[dict, RollupGroup]]]],
)

slots.associations = Slot(
    uri=ONTOASSOC.associations,
    name="associations",
    curie=ONTOASSOC.curie("associations"),
    model_uri=ONTOASSOC.associations,
    domain=None,
    range=Optional[Union[Union[dict, Association], List[Union[dict, Association]]]],
)

slots.parserConfiguration__preserve_negated_associations = Slot(
    uri=ONTOASSOC.preserve_negated_associations,
    name="parserConfiguration__preserve_negated_associations",
    curie=ONTOASSOC.curie("preserve_negated_associations"),
    model_uri=ONTOASSOC.parserConfiguration__preserve_negated_associations,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.parserConfiguration__include_association_attributes = Slot(
    uri=ONTOASSOC.include_association_attributes,
    name="parserConfiguration__include_association_attributes",
    curie=ONTOASSOC.curie("include_association_attributes"),
    model_uri=ONTOASSOC.parserConfiguration__include_association_attributes,
    domain=None,
    range=Optional[Union[bool, Bool]],
)
