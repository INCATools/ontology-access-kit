# Auto generated from taxon_constraints.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-15T11:25:58
# Schema: taxon-constraints
#
# id: https://w3id.org/linkml/taxon_constraints
# description: A datamodel for representing inferred and asserted taxon constraints
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
from linkml_runtime.linkml_model.types import Boolean, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
NCBITAXON = CurieNamespace('NCBITaxon', 'http://example.org/UNKNOWN/NCBITaxon/')
NCBITAXON_UNION = CurieNamespace('NCBITaxon_Union', 'http://example.org/UNKNOWN/NCBITaxon_Union/')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TC = CurieNamespace('tc', 'https://w3id.org/linkml/taxon_constraints/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = TC


# Types

# Class references



@dataclass
class Term(YAMLRoot):
    """
    An ontology term. In this model this is either the SubjectTerm of a taxon constraint, or an actual taxon
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = TC.Term

    id: Optional[Union[str, URIorCURIE]] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, URIorCURIE):
            self.id = URIorCURIE(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class SubjectTerm(Term):
    """
    A term that is the subject of a taxon constraint. Typically comes from ontologies like GO, UBERON, CL, ...
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TC.SubjectTerm
    class_class_curie: ClassVar[str] = "tc:SubjectTerm"
    class_name: ClassVar[str] = "SubjectTerm"
    class_model_uri: ClassVar[URIRef] = TC.SubjectTerm

    never_in: Optional[Union[Union[dict, "TaxonConstraint"], List[Union[dict, "TaxonConstraint"]]]] = empty_list()
    only_in: Optional[Union[Union[dict, "TaxonConstraint"], List[Union[dict, "TaxonConstraint"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.never_in, list):
            self.never_in = [self.never_in] if self.never_in is not None else []
        self.never_in = [v if isinstance(v, TaxonConstraint) else TaxonConstraint(**as_dict(v)) for v in self.never_in]

        if not isinstance(self.only_in, list):
            self.only_in = [self.only_in] if self.only_in is not None else []
        self.only_in = [v if isinstance(v, TaxonConstraint) else TaxonConstraint(**as_dict(v)) for v in self.only_in]

        super().__post_init__(**kwargs)


class Taxon(Term):
    """
    A term that represents a taxonomic group
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TC.Taxon
    class_class_curie: ClassVar[str] = "tc:Taxon"
    class_name: ClassVar[str] = "Taxon"
    class_model_uri: ClassVar[URIRef] = TC.Taxon


class PredicateTerm(Term):
    """
    A term that represents a relationship type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TC.PredicateTerm
    class_class_curie: ClassVar[str] = "tc:PredicateTerm"
    class_name: ClassVar[str] = "PredicateTerm"
    class_model_uri: ClassVar[URIRef] = TC.PredicateTerm


@dataclass
class TaxonConstraint(YAMLRoot):
    """
    An individual taxon constraint
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TC.TaxonConstraint
    class_class_curie: ClassVar[str] = "tc:TaxonConstraint"
    class_name: ClassVar[str] = "TaxonConstraint"
    class_model_uri: ClassVar[URIRef] = TC.TaxonConstraint

    asserted: Optional[Union[bool, Bool]] = None
    redundant: Optional[Union[bool, Bool]] = None
    redundant_with_only_in: Optional[Union[bool, Bool]] = None
    taxon: Optional[Union[dict, Taxon]] = None
    redundant_with: Optional[Union[Union[dict, "TaxonConstraint"], List[Union[dict, "TaxonConstraint"]]]] = empty_list()
    via_terms: Optional[Union[Union[dict, SubjectTerm], List[Union[dict, SubjectTerm]]]] = empty_list()
    predicates: Optional[Union[Union[dict, PredicateTerm], List[Union[dict, PredicateTerm]]]] = empty_list()
    sources: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.asserted is not None and not isinstance(self.asserted, Bool):
            self.asserted = Bool(self.asserted)

        if self.redundant is not None and not isinstance(self.redundant, Bool):
            self.redundant = Bool(self.redundant)

        if self.redundant_with_only_in is not None and not isinstance(self.redundant_with_only_in, Bool):
            self.redundant_with_only_in = Bool(self.redundant_with_only_in)

        if self.taxon is not None and not isinstance(self.taxon, Taxon):
            self.taxon = Taxon(**as_dict(self.taxon))

        if not isinstance(self.redundant_with, list):
            self.redundant_with = [self.redundant_with] if self.redundant_with is not None else []
        self.redundant_with = [v if isinstance(v, TaxonConstraint) else TaxonConstraint(**as_dict(v)) for v in self.redundant_with]

        if not isinstance(self.via_terms, list):
            self.via_terms = [self.via_terms] if self.via_terms is not None else []
        self.via_terms = [v if isinstance(v, SubjectTerm) else SubjectTerm(**as_dict(v)) for v in self.via_terms]

        if not isinstance(self.predicates, list):
            self.predicates = [self.predicates] if self.predicates is not None else []
        self.predicates = [v if isinstance(v, PredicateTerm) else PredicateTerm(**as_dict(v)) for v in self.predicates]

        if not isinstance(self.sources, list):
            self.sources = [self.sources] if self.sources is not None else []
        self.sources = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.sources]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.term__id = Slot(uri=TC.id, name="term__id", curie=TC.curie('id'),
                   model_uri=TC.term__id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.term__label = Slot(uri=RDFS.label, name="term__label", curie=RDFS.curie('label'),
                   model_uri=TC.term__label, domain=None, range=Optional[str])

slots.subjectTerm__never_in = Slot(uri=RO['0002161'], name="subjectTerm__never_in", curie=RO.curie('0002161'),
                   model_uri=TC.subjectTerm__never_in, domain=None, range=Optional[Union[Union[dict, TaxonConstraint], List[Union[dict, TaxonConstraint]]]])

slots.subjectTerm__only_in = Slot(uri=RO['0002160'], name="subjectTerm__only_in", curie=RO.curie('0002160'),
                   model_uri=TC.subjectTerm__only_in, domain=None, range=Optional[Union[Union[dict, TaxonConstraint], List[Union[dict, TaxonConstraint]]]])

slots.taxonConstraint__asserted = Slot(uri=TC.asserted, name="taxonConstraint__asserted", curie=TC.curie('asserted'),
                   model_uri=TC.taxonConstraint__asserted, domain=None, range=Optional[Union[bool, Bool]])

slots.taxonConstraint__redundant = Slot(uri=TC.redundant, name="taxonConstraint__redundant", curie=TC.curie('redundant'),
                   model_uri=TC.taxonConstraint__redundant, domain=None, range=Optional[Union[bool, Bool]])

slots.taxonConstraint__redundant_with_only_in = Slot(uri=TC.redundant_with_only_in, name="taxonConstraint__redundant_with_only_in", curie=TC.curie('redundant_with_only_in'),
                   model_uri=TC.taxonConstraint__redundant_with_only_in, domain=None, range=Optional[Union[bool, Bool]])

slots.taxonConstraint__taxon = Slot(uri=TC.taxon, name="taxonConstraint__taxon", curie=TC.curie('taxon'),
                   model_uri=TC.taxonConstraint__taxon, domain=None, range=Optional[Union[dict, Taxon]])

slots.taxonConstraint__redundant_with = Slot(uri=TC.redundant_with, name="taxonConstraint__redundant_with", curie=TC.curie('redundant_with'),
                   model_uri=TC.taxonConstraint__redundant_with, domain=None, range=Optional[Union[Union[dict, TaxonConstraint], List[Union[dict, TaxonConstraint]]]])

slots.taxonConstraint__via_terms = Slot(uri=TC.via_terms, name="taxonConstraint__via_terms", curie=TC.curie('via_terms'),
                   model_uri=TC.taxonConstraint__via_terms, domain=None, range=Optional[Union[Union[dict, SubjectTerm], List[Union[dict, SubjectTerm]]]])

slots.taxonConstraint__predicates = Slot(uri=TC.predicates, name="taxonConstraint__predicates", curie=TC.curie('predicates'),
                   model_uri=TC.taxonConstraint__predicates, domain=None, range=Optional[Union[Union[dict, PredicateTerm], List[Union[dict, PredicateTerm]]]])

slots.taxonConstraint__sources = Slot(uri=TC.sources, name="taxonConstraint__sources", curie=TC.curie('sources'),
                   model_uri=TC.taxonConstraint__sources, domain=None, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])
