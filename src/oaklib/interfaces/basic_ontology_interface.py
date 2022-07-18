import logging
from abc import ABC
from dataclasses import field
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib.datamodels.vocabulary import (
    BIOPORTAL_PURL,
    IS_A,
    OBO_PURL,
    OWL_CLASS,
    OWL_NOTHING,
    OWL_THING,
)
from oaklib.interfaces.ontology_interface import OntologyInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE, URI
from oaklib.utilities.basic_utils import get_curie_prefix

NC_NAME = str
PREFIX_MAP = Dict[NC_NAME, URI]
RELATIONSHIP_MAP = Dict[PRED_CURIE, List[CURIE]]
ALIAS_MAP = Dict[PRED_CURIE, List[str]]
METADATA_MAP = Dict[PRED_CURIE, List[str]]
# ANNOTATED_METADATA_MAP = Dict[PRED_CURIE, List[Tuple[str, METADATA_MAP]]]
RELATIONSHIP = Tuple[CURIE, PRED_CURIE, CURIE]


class BasicOntologyInterface(OntologyInterface, ABC):
    """
    Basic lookup operations on ontologies

    No Object Model is used - input and payloads are simple scalars, dicts, and lists

    This presents an intentionally highly simplistic, lossy view of an ontology. It
    is intended to fit the "80% of uses" scenario - for more advanced uses, use one of the
    more specialized subclasses

    Basic concepts:

    - An ontology is a collection of entities
    - Entities are typically classes (terms), but they may be other types
    - An entity MUST BE uniquely identifier by a CURIE
    - Each entity SHOULD have a single name
    - Entities may have hierarchical parents and children
    - Entities may have simple relationships to other terms

        - A relationship is a simple triple (in OWL terms, these may represent existential relationships)
        - A CURIE is used for the predicate
    - Entities may have aliases (synonyms)

       - these MAY be typed (scoped)

    - Entities have simple key-value metadata associated with them, where keys are open-ended

    Out of scope:

    - Many OWL axioms including:

        - Disjointness
        - Equivalence (including "logical definitions")
        - Property characteristics

    - All OWL expressions

        - but note that simple SomeValuesFrom expressions are included as relationships

    - Information about specific assignments ("axiom annotations" in OWL terms)

        - this includes attribution for synonyms, definitions, ...

    - A fixed datamodel for metadata, beyond core minimal information

    CURIEs are used as the default means of identifying entities.

    In some cases there may not be a defined CURIE form for an entity, such as an ontology,
    in which case URIs may be used

    """

    strict: bool = False
    autosave: bool = field(default_factory=lambda: True)

    def get_prefix_map(self) -> PREFIX_MAP:
        """
        Returns all prefixes known to the resource plus their URI expansion

        :return:
        """
        raise NotImplementedError

    def curie_to_uri(self, curie: CURIE, strict=False) -> Optional[URI]:
        """
        Expands a CURIE

        :param curie:
        :param strict:
        :return:
        """
        if curie.startswith("http"):
            return curie
        pm = self.get_prefix_map()
        parts = curie.split(":")
        if len(parts) == 2:
            pfx, local_id = parts
        else:
            if strict:
                raise ValueError(f"Bad CURIE: {curie} parts: {parts}")
            else:
                return curie
        if pfx in pm:
            return f"{pm[pfx]}{local_id}"
        else:
            # TODO: not hardcode
            return f"{OBO_PURL}{pfx}_{local_id}"

    def uri_to_curie(self, uri: URI, strict=True) -> Optional[CURIE]:
        """
        Contracts a URI

        If strict conditions hold, then no URI can map to more than one CURIE
        (i.e one URI base should not start with another).

        :param uri: URI
        :param strict: Boolean [default: True]
        :return: CURIE
        """
        pm = self.get_prefix_map()
        for k, v in pm.items():
            if uri.startswith(v):
                return uri.replace(v, f"{k}:")
        if uri.startswith(OBO_PURL):
            # TODO: do not hardcode OBO purl behavior
            uri = uri.replace(f"{OBO_PURL}", "")
            return uri.replace("_", ":")
        if uri.startswith(BIOPORTAL_PURL):
            # TODO: do not hardcode OBO purl behavior
            uri = uri.replace(f"{BIOPORTAL_PURL}", "")
            return uri.replace("_", ":")
        return uri

    def all_ontology_curies(self) -> Iterable[CURIE]:
        """
        returns iterator over all known ontology CURIEs

        Many OntologyInterfaces will wrap a single ontology, others will wrap multiple.
        Even when a single ontology is wrapped, there may be multiple ontologies included as imports

        :return: iterator
        """
        raise NotImplementedError

    def all_obsolete_curies(self) -> Iterable[CURIE]:
        """
        returns iterator over all known CURIEs that are obsolete

        :return: iterator
        """
        raise NotImplementedError

    def ontology_versions(self, ontology: CURIE) -> Iterable[str]:
        """
        returns iterator over all version identifiers for an ontology
        :param ontology:
        :return: iterator
        """
        raise NotImplementedError

    def ontology_metadata(self, ontology: CURIE) -> METADATA_MAP:
        """
        Basic metadata about an ontology

        :param ontology:
        :return:
        """
        raise NotImplementedError

    def all_entity_curies(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        """
        returns iterator over all known entity CURIEs

        :param filter_obsoletes: if True, exclude any obsolete/deprecated element
        :param owl_type: e.g. owl:Class
        :return: iterator
        """
        raise NotImplementedError

    def roots(
        self,
        predicates: List[PRED_CURIE] = None,
        ignore_owl_thing=True,
        filter_obsoletes=True,
        id_prefixes: List[CURIE] = None,
    ) -> Iterable[CURIE]:
        """
        All root nodes, where root is defined as any node that is not the subject of
        a relationship with one of the specified predicates

        :param predicates:
        :param ignore_owl_thing: do not consider artificial/trivial owl:Thing when calculating (default=True)
        :param filter_obsoletes: do not include obsolete/deprecated nodes in results (default=True)
        :param id_prefixes: limit search to specific prefixes
        :return:
        """
        # this interface-level method should be replaced by specific implementations
        logging.info("Using naive approach for root detection, may be slow")
        candidates = []
        for curie in self.all_entity_curies(owl_type=OWL_CLASS):
            if id_prefixes is None or get_curie_prefix(curie) in id_prefixes:
                candidates.append(curie)
        logging.info(f"Candidates: {len(candidates)}")
        for subject, pred, object in self.all_relationships():
            if subject == object:
                continue
            if ignore_owl_thing and object == OWL_THING:
                continue
            if not (id_prefixes is None or get_curie_prefix(object) in id_prefixes):
                continue
            # if object not in all_curies:
            #    continue
            if subject in candidates:
                if predicates is None or pred in predicates:
                    candidates.remove(subject)
                    logging.debug(f"Not a root: {subject} [{pred} {object}]")
        if filter_obsoletes:
            exclusion_list = list(self.all_obsolete_curies())
        else:
            exclusion_list = []
        exclusion_list += [OWL_THING, OWL_NOTHING]
        for term in candidates:
            if term not in exclusion_list:
                yield term

    def leafs(
        self, predicates: List[PRED_CURIE] = None, ignore_owl_nothing=True, filter_obsoletes=True
    ) -> Iterable[CURIE]:
        """
        All leaf nodes, where root is defined as any node that is not the object of
        a relationship with one of the specified predicates

        :param predicates:
        :param ignore_owl_nothing: do not consider artificial/trivial owl:Nothing when calculating (default=True)
        :param filter_obsoletes: do not include obsolete/deprecated nodes in results (default=True)
        :return:
        """
        all_curies = set(list(self.all_entity_curies(owl_type=OWL_CLASS)))
        candidates = all_curies
        logging.info(f"Candidates: {len(candidates)}")
        for subject, pred, object in self.all_relationships():
            if subject == object:
                continue
            if ignore_owl_nothing and subject == OWL_NOTHING:
                continue
            if object in candidates:
                if predicates is None or pred in predicates:
                    candidates.remove(object)
                    logging.debug(f"Not a leaf: {object} [inv({pred}) {subject}]")
        if filter_obsoletes:
            exclusion_list = list(self.all_obsolete_curies())
        else:
            exclusion_list = []
        exclusion_list += [OWL_THING, OWL_NOTHING]
        for term in candidates:
            if term not in exclusion_list:
                yield term

    def all_subset_curies(self) -> Iterable[SUBSET_CURIE]:
        """
        returns iterator over all known subset CURIEs

        :return: iterator
        """
        raise NotImplementedError

    def curies_by_subset(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        """
        returns iterator over all CURIEs belonging to a subset

        :return: iterator
        """
        raise NotImplementedError

    def get_label_by_curie(self, curie: CURIE) -> Optional[str]:
        """
        fetches the unique label for a CURIE

        The CURIE may be for a class, individual, property, or ontology

        :param curie:
        :return:
        """
        raise NotImplementedError

    def get_labels_for_curies(
        self, curies: Iterable[CURIE], allow_none=True
    ) -> Iterable[Tuple[CURIE, str]]:
        """
        fetches the unique label for a CURIE

        The CURIE may be for a class, individual, property, or ontology

        :param curie:
        :param allow_none:
        :return:
        """
        # default implementation: may be overridden for efficiency
        for curie in curies:
            yield [curie, self.get_label_by_curie(curie)]

    def set_label_for_curie(self, curie: CURIE, label: str) -> bool:
        """
        updates the label

        :param curie:
        :param label:
        :return:
        """
        raise NotImplementedError

    def get_curies_by_label(self, label: str) -> List[CURIE]:
        """
        Fetches all curies with a given label

        This SHOULD return maximum one CURIE but there are circumstances where multiple CURIEs
        may share a label

        :param label:
        :return:
        """
        raise NotImplementedError()

    def get_hierararchical_parents_by_curie(
        self, curie: CURIE, isa_only: bool = False
    ) -> List[CURIE]:
        """
        Returns all hierarchical parents

        The definition of hierarchical parent depends on the provider. For example, in OLS,
        this will return part-of parents for GO, as well as is-a

        This only returns Named Entities; i.e. if an RDF source is wrapped, this will NOT return blank nodes

        To get all relationships, see :ref:`get_outgoing_relationships_by_curie`

        A fresh map is created each invocation

        :param curie:
        :param isa_only: restrict hierarchical parents to isa only
        :return:
        """
        return self.get_outgoing_relationship_map_by_curie(curie)[IS_A]

    def get_outgoing_relationship_map_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        """
        The return relationship map is keyed by relationship type, where the values
        are the 'parents' or fillers

        OWL formulation:

         - is_a: {P : SubClassOf(C P), class(P)}
         - R: {P : SubClassOf(C ObjectSomeValuesFrom( RP), class(P), property(P)}

        :param curie: the 'child' term
        :return:
        """
        raise NotImplementedError()

    def get_outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        """
        Returns relationships where curie in the subject

        :param curie:
        :param predicates: if None, do not filter
        :return:
        """
        for p, vs in self.get_outgoing_relationship_map_by_curie(curie).items():
            if predicates is not None and p not in predicates:
                continue
            for v in vs:
                yield p, v

    def get_incoming_relationship_map_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

    def get_incoming_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        """
        Returns relationships where curie in the object

        :param curie:
        :param predicates: if None, do not filter
        :return:
        """
        for p, vs in self.get_incoming_relationship_map_by_curie(curie).items():
            if predicates is None or p not in predicates:
                continue
            for v in vs:
                yield p, v

    def get_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
    ) -> Iterator[RELATIONSHIP]:
        """
        Returns all matching relationships

        :param subjects:
        :param predicates:
        :param objects:
        :return:
        """
        if not subjects:
            subjects = list(self.all_entity_curies())
        logging.info(f"Subjects: {len(subjects)}")
        for subject in subjects:
            for this_predicate, this_objects in self.get_outgoing_relationship_map_by_curie(
                subject
            ).items():
                if predicates and this_predicate not in predicates:
                    continue
                for this_object in this_objects:
                    if objects and this_object not in objects:
                        continue
                    yield subject, this_predicate, this_object

    def all_relationships(self) -> Iterable[RELATIONSHIP]:
        """
        returns iterator over all known relationships

        :return:
        """
        for curie in self.all_entity_curies():
            for pred, fillers in self.get_outgoing_relationship_map_by_curie(curie).items():
                for filler in fillers:
                    yield curie, pred, filler

    def get_definition_by_curie(self, curie: CURIE) -> Optional[str]:
        """

        :param curie:
        :return:x`
        """
        raise NotImplementedError()

    def get_simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError()

    def aliases_by_curie(self, curie: CURIE) -> List[str]:
        """
        All aliases/synonyms for a given CURIE

        This lumps together all synonym categories (scopes)

        :param curie:
        :return:
        """
        aliases = set()
        for v in self.alias_map_by_curie(curie).values():
            aliases.update(set(v))
        return list(aliases)

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        """
        Returns aliases keyed by alias type (scope in OBO terms)

        - The alias map MUST include rdfs:label annotations
        - The alias map MAY include other properties the implementation deems to serve an alias role

        :param curie:
        :return:
        """
        raise NotImplementedError

    def metadata_map_by_curie(self, curie: CURIE) -> METADATA_MAP:
        """
        Returns a dictionary keyed by property predicate, with a list of zero or more values,
        where each key corresponds to any of a set of open-ended metadata predicates

        This is a simplified version of the metadata model in many ontologies

        :param curie:
        :return:
        """
        raise NotImplementedError

    def create_entity(
        self, curie: CURIE, label: str = None, relationships: RELATIONSHIP_MAP = None
    ) -> CURIE:
        """
        Adds an entity to the resource

        :param curie:
        :param label:
        :param relationships:
        :return:
        """
        raise NotImplementedError

    def save(self):
        """
        Saves current state

        :return:
        """
        raise NotImplementedError

    def dump(self, path: str = None, syntax: str = None):
        """
        Exports current state

        :param path:
        :param syntax:
        :return:
        """
        raise NotImplementedError

    def clone(self, resource: Any) -> None:
        """
        Clones the ontology interface to a new resource

        :param resource:
        :return:
        """
        raise NotImplementedError
