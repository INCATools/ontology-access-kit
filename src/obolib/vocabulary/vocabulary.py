from obolib.vocabulary.ontology_metadata import slots as omd_slots
import obolib.vocabulary.ontology_metadata as omd

# TODO: replace with oio vocab
LABEL_PREDICATE = omd.slots.label.curie
HAS_EXACT_SYNONYM = omd.slots.has_exact_synonym.curie
HAS_BROAD_SYNONYM = omd.slots.has_broad_synonym.curie
HAS_NARROW_SYNONYM = omd.slots.has_narrow_synonym.curie
HAS_RELATED_SYNONYM = omd.slots.has_related_synonym.curie
SYNONYM_PREDICATES = [HAS_RELATED_SYNONYM, HAS_NARROW_SYNONYM, HAS_EXACT_SYNONYM, HAS_BROAD_SYNONYM]

SUBCLASS_OF = omd.slots.subClassOf.curie
IS_A = omd.slots.subClassOf.curie
