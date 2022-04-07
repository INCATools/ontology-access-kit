from oaklib.datamodels.ontology_metadata import slots as omd_slots
import oaklib.datamodels.ontology_metadata as omd

APP_NAME = 'ontology-access-kit'

# TODO: replace with oio vocab
LABEL_PREDICATE = omd.slots.label.curie
HAS_EXACT_SYNONYM = omd.slots.has_exact_synonym.curie
HAS_BROAD_SYNONYM = omd.slots.has_broad_synonym.curie
HAS_NARROW_SYNONYM = omd.slots.has_narrow_synonym.curie
HAS_RELATED_SYNONYM = omd.slots.has_related_synonym.curie
SYNONYM_PREDICATES = [HAS_RELATED_SYNONYM, HAS_NARROW_SYNONYM, HAS_EXACT_SYNONYM, HAS_BROAD_SYNONYM]

SCOPE_TO_SYNONYM_PRED_MAP = {
    'EXACT': HAS_EXACT_SYNONYM,
    'RELATED': HAS_RELATED_SYNONYM,
    'NARROW': HAS_NARROW_SYNONYM,
    'BROAD': HAS_BROAD_SYNONYM
}

SUBCLASS_OF = omd.slots.subClassOf.curie
IS_A = omd.slots.subClassOf.curie
EQUIVALENT_CLASS = 'owl:equivalentClass'
PART_OF = 'BFO:0000050'
HAS_PART = 'BFO:0000051'

OBO_PURL = 'http://purl.obolibrary.org/obo/'
BIOPORTAL_PURL = 'http://purl.bioontology.org/ontology/'

IN_SUBSET = omd.slots.in_subset.curie

SKOS_EXACT_MATCH = omd.slots.exactMatch.curie
SKOS_CLOSE_MATCH = omd.slots.closeMatch.curie
SKOS_NARROW_MATCH = omd.slots.narrowMatch.curie
SKOS_BROAD_MATCH = omd.slots.broadMatch.curie
HAS_DBXREF = omd.slots.database_cross_reference.curie
HAS_DEFINITION_URI = omd.slots.definition.uri