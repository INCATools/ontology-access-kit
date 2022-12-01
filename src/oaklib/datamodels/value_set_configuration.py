# Auto generated from value_set_configuration.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-27T17:19:16
# Schema: value-set-configuration
#
# id: https://w3id.org/linkml/value-set-configuration
# description: A datamodel for configuring value sets and value set expabsions
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions,
)
from linkml_runtime.linkml_model.types import String, Uri
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import URI, bnode, empty_dict, empty_list
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
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
VSCONF = CurieNamespace("vsconf", "https://w3id.org/linkml/value-set-configuration/")
DEFAULT_ = VSCONF


# Types

# Class references
class ResolverName(extended_str):
    pass


class NamedResolverName(ResolverName):
    pass


@dataclass
class ValueSetConfiguration(YAMLRoot):
    """
    configuration for value sets
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VSCONF.ValueSetConfiguration
    class_class_curie: ClassVar[str] = "vsconf:ValueSetConfiguration"
    class_name: ClassVar[str] = "ValueSetConfiguration"
    class_model_uri: ClassVar[URIRef] = VSCONF.ValueSetConfiguration

    default_resolver: Optional[Union[dict, "Resolver"]] = None
    resource_resolvers: Optional[
        Union[
            Dict[Union[str, ResolverName], Union[dict, "Resolver"]], List[Union[dict, "Resolver"]]
        ]
    ] = empty_dict()
    prefix_resolvers: Optional[
        Union[
            Dict[Union[str, ResolverName], Union[dict, "Resolver"]], List[Union[dict, "Resolver"]]
        ]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.default_resolver is not None and not isinstance(self.default_resolver, Resolver):
            self.default_resolver = Resolver(**as_dict(self.default_resolver))

        self._normalize_inlined_as_dict(
            slot_name="resource_resolvers", slot_type=Resolver, key_name="name", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="prefix_resolvers", slot_type=Resolver, key_name="name", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass
class Resolver(YAMLRoot):
    """
    A mechanism for resolving using an ontology
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VSCONF.Resolver
    class_class_curie: ClassVar[str] = "vsconf:Resolver"
    class_name: ClassVar[str] = "Resolver"
    class_model_uri: ClassVar[URIRef] = VSCONF.Resolver

    name: Union[str, ResolverName] = None
    shorthand_prefix: Optional[str] = None
    shorthand: Optional[str] = None
    method: Optional[Union[str, "ResolverMethod"]] = None
    url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ResolverName):
            self.name = ResolverName(self.name)

        if self.shorthand_prefix is not None and not isinstance(self.shorthand_prefix, str):
            self.shorthand_prefix = str(self.shorthand_prefix)

        if self.shorthand is not None and not isinstance(self.shorthand, str):
            self.shorthand = str(self.shorthand)

        if self.method is not None and not isinstance(self.method, ResolverMethod):
            self.method = ResolverMethod(self.method)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        super().__post_init__(**kwargs)


@dataclass
class NamedResolver(Resolver):
    """
    A resolver that is associated with a named resource or prefix
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VSCONF.NamedResolver
    class_class_curie: ClassVar[str] = "vsconf:NamedResolver"
    class_name: ClassVar[str] = "NamedResolver"
    class_model_uri: ClassVar[URIRef] = VSCONF.NamedResolver

    name: Union[str, NamedResolverName] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, NamedResolverName):
            self.name = NamedResolverName(self.name)

        super().__post_init__(**kwargs)


# Enumerations
class ResolverMethod(EnumDefinitionImpl):

    SemanticSQL = PermissibleValue(text="SemanticSQL")
    OLS = PermissibleValue(text="OLS")
    BioPortal = PermissibleValue(text="BioPortal")
    OntoBee = PermissibleValue(text="OntoBee")
    Ubergraph = PermissibleValue(text="Ubergraph")
    TCCM = PermissibleValue(text="TCCM")
    SPARQL = PermissibleValue(text="SPARQL")
    LOV = PermissibleValue(text="LOV")
    Pronto = PermissibleValue(text="Pronto")
    Uniprot = PermissibleValue(text="Uniprot")

    _defn = EnumDefinition(
        name="ResolverMethod",
    )


# Slots
class slots:
    pass


slots.valueSetConfiguration__default_resolver = Slot(
    uri=VSCONF.default_resolver,
    name="valueSetConfiguration__default_resolver",
    curie=VSCONF.curie("default_resolver"),
    model_uri=VSCONF.valueSetConfiguration__default_resolver,
    domain=None,
    range=Optional[Union[dict, Resolver]],
)

slots.valueSetConfiguration__resource_resolvers = Slot(
    uri=VSCONF.resource_resolvers,
    name="valueSetConfiguration__resource_resolvers",
    curie=VSCONF.curie("resource_resolvers"),
    model_uri=VSCONF.valueSetConfiguration__resource_resolvers,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, ResolverName], Union[dict, Resolver]], List[Union[dict, Resolver]]]
    ],
)

slots.valueSetConfiguration__prefix_resolvers = Slot(
    uri=VSCONF.prefix_resolvers,
    name="valueSetConfiguration__prefix_resolvers",
    curie=VSCONF.curie("prefix_resolvers"),
    model_uri=VSCONF.valueSetConfiguration__prefix_resolvers,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, ResolverName], Union[dict, Resolver]], List[Union[dict, Resolver]]]
    ],
)

slots.resolver__name = Slot(
    uri=VSCONF.name,
    name="resolver__name",
    curie=VSCONF.curie("name"),
    model_uri=VSCONF.resolver__name,
    domain=None,
    range=URIRef,
)

slots.resolver__shorthand_prefix = Slot(
    uri=VSCONF.shorthand_prefix,
    name="resolver__shorthand_prefix",
    curie=VSCONF.curie("shorthand_prefix"),
    model_uri=VSCONF.resolver__shorthand_prefix,
    domain=None,
    range=Optional[str],
)

slots.resolver__shorthand = Slot(
    uri=VSCONF.shorthand,
    name="resolver__shorthand",
    curie=VSCONF.curie("shorthand"),
    model_uri=VSCONF.resolver__shorthand,
    domain=None,
    range=Optional[str],
)

slots.resolver__method = Slot(
    uri=VSCONF.method,
    name="resolver__method",
    curie=VSCONF.curie("method"),
    model_uri=VSCONF.resolver__method,
    domain=None,
    range=Optional[Union[str, "ResolverMethod"]],
)

slots.resolver__url = Slot(
    uri=VSCONF.url,
    name="resolver__url",
    curie=VSCONF.curie("url"),
    model_uri=VSCONF.resolver__url,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.namedResolver__name = Slot(
    uri=VSCONF.name,
    name="namedResolver__name",
    curie=VSCONF.curie("name"),
    model_uri=VSCONF.namedResolver__name,
    domain=None,
    range=URIRef,
)
