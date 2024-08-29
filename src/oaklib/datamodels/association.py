# Auto generated from association.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-08-07T13:29:21
# Schema: association
#
# id: https://w3id.org/oak/association
# description: A data model for representing generic associations and changes of these associations.
#
#   The core data model is broad, encompassing the W3 Open Annotation data model as well
#   as common ontology annotation data models using in the biosciences, such as the GAF
#   data model used by the Gene Ontology, and the HPOA association model used by the Human Phenotype
#   Ontology.
#
#   The core elements of the data model are the *subject* (the entity being described) and the *object*
#   (the term, descriptor, or other entity that describes some aspect of the subject).
#
#   A subject might be a biological entity such as gene, drug, disease, person, or chemical. The object is typically
#   a class from an ontology such as a term from GO.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/vocab/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OA = CurieNamespace('oa', 'http://www.w3.org/ns/oa#')
ONTOASSOC = CurieNamespace('ontoassoc', 'https://w3id.org/oak/association/')
RDF = CurieNamespace('rdf', 'http://example.org/UNKNOWN/rdf/')
RDFS = CurieNamespace('rdfs', 'http://example.org/UNKNOWN/rdfs/')
SSSOM = CurieNamespace('sssom', 'https://w3id.org/sssom/')
DEFAULT_ = ONTOASSOC


# Types

# Class references



@dataclass
class PositiveOrNegativeAssociation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["PositiveOrNegativeAssociation"]
    class_class_curie: ClassVar[str] = "ontoassoc:PositiveOrNegativeAssociation"
    class_name: ClassVar[str] = "PositiveOrNegativeAssociation"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.PositiveOrNegativeAssociation

    subject: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None
    property_values: Optional[Union[Union[dict, "PropertyValue"], List[Union[dict, "PropertyValue"]]]] = empty_list()
    subject_label: Optional[str] = None
    predicate_label: Optional[str] = None
    object_label: Optional[str] = None
    negated: Optional[Union[bool, Bool]] = None
    publications: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    evidence_type: Optional[Union[str, URIorCURIE]] = None
    supporting_objects: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    primary_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    aggregator_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    subject_closure: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    subject_closure_label: Optional[Union[str, List[str]]] = empty_list()
    object_closure: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    object_closure_label: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        if not isinstance(self.property_values, list):
            self.property_values = [self.property_values] if self.property_values is not None else []
        self.property_values = [v if isinstance(v, PropertyValue) else PropertyValue(**as_dict(v)) for v in self.property_values]

        if self.subject_label is not None and not isinstance(self.subject_label, str):
            self.subject_label = str(self.subject_label)

        if self.predicate_label is not None and not isinstance(self.predicate_label, str):
            self.predicate_label = str(self.predicate_label)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        if not isinstance(self.publications, list):
            self.publications = [self.publications] if self.publications is not None else []
        self.publications = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.publications]

        if self.evidence_type is not None and not isinstance(self.evidence_type, URIorCURIE):
            self.evidence_type = URIorCURIE(self.evidence_type)

        if not isinstance(self.supporting_objects, list):
            self.supporting_objects = [self.supporting_objects] if self.supporting_objects is not None else []
        self.supporting_objects = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.supporting_objects]

        if self.primary_knowledge_source is not None and not isinstance(self.primary_knowledge_source, URIorCURIE):
            self.primary_knowledge_source = URIorCURIE(self.primary_knowledge_source)

        if self.aggregator_knowledge_source is not None and not isinstance(self.aggregator_knowledge_source, URIorCURIE):
            self.aggregator_knowledge_source = URIorCURIE(self.aggregator_knowledge_source)

        if not isinstance(self.subject_closure, list):
            self.subject_closure = [self.subject_closure] if self.subject_closure is not None else []
        self.subject_closure = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.subject_closure]

        if not isinstance(self.subject_closure_label, list):
            self.subject_closure_label = [self.subject_closure_label] if self.subject_closure_label is not None else []
        self.subject_closure_label = [v if isinstance(v, str) else str(v) for v in self.subject_closure_label]

        if not isinstance(self.object_closure, list):
            self.object_closure = [self.object_closure] if self.object_closure is not None else []
        self.object_closure = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.object_closure]

        if not isinstance(self.object_closure_label, list):
            self.object_closure_label = [self.object_closure_label] if self.object_closure_label is not None else []
        self.object_closure_label = [v if isinstance(v, str) else str(v) for v in self.object_closure_label]

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        super().__post_init__(**kwargs)


@dataclass
class Association(PositiveOrNegativeAssociation):
    """
    A generic association between a thing (subject) and another thing (object).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OA["Annotation"]
    class_class_curie: ClassVar[str] = "oa:Annotation"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.Association

    negated: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        super().__post_init__(**kwargs)


@dataclass
class NegatedAssociation(PositiveOrNegativeAssociation):
    """
    A negated association between a thing (subject) and another thing (object).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["NegatedAssociation"]
    class_class_curie: ClassVar[str] = "ontoassoc:NegatedAssociation"
    class_name: ClassVar[str] = "NegatedAssociation"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.NegatedAssociation

    negated: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        super().__post_init__(**kwargs)


@dataclass
class PropertyValue(YAMLRoot):
    """
    A generic tag-value that can be associated with an association.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["PropertyValue"]
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

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["RollupGroup"]
    class_class_curie: ClassVar[str] = "ontoassoc:RollupGroup"
    class_name: ClassVar[str] = "RollupGroup"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.RollupGroup

    group_object: Optional[Union[str, URIorCURIE]] = None
    sub_groups: Optional[Union[Union[dict, "RollupGroup"], List[Union[dict, "RollupGroup"]]]] = empty_list()
    associations: Optional[Union[Union[dict, Association], List[Union[dict, Association]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.group_object is not None and not isinstance(self.group_object, URIorCURIE):
            self.group_object = URIorCURIE(self.group_object)

        if not isinstance(self.sub_groups, list):
            self.sub_groups = [self.sub_groups] if self.sub_groups is not None else []
        self.sub_groups = [v if isinstance(v, RollupGroup) else RollupGroup(**as_dict(v)) for v in self.sub_groups]

        if not isinstance(self.associations, list):
            self.associations = [self.associations] if self.associations is not None else []
        self.associations = [v if isinstance(v, Association) else Association(**as_dict(v)) for v in self.associations]

        super().__post_init__(**kwargs)


@dataclass
class PairwiseCoAssociation(YAMLRoot):
    """
    A collection of subjects co-associated with two objects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["PairwiseCoAssociation"]
    class_class_curie: ClassVar[str] = "ontoassoc:PairwiseCoAssociation"
    class_name: ClassVar[str] = "PairwiseCoAssociation"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.PairwiseCoAssociation

    object1: Union[str, URIorCURIE] = None
    object2: Union[str, URIorCURIE] = None
    object1_label: Optional[str] = None
    object2_label: Optional[str] = None
    number_subjects_in_common: Optional[int] = None
    proportion_subjects_in_common: Optional[float] = None
    number_subjects_in_union: Optional[int] = None
    number_subject_unique_to_entity1: Optional[int] = None
    number_subject_unique_to_entity2: Optional[int] = None
    subjects_in_common: Optional[Union[str, List[str]]] = empty_list()
    associations_for_subjects_in_common: Optional[Union[Union[dict, Association], List[Union[dict, Association]]]] = empty_list()
    proportion_entity1_subjects_in_entity2: Optional[float] = None
    proportion_entity2_subjects_in_entity1: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object1):
            self.MissingRequiredField("object1")
        if not isinstance(self.object1, URIorCURIE):
            self.object1 = URIorCURIE(self.object1)

        if self._is_empty(self.object2):
            self.MissingRequiredField("object2")
        if not isinstance(self.object2, URIorCURIE):
            self.object2 = URIorCURIE(self.object2)

        if self.object1_label is not None and not isinstance(self.object1_label, str):
            self.object1_label = str(self.object1_label)

        if self.object2_label is not None and not isinstance(self.object2_label, str):
            self.object2_label = str(self.object2_label)

        if self.number_subjects_in_common is not None and not isinstance(self.number_subjects_in_common, int):
            self.number_subjects_in_common = int(self.number_subjects_in_common)

        if self.proportion_subjects_in_common is not None and not isinstance(self.proportion_subjects_in_common, float):
            self.proportion_subjects_in_common = float(self.proportion_subjects_in_common)

        if self.number_subjects_in_union is not None and not isinstance(self.number_subjects_in_union, int):
            self.number_subjects_in_union = int(self.number_subjects_in_union)

        if self.number_subject_unique_to_entity1 is not None and not isinstance(self.number_subject_unique_to_entity1, int):
            self.number_subject_unique_to_entity1 = int(self.number_subject_unique_to_entity1)

        if self.number_subject_unique_to_entity2 is not None and not isinstance(self.number_subject_unique_to_entity2, int):
            self.number_subject_unique_to_entity2 = int(self.number_subject_unique_to_entity2)

        if not isinstance(self.subjects_in_common, list):
            self.subjects_in_common = [self.subjects_in_common] if self.subjects_in_common is not None else []
        self.subjects_in_common = [v if isinstance(v, str) else str(v) for v in self.subjects_in_common]

        if not isinstance(self.associations_for_subjects_in_common, list):
            self.associations_for_subjects_in_common = [self.associations_for_subjects_in_common] if self.associations_for_subjects_in_common is not None else []
        self.associations_for_subjects_in_common = [v if isinstance(v, Association) else Association(**as_dict(v)) for v in self.associations_for_subjects_in_common]

        if self.proportion_entity1_subjects_in_entity2 is not None and not isinstance(self.proportion_entity1_subjects_in_entity2, float):
            self.proportion_entity1_subjects_in_entity2 = float(self.proportion_entity1_subjects_in_entity2)

        if self.proportion_entity2_subjects_in_entity1 is not None and not isinstance(self.proportion_entity2_subjects_in_entity1, float):
            self.proportion_entity2_subjects_in_entity1 = float(self.proportion_entity2_subjects_in_entity1)

        super().__post_init__(**kwargs)


@dataclass
class ParserConfiguration(YAMLRoot):
    """
    Settings that determine behavior when parsing associations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["ParserConfiguration"]
    class_class_curie: ClassVar[str] = "ontoassoc:ParserConfiguration"
    class_name: ClassVar[str] = "ParserConfiguration"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.ParserConfiguration

    preserve_negated_associations: Optional[Union[bool, Bool]] = None
    include_association_attributes: Optional[Union[bool, Bool]] = None
    primary_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    aggregator_knowledge_source: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.preserve_negated_associations is not None and not isinstance(self.preserve_negated_associations, Bool):
            self.preserve_negated_associations = Bool(self.preserve_negated_associations)

        if self.include_association_attributes is not None and not isinstance(self.include_association_attributes, Bool):
            self.include_association_attributes = Bool(self.include_association_attributes)

        if self.primary_knowledge_source is not None and not isinstance(self.primary_knowledge_source, URIorCURIE):
            self.primary_knowledge_source = URIorCURIE(self.primary_knowledge_source)

        if self.aggregator_knowledge_source is not None and not isinstance(self.aggregator_knowledge_source, URIorCURIE):
            self.aggregator_knowledge_source = URIorCURIE(self.aggregator_knowledge_source)

        super().__post_init__(**kwargs)


@dataclass
class AssociationChange(YAMLRoot):
    """
    A change object describing a change between two associations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOASSOC["AssociationChange"]
    class_class_curie: ClassVar[str] = "ontoassoc:AssociationChange"
    class_name: ClassVar[str] = "AssociationChange"
    class_model_uri: ClassVar[URIRef] = ONTOASSOC.AssociationChange

    summary_group: Optional[str] = None
    old_date: Optional[str] = None
    new_date: Optional[str] = None
    primary_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    aggregator_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    publications: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    publication_is_added: Optional[Union[bool, Bool]] = None
    publication_is_deleted: Optional[Union[bool, Bool]] = None
    subject: Optional[Union[str, URIorCURIE]] = None
    old_predicate: Optional[Union[str, URIorCURIE]] = None
    new_predicate: Optional[Union[str, URIorCURIE]] = None
    old_object: Optional[Union[str, URIorCURIE]] = None
    new_object: Optional[Union[str, URIorCURIE]] = None
    old_object_obsolete: Optional[Union[bool, Bool]] = None
    is_migration: Optional[Union[bool, Bool]] = None
    is_generalization: Optional[Union[bool, Bool]] = None
    is_specialization: Optional[Union[bool, Bool]] = None
    is_creation: Optional[Union[bool, Bool]] = None
    is_deletion: Optional[Union[bool, Bool]] = None
    closure_predicates: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    closure_delta: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.summary_group is not None and not isinstance(self.summary_group, str):
            self.summary_group = str(self.summary_group)

        if self.old_date is not None and not isinstance(self.old_date, str):
            self.old_date = str(self.old_date)

        if self.new_date is not None and not isinstance(self.new_date, str):
            self.new_date = str(self.new_date)

        if self.primary_knowledge_source is not None and not isinstance(self.primary_knowledge_source, URIorCURIE):
            self.primary_knowledge_source = URIorCURIE(self.primary_knowledge_source)

        if self.aggregator_knowledge_source is not None and not isinstance(self.aggregator_knowledge_source, URIorCURIE):
            self.aggregator_knowledge_source = URIorCURIE(self.aggregator_knowledge_source)

        if not isinstance(self.publications, list):
            self.publications = [self.publications] if self.publications is not None else []
        self.publications = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.publications]

        if self.publication_is_added is not None and not isinstance(self.publication_is_added, Bool):
            self.publication_is_added = Bool(self.publication_is_added)

        if self.publication_is_deleted is not None and not isinstance(self.publication_is_deleted, Bool):
            self.publication_is_deleted = Bool(self.publication_is_deleted)

        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.old_predicate is not None and not isinstance(self.old_predicate, URIorCURIE):
            self.old_predicate = URIorCURIE(self.old_predicate)

        if self.new_predicate is not None and not isinstance(self.new_predicate, URIorCURIE):
            self.new_predicate = URIorCURIE(self.new_predicate)

        if self.old_object is not None and not isinstance(self.old_object, URIorCURIE):
            self.old_object = URIorCURIE(self.old_object)

        if self.new_object is not None and not isinstance(self.new_object, URIorCURIE):
            self.new_object = URIorCURIE(self.new_object)

        if self.old_object_obsolete is not None and not isinstance(self.old_object_obsolete, Bool):
            self.old_object_obsolete = Bool(self.old_object_obsolete)

        if self.is_migration is not None and not isinstance(self.is_migration, Bool):
            self.is_migration = Bool(self.is_migration)

        if self.is_generalization is not None and not isinstance(self.is_generalization, Bool):
            self.is_generalization = Bool(self.is_generalization)

        if self.is_specialization is not None and not isinstance(self.is_specialization, Bool):
            self.is_specialization = Bool(self.is_specialization)

        if self.is_creation is not None and not isinstance(self.is_creation, Bool):
            self.is_creation = Bool(self.is_creation)

        if self.is_deletion is not None and not isinstance(self.is_deletion, Bool):
            self.is_deletion = Bool(self.is_deletion)

        if not isinstance(self.closure_predicates, list):
            self.closure_predicates = [self.closure_predicates] if self.closure_predicates is not None else []
        self.closure_predicates = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.closure_predicates]

        if self.closure_delta is not None and not isinstance(self.closure_delta, int):
            self.closure_delta = int(self.closure_delta)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.subject = Slot(uri=RDF.subject, name="subject", curie=RDF.curie('subject'),
                   model_uri=ONTOASSOC.subject, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.subject_label = Slot(uri=SSSOM.subject_label, name="subject_label", curie=SSSOM.curie('subject_label'),
                   model_uri=ONTOASSOC.subject_label, domain=None, range=Optional[str])

slots.predicate = Slot(uri=RDF.predicate, name="predicate", curie=RDF.curie('predicate'),
                   model_uri=ONTOASSOC.predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.predicate_label = Slot(uri=SSSOM.predicate_label, name="predicate_label", curie=SSSOM.curie('predicate_label'),
                   model_uri=ONTOASSOC.predicate_label, domain=None, range=Optional[str])

slots.object = Slot(uri=RDF.object, name="object", curie=RDF.curie('object'),
                   model_uri=ONTOASSOC.object, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.object_label = Slot(uri=SSSOM.object_label, name="object_label", curie=SSSOM.curie('object_label'),
                   model_uri=ONTOASSOC.object_label, domain=None, range=Optional[str])

slots.core_triple = Slot(uri=ONTOASSOC.core_triple, name="core_triple", curie=ONTOASSOC.curie('core_triple'),
                   model_uri=ONTOASSOC.core_triple, domain=None, range=Optional[str])

slots.negated = Slot(uri=ONTOASSOC.negated, name="negated", curie=ONTOASSOC.curie('negated'),
                   model_uri=ONTOASSOC.negated, domain=None, range=Optional[Union[bool, Bool]])

slots.property_values = Slot(uri=ONTOASSOC.property_values, name="property_values", curie=ONTOASSOC.curie('property_values'),
                   model_uri=ONTOASSOC.property_values, domain=None, range=Optional[Union[Union[dict, PropertyValue], List[Union[dict, PropertyValue]]]])

slots.group_object = Slot(uri=RDF.object, name="group_object", curie=RDF.curie('object'),
                   model_uri=ONTOASSOC.group_object, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.sub_groups = Slot(uri=ONTOASSOC.sub_groups, name="sub_groups", curie=ONTOASSOC.curie('sub_groups'),
                   model_uri=ONTOASSOC.sub_groups, domain=None, range=Optional[Union[Union[dict, RollupGroup], List[Union[dict, RollupGroup]]]])

slots.associations = Slot(uri=ONTOASSOC.associations, name="associations", curie=ONTOASSOC.curie('associations'),
                   model_uri=ONTOASSOC.associations, domain=None, range=Optional[Union[Union[dict, Association], List[Union[dict, Association]]]])

slots.original_subject = Slot(uri=BIOLINK.original_subject, name="original_subject", curie=BIOLINK.curie('original_subject'),
                   model_uri=ONTOASSOC.original_subject, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.original_predicate = Slot(uri=BIOLINK.original_predicate, name="original_predicate", curie=BIOLINK.curie('original_predicate'),
                   model_uri=ONTOASSOC.original_predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.original_object = Slot(uri=BIOLINK.original_object, name="original_object", curie=BIOLINK.curie('original_object'),
                   model_uri=ONTOASSOC.original_object, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.publications = Slot(uri=BIOLINK.publications, name="publications", curie=BIOLINK.curie('publications'),
                   model_uri=ONTOASSOC.publications, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.primary_knowledge_source = Slot(uri=BIOLINK.primary_knowledge_source, name="primary_knowledge_source", curie=BIOLINK.curie('primary_knowledge_source'),
                   model_uri=ONTOASSOC.primary_knowledge_source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.aggregator_knowledge_source = Slot(uri=BIOLINK.aggregator_knowledge_source, name="aggregator_knowledge_source", curie=BIOLINK.curie('aggregator_knowledge_source'),
                   model_uri=ONTOASSOC.aggregator_knowledge_source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.evidence_type = Slot(uri=ONTOASSOC.evidence_type, name="evidence_type", curie=ONTOASSOC.curie('evidence_type'),
                   model_uri=ONTOASSOC.evidence_type, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.supporting_objects = Slot(uri=ONTOASSOC.supporting_objects, name="supporting_objects", curie=ONTOASSOC.curie('supporting_objects'),
                   model_uri=ONTOASSOC.supporting_objects, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.comments = Slot(uri=RDFS.comment, name="comments", curie=RDFS.curie('comment'),
                   model_uri=ONTOASSOC.comments, domain=None, range=Optional[Union[str, List[str]]])

slots.denormalized_slot = Slot(uri=ONTOASSOC.denormalized_slot, name="denormalized_slot", curie=ONTOASSOC.curie('denormalized_slot'),
                   model_uri=ONTOASSOC.denormalized_slot, domain=None, range=Optional[str])

slots.date = Slot(uri=ONTOASSOC.date, name="date", curie=ONTOASSOC.curie('date'),
                   model_uri=ONTOASSOC.date, domain=None, range=Optional[str])

slots.modification_date = Slot(uri=ONTOASSOC.modification_date, name="modification_date", curie=ONTOASSOC.curie('modification_date'),
                   model_uri=ONTOASSOC.modification_date, domain=None, range=Optional[str])

slots.creation_date = Slot(uri=ONTOASSOC.creation_date, name="creation_date", curie=ONTOASSOC.curie('creation_date'),
                   model_uri=ONTOASSOC.creation_date, domain=None, range=Optional[str])

slots.diff_slot = Slot(uri=ONTOASSOC.diff_slot, name="diff_slot", curie=ONTOASSOC.curie('diff_slot'),
                   model_uri=ONTOASSOC.diff_slot, domain=None, range=Optional[str])

slots.old_date = Slot(uri=ONTOASSOC.old_date, name="old_date", curie=ONTOASSOC.curie('old_date'),
                   model_uri=ONTOASSOC.old_date, domain=None, range=Optional[str])

slots.new_date = Slot(uri=ONTOASSOC.new_date, name="new_date", curie=ONTOASSOC.curie('new_date'),
                   model_uri=ONTOASSOC.new_date, domain=None, range=Optional[str])

slots.summary_group = Slot(uri=ONTOASSOC.summary_group, name="summary_group", curie=ONTOASSOC.curie('summary_group'),
                   model_uri=ONTOASSOC.summary_group, domain=None, range=Optional[str])

slots.publication_is_added = Slot(uri=ONTOASSOC.publication_is_added, name="publication_is_added", curie=ONTOASSOC.curie('publication_is_added'),
                   model_uri=ONTOASSOC.publication_is_added, domain=None, range=Optional[Union[bool, Bool]])

slots.publication_is_deleted = Slot(uri=ONTOASSOC.publication_is_deleted, name="publication_is_deleted", curie=ONTOASSOC.curie('publication_is_deleted'),
                   model_uri=ONTOASSOC.publication_is_deleted, domain=None, range=Optional[Union[bool, Bool]])

slots.old_predicate = Slot(uri=ONTOASSOC.old_predicate, name="old_predicate", curie=ONTOASSOC.curie('old_predicate'),
                   model_uri=ONTOASSOC.old_predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.new_predicate = Slot(uri=ONTOASSOC.new_predicate, name="new_predicate", curie=ONTOASSOC.curie('new_predicate'),
                   model_uri=ONTOASSOC.new_predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.old_object = Slot(uri=ONTOASSOC.old_object, name="old_object", curie=ONTOASSOC.curie('old_object'),
                   model_uri=ONTOASSOC.old_object, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.new_object = Slot(uri=ONTOASSOC.new_object, name="new_object", curie=ONTOASSOC.curie('new_object'),
                   model_uri=ONTOASSOC.new_object, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.old_object_obsolete = Slot(uri=ONTOASSOC.old_object_obsolete, name="old_object_obsolete", curie=ONTOASSOC.curie('old_object_obsolete'),
                   model_uri=ONTOASSOC.old_object_obsolete, domain=None, range=Optional[Union[bool, Bool]])

slots.is_migration = Slot(uri=ONTOASSOC.is_migration, name="is_migration", curie=ONTOASSOC.curie('is_migration'),
                   model_uri=ONTOASSOC.is_migration, domain=None, range=Optional[Union[bool, Bool]])

slots.is_generalization = Slot(uri=ONTOASSOC.is_generalization, name="is_generalization", curie=ONTOASSOC.curie('is_generalization'),
                   model_uri=ONTOASSOC.is_generalization, domain=None, range=Optional[Union[bool, Bool]])

slots.is_specialization = Slot(uri=ONTOASSOC.is_specialization, name="is_specialization", curie=ONTOASSOC.curie('is_specialization'),
                   model_uri=ONTOASSOC.is_specialization, domain=None, range=Optional[Union[bool, Bool]])

slots.is_creation = Slot(uri=ONTOASSOC.is_creation, name="is_creation", curie=ONTOASSOC.curie('is_creation'),
                   model_uri=ONTOASSOC.is_creation, domain=None, range=Optional[Union[bool, Bool]])

slots.is_deletion = Slot(uri=ONTOASSOC.is_deletion, name="is_deletion", curie=ONTOASSOC.curie('is_deletion'),
                   model_uri=ONTOASSOC.is_deletion, domain=None, range=Optional[Union[bool, Bool]])

slots.closure_predicates = Slot(uri=ONTOASSOC.closure_predicates, name="closure_predicates", curie=ONTOASSOC.curie('closure_predicates'),
                   model_uri=ONTOASSOC.closure_predicates, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.closure_delta = Slot(uri=ONTOASSOC.closure_delta, name="closure_delta", curie=ONTOASSOC.curie('closure_delta'),
                   model_uri=ONTOASSOC.closure_delta, domain=None, range=Optional[int])

slots.closure_information_content_delta = Slot(uri=ONTOASSOC.closure_information_content_delta, name="closure_information_content_delta", curie=ONTOASSOC.curie('closure_information_content_delta'),
                   model_uri=ONTOASSOC.closure_information_content_delta, domain=None, range=Optional[float])

slots.subject_closure = Slot(uri=ONTOASSOC.subject_closure, name="subject_closure", curie=ONTOASSOC.curie('subject_closure'),
                   model_uri=ONTOASSOC.subject_closure, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.object_closure = Slot(uri=ONTOASSOC.object_closure, name="object_closure", curie=ONTOASSOC.curie('object_closure'),
                   model_uri=ONTOASSOC.object_closure, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.subject_closure_label = Slot(uri=ONTOASSOC.subject_closure_label, name="subject_closure_label", curie=ONTOASSOC.curie('subject_closure_label'),
                   model_uri=ONTOASSOC.subject_closure_label, domain=None, range=Optional[Union[str, List[str]]])

slots.object_closure_label = Slot(uri=ONTOASSOC.object_closure_label, name="object_closure_label", curie=ONTOASSOC.curie('object_closure_label'),
                   model_uri=ONTOASSOC.object_closure_label, domain=None, range=Optional[Union[str, List[str]]])

slots.object1 = Slot(uri=ONTOASSOC.object1, name="object1", curie=ONTOASSOC.curie('object1'),
                   model_uri=ONTOASSOC.object1, domain=None, range=Union[str, URIorCURIE])

slots.object2 = Slot(uri=ONTOASSOC.object2, name="object2", curie=ONTOASSOC.curie('object2'),
                   model_uri=ONTOASSOC.object2, domain=None, range=Union[str, URIorCURIE])

slots.object1_label = Slot(uri=ONTOASSOC.object1_label, name="object1_label", curie=ONTOASSOC.curie('object1_label'),
                   model_uri=ONTOASSOC.object1_label, domain=None, range=Optional[str])

slots.object2_label = Slot(uri=ONTOASSOC.object2_label, name="object2_label", curie=ONTOASSOC.curie('object2_label'),
                   model_uri=ONTOASSOC.object2_label, domain=None, range=Optional[str])

slots.number_subjects_in_common = Slot(uri=ONTOASSOC.number_subjects_in_common, name="number_subjects_in_common", curie=ONTOASSOC.curie('number_subjects_in_common'),
                   model_uri=ONTOASSOC.number_subjects_in_common, domain=None, range=Optional[int])

slots.proportion_subjects_in_common = Slot(uri=ONTOASSOC.proportion_subjects_in_common, name="proportion_subjects_in_common", curie=ONTOASSOC.curie('proportion_subjects_in_common'),
                   model_uri=ONTOASSOC.proportion_subjects_in_common, domain=None, range=Optional[float])

slots.proportion_entity1_subjects_in_entity2 = Slot(uri=ONTOASSOC.proportion_entity1_subjects_in_entity2, name="proportion_entity1_subjects_in_entity2", curie=ONTOASSOC.curie('proportion_entity1_subjects_in_entity2'),
                   model_uri=ONTOASSOC.proportion_entity1_subjects_in_entity2, domain=None, range=Optional[float])

slots.proportion_entity2_subjects_in_entity1 = Slot(uri=ONTOASSOC.proportion_entity2_subjects_in_entity1, name="proportion_entity2_subjects_in_entity1", curie=ONTOASSOC.curie('proportion_entity2_subjects_in_entity1'),
                   model_uri=ONTOASSOC.proportion_entity2_subjects_in_entity1, domain=None, range=Optional[float])

slots.number_subjects_in_union = Slot(uri=ONTOASSOC.number_subjects_in_union, name="number_subjects_in_union", curie=ONTOASSOC.curie('number_subjects_in_union'),
                   model_uri=ONTOASSOC.number_subjects_in_union, domain=None, range=Optional[int])

slots.number_subject_unique_to_entity1 = Slot(uri=ONTOASSOC.number_subject_unique_to_entity1, name="number_subject_unique_to_entity1", curie=ONTOASSOC.curie('number_subject_unique_to_entity1'),
                   model_uri=ONTOASSOC.number_subject_unique_to_entity1, domain=None, range=Optional[int])

slots.number_subject_unique_to_entity2 = Slot(uri=ONTOASSOC.number_subject_unique_to_entity2, name="number_subject_unique_to_entity2", curie=ONTOASSOC.curie('number_subject_unique_to_entity2'),
                   model_uri=ONTOASSOC.number_subject_unique_to_entity2, domain=None, range=Optional[int])

slots.subjects_in_common = Slot(uri=ONTOASSOC.subjects_in_common, name="subjects_in_common", curie=ONTOASSOC.curie('subjects_in_common'),
                   model_uri=ONTOASSOC.subjects_in_common, domain=None, range=Optional[Union[str, List[str]]])

slots.associations_for_subjects_in_common = Slot(uri=ONTOASSOC.associations_for_subjects_in_common, name="associations_for_subjects_in_common", curie=ONTOASSOC.curie('associations_for_subjects_in_common'),
                   model_uri=ONTOASSOC.associations_for_subjects_in_common, domain=None, range=Optional[Union[Union[dict, Association], List[Union[dict, Association]]]])

slots.parserConfiguration__preserve_negated_associations = Slot(uri=ONTOASSOC.preserve_negated_associations, name="parserConfiguration__preserve_negated_associations", curie=ONTOASSOC.curie('preserve_negated_associations'),
                   model_uri=ONTOASSOC.parserConfiguration__preserve_negated_associations, domain=None, range=Optional[Union[bool, Bool]])

slots.parserConfiguration__include_association_attributes = Slot(uri=ONTOASSOC.include_association_attributes, name="parserConfiguration__include_association_attributes", curie=ONTOASSOC.curie('include_association_attributes'),
                   model_uri=ONTOASSOC.parserConfiguration__include_association_attributes, domain=None, range=Optional[Union[bool, Bool]])

slots.parserConfiguration__primary_knowledge_source = Slot(uri=BIOLINK.primary_knowledge_source, name="parserConfiguration__primary_knowledge_source", curie=BIOLINK.curie('primary_knowledge_source'),
                   model_uri=ONTOASSOC.parserConfiguration__primary_knowledge_source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.parserConfiguration__aggregator_knowledge_source = Slot(uri=BIOLINK.aggregator_knowledge_source, name="parserConfiguration__aggregator_knowledge_source", curie=BIOLINK.curie('aggregator_knowledge_source'),
                   model_uri=ONTOASSOC.parserConfiguration__aggregator_knowledge_source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.Association_negated = Slot(uri=ONTOASSOC.negated, name="Association_negated", curie=ONTOASSOC.curie('negated'),
                   model_uri=ONTOASSOC.Association_negated, domain=Association, range=Optional[Union[bool, Bool]])

slots.NegatedAssociation_negated = Slot(uri=ONTOASSOC.negated, name="NegatedAssociation_negated", curie=ONTOASSOC.curie('negated'),
                   model_uri=ONTOASSOC.NegatedAssociation_negated, domain=NegatedAssociation, range=Optional[Union[bool, Bool]])
