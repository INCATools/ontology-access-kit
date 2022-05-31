# Auto generated from cross_ontology_diff.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-05-29T22:40:51
# Schema: cross-ontology-diff
#
# id: https://w3id.org/linkml/cross_ontology_diff
# description: A datamodel for representing the results of relational diffs across a pair of ontologies connected
#              by mappings
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
from linkml_runtime.linkml_model.types import Boolean, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ANN = CurieNamespace('ann', 'https://w3id.org/linkml/text_annotator/')
BPA = CurieNamespace('bpa', 'https://bioportal.bioontology.org/annotator/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SSSOM = CurieNamespace('sssom', 'http://w3id.org/sssom/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = ANN


# Types
class Position(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "Position"
    type_model_uri = ANN.Position


# Class references



@dataclass
class StructureDiffResultSet(YAMLRoot):
    """
    A collection of results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.StructureDiffResultSet
    class_class_curie: ClassVar[str] = "ann:StructureDiffResultSet"
    class_name: ClassVar[str] = "StructureDiffResultSet"
    class_model_uri: ClassVar[URIRef] = ANN.StructureDiffResultSet

    results: Optional[Union[Union[dict, "RelationalDiff"], List[Union[dict, "RelationalDiff"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="results", slot_type=RelationalDiff, key_name="left_subject_id", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class RelationalDiff(YAMLRoot):
    """
    A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in
    another ontology (or a different version of the same ontology). The diff is from the perspective of one ontology
    (the one on the "left" side). For every edge in the left ontology, the subject and object are mapped to the right
    ontology. If mappings cannot be found then the diff is categorized as missing mappings. The predicate is also
    mapped, with the reflexivity assumption. for every mapped subject and object pair (the "right" subject and
    object), the entailed relationship is examined to determine if it consistent with the left predicate.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.RelationalDiff
    class_class_curie: ClassVar[str] = "ann:RelationalDiff"
    class_name: ClassVar[str] = "RelationalDiff"
    class_model_uri: ClassVar[URIRef] = ANN.RelationalDiff

    left_subject_id: Union[str, URIorCURIE] = None
    left_object_id: Union[str, URIorCURIE] = None
    left_predicate_id: Union[str, URIorCURIE] = None
    category: Optional[Union[str, "DiffCategory"]] = None
    left_subject_label: Optional[str] = None
    left_object_label: Optional[str] = None
    left_predicate_label: Optional[str] = None
    right_subject_id: Optional[Union[str, URIorCURIE]] = None
    right_object_id: Optional[Union[str, URIorCURIE]] = None
    right_predicate_ids: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    right_subject_label: Optional[str] = None
    right_object_label: Optional[str] = None
    right_predicate_labels: Optional[Union[str, List[str]]] = empty_list()
    left_subject_is_functional: Optional[Union[bool, Bool]] = None
    left_object_is_functional: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.left_subject_id):
            self.MissingRequiredField("left_subject_id")
        if not isinstance(self.left_subject_id, URIorCURIE):
            self.left_subject_id = URIorCURIE(self.left_subject_id)

        if self._is_empty(self.left_object_id):
            self.MissingRequiredField("left_object_id")
        if not isinstance(self.left_object_id, URIorCURIE):
            self.left_object_id = URIorCURIE(self.left_object_id)

        if self._is_empty(self.left_predicate_id):
            self.MissingRequiredField("left_predicate_id")
        if not isinstance(self.left_predicate_id, URIorCURIE):
            self.left_predicate_id = URIorCURIE(self.left_predicate_id)

        if self.category is not None and not isinstance(self.category, DiffCategory):
            self.category = DiffCategory(self.category)

        if self.left_subject_label is not None and not isinstance(self.left_subject_label, str):
            self.left_subject_label = str(self.left_subject_label)

        if self.left_object_label is not None and not isinstance(self.left_object_label, str):
            self.left_object_label = str(self.left_object_label)

        if self.left_predicate_label is not None and not isinstance(self.left_predicate_label, str):
            self.left_predicate_label = str(self.left_predicate_label)

        if self.right_subject_id is not None and not isinstance(self.right_subject_id, URIorCURIE):
            self.right_subject_id = URIorCURIE(self.right_subject_id)

        if self.right_object_id is not None and not isinstance(self.right_object_id, URIorCURIE):
            self.right_object_id = URIorCURIE(self.right_object_id)

        if not isinstance(self.right_predicate_ids, list):
            self.right_predicate_ids = [self.right_predicate_ids] if self.right_predicate_ids is not None else []
        self.right_predicate_ids = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.right_predicate_ids]

        if self.right_subject_label is not None and not isinstance(self.right_subject_label, str):
            self.right_subject_label = str(self.right_subject_label)

        if self.right_object_label is not None and not isinstance(self.right_object_label, str):
            self.right_object_label = str(self.right_object_label)

        if not isinstance(self.right_predicate_labels, list):
            self.right_predicate_labels = [self.right_predicate_labels] if self.right_predicate_labels is not None else []
        self.right_predicate_labels = [v if isinstance(v, str) else str(v) for v in self.right_predicate_labels]

        if self.left_subject_is_functional is not None and not isinstance(self.left_subject_is_functional, Bool):
            self.left_subject_is_functional = Bool(self.left_subject_is_functional)

        if self.left_object_is_functional is not None and not isinstance(self.left_object_is_functional, Bool):
            self.left_object_is_functional = Bool(self.left_object_is_functional)

        super().__post_init__(**kwargs)


# Enumerations
class DiffCategory(EnumDefinitionImpl):
    """
    Category of the cross-ontology diff, from the perspective of the left-hand edge
    """
    Identical = PermissibleValue(text="Identical",
                                         description="there is a direct analogous direct asserted edge with the same predicate")
    Consistent = PermissibleValue(text="Consistent",
                                           description="there is an entailed analogous edge with the same predicate or more specific predicate")
    OtherRelationship = PermissibleValue(text="OtherRelationship",
                                                         description="there is an analogous edge with a different predicate that is not entailed")
    MissingMapping = PermissibleValue(text="MissingMapping",
                                                   description="one or both mappings are missing")
    MissingSubjectMapping = PermissibleValue(text="MissingSubjectMapping",
                                                                 description="there is no mapping for the subject")
    MissingObjectMapping = PermissibleValue(text="MissingObjectMapping",
                                                               description="there is no mapping for the object")

    _defn = EnumDefinition(
        name="DiffCategory",
        description="Category of the cross-ontology diff, from the perspective of the left-hand edge",
    )

# Slots
class slots:
    pass

slots.structureDiffResultSet__results = Slot(uri=ANN.results, name="structureDiffResultSet__results", curie=ANN.curie('results'),
                   model_uri=ANN.structureDiffResultSet__results, domain=None, range=Optional[Union[Union[dict, RelationalDiff], List[Union[dict, RelationalDiff]]]])

slots.relationalDiff__category = Slot(uri=ANN.category, name="relationalDiff__category", curie=ANN.curie('category'),
                   model_uri=ANN.relationalDiff__category, domain=None, range=Optional[Union[str, "DiffCategory"]])

slots.relationalDiff__left_subject_id = Slot(uri=ANN.left_subject_id, name="relationalDiff__left_subject_id", curie=ANN.curie('left_subject_id'),
                   model_uri=ANN.relationalDiff__left_subject_id, domain=None, range=Union[str, URIorCURIE])

slots.relationalDiff__left_object_id = Slot(uri=ANN.left_object_id, name="relationalDiff__left_object_id", curie=ANN.curie('left_object_id'),
                   model_uri=ANN.relationalDiff__left_object_id, domain=None, range=Union[str, URIorCURIE])

slots.relationalDiff__left_predicate_id = Slot(uri=ANN.left_predicate_id, name="relationalDiff__left_predicate_id", curie=ANN.curie('left_predicate_id'),
                   model_uri=ANN.relationalDiff__left_predicate_id, domain=None, range=Union[str, URIorCURIE])

slots.relationalDiff__left_subject_label = Slot(uri=ANN.left_subject_label, name="relationalDiff__left_subject_label", curie=ANN.curie('left_subject_label'),
                   model_uri=ANN.relationalDiff__left_subject_label, domain=None, range=Optional[str])

slots.relationalDiff__left_object_label = Slot(uri=ANN.left_object_label, name="relationalDiff__left_object_label", curie=ANN.curie('left_object_label'),
                   model_uri=ANN.relationalDiff__left_object_label, domain=None, range=Optional[str])

slots.relationalDiff__left_predicate_label = Slot(uri=ANN.left_predicate_label, name="relationalDiff__left_predicate_label", curie=ANN.curie('left_predicate_label'),
                   model_uri=ANN.relationalDiff__left_predicate_label, domain=None, range=Optional[str])

slots.relationalDiff__right_subject_id = Slot(uri=ANN.right_subject_id, name="relationalDiff__right_subject_id", curie=ANN.curie('right_subject_id'),
                   model_uri=ANN.relationalDiff__right_subject_id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationalDiff__right_object_id = Slot(uri=ANN.right_object_id, name="relationalDiff__right_object_id", curie=ANN.curie('right_object_id'),
                   model_uri=ANN.relationalDiff__right_object_id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationalDiff__right_predicate_ids = Slot(uri=ANN.right_predicate_ids, name="relationalDiff__right_predicate_ids", curie=ANN.curie('right_predicate_ids'),
                   model_uri=ANN.relationalDiff__right_predicate_ids, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.relationalDiff__right_subject_label = Slot(uri=ANN.right_subject_label, name="relationalDiff__right_subject_label", curie=ANN.curie('right_subject_label'),
                   model_uri=ANN.relationalDiff__right_subject_label, domain=None, range=Optional[str])

slots.relationalDiff__right_object_label = Slot(uri=ANN.right_object_label, name="relationalDiff__right_object_label", curie=ANN.curie('right_object_label'),
                   model_uri=ANN.relationalDiff__right_object_label, domain=None, range=Optional[str])

slots.relationalDiff__right_predicate_labels = Slot(uri=ANN.right_predicate_labels, name="relationalDiff__right_predicate_labels", curie=ANN.curie('right_predicate_labels'),
                   model_uri=ANN.relationalDiff__right_predicate_labels, domain=None, range=Optional[Union[str, List[str]]])

slots.relationalDiff__left_subject_is_functional = Slot(uri=ANN.left_subject_is_functional, name="relationalDiff__left_subject_is_functional", curie=ANN.curie('left_subject_is_functional'),
                   model_uri=ANN.relationalDiff__left_subject_is_functional, domain=None, range=Optional[Union[bool, Bool]])

slots.relationalDiff__left_object_is_functional = Slot(uri=ANN.left_object_is_functional, name="relationalDiff__left_object_is_functional", curie=ANN.curie('left_object_is_functional'),
                   model_uri=ANN.relationalDiff__left_object_is_functional, domain=None, range=Optional[Union[bool, Bool]])
