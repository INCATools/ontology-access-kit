from enum import Enum

from linkml_runtime import CurieNamespace

import oaklib.datamodels.ontology_metadata as omd
from oaklib.datamodels.ontology_metadata import slots as omd_slots  # noqa F401

WIKIDATA = CurieNamespace("wikidata", "http://www.wikidata.org/entity/")
WDP = CurieNamespace("wdp", "http://www.wikidata.org/prop/direct/")
NAMESPACES = [omd.OWL, omd.SKOS, omd.RDF, omd.RDFS, omd.OIO, WIKIDATA, WDP]
DEFAULT_PREFIX_MAP = {ns.prefix: str(ns) for ns in NAMESPACES}

APP_NAME = "ontology-access-kit"

IDENTIFIER_PREDICATE = "rdf:ID"
URL_PREDICATE = "schema:url"
PREFIX_PREDICATE = "sh:prefix"

# TODO: replace with oio vocab
LABEL_PREDICATE = omd.slots.label.curie
HAS_EXACT_SYNONYM = omd.slots.has_exact_synonym.curie
HAS_BROAD_SYNONYM = omd.slots.has_broad_synonym.curie
HAS_NARROW_SYNONYM = omd.slots.has_narrow_synonym.curie
HAS_RELATED_SYNONYM = omd.slots.has_related_synonym.curie
SKOS_ALT_LABEL = "skos:altLabel"
IAO_ALTERNATIVE_LABEL = "IAO:0000118"
SYNONYM_PREDICATES = [
    HAS_RELATED_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_EXACT_SYNONYM,
    HAS_BROAD_SYNONYM,
    SKOS_ALT_LABEL,
    IAO_ALTERNATIVE_LABEL,
]

SCOPE_TO_SYNONYM_PRED_MAP = {
    "EXACT": HAS_EXACT_SYNONYM,
    "RELATED": HAS_RELATED_SYNONYM,
    "NARROW": HAS_NARROW_SYNONYM,
    "BROAD": HAS_BROAD_SYNONYM,
}
SYNONYM_PRED_TO_SCOPE_MAP = {v: k for k, v in SCOPE_TO_SYNONYM_PRED_MAP.items()}


DEPRECATED_PREDICATE = omd.slots.deprecated.curie
TERM_REPLACED_BY = omd.slots.term_replaced_by.curie
CONSIDER_REPLACEMENT = omd.slots.consider.curie
HAS_OBSOLESCENCE_REASON = omd.slots.has_obsolescence_reason.curie
TERMS_MERGED = "IAO:0000227"
OBSOLETION_RELATIONSHIP_PREDICATES = [TERM_REPLACED_BY, CONSIDER_REPLACEMENT]

HAS_ONTOLOGY_ROOT_TERM = omd.slots.has_ontology_root_term.curie
HAS_OBO_NAMESPACE = omd.slots.has_obo_namespace.curie

BIOLINK_CATEGORY = "biolink:category"
IN_CATEGORY_PREDS = [BIOLINK_CATEGORY, "dbont:category"]
RELATED_TO = "biolink:related_to"

OWL_CLASS = "owl:Class"
OWL_NAMED_INDIVIDUAL = "owl:NamedIndividual"
OWL_OBJECT_PROPERTY = "owl:ObjectProperty"
OWL_DATATYPE_PROPERTY = "owl:DatatypeProperty"
OWL_ANNOTATION_PROPERTY = "owl:AnnotationProperty"
OWL_TRANSITIVE_PROPERTY = "owl:TransitiveProperty"
OWL_SYMMETRIC_PROPERTY = "owl:SymmetricProperty"
OWL_ASYMMETRIC_PROPERTY = "owl:SymmetricProperty"
OWL_REFLEXIVE_PROPERTY = "owl:ReflexiveProperty"
OWL_IRREFLEXIVE_PROPERTY = "owl:IrreflexiveProperty"
OWL_THING = "owl:Thing"
OWL_NOTHING = "owl:Nothing"
IS_DEFINED_BY = "rdfs:isDefinedBy"
RDFS_COMMENT = "rdfs:comment"
SUBCLASS_OF = omd.slots.subClassOf.curie
IS_A = omd.slots.subClassOf.curie
DISJOINT_WITH = "owl:disjointWith"
SUBPROPERTY_OF = "rdfs:subPropertyOf"
RDFS_DOMAIN = "rdfs:domain"
RDFS_RANGE = "rdfs:range"
INVERSE_OF = "owl:inverseOf"
RDF_TYPE = "rdf:type"
RDFS_LABEL = "rdfs:label"
EQUIVALENT_CLASS = "owl:equivalentClass"
OWL_SAME_AS = "owl:sameAs"
RDFS_SEE_ALSO = "rdfs:seeAlso"
RDF_SEE_ALSO = "rdfs:seeAlso" ## DEPRECATED
OWL_RESTRICTION = "owl:Restriction"
OWL_ON_PROPERTY = "owl:onProperty"
OWL_SOME_VALUES_FROM = "owl:someValuesFrom"
OWL_PROPERTY_CHAIN_AXIOM = "owl:propertyChainAxiom"

OWL_META_CLASSES = [
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    OWL_NAMED_INDIVIDUAL,
    OWL_DATATYPE_PROPERTY,
    OWL_ANNOTATION_PROPERTY,
    OWL_TRANSITIVE_PROPERTY,
    OWL_SYMMETRIC_PROPERTY,
]

DCTERMS_LANGUAGE = "dcterms:language"
PROTEGE_PREFERRED_LANGUAGE = "protege:preferredLanguage"
ONTOLOGY_LEVEL_LANGUAGE_INDICATORS = [DCTERMS_LANGUAGE, PROTEGE_PREFERRED_LANGUAGE]

STANDARD_ANNOTATION_PROPERTIES = [
    TERM_REPLACED_BY,
    CONSIDER_REPLACEMENT,
    DEPRECATED_PREDICATE,
    HAS_OBSOLESCENCE_REASON,
    TERMS_MERGED,
    HAS_ONTOLOGY_ROOT_TERM,
    HAS_OBO_NAMESPACE,
    LABEL_PREDICATE,
    RDFS_COMMENT,
    RDFS_SEE_ALSO,
]

PART_OF = "BFO:0000050"
PRECEDED_BY = "BFO:0000062"
OVERLAPS = "RO:0002131"
LOCATED_IN = "RO:0001025"
DEVELOPS_FROM = "RO:0002202"
HAS_PART = "BFO:0000051"
OCCURS_IN = "BFO:0000066"
ONLY_IN_TAXON = "RO:0002160"
NEVER_IN_TAXON = "RO:0002161"
IN_TAXON = "RO:0002162"
PRESENT_IN_TAXON = "RO:0002175"
NEGATIVELY_REGULATES = "RO:0002212"
POSITIVELY_REGULATES = "RO:0002213"
REGULATES = "RO:0002211"
ENABLES = "RO:0002327"
ENABLED_BY = "RO:0002333"
HAS_DIRECT_INPUT = "RO:0002400"
HAS_INPUT = "RO:0002233"
HAS_OUTPUT = "RO:0002234"

BIOLOGICAL_PROCESS = "GO:0008150"
CELLULAR_COMPONENT = "GO:0005575"
MOLECULAR_FUNCTION = "GO:0003674"

OBO_PURL = "http://purl.obolibrary.org/obo/"

IN_SUBSET = omd.slots.in_subset.curie

SKOS_EXACT_MATCH = omd.slots.exactMatch.curie
SKOS_CLOSE_MATCH = omd.slots.closeMatch.curie
SKOS_NARROW_MATCH = omd.slots.narrowMatch.curie
SKOS_BROAD_MATCH = omd.slots.broadMatch.curie
# SKOS_RELATED_MATCH = omd.slots.relatedMatch.curie
SKOS_RELATED_MATCH = "skos:relatedMatch"
SKOS_MATCH_PREDICATES = [
    SKOS_BROAD_MATCH,
    SKOS_NARROW_MATCH,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
    SKOS_RELATED_MATCH,
]
HAS_DBXREF = omd.slots.database_cross_reference.curie
HAS_SYNONYM_TYPE = "oio:hasSynonymType"
OIO_SUBSET_PROPERTY = "oio:SubsetProperty"
OIO_SYNONYM_TYPE_PROPERTY = "oio:SynonymTypeProperty"
ALL_MATCH_PREDICATES = SKOS_MATCH_PREDICATES + [HAS_DBXREF, OWL_SAME_AS]
HAS_DEFINITION_URI = omd.slots.definition.uri
HAS_DEFINITION_CURIE = omd.slots.definition.curie
SKOS_DEFINITION_CURIE = "skos:definition"

DEFINITION_SOURCE = omd.slots.definition_source.curie
ENTITY_LEVEL_DEFINITION_PREDICATES = [DEFINITION_SOURCE]

TERM_TRACKER_ITEM = omd.slots.term_tracker_item.curie
TITLE = "dcterms:title"
DESCRIPTION = "dcterms:description"

OIO_CREATED_BY = "oio:created_by"
OIO_CREATION_DATE = "oio:creation_date"
CONTRIBUTOR = "dcterms:contributor"
CREATOR = "dcterms:creator"
CREATED = "dcterms:created"
IAO_TERM_EDITOR = "IAO:0000117"
ALL_CONTRIBUTOR_PREDICATES = [OIO_CREATED_BY, CONTRIBUTOR, CREATOR, IAO_TERM_EDITOR]

OWL_VERSION_INFO = "owl:versionInfo"
OWL_VERSION_IRI = "owl:versionIRI"

CLASS_CREATION = "ClassCreation"
NODE_CREATION = "NodeCreation"
NODE_DELETION = "NodeDeletion"
NODE_TEXT_DEFINITION_CHANGE = "NodeTextDefinitionChange"

EXTENDED_SCOPE_TO_SYNONYM_PRED_MAP = {
    "LABEL": LABEL_PREDICATE,
    "DEFINITION": HAS_DEFINITION_CURIE,
    **SYNONYM_PRED_TO_SCOPE_MAP,
}


class SEMAPV(Enum):
    """SEMAPV Enum containing different mapping_justification."""

    LexicalMatching = "semapv:LexicalMatching"
    LogicalReasoning = "semapv:LogicalReasoning"
    CompositeMatching = "semapv:CompositeMatching"
    UnspecifiedMatching = "semapv:UnspecifiedMatching"
    SemanticSimilarityThresholdMatching = "semapv:SemanticSimilarityThresholdMatching"
    LexicalSimilarityThresholdMatching = "semapv:LexicalSimilarityThresholdMatching"
    MappingChaining = "semapv:MappingChaining"
    MappingReview = "semapv:MappingReview"
    ManualMappingCuration = "semapv:ManualMappingCuration"
    RegularExpressionReplacement = "semapv:RegularExpressionReplacement"
