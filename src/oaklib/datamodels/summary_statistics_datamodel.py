# Auto generated from summary_statistics_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-23T14:14:36
# Schema: summary-statistics
#
# id: https://w3id.org/linkml/summary_statistics
# description: A datamodel for reports on data
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
from linkml_runtime.linkml_model.types import Integer, String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
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
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
REPORTING = CurieNamespace("reporting", "https://w3id.org/linkml/report")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = REPORTING


# Types

# Class references
class FacetedCountFacet(extended_str):
    pass


@dataclass
class SummaryStatisticCollection(YAMLRoot):
    """
    A summary statistics report object
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.SummaryStatisticCollection
    class_class_curie: ClassVar[str] = "reporting:SummaryStatisticCollection"
    class_name: ClassVar[str] = "SummaryStatisticCollection"
    class_model_uri: ClassVar[URIRef] = REPORTING.SummaryStatisticCollection

    id: str = None
    class_count: Optional[int] = None
    anonymous_class_expression_count: Optional[int] = None
    unsatisfiable_class_count: Optional[int] = None
    deprecated_class_count: Optional[int] = None
    non_deprecated_class_count: Optional[int] = None
    merged_class_count: Optional[int] = None
    class_count_with_text_definitions: Optional[int] = None
    class_count_without_text_definitions: Optional[int] = None
    property_count: Optional[int] = None
    object_property_count: Optional[int] = None
    deprecated_object_property_count: Optional[int] = None
    non_deprecated_object_property_count: Optional[int] = None
    datatype_property_count: Optional[int] = None
    annotation_property_count: Optional[int] = None
    individual_count: Optional[int] = None
    named_individual_count: Optional[int] = None
    anonymous_individual_count: Optional[int] = None
    untyped_entity_count: Optional[int] = None
    subset_count: Optional[int] = None
    description_logic_profile: Optional[str] = None
    owl_axiom_count: Optional[int] = None
    rdf_triple_count: Optional[int] = None
    subclass_of_axiom_count: Optional[int] = None
    equivalent_classes_axiom_count: Optional[int] = None
    edge_count_by_predicate: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    entailed_edge_count_by_predicate: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    distinct_synonym_count: Optional[int] = None
    synonym_statement_count: Optional[int] = None
    synonym_statement_count_by_predicate: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    class_count_by_subset: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    class_count_by_category: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    mapping_count: Optional[int] = None
    mapping_statement_count_by_predicate: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    ontology_count: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        if self.class_count is not None and not isinstance(self.class_count, int):
            self.class_count = int(self.class_count)

        if self.anonymous_class_expression_count is not None and not isinstance(
            self.anonymous_class_expression_count, int
        ):
            self.anonymous_class_expression_count = int(self.anonymous_class_expression_count)

        if self.unsatisfiable_class_count is not None and not isinstance(
            self.unsatisfiable_class_count, int
        ):
            self.unsatisfiable_class_count = int(self.unsatisfiable_class_count)

        if self.deprecated_class_count is not None and not isinstance(
            self.deprecated_class_count, int
        ):
            self.deprecated_class_count = int(self.deprecated_class_count)

        if self.non_deprecated_class_count is not None and not isinstance(
            self.non_deprecated_class_count, int
        ):
            self.non_deprecated_class_count = int(self.non_deprecated_class_count)

        if self.merged_class_count is not None and not isinstance(self.merged_class_count, int):
            self.merged_class_count = int(self.merged_class_count)

        if self.class_count_with_text_definitions is not None and not isinstance(
            self.class_count_with_text_definitions, int
        ):
            self.class_count_with_text_definitions = int(self.class_count_with_text_definitions)

        if self.class_count_without_text_definitions is not None and not isinstance(
            self.class_count_without_text_definitions, int
        ):
            self.class_count_without_text_definitions = int(
                self.class_count_without_text_definitions
            )

        if self.property_count is not None and not isinstance(self.property_count, int):
            self.property_count = int(self.property_count)

        if self.object_property_count is not None and not isinstance(
            self.object_property_count, int
        ):
            self.object_property_count = int(self.object_property_count)

        if self.deprecated_object_property_count is not None and not isinstance(
            self.deprecated_object_property_count, int
        ):
            self.deprecated_object_property_count = int(self.deprecated_object_property_count)

        if self.non_deprecated_object_property_count is not None and not isinstance(
            self.non_deprecated_object_property_count, int
        ):
            self.non_deprecated_object_property_count = int(
                self.non_deprecated_object_property_count
            )

        if self.datatype_property_count is not None and not isinstance(
            self.datatype_property_count, int
        ):
            self.datatype_property_count = int(self.datatype_property_count)

        if self.annotation_property_count is not None and not isinstance(
            self.annotation_property_count, int
        ):
            self.annotation_property_count = int(self.annotation_property_count)

        if self.individual_count is not None and not isinstance(self.individual_count, int):
            self.individual_count = int(self.individual_count)

        if self.named_individual_count is not None and not isinstance(
            self.named_individual_count, int
        ):
            self.named_individual_count = int(self.named_individual_count)

        if self.anonymous_individual_count is not None and not isinstance(
            self.anonymous_individual_count, int
        ):
            self.anonymous_individual_count = int(self.anonymous_individual_count)

        if self.untyped_entity_count is not None and not isinstance(self.untyped_entity_count, int):
            self.untyped_entity_count = int(self.untyped_entity_count)

        if self.subset_count is not None and not isinstance(self.subset_count, int):
            self.subset_count = int(self.subset_count)

        if self.description_logic_profile is not None and not isinstance(
            self.description_logic_profile, str
        ):
            self.description_logic_profile = str(self.description_logic_profile)

        if self.owl_axiom_count is not None and not isinstance(self.owl_axiom_count, int):
            self.owl_axiom_count = int(self.owl_axiom_count)

        if self.rdf_triple_count is not None and not isinstance(self.rdf_triple_count, int):
            self.rdf_triple_count = int(self.rdf_triple_count)

        if self.subclass_of_axiom_count is not None and not isinstance(
            self.subclass_of_axiom_count, int
        ):
            self.subclass_of_axiom_count = int(self.subclass_of_axiom_count)

        if self.equivalent_classes_axiom_count is not None and not isinstance(
            self.equivalent_classes_axiom_count, int
        ):
            self.equivalent_classes_axiom_count = int(self.equivalent_classes_axiom_count)

        self._normalize_inlined_as_dict(
            slot_name="edge_count_by_predicate",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        self._normalize_inlined_as_dict(
            slot_name="entailed_edge_count_by_predicate",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        if self.distinct_synonym_count is not None and not isinstance(
            self.distinct_synonym_count, int
        ):
            self.distinct_synonym_count = int(self.distinct_synonym_count)

        if self.synonym_statement_count is not None and not isinstance(
            self.synonym_statement_count, int
        ):
            self.synonym_statement_count = int(self.synonym_statement_count)

        self._normalize_inlined_as_dict(
            slot_name="synonym_statement_count_by_predicate",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        self._normalize_inlined_as_dict(
            slot_name="class_count_by_subset", slot_type=FacetedCount, key_name="facet", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="class_count_by_category",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        if self.mapping_count is not None and not isinstance(self.mapping_count, int):
            self.mapping_count = int(self.mapping_count)

        self._normalize_inlined_as_dict(
            slot_name="mapping_statement_count_by_predicate",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        if self.ontology_count is not None and not isinstance(self.ontology_count, int):
            self.ontology_count = int(self.ontology_count)

        super().__post_init__(**kwargs)


@dataclass
class GlobalStatistics(YAMLRoot):
    """
    summary statistics for the entire resource
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.GlobalStatistics
    class_class_curie: ClassVar[str] = "reporting:GlobalStatistics"
    class_name: ClassVar[str] = "GlobalStatistics"
    class_model_uri: ClassVar[URIRef] = REPORTING.GlobalStatistics

    description: Optional[str] = None
    partitions: Optional[
        Union[
            Union[dict, SummaryStatisticCollection], List[Union[dict, SummaryStatisticCollection]]
        ]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(
            slot_name="partitions", slot_type=SummaryStatisticCollection, key_name="id", keyed=False
        )

        super().__post_init__(**kwargs)


@dataclass
class FacetedCount(YAMLRoot):
    """
    Counts broken down by a facet
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.FacetedCount
    class_class_curie: ClassVar[str] = "reporting:FacetedCount"
    class_name: ClassVar[str] = "FacetedCount"
    class_model_uri: ClassVar[URIRef] = REPORTING.FacetedCount

    facet: Union[str, FacetedCountFacet] = None
    filtered_count: int = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.facet):
            self.MissingRequiredField("facet")
        if not isinstance(self.facet, FacetedCountFacet):
            self.facet = FacetedCountFacet(self.facet)

        if self._is_empty(self.filtered_count):
            self.MissingRequiredField("filtered_count")
        if not isinstance(self.filtered_count, int):
            self.filtered_count = int(self.filtered_count)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.count_statistic = Slot(
    uri=REPORTING.count_statistic,
    name="count_statistic",
    curie=REPORTING.curie("count_statistic"),
    model_uri=REPORTING.count_statistic,
    domain=None,
    range=Optional[int],
)

slots.class_statistic_group = Slot(
    uri=REPORTING.class_statistic_group,
    name="class_statistic_group",
    curie=REPORTING.curie("class_statistic_group"),
    model_uri=REPORTING.class_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.property_statistic_group = Slot(
    uri=REPORTING.property_statistic_group,
    name="property_statistic_group",
    curie=REPORTING.curie("property_statistic_group"),
    model_uri=REPORTING.property_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.individual_statistic_group = Slot(
    uri=REPORTING.individual_statistic_group,
    name="individual_statistic_group",
    curie=REPORTING.curie("individual_statistic_group"),
    model_uri=REPORTING.individual_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.metadata_statistic_group = Slot(
    uri=REPORTING.metadata_statistic_group,
    name="metadata_statistic_group",
    curie=REPORTING.curie("metadata_statistic_group"),
    model_uri=REPORTING.metadata_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.owl_statistic_group = Slot(
    uri=REPORTING.owl_statistic_group,
    name="owl_statistic_group",
    curie=REPORTING.curie("owl_statistic_group"),
    model_uri=REPORTING.owl_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.summaryStatisticCollection__id = Slot(
    uri=REPORTING.id,
    name="summaryStatisticCollection__id",
    curie=REPORTING.curie("id"),
    model_uri=REPORTING.summaryStatisticCollection__id,
    domain=None,
    range=str,
)

slots.summaryStatisticCollection__class_count = Slot(
    uri=REPORTING.class_count,
    name="summaryStatisticCollection__class_count",
    curie=REPORTING.curie("class_count"),
    model_uri=REPORTING.summaryStatisticCollection__class_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__anonymous_class_expression_count = Slot(
    uri=REPORTING.anonymous_class_expression_count,
    name="summaryStatisticCollection__anonymous_class_expression_count",
    curie=REPORTING.curie("anonymous_class_expression_count"),
    model_uri=REPORTING.summaryStatisticCollection__anonymous_class_expression_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__unsatisfiable_class_count = Slot(
    uri=REPORTING.unsatisfiable_class_count,
    name="summaryStatisticCollection__unsatisfiable_class_count",
    curie=REPORTING.curie("unsatisfiable_class_count"),
    model_uri=REPORTING.summaryStatisticCollection__unsatisfiable_class_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__deprecated_class_count = Slot(
    uri=REPORTING.deprecated_class_count,
    name="summaryStatisticCollection__deprecated_class_count",
    curie=REPORTING.curie("deprecated_class_count"),
    model_uri=REPORTING.summaryStatisticCollection__deprecated_class_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__non_deprecated_class_count = Slot(
    uri=REPORTING.non_deprecated_class_count,
    name="summaryStatisticCollection__non_deprecated_class_count",
    curie=REPORTING.curie("non_deprecated_class_count"),
    model_uri=REPORTING.summaryStatisticCollection__non_deprecated_class_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__merged_class_count = Slot(
    uri=REPORTING.merged_class_count,
    name="summaryStatisticCollection__merged_class_count",
    curie=REPORTING.curie("merged_class_count"),
    model_uri=REPORTING.summaryStatisticCollection__merged_class_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__class_count_with_text_definitions = Slot(
    uri=REPORTING.class_count_with_text_definitions,
    name="summaryStatisticCollection__class_count_with_text_definitions",
    curie=REPORTING.curie("class_count_with_text_definitions"),
    model_uri=REPORTING.summaryStatisticCollection__class_count_with_text_definitions,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__class_count_without_text_definitions = Slot(
    uri=REPORTING.class_count_without_text_definitions,
    name="summaryStatisticCollection__class_count_without_text_definitions",
    curie=REPORTING.curie("class_count_without_text_definitions"),
    model_uri=REPORTING.summaryStatisticCollection__class_count_without_text_definitions,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__property_count = Slot(
    uri=REPORTING.property_count,
    name="summaryStatisticCollection__property_count",
    curie=REPORTING.curie("property_count"),
    model_uri=REPORTING.summaryStatisticCollection__property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__object_property_count = Slot(
    uri=REPORTING.object_property_count,
    name="summaryStatisticCollection__object_property_count",
    curie=REPORTING.curie("object_property_count"),
    model_uri=REPORTING.summaryStatisticCollection__object_property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__deprecated_object_property_count = Slot(
    uri=REPORTING.deprecated_object_property_count,
    name="summaryStatisticCollection__deprecated_object_property_count",
    curie=REPORTING.curie("deprecated_object_property_count"),
    model_uri=REPORTING.summaryStatisticCollection__deprecated_object_property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__non_deprecated_object_property_count = Slot(
    uri=REPORTING.non_deprecated_object_property_count,
    name="summaryStatisticCollection__non_deprecated_object_property_count",
    curie=REPORTING.curie("non_deprecated_object_property_count"),
    model_uri=REPORTING.summaryStatisticCollection__non_deprecated_object_property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__datatype_property_count = Slot(
    uri=REPORTING.datatype_property_count,
    name="summaryStatisticCollection__datatype_property_count",
    curie=REPORTING.curie("datatype_property_count"),
    model_uri=REPORTING.summaryStatisticCollection__datatype_property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__annotation_property_count = Slot(
    uri=REPORTING.annotation_property_count,
    name="summaryStatisticCollection__annotation_property_count",
    curie=REPORTING.curie("annotation_property_count"),
    model_uri=REPORTING.summaryStatisticCollection__annotation_property_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__individual_count = Slot(
    uri=REPORTING.individual_count,
    name="summaryStatisticCollection__individual_count",
    curie=REPORTING.curie("individual_count"),
    model_uri=REPORTING.summaryStatisticCollection__individual_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__named_individual_count = Slot(
    uri=REPORTING.named_individual_count,
    name="summaryStatisticCollection__named_individual_count",
    curie=REPORTING.curie("named_individual_count"),
    model_uri=REPORTING.summaryStatisticCollection__named_individual_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__anonymous_individual_count = Slot(
    uri=REPORTING.anonymous_individual_count,
    name="summaryStatisticCollection__anonymous_individual_count",
    curie=REPORTING.curie("anonymous_individual_count"),
    model_uri=REPORTING.summaryStatisticCollection__anonymous_individual_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__untyped_entity_count = Slot(
    uri=REPORTING.untyped_entity_count,
    name="summaryStatisticCollection__untyped_entity_count",
    curie=REPORTING.curie("untyped_entity_count"),
    model_uri=REPORTING.summaryStatisticCollection__untyped_entity_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__subset_count = Slot(
    uri=REPORTING.subset_count,
    name="summaryStatisticCollection__subset_count",
    curie=REPORTING.curie("subset_count"),
    model_uri=REPORTING.summaryStatisticCollection__subset_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__description_logic_profile = Slot(
    uri=REPORTING.description_logic_profile,
    name="summaryStatisticCollection__description_logic_profile",
    curie=REPORTING.curie("description_logic_profile"),
    model_uri=REPORTING.summaryStatisticCollection__description_logic_profile,
    domain=None,
    range=Optional[str],
)

slots.summaryStatisticCollection__owl_axiom_count = Slot(
    uri=REPORTING.owl_axiom_count,
    name="summaryStatisticCollection__owl_axiom_count",
    curie=REPORTING.curie("owl_axiom_count"),
    model_uri=REPORTING.summaryStatisticCollection__owl_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__rdf_triple_count = Slot(
    uri=REPORTING.rdf_triple_count,
    name="summaryStatisticCollection__rdf_triple_count",
    curie=REPORTING.curie("rdf_triple_count"),
    model_uri=REPORTING.summaryStatisticCollection__rdf_triple_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__subclass_of_axiom_count = Slot(
    uri=REPORTING.subclass_of_axiom_count,
    name="summaryStatisticCollection__subclass_of_axiom_count",
    curie=REPORTING.curie("subclass_of_axiom_count"),
    model_uri=REPORTING.summaryStatisticCollection__subclass_of_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__equivalent_classes_axiom_count = Slot(
    uri=REPORTING.equivalent_classes_axiom_count,
    name="summaryStatisticCollection__equivalent_classes_axiom_count",
    curie=REPORTING.curie("equivalent_classes_axiom_count"),
    model_uri=REPORTING.summaryStatisticCollection__equivalent_classes_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__edge_count_by_predicate = Slot(
    uri=REPORTING.edge_count_by_predicate,
    name="summaryStatisticCollection__edge_count_by_predicate",
    curie=REPORTING.curie("edge_count_by_predicate"),
    model_uri=REPORTING.summaryStatisticCollection__edge_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__entailed_edge_count_by_predicate = Slot(
    uri=REPORTING.entailed_edge_count_by_predicate,
    name="summaryStatisticCollection__entailed_edge_count_by_predicate",
    curie=REPORTING.curie("entailed_edge_count_by_predicate"),
    model_uri=REPORTING.summaryStatisticCollection__entailed_edge_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__distinct_synonym_count = Slot(
    uri=REPORTING.distinct_synonym_count,
    name="summaryStatisticCollection__distinct_synonym_count",
    curie=REPORTING.curie("distinct_synonym_count"),
    model_uri=REPORTING.summaryStatisticCollection__distinct_synonym_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__synonym_statement_count = Slot(
    uri=REPORTING.synonym_statement_count,
    name="summaryStatisticCollection__synonym_statement_count",
    curie=REPORTING.curie("synonym_statement_count"),
    model_uri=REPORTING.summaryStatisticCollection__synonym_statement_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__synonym_statement_count_by_predicate = Slot(
    uri=REPORTING.synonym_statement_count_by_predicate,
    name="summaryStatisticCollection__synonym_statement_count_by_predicate",
    curie=REPORTING.curie("synonym_statement_count_by_predicate"),
    model_uri=REPORTING.summaryStatisticCollection__synonym_statement_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__class_count_by_subset = Slot(
    uri=REPORTING.class_count_by_subset,
    name="summaryStatisticCollection__class_count_by_subset",
    curie=REPORTING.curie("class_count_by_subset"),
    model_uri=REPORTING.summaryStatisticCollection__class_count_by_subset,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__class_count_by_category = Slot(
    uri=REPORTING.class_count_by_category,
    name="summaryStatisticCollection__class_count_by_category",
    curie=REPORTING.curie("class_count_by_category"),
    model_uri=REPORTING.summaryStatisticCollection__class_count_by_category,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__mapping_count = Slot(
    uri=REPORTING.mapping_count,
    name="summaryStatisticCollection__mapping_count",
    curie=REPORTING.curie("mapping_count"),
    model_uri=REPORTING.summaryStatisticCollection__mapping_count,
    domain=None,
    range=Optional[int],
)

slots.summaryStatisticCollection__mapping_statement_count_by_predicate = Slot(
    uri=REPORTING.mapping_statement_count_by_predicate,
    name="summaryStatisticCollection__mapping_statement_count_by_predicate",
    curie=REPORTING.curie("mapping_statement_count_by_predicate"),
    model_uri=REPORTING.summaryStatisticCollection__mapping_statement_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.summaryStatisticCollection__ontology_count = Slot(
    uri=REPORTING.ontology_count,
    name="summaryStatisticCollection__ontology_count",
    curie=REPORTING.curie("ontology_count"),
    model_uri=REPORTING.summaryStatisticCollection__ontology_count,
    domain=None,
    range=Optional[int],
)

slots.globalStatistics__description = Slot(
    uri=REPORTING.description,
    name="globalStatistics__description",
    curie=REPORTING.curie("description"),
    model_uri=REPORTING.globalStatistics__description,
    domain=None,
    range=Optional[str],
)

slots.globalStatistics__partitions = Slot(
    uri=REPORTING.partitions,
    name="globalStatistics__partitions",
    curie=REPORTING.curie("partitions"),
    model_uri=REPORTING.globalStatistics__partitions,
    domain=None,
    range=Optional[
        Union[
            Union[dict, SummaryStatisticCollection], List[Union[dict, SummaryStatisticCollection]]
        ]
    ],
)

slots.facetedCount__facet = Slot(
    uri=REPORTING.facet,
    name="facetedCount__facet",
    curie=REPORTING.curie("facet"),
    model_uri=REPORTING.facetedCount__facet,
    domain=None,
    range=URIRef,
)

slots.facetedCount__filtered_count = Slot(
    uri=REPORTING.filtered_count,
    name="facetedCount__filtered_count",
    curie=REPORTING.curie("filtered_count"),
    model_uri=REPORTING.facetedCount__filtered_count,
    domain=None,
    range=int,
)
