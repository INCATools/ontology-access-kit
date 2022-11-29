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
SYNONYM_PREDICATES = [
    HAS_RELATED_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_EXACT_SYNONYM,
    HAS_BROAD_SYNONYM,
    SKOS_ALT_LABEL,
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

IN_CATEGORY_PREDS = ["biolink:category", "dbont:category"]

OWL_CLASS = "owl:Class"
OWL_OBJECT_PROPERTY = "owl:ObjectProperty"
OWL_THING = "owl:Thing"
OWL_NOTHING = "owl:Nothing"
IS_DEFINED_BY = "rdfs:isDefinedBy"
SUBCLASS_OF = omd.slots.subClassOf.curie
IS_A = omd.slots.subClassOf.curie
DISJOINT_WITH = "owl:disjointWith"
SUBPROPERTY_OF = "owl:subPropertyOf"
INVERSE_OF = "owl:inverseOf"
RDF_TYPE = "rdf:type"
EQUIVALENT_CLASS = "owl:equivalentClass"
OWL_SAME_AS = "owl:sameAs"
RDF_SEE_ALSO = "rdfs:seeAlso"
PART_OF = "BFO:0000050"
LOCATED_IN = "RO:0001025"
DEVELOPS_FROM = "RO:0002202"
HAS_PART = "BFO:0000051"
ONLY_IN_TAXON = "RO:0002160"
NEVER_IN_TAXON = "RO:0002161"
IN_TAXON = "RO:0002162"
PRESENT_IN_TAXON = "RO:0002175"

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
