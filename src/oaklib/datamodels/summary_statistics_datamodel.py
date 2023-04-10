# Auto generated from summary_statistics_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-04-09T15:53:54
# Schema: summary-statistics
#
# id: https://w3id.org/oak/summary_statistics
# description: A datamodel for reports on data
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
from linkml_runtime.linkml_model.types import Datetime, Integer, String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    URIorCURIE,
    XSDDateTime,
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
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
SUMMARY_STATISTICS = CurieNamespace(
    "summary_statistics", "https://w3id.org/oaklib/summary_statistics."
)
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = SUMMARY_STATISTICS


# Types


# Class references
class FacetedCountFacet(extended_str):
    pass


class ChangeTypeStatisticFacet(extended_str):
    pass


class ContributorStatisticsContributorId(URIorCURIE):
    pass


class OntologyId(extended_str):
    pass


class AgentId(extended_str):
    pass


class ContributorRoleId(URIorCURIE):
    pass


@dataclass
class SummaryStatisticsReport(YAMLRoot):
    """
    abstract base class for all summary statistics reports
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.SummaryStatisticsReport
    class_class_curie: ClassVar[str] = "summary_statistics:SummaryStatisticsReport"
    class_name: ClassVar[str] = "SummaryStatisticsReport"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.SummaryStatisticsReport

    id: str = None
    ontologies: Optional[
        Union[Dict[Union[str, OntologyId], Union[dict, "Ontology"]], List[Union[dict, "Ontology"]]]
    ] = empty_dict()
    compared_with: Optional[
        Union[Dict[Union[str, OntologyId], Union[dict, "Ontology"]], List[Union[dict, "Ontology"]]]
    ] = empty_dict()
    was_generated_by: Optional[Union[dict, "SummaryStatisticsCalculationActivity"]] = None
    agents: Optional[
        Union[Dict[Union[str, AgentId], Union[dict, "Agent"]], List[Union[dict, "Agent"]]]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        self._normalize_inlined_as_list(
            slot_name="ontologies", slot_type=Ontology, key_name="id", keyed=True
        )

        self._normalize_inlined_as_list(
            slot_name="compared_with", slot_type=Ontology, key_name="id", keyed=True
        )

        if self.was_generated_by is not None and not isinstance(
            self.was_generated_by, SummaryStatisticsCalculationActivity
        ):
            self.was_generated_by = SummaryStatisticsCalculationActivity(
                **as_dict(self.was_generated_by)
            )

        self._normalize_inlined_as_list(
            slot_name="agents", slot_type=Agent, key_name="id", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass
class GroupedStatistics(SummaryStatisticsReport):
    """
    summary statistics for the entire resource
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.GroupedStatistics
    class_class_curie: ClassVar[str] = "summary_statistics:GroupedStatistics"
    class_name: ClassVar[str] = "GroupedStatistics"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.GroupedStatistics

    id: str = None
    partitions: Optional[
        Union[Union[dict, "UngroupedStatistics"], List[Union[dict, "UngroupedStatistics"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(
            slot_name="partitions", slot_type=UngroupedStatistics, key_name="id", keyed=False
        )

        super().__post_init__(**kwargs)


@dataclass
class UngroupedStatistics(SummaryStatisticsReport):
    """
    A summary statistics report object
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.UngroupedStatistics
    class_class_curie: ClassVar[str] = "summary_statistics:UngroupedStatistics"
    class_name: ClassVar[str] = "UngroupedStatistics"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.UngroupedStatistics

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
    mapping_statement_count_by_object_source: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    mapping_statement_count_subject_by_object_source: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, "FacetedCount"]],
            List[Union[dict, "FacetedCount"]],
        ]
    ] = empty_dict()
    ontology_count: Optional[int] = None
    contributor_summary: Optional[
        Union[
            Dict[
                Union[str, ContributorStatisticsContributorId], Union[dict, "ContributorStatistics"]
            ],
            List[Union[dict, "ContributorStatistics"]],
        ]
    ] = empty_dict()
    change_summary: Optional[
        Union[
            Dict[Union[str, ChangeTypeStatisticFacet], Union[dict, "ChangeTypeStatistic"]],
            List[Union[dict, "ChangeTypeStatistic"]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
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

        self._normalize_inlined_as_dict(
            slot_name="mapping_statement_count_by_object_source",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        self._normalize_inlined_as_dict(
            slot_name="mapping_statement_count_subject_by_object_source",
            slot_type=FacetedCount,
            key_name="facet",
            keyed=True,
        )

        if self.ontology_count is not None and not isinstance(self.ontology_count, int):
            self.ontology_count = int(self.ontology_count)

        self._normalize_inlined_as_dict(
            slot_name="contributor_summary",
            slot_type=ContributorStatistics,
            key_name="contributor_id",
            keyed=True,
        )

        self._normalize_inlined_as_dict(
            slot_name="change_summary", slot_type=ChangeTypeStatistic, key_name="facet", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass
class FacetedCount(YAMLRoot):
    """
    Counts broken down by a facet
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.FacetedCount
    class_class_curie: ClassVar[str] = "summary_statistics:FacetedCount"
    class_name: ClassVar[str] = "FacetedCount"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.FacetedCount

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


@dataclass
class ChangeTypeStatistic(YAMLRoot):
    """
    statistics for a particular kind of diff
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.ChangeTypeStatistic
    class_class_curie: ClassVar[str] = "summary_statistics:ChangeTypeStatistic"
    class_name: ClassVar[str] = "ChangeTypeStatistic"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.ChangeTypeStatistic

    facet: Union[str, ChangeTypeStatisticFacet] = None
    filtered_count: int = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.facet):
            self.MissingRequiredField("facet")
        if not isinstance(self.facet, ChangeTypeStatisticFacet):
            self.facet = ChangeTypeStatisticFacet(self.facet)

        if self._is_empty(self.filtered_count):
            self.MissingRequiredField("filtered_count")
        if not isinstance(self.filtered_count, int):
            self.filtered_count = int(self.filtered_count)

        super().__post_init__(**kwargs)


@dataclass
class ContributorStatistics(YAMLRoot):
    """
    Statistics for a contributor
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.ContributorStatistics
    class_class_curie: ClassVar[str] = "summary_statistics:ContributorStatistics"
    class_name: ClassVar[str] = "ContributorStatistics"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.ContributorStatistics

    contributor_id: Union[str, ContributorStatisticsContributorId] = None
    contributor_name: Optional[str] = None
    normalization_comments: Optional[str] = None
    role_counts: Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.contributor_id):
            self.MissingRequiredField("contributor_id")
        if not isinstance(self.contributor_id, ContributorStatisticsContributorId):
            self.contributor_id = ContributorStatisticsContributorId(self.contributor_id)

        if self.contributor_name is not None and not isinstance(self.contributor_name, str):
            self.contributor_name = str(self.contributor_name)

        if self.normalization_comments is not None and not isinstance(
            self.normalization_comments, str
        ):
            self.normalization_comments = str(self.normalization_comments)

        self._normalize_inlined_as_dict(
            slot_name="role_counts", slot_type=FacetedCount, key_name="facet", keyed=True
        )

        super().__post_init__(**kwargs)


@dataclass
class Ontology(YAMLRoot):
    """
    An ontology
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Ontology
    class_class_curie: ClassVar[str] = "owl:Ontology"
    class_name: ClassVar[str] = "Ontology"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.Ontology

    id: Union[str, OntologyId] = None
    description: Optional[str] = None
    title: Optional[str] = None
    prefix: Optional[str] = None
    version: Optional[str] = None
    version_info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyId):
            self.id = OntologyId(self.id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.version_info is not None and not isinstance(self.version_info, str):
            self.version_info = str(self.version_info)

        super().__post_init__(**kwargs)


@dataclass
class SummaryStatisticsCalculationActivity(YAMLRoot):
    """
    An activity that calculates summary statistics for an ontology
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.SummaryStatisticsCalculationActivity
    class_class_curie: ClassVar[str] = "summary_statistics:SummaryStatisticsCalculationActivity"
    class_name: ClassVar[str] = "SummaryStatisticsCalculationActivity"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.SummaryStatisticsCalculationActivity

    started_at_time: Optional[Union[str, XSDDateTime]] = None
    ended_at_time: Optional[Union[str, XSDDateTime]] = None
    was_associated_with: Optional[Union[str, AgentId]] = None
    acted_on_behalf_of: Optional[Union[str, AgentId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDateTime):
            self.started_at_time = XSDDateTime(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDateTime):
            self.ended_at_time = XSDDateTime(self.ended_at_time)

        if self.was_associated_with is not None and not isinstance(
            self.was_associated_with, AgentId
        ):
            self.was_associated_with = AgentId(self.was_associated_with)

        if self.acted_on_behalf_of is not None and not isinstance(self.acted_on_behalf_of, AgentId):
            self.acted_on_behalf_of = AgentId(self.acted_on_behalf_of)

        super().__post_init__(**kwargs)


@dataclass
class Agent(YAMLRoot):
    """
    An agent
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Agent
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.Agent

    id: Union[str, AgentId] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class ContributorRole(YAMLRoot):
    """
    A role that a contributor can have
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ContributorRole
    class_class_curie: ClassVar[str] = "sh:ContributorRole"
    class_name: ClassVar[str] = "ContributorRole"
    class_model_uri: ClassVar[URIRef] = SUMMARY_STATISTICS.ContributorRole

    id: Union[str, ContributorRoleId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ContributorRoleId):
            self.id = ContributorRoleId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.count_statistic = Slot(
    uri=SUMMARY_STATISTICS.count_statistic,
    name="count_statistic",
    curie=SUMMARY_STATISTICS.curie("count_statistic"),
    model_uri=SUMMARY_STATISTICS.count_statistic,
    domain=None,
    range=Optional[int],
)

slots.class_statistic_group = Slot(
    uri=SUMMARY_STATISTICS.class_statistic_group,
    name="class_statistic_group",
    curie=SUMMARY_STATISTICS.curie("class_statistic_group"),
    model_uri=SUMMARY_STATISTICS.class_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.property_statistic_group = Slot(
    uri=SUMMARY_STATISTICS.property_statistic_group,
    name="property_statistic_group",
    curie=SUMMARY_STATISTICS.curie("property_statistic_group"),
    model_uri=SUMMARY_STATISTICS.property_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.individual_statistic_group = Slot(
    uri=SUMMARY_STATISTICS.individual_statistic_group,
    name="individual_statistic_group",
    curie=SUMMARY_STATISTICS.curie("individual_statistic_group"),
    model_uri=SUMMARY_STATISTICS.individual_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.metadata_statistic_group = Slot(
    uri=SUMMARY_STATISTICS.metadata_statistic_group,
    name="metadata_statistic_group",
    curie=SUMMARY_STATISTICS.curie("metadata_statistic_group"),
    model_uri=SUMMARY_STATISTICS.metadata_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.owl_statistic_group = Slot(
    uri=SUMMARY_STATISTICS.owl_statistic_group,
    name="owl_statistic_group",
    curie=SUMMARY_STATISTICS.curie("owl_statistic_group"),
    model_uri=SUMMARY_STATISTICS.owl_statistic_group,
    domain=None,
    range=Optional[str],
)

slots.summaryStatisticsReport__id = Slot(
    uri=SUMMARY_STATISTICS.id,
    name="summaryStatisticsReport__id",
    curie=SUMMARY_STATISTICS.curie("id"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsReport__id,
    domain=None,
    range=str,
)

slots.summaryStatisticsReport__ontologies = Slot(
    uri=SUMMARY_STATISTICS.ontologies,
    name="summaryStatisticsReport__ontologies",
    curie=SUMMARY_STATISTICS.curie("ontologies"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsReport__ontologies,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, OntologyId], Union[dict, Ontology]], List[Union[dict, Ontology]]]
    ],
)

slots.summaryStatisticsReport__compared_with = Slot(
    uri=SUMMARY_STATISTICS.compared_with,
    name="summaryStatisticsReport__compared_with",
    curie=SUMMARY_STATISTICS.curie("compared_with"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsReport__compared_with,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, OntologyId], Union[dict, Ontology]], List[Union[dict, Ontology]]]
    ],
)

slots.summaryStatisticsReport__was_generated_by = Slot(
    uri=SUMMARY_STATISTICS.was_generated_by,
    name="summaryStatisticsReport__was_generated_by",
    curie=SUMMARY_STATISTICS.curie("was_generated_by"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsReport__was_generated_by,
    domain=None,
    range=Optional[Union[dict, SummaryStatisticsCalculationActivity]],
)

slots.summaryStatisticsReport__agents = Slot(
    uri=SUMMARY_STATISTICS.agents,
    name="summaryStatisticsReport__agents",
    curie=SUMMARY_STATISTICS.curie("agents"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsReport__agents,
    domain=None,
    range=Optional[Union[Dict[Union[str, AgentId], Union[dict, Agent]], List[Union[dict, Agent]]]],
)

slots.groupedStatistics__partitions = Slot(
    uri=SUMMARY_STATISTICS.partitions,
    name="groupedStatistics__partitions",
    curie=SUMMARY_STATISTICS.curie("partitions"),
    model_uri=SUMMARY_STATISTICS.groupedStatistics__partitions,
    domain=None,
    range=Optional[Union[Union[dict, UngroupedStatistics], List[Union[dict, UngroupedStatistics]]]],
)

slots.ungroupedStatistics__class_count = Slot(
    uri=SUMMARY_STATISTICS.class_count,
    name="ungroupedStatistics__class_count",
    curie=SUMMARY_STATISTICS.curie("class_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__class_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__anonymous_class_expression_count = Slot(
    uri=SUMMARY_STATISTICS.anonymous_class_expression_count,
    name="ungroupedStatistics__anonymous_class_expression_count",
    curie=SUMMARY_STATISTICS.curie("anonymous_class_expression_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__anonymous_class_expression_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__unsatisfiable_class_count = Slot(
    uri=SUMMARY_STATISTICS.unsatisfiable_class_count,
    name="ungroupedStatistics__unsatisfiable_class_count",
    curie=SUMMARY_STATISTICS.curie("unsatisfiable_class_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__unsatisfiable_class_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__deprecated_class_count = Slot(
    uri=SUMMARY_STATISTICS.deprecated_class_count,
    name="ungroupedStatistics__deprecated_class_count",
    curie=SUMMARY_STATISTICS.curie("deprecated_class_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__deprecated_class_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__non_deprecated_class_count = Slot(
    uri=SUMMARY_STATISTICS.non_deprecated_class_count,
    name="ungroupedStatistics__non_deprecated_class_count",
    curie=SUMMARY_STATISTICS.curie("non_deprecated_class_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__non_deprecated_class_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__merged_class_count = Slot(
    uri=SUMMARY_STATISTICS.merged_class_count,
    name="ungroupedStatistics__merged_class_count",
    curie=SUMMARY_STATISTICS.curie("merged_class_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__merged_class_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__class_count_with_text_definitions = Slot(
    uri=SUMMARY_STATISTICS.class_count_with_text_definitions,
    name="ungroupedStatistics__class_count_with_text_definitions",
    curie=SUMMARY_STATISTICS.curie("class_count_with_text_definitions"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__class_count_with_text_definitions,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__class_count_without_text_definitions = Slot(
    uri=SUMMARY_STATISTICS.class_count_without_text_definitions,
    name="ungroupedStatistics__class_count_without_text_definitions",
    curie=SUMMARY_STATISTICS.curie("class_count_without_text_definitions"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__class_count_without_text_definitions,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__property_count = Slot(
    uri=SUMMARY_STATISTICS.property_count,
    name="ungroupedStatistics__property_count",
    curie=SUMMARY_STATISTICS.curie("property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__object_property_count = Slot(
    uri=SUMMARY_STATISTICS.object_property_count,
    name="ungroupedStatistics__object_property_count",
    curie=SUMMARY_STATISTICS.curie("object_property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__object_property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__deprecated_object_property_count = Slot(
    uri=SUMMARY_STATISTICS.deprecated_object_property_count,
    name="ungroupedStatistics__deprecated_object_property_count",
    curie=SUMMARY_STATISTICS.curie("deprecated_object_property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__deprecated_object_property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__non_deprecated_object_property_count = Slot(
    uri=SUMMARY_STATISTICS.non_deprecated_object_property_count,
    name="ungroupedStatistics__non_deprecated_object_property_count",
    curie=SUMMARY_STATISTICS.curie("non_deprecated_object_property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__non_deprecated_object_property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__datatype_property_count = Slot(
    uri=SUMMARY_STATISTICS.datatype_property_count,
    name="ungroupedStatistics__datatype_property_count",
    curie=SUMMARY_STATISTICS.curie("datatype_property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__datatype_property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__annotation_property_count = Slot(
    uri=SUMMARY_STATISTICS.annotation_property_count,
    name="ungroupedStatistics__annotation_property_count",
    curie=SUMMARY_STATISTICS.curie("annotation_property_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__annotation_property_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__individual_count = Slot(
    uri=SUMMARY_STATISTICS.individual_count,
    name="ungroupedStatistics__individual_count",
    curie=SUMMARY_STATISTICS.curie("individual_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__individual_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__named_individual_count = Slot(
    uri=SUMMARY_STATISTICS.named_individual_count,
    name="ungroupedStatistics__named_individual_count",
    curie=SUMMARY_STATISTICS.curie("named_individual_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__named_individual_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__anonymous_individual_count = Slot(
    uri=SUMMARY_STATISTICS.anonymous_individual_count,
    name="ungroupedStatistics__anonymous_individual_count",
    curie=SUMMARY_STATISTICS.curie("anonymous_individual_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__anonymous_individual_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__untyped_entity_count = Slot(
    uri=SUMMARY_STATISTICS.untyped_entity_count,
    name="ungroupedStatistics__untyped_entity_count",
    curie=SUMMARY_STATISTICS.curie("untyped_entity_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__untyped_entity_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__subset_count = Slot(
    uri=SUMMARY_STATISTICS.subset_count,
    name="ungroupedStatistics__subset_count",
    curie=SUMMARY_STATISTICS.curie("subset_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__subset_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__description_logic_profile = Slot(
    uri=SUMMARY_STATISTICS.description_logic_profile,
    name="ungroupedStatistics__description_logic_profile",
    curie=SUMMARY_STATISTICS.curie("description_logic_profile"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__description_logic_profile,
    domain=None,
    range=Optional[str],
)

slots.ungroupedStatistics__owl_axiom_count = Slot(
    uri=SUMMARY_STATISTICS.owl_axiom_count,
    name="ungroupedStatistics__owl_axiom_count",
    curie=SUMMARY_STATISTICS.curie("owl_axiom_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__owl_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__rdf_triple_count = Slot(
    uri=SUMMARY_STATISTICS.rdf_triple_count,
    name="ungroupedStatistics__rdf_triple_count",
    curie=SUMMARY_STATISTICS.curie("rdf_triple_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__rdf_triple_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__subclass_of_axiom_count = Slot(
    uri=SUMMARY_STATISTICS.subclass_of_axiom_count,
    name="ungroupedStatistics__subclass_of_axiom_count",
    curie=SUMMARY_STATISTICS.curie("subclass_of_axiom_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__subclass_of_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__equivalent_classes_axiom_count = Slot(
    uri=SUMMARY_STATISTICS.equivalent_classes_axiom_count,
    name="ungroupedStatistics__equivalent_classes_axiom_count",
    curie=SUMMARY_STATISTICS.curie("equivalent_classes_axiom_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__equivalent_classes_axiom_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__edge_count_by_predicate = Slot(
    uri=SUMMARY_STATISTICS.edge_count_by_predicate,
    name="ungroupedStatistics__edge_count_by_predicate",
    curie=SUMMARY_STATISTICS.curie("edge_count_by_predicate"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__edge_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__entailed_edge_count_by_predicate = Slot(
    uri=SUMMARY_STATISTICS.entailed_edge_count_by_predicate,
    name="ungroupedStatistics__entailed_edge_count_by_predicate",
    curie=SUMMARY_STATISTICS.curie("entailed_edge_count_by_predicate"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__entailed_edge_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__distinct_synonym_count = Slot(
    uri=SUMMARY_STATISTICS.distinct_synonym_count,
    name="ungroupedStatistics__distinct_synonym_count",
    curie=SUMMARY_STATISTICS.curie("distinct_synonym_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__distinct_synonym_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__synonym_statement_count = Slot(
    uri=SUMMARY_STATISTICS.synonym_statement_count,
    name="ungroupedStatistics__synonym_statement_count",
    curie=SUMMARY_STATISTICS.curie("synonym_statement_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__synonym_statement_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__synonym_statement_count_by_predicate = Slot(
    uri=SUMMARY_STATISTICS.synonym_statement_count_by_predicate,
    name="ungroupedStatistics__synonym_statement_count_by_predicate",
    curie=SUMMARY_STATISTICS.curie("synonym_statement_count_by_predicate"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__synonym_statement_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__class_count_by_subset = Slot(
    uri=SUMMARY_STATISTICS.class_count_by_subset,
    name="ungroupedStatistics__class_count_by_subset",
    curie=SUMMARY_STATISTICS.curie("class_count_by_subset"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__class_count_by_subset,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__class_count_by_category = Slot(
    uri=SUMMARY_STATISTICS.class_count_by_category,
    name="ungroupedStatistics__class_count_by_category",
    curie=SUMMARY_STATISTICS.curie("class_count_by_category"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__class_count_by_category,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__mapping_count = Slot(
    uri=SUMMARY_STATISTICS.mapping_count,
    name="ungroupedStatistics__mapping_count",
    curie=SUMMARY_STATISTICS.curie("mapping_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__mapping_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__mapping_statement_count_by_predicate = Slot(
    uri=SUMMARY_STATISTICS.mapping_statement_count_by_predicate,
    name="ungroupedStatistics__mapping_statement_count_by_predicate",
    curie=SUMMARY_STATISTICS.curie("mapping_statement_count_by_predicate"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__mapping_statement_count_by_predicate,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__mapping_statement_count_by_object_source = Slot(
    uri=SUMMARY_STATISTICS.mapping_statement_count_by_object_source,
    name="ungroupedStatistics__mapping_statement_count_by_object_source",
    curie=SUMMARY_STATISTICS.curie("mapping_statement_count_by_object_source"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__mapping_statement_count_by_object_source,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__mapping_statement_count_subject_by_object_source = Slot(
    uri=SUMMARY_STATISTICS.mapping_statement_count_subject_by_object_source,
    name="ungroupedStatistics__mapping_statement_count_subject_by_object_source",
    curie=SUMMARY_STATISTICS.curie("mapping_statement_count_subject_by_object_source"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__mapping_statement_count_subject_by_object_source,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ungroupedStatistics__ontology_count = Slot(
    uri=SUMMARY_STATISTICS.ontology_count,
    name="ungroupedStatistics__ontology_count",
    curie=SUMMARY_STATISTICS.curie("ontology_count"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__ontology_count,
    domain=None,
    range=Optional[int],
)

slots.ungroupedStatistics__contributor_summary = Slot(
    uri=SUMMARY_STATISTICS.contributor_summary,
    name="ungroupedStatistics__contributor_summary",
    curie=SUMMARY_STATISTICS.curie("contributor_summary"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__contributor_summary,
    domain=None,
    range=Optional[
        Union[
            Dict[
                Union[str, ContributorStatisticsContributorId], Union[dict, ContributorStatistics]
            ],
            List[Union[dict, ContributorStatistics]],
        ]
    ],
)

slots.ungroupedStatistics__change_summary = Slot(
    uri=SUMMARY_STATISTICS.change_summary,
    name="ungroupedStatistics__change_summary",
    curie=SUMMARY_STATISTICS.curie("change_summary"),
    model_uri=SUMMARY_STATISTICS.ungroupedStatistics__change_summary,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, ChangeTypeStatisticFacet], Union[dict, ChangeTypeStatistic]],
            List[Union[dict, ChangeTypeStatistic]],
        ]
    ],
)

slots.facetedCount__facet = Slot(
    uri=SUMMARY_STATISTICS.facet,
    name="facetedCount__facet",
    curie=SUMMARY_STATISTICS.curie("facet"),
    model_uri=SUMMARY_STATISTICS.facetedCount__facet,
    domain=None,
    range=URIRef,
)

slots.facetedCount__filtered_count = Slot(
    uri=SUMMARY_STATISTICS.filtered_count,
    name="facetedCount__filtered_count",
    curie=SUMMARY_STATISTICS.curie("filtered_count"),
    model_uri=SUMMARY_STATISTICS.facetedCount__filtered_count,
    domain=None,
    range=int,
)

slots.changeTypeStatistic__facet = Slot(
    uri=SUMMARY_STATISTICS.facet,
    name="changeTypeStatistic__facet",
    curie=SUMMARY_STATISTICS.curie("facet"),
    model_uri=SUMMARY_STATISTICS.changeTypeStatistic__facet,
    domain=None,
    range=URIRef,
)

slots.changeTypeStatistic__filtered_count = Slot(
    uri=SUMMARY_STATISTICS.filtered_count,
    name="changeTypeStatistic__filtered_count",
    curie=SUMMARY_STATISTICS.curie("filtered_count"),
    model_uri=SUMMARY_STATISTICS.changeTypeStatistic__filtered_count,
    domain=None,
    range=int,
)

slots.contributorStatistics__contributor_id = Slot(
    uri=SUMMARY_STATISTICS.contributor_id,
    name="contributorStatistics__contributor_id",
    curie=SUMMARY_STATISTICS.curie("contributor_id"),
    model_uri=SUMMARY_STATISTICS.contributorStatistics__contributor_id,
    domain=None,
    range=URIRef,
)

slots.contributorStatistics__contributor_name = Slot(
    uri=SUMMARY_STATISTICS.contributor_name,
    name="contributorStatistics__contributor_name",
    curie=SUMMARY_STATISTICS.curie("contributor_name"),
    model_uri=SUMMARY_STATISTICS.contributorStatistics__contributor_name,
    domain=None,
    range=Optional[str],
)

slots.contributorStatistics__normalization_comments = Slot(
    uri=SUMMARY_STATISTICS.normalization_comments,
    name="contributorStatistics__normalization_comments",
    curie=SUMMARY_STATISTICS.curie("normalization_comments"),
    model_uri=SUMMARY_STATISTICS.contributorStatistics__normalization_comments,
    domain=None,
    range=Optional[str],
)

slots.contributorStatistics__role_counts = Slot(
    uri=SUMMARY_STATISTICS.role_counts,
    name="contributorStatistics__role_counts",
    curie=SUMMARY_STATISTICS.curie("role_counts"),
    model_uri=SUMMARY_STATISTICS.contributorStatistics__role_counts,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, FacetedCountFacet], Union[dict, FacetedCount]],
            List[Union[dict, FacetedCount]],
        ]
    ],
)

slots.ontology__id = Slot(
    uri=SUMMARY_STATISTICS.id,
    name="ontology__id",
    curie=SUMMARY_STATISTICS.curie("id"),
    model_uri=SUMMARY_STATISTICS.ontology__id,
    domain=None,
    range=URIRef,
)

slots.ontology__description = Slot(
    uri=DCTERMS.description,
    name="ontology__description",
    curie=DCTERMS.curie("description"),
    model_uri=SUMMARY_STATISTICS.ontology__description,
    domain=None,
    range=Optional[str],
)

slots.ontology__title = Slot(
    uri=DCTERMS.title,
    name="ontology__title",
    curie=DCTERMS.curie("title"),
    model_uri=SUMMARY_STATISTICS.ontology__title,
    domain=None,
    range=Optional[str],
)

slots.ontology__prefix = Slot(
    uri=SH.prefix,
    name="ontology__prefix",
    curie=SH.curie("prefix"),
    model_uri=SUMMARY_STATISTICS.ontology__prefix,
    domain=None,
    range=Optional[str],
)

slots.ontology__version = Slot(
    uri=OWL.versionIRI,
    name="ontology__version",
    curie=OWL.curie("versionIRI"),
    model_uri=SUMMARY_STATISTICS.ontology__version,
    domain=None,
    range=Optional[str],
)

slots.ontology__version_info = Slot(
    uri=OWL.versionInfo,
    name="ontology__version_info",
    curie=OWL.curie("versionInfo"),
    model_uri=SUMMARY_STATISTICS.ontology__version_info,
    domain=None,
    range=Optional[str],
)

slots.summaryStatisticsCalculationActivity__started_at_time = Slot(
    uri=PROV.startedAtTime,
    name="summaryStatisticsCalculationActivity__started_at_time",
    curie=PROV.curie("startedAtTime"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsCalculationActivity__started_at_time,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.summaryStatisticsCalculationActivity__ended_at_time = Slot(
    uri=PROV.endedAtTime,
    name="summaryStatisticsCalculationActivity__ended_at_time",
    curie=PROV.curie("endedAtTime"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsCalculationActivity__ended_at_time,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.summaryStatisticsCalculationActivity__was_associated_with = Slot(
    uri=PROV.wasAssociatedWith,
    name="summaryStatisticsCalculationActivity__was_associated_with",
    curie=PROV.curie("wasAssociatedWith"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsCalculationActivity__was_associated_with,
    domain=None,
    range=Optional[Union[str, AgentId]],
)

slots.summaryStatisticsCalculationActivity__acted_on_behalf_of = Slot(
    uri=PROV.actedOnBehalfOf,
    name="summaryStatisticsCalculationActivity__acted_on_behalf_of",
    curie=PROV.curie("actedOnBehalfOf"),
    model_uri=SUMMARY_STATISTICS.summaryStatisticsCalculationActivity__acted_on_behalf_of,
    domain=None,
    range=Optional[Union[str, AgentId]],
)

slots.agent__id = Slot(
    uri=SUMMARY_STATISTICS.id,
    name="agent__id",
    curie=SUMMARY_STATISTICS.curie("id"),
    model_uri=SUMMARY_STATISTICS.agent__id,
    domain=None,
    range=URIRef,
)

slots.agent__label = Slot(
    uri=RDFS.label,
    name="agent__label",
    curie=RDFS.curie("label"),
    model_uri=SUMMARY_STATISTICS.agent__label,
    domain=None,
    range=Optional[str],
)

slots.contributorRole__id = Slot(
    uri=SUMMARY_STATISTICS.id,
    name="contributorRole__id",
    curie=SUMMARY_STATISTICS.curie("id"),
    model_uri=SUMMARY_STATISTICS.contributorRole__id,
    domain=None,
    range=URIRef,
)
