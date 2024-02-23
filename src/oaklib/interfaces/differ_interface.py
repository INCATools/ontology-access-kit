import logging
import multiprocessing
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, Tuple

import kgcl_schema.datamodel.kgcl as kgcl
from kgcl_schema.datamodel.kgcl import (
    Change,
    ClassCreation,
    Edge,
    EdgeDeletion,
    NewSynonym,
    NewTextDefinition,
    NodeCreation,
    NodeDeletion,
    NodeDirectMerge,
    NodeMove,
    NodeObsoletion,
    NodeObsoletionWithDirectReplacement,
    NodeRename,
    NodeTextDefinitionChange,
    NodeUnobsoletion,
    PredicateChange,
    RemoveSynonym,
    SynonymPredicateChange,
)

from oaklib.constants import (
    CLASS_CREATION,
    NEW_TEXT_DEFINITION,
    NODE_CREATION,
    NODE_DELETION,
    NODE_RENAME,
    NODE_TEXT_DEFINITION_CHANGE,
)
from oaklib.datamodels.vocabulary import (
    DEPRECATED_PREDICATE,
    HAS_OBSOLESCENCE_REASON,
    OWL_CLASS,
    TERM_REPLACED_BY,
    TERMS_MERGED,
)
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.kgcl_utilities import generate_change_id

TERM_LIST_DIFF = Tuple[CURIE, CURIE]
RESIDUAL_KEY = "__RESIDUAL__"


@dataclass
class DiffConfiguration:
    """Configuration for the differ."""

    simple: bool = False
    group_by_property: PRED_CURIE = None


def _gen_id():
    return generate_change_id()


class DifferInterface(BasicOntologyInterface, ABC):
    """
    Generates Change objects between one ontology and another.

    This uses the KGCL datamodel, see :ref:`kgcl-datamodel` for more information.
    """

    def diff(
        self, other_ontology: BasicOntologyInterface, configuration: DiffConfiguration = None
    ) -> Iterator[Change]:
        """
        Diffs two ontologies.

        The changes that are yielded describe transitions from the current ontology to the other ontology.

        Note that this is not guaranteed to diff every axiom in both ontologies. Only a subset of KGCL change
        types are supported:

        - NodeCreation
        - NodeDeletion
        - NodeMove
        - NodeRename
        - PredicateChange
        - NewTextDefinition
        - NodeTextDefinitionChange

        :param other_ontology:
        :param configuration:
        :return: KGCL change object
        """
        if configuration is None:
            configuration = DiffConfiguration()
        other_ontology_entities = set(list(other_ontology.entities(filter_obsoletes=False)))
        self_entities = set(list(self.entities(filter_obsoletes=False)))
        logging.info(f"Comparing {len(self_entities)} terms in this ontology")
        for e1 in self_entities:
            # e1_types = self.owl_type(e1)
            # is_class = OWL_CLASS in e1_types
            logging.debug(f"Comparing e1 {e1}")
            if e1 not in other_ontology_entities:
                yield NodeDeletion(id=_gen_id(), about_node=e1)
                continue
            if configuration.simple:
                continue
            e1_metadata = self.entity_metadata_map(e1)
            e2_metadata = other_ontology.entity_metadata_map(e1)
            metadata_props = set(e1_metadata.keys()).union(e2_metadata.keys())
            if DEPRECATED_PREDICATE in metadata_props:
                e1_dep = e1_metadata.get(DEPRECATED_PREDICATE, [False])[0]
                e2_dep = e2_metadata.get(DEPRECATED_PREDICATE, [False])[0]
                if e1_dep != e2_dep:
                    # TODO: bundle associated changes
                    if e1_dep and not e2_dep:
                        yield NodeUnobsoletion(id=_gen_id(), about_node=e1)
                    elif not e1_dep and e2_dep:
                        if TERM_REPLACED_BY in e2_metadata:
                            if TERMS_MERGED in e2_metadata.get(HAS_OBSOLESCENCE_REASON, []):
                                yield NodeDirectMerge(
                                    id=_gen_id(),
                                    about_node=e1,
                                    has_direct_replacement=e2_metadata[TERM_REPLACED_BY][0],
                                )
                            else:
                                yield NodeObsoletionWithDirectReplacement(
                                    id=_gen_id(),
                                    about_node=e1,
                                    has_direct_replacement=e2_metadata[TERM_REPLACED_BY][0],
                                )
                        else:
                            yield NodeObsoletion(id=_gen_id(), about_node=e1)
            # Check for definition change/addition
            if self.definition(e1) != other_ontology.definition(e1):
                if self.definition(e1) is None or other_ontology.definition(e1) is None:
                    old_value = new_value = None
                    if self.definition(e1):
                        old_value = self.definition(e1)

                    if other_ontology.definition(e1):
                        new_value = other_ontology.definition(e1)

                    yield NewTextDefinition(
                        id=_gen_id(), about_node=e1, new_value=new_value, old_value=old_value
                    )
                elif self.definition(e1) is not None and other_ontology.definition(e1) is not None:
                    yield NodeTextDefinitionChange(
                        id=_gen_id(),
                        about_node=e1,
                        new_value=other_ontology.definition(e1),
                        old_value=self.definition(e1),
                    )
                else:
                    logging.info(f"Both ontologies have no definition for {e1}")

            differs = self.different_from(e1, other_ontology)
            if differs is not None and not differs:
                continue
            e1_arels = set(self.alias_relationships(e1, exclude_labels=True))
            e2_arels = set(other_ontology.alias_relationships(e1, exclude_labels=True))
            for arel in e1_arels.difference(e2_arels):
                pred, alias = arel
                switches = {r[0] for r in e2_arels if r[1] == alias}
                if len(switches) == 1:
                    e2_arels = set([x for x in e2_arels if x[1] != alias])
                    # TODO: KGCL model needs to include predicates
                    yield SynonymPredicateChange(id=_gen_id(), about_node=e1, old_value=alias)
                else:
                    yield RemoveSynonym(id=_gen_id(), about_node=e1, old_value=alias)
            for arel in e2_arels.difference(e1_arels):
                pred, alias = arel
                yield NewSynonym(id=_gen_id(), about_node=e1, new_value=alias)
            e1_label = self.label(e1)
            e2_label = other_ontology.label(e1)
            if e1_label != e2_label:
                yield NodeRename(
                    id=_gen_id(), about_node=e1, old_value=e1_label, new_value=e2_label
                )
            e1_rels = set(self.outgoing_relationships(e1))
            e2_rels = set(other_ontology.outgoing_relationships(e1))
            for rel in e1_rels.difference(e2_rels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                switches = list({r[0] for r in e2_rels if r[1] == filler})
                if len(switches) == 1:
                    e2_rels = set([x for x in e2_rels if x[1] != filler])
                    if pred != switches[0]:
                        yield PredicateChange(
                            id=_gen_id(), about_edge=edge, old_value=pred, new_value=switches[0]
                        )
                else:
                    yield EdgeDeletion(id=_gen_id(), subject=e1, predicate=pred, object=filler)
            for rel in e2_rels.difference(e1_rels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                yield NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
        logging.info(f"Comparing {len(other_ontology_entities)} terms in other ontology")
        for e2 in other_ontology_entities:
            logging.debug(f"Comparing e2 {e2}")
            if e2 not in self_entities:
                e2_types = other_ontology.owl_type(e2)
                is_class = OWL_CLASS in e2_types
                if is_class:
                    yield ClassCreation(id=_gen_id(), about_node=e2)
                else:
                    yield NodeCreation(id=_gen_id(), about_node=e2)
                continue

    def diff_summary(
        self, other_ontology: BasicOntologyInterface, configuration: DiffConfiguration = None
    ) -> Dict[str, Any]:
        """
        Provides high level summary of differences.

        The result is a two-level dictionary

        - the first level is the grouping key
        - the second level is the type of change

        The value of the second level is a count of the number of changes of that type.



        :param other_ontology:
        :param configuration:
        :return:
        """
        summary = {}
        bins = {
            "All_Obsoletion": [
                kgcl.NodeObsoletion.__name__,
                kgcl.NodeObsoletionWithDirectReplacement.__name__,
                kgcl.NodeDirectMerge.__name__,
            ],
            "All_Synonym": [
                kgcl.NewSynonym.__name__,
                kgcl.RemoveSynonym.__name__,
                kgcl.SynonymPredicateChange.__name__,
                kgcl.SynonymReplacement.__name__,
            ],
        }
        for change in self.diff(other_ontology, configuration):
            if isinstance(change, kgcl.NodeChange):
                about = change.about_node
            elif isinstance(change, kgcl.EdgeChange):
                if isinstance(change, kgcl.EdgeDeletion):
                    about = change.subject
                else:
                    about = change.about_edge.subject
            else:
                about = None
            partition = RESIDUAL_KEY
            if about and configuration and configuration.group_by_property:
                md = self.entity_metadata_map(about)
                if not md or configuration.group_by_property not in md:
                    md = other_ontology.entity_metadata_map(about)
                if configuration.group_by_property in md:
                    v = md[configuration.group_by_property]
                    if len(v) == 1:
                        partition = v[0]
                    else:
                        logging.warning(
                            f"Multiple values for {configuration.group_by_property} = {v}"
                        )
            if partition not in summary:
                summary[partition] = {}
            typ = type(change).__name__
            if typ not in summary[partition]:
                summary[partition][typ] = 0
            summary[partition][typ] += 1
        for partition_summary in summary.values():
            for k, categories in bins.items():
                partition_summary[k] = sum([partition_summary.get(cat, 0) for cat in categories])
        return dict(summary)

    def different_from(
        self, entity: CURIE, other_ontology: BasicOntologyInterface
    ) -> Optional[bool]:
        return None

    def compare_ontology_term_lists(
        self, other_ontology: BasicOntologyInterface
    ) -> Iterator[Change]:
        """
        Provides high level summary of differences

        :param other_ontology:
        :return:
        """
        this_terms = set(self.entities())
        other_terms = set(other_ontology.entities())
        for t in this_terms.difference(other_terms):
            yield NodeDeletion(
                id="x",
                # type='NodeDeletion',
                about_node=t,
            )
        for t in other_terms.difference(this_terms):
            yield NodeCreation(id="x", about_node=t)

    def compare_term_in_two_ontologies(
        self, other_ontology: BasicOntologyInterface, curie: CURIE, other_curie: CURIE = None
    ) -> Any:
        raise NotImplementedError

    def diff_structured(
        self,
        other_ontology: BasicOntologyInterface,
        configuration: DiffConfiguration = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Provides a structured diff of two ontologies

        Required sequence of changes:
        1. New classes
        2. Label changes
        3. Definition changes
        4. Obsoletions
        5. Added synonyms
        6. Added definitions
        7. Changed relationships

        :param other_ontology: Ontology to compare against
        :param configuration: Configuration for the differentiation
        :return: A sequence of changes in the form of a dictionary
        """
        if configuration is None:
            configuration = DiffConfiguration()
        other_ontology_entities = set(list(other_ontology.entities(filter_obsoletes=False)))
        self_entities = set(list(self.entities(filter_obsoletes=False)))

        # ! New classes
        """
            other_ontology_entities - self_entities => ClassCreation/NodeCreation
            self_entities - other_ontology_entities => NodeDeletion
        """
        # Node/Class Creation
        if other_ontology_entities - self_entities:
            list_of_created_nodes = list(other_ontology_entities - self_entities)
            dict_nodes_or_classes = {
                ent: other_ontology.owl_type(ent) for ent in list_of_created_nodes
            }
            if all(OWL_CLASS in types for types in dict_nodes_or_classes.values()):
                yield {
                    CLASS_CREATION: [
                        ClassCreation(id=_gen_id(), about_node=node)
                        for node in list_of_created_nodes
                    ]
                }
            elif all(OWL_CLASS not in types for types in dict_nodes_or_classes.values()):
                yield {
                    NODE_CREATION: [
                        NodeCreation(id=_gen_id(), about_node=node)
                        for node in list_of_created_nodes
                    ]
                }
            else:
                yield {
                    NODE_CREATION: [
                        NodeCreation(id=_gen_id(), about_node=node)
                        for node in list_of_created_nodes
                        if OWL_CLASS not in dict_nodes_or_classes[node]
                    ],
                    CLASS_CREATION: [
                        ClassCreation(id=_gen_id(), about_node=node)
                        for node in list_of_created_nodes
                        if OWL_CLASS in dict_nodes_or_classes[node]
                    ],
                }
        # Node Deletion
        if self_entities - other_ontology_entities:
            list_of_deleted_nodes = list(self_entities - other_ontology_entities)
            yield {
                NODE_DELETION: [
                    NodeDeletion(id=_gen_id(), about_node=node) for node in list_of_deleted_nodes
                ]
            }

        # ! Label changes
        label_change_list = [
            NodeRename(
                id=_gen_id(),
                about_node=entity,
                old_value=self.label(entity),
                new_value=other_ontology.label(entity),
            )
            for entity in self_entities.intersection(other_ontology_entities)
            if self.label(entity) != other_ontology.label(entity)
        ]
        if label_change_list:
            yield {NODE_RENAME: label_change_list}

        # ! Definition changes
        definition_change_list = [
            NodeTextDefinitionChange(
                id=_gen_id(),
                about_node=entity,
                new_value=other_ontology.definition(entity),
                old_value=self.definition(entity),
            )
            for entity in self_entities.intersection(other_ontology_entities)
            if self.definition(entity) != other_ontology.definition(entity)
            and self.definition(entity) is not None
            and other_ontology.definition(entity) is not None
        ]
        if definition_change_list:
            yield {NODE_TEXT_DEFINITION_CHANGE: definition_change_list}

        # ! Obsoletions
        # obsoletion_generator = _generate_obsoletion_changes(
        #     self_entities, self.entity_metadata_map, other_ontology.entity_metadata_map
        # )
        # for obsoletion_change in obsoletion_generator:
        #     if any(obsoletion_change.values()):
        #         yield obsoletion_change
        obsoletion_generator = _generate_obsoletion_changes(
            self_entities, self.entity_metadata_map, other_ontology.entity_metadata_map
        )

        for obsoletion_change in obsoletion_generator:
            if any(obsoletion_change.values()):
                yield obsoletion_change

        # ! Synonyms
        self_aliases = {
            entity: set(self.alias_relationships(entity, exclude_labels=True))
            for entity in self_entities
        }
        other_aliases = {
            entity: set(other_ontology.alias_relationships(entity, exclude_labels=True))
            for entity in self_entities
        }
        synonyms_generator = _generate_synonym_changes(self_entities, self_aliases, other_aliases)
        synonym_changes = defaultdict(list)
        for synonyms_change in synonyms_generator:
            synonym_changes.setdefault(synonyms_change.__class__.__name__, []).append(
                synonyms_change
            )
        if synonym_changes:
            yield synonym_changes

        # ! New definitions
        new_definition_list = [
            NewTextDefinition(
                id=_gen_id(),
                about_node=entity,
                new_value=other_ontology.definition(entity),
                old_value=self.definition(entity),
            )
            for entity in self_entities.intersection(other_ontology_entities)
            if self.definition(entity) is None and other_ontology.definition(entity) is not None
        ]
        if new_definition_list:
            yield {NEW_TEXT_DEFINITION: new_definition_list}

        # ! Relationships
        self_out_rels = {
            entity: set(self.outgoing_relationships(entity)) for entity in self_entities
        }
        other_out_rels = {
            entity: set(other_ontology.outgoing_relationships(entity)) for entity in self_entities
        }

        # Process the entities in parallel using a generator
        for relationship_change in _parallely_get_relationship_changes(
            self_entities, self_out_rels, other_out_rels
        ):
            yield relationship_change


# ! Helper functions
# def _generate_obsoletion_changes(
#     self_entities, self_entity_metadata_map, other_ontology_entity_metadata_map
# ):
#     # Initialize a dictionary to hold the KGCL class objects
#     obsoletion_changes = {
#         NODE_UNOBSOLETION: [],
#         NODE_DIRECT_MERGE: [],
#         NODE_OBSOLETION_WITH_DIRECT_REPLACEMENT: [],
#         NODE_OBSOLETION: [],
#     }

#     # Precompute metadata maps outside of the loop to avoid redundant calculations
#     self_metadata_map = {entity: self_entity_metadata_map(entity) for entity in self_entities}
#     other_metadata_map = {
#         entity: other_ontology_entity_metadata_map(entity) for entity in self_entities
#     }

#     # Prepare deprecation status data using a list comprehension
#     deprecation_data = [
#         (
#             entity,
#             self_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
#             other_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
#         )
#         for entity in self_entities
#     ]

#     # Initialize the dictionary to collect changes
#     obsoletion_changes = {}

#     # Process the prepared deprecation data
#     for e1, e1_dep, e2_dep in deprecation_data:
#         if e1_dep != e2_dep:
#             kgcl_obj = _create_obsoletion_object(e1, e1_dep, e2_dep, other_metadata_map[e1])
#             # Only add key if it has a value
#             if kgcl_obj:
#                 class_name = kgcl_obj.__class__.__name__
#                 # Use setdefault to initialize the list if the key doesn't exist yet
#                 obsoletion_changes.setdefault(class_name, []).append(kgcl_obj)

#     # Yield the collected changes as a single dictionary
#     yield obsoletion_changes


def _create_obsoletion_object(e1, e1_dep, e2_dep, e2_meta):
    if not e1_dep and e2_dep:
        term_replaced_by = e2_meta.get(TERM_REPLACED_BY)
        if term_replaced_by:
            has_obsolescence_reason = e2_meta.get(HAS_OBSOLESCENCE_REASON, [])
            if TERMS_MERGED in has_obsolescence_reason:
                return NodeDirectMerge(
                    id=_gen_id(),
                    about_node=e1,
                    has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
                )
            else:
                return NodeObsoletionWithDirectReplacement(
                    id=_gen_id(),
                    about_node=e1,
                    has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
                )
        else:
            return NodeObsoletion(id=_gen_id(), about_node=e1)
    else:
        return NodeUnobsoletion(id=_gen_id(), about_node=e1)


def _generate_synonym_changes(self_entities, self_aliases, other_aliases):
    for e1 in self_entities:
        e1_arels = self_aliases[e1]
        e2_arels = other_aliases[e1]

        # Pre-calculate the differences
        e1_diff = e1_arels.difference(e2_arels)
        e2_diff = e2_arels.difference(e1_arels)

        for arel in e1_diff:
            _, alias = arel
            switches = {r[0] for r in e2_arels if r[1] == alias}
            if len(switches) == 1:
                # Update e2_arels to remove the alias
                e2_arels = {x for x in e2_arels if x[1] != alias}
                synonym_change = SynonymPredicateChange(
                    id=_gen_id(), about_node=e1, old_value=alias
                )
            else:
                synonym_change = RemoveSynonym(id=_gen_id(), about_node=e1, old_value=alias)

            yield synonym_change

        for arel in e2_diff:
            _, alias = arel
            synonym_change = NewSynonym(id=_gen_id(), about_node=e1, new_value=alias)
            yield synonym_change


def _process_deprecation_data(deprecation_data_item):
    e1, e1_dep, e2_dep, e2_meta = deprecation_data_item
    if e1_dep != e2_dep:
        kgcl_obj = _create_obsoletion_object(e1, e1_dep, e2_dep, e2_meta)
        if kgcl_obj:
            return kgcl_obj.__class__.__name__, kgcl_obj
    return None


def _generate_obsoletion_changes(
    self_entities, self_entity_metadata_map, other_ontology_entity_metadata_map
):
    self_metadata_map = {entity: self_entity_metadata_map(entity) for entity in self_entities}
    other_metadata_map = {
        entity: other_ontology_entity_metadata_map(entity) for entity in self_entities
    }

    deprecation_data = [
        (
            entity,
            self_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
            other_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
            other_metadata_map[entity],
        )
        for entity in self_entities
    ]

    with multiprocessing.Pool() as pool:
        results = pool.map(_process_deprecation_data, deprecation_data)

    obsoletion_changes = {}
    for result in results:
        if result:
            class_name, kgcl_obj = result
            obsoletion_changes.setdefault(class_name, []).append(kgcl_obj)

    yield obsoletion_changes


def _generate_relation_changes(e1, self_out_rels, other_out_rels):
    e1_rels = self_out_rels[e1]
    e2_rels = other_out_rels[e1]
    changes = {}

    for rel in e1_rels.difference(e2_rels):
        pred, filler = rel
        edge = Edge(subject=e1, predicate=pred, object=filler)
        switches = list({r[0] for r in e2_rels if r[1] == filler})
        if len(switches) == 1:
            e2_rels.discard((switches[0], filler))
            if pred != switches[0]:
                changes.setdefault(PredicateChange.__name__, []).append(
                    PredicateChange(
                        id=_gen_id(), about_edge=edge, old_value=pred, new_value=switches[0]
                    )
                )
        else:
            changes.setdefault(EdgeDeletion.__name__, []).append(
                EdgeDeletion(id=_gen_id(), subject=e1, predicate=pred, object=filler)
            )

    for rel in e2_rels.difference(e1_rels):
        pred, filler = rel
        edge = Edge(subject=e1, predicate=pred, object=filler)
        changes.setdefault(NodeMove.__name__, []).append(
            NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
        )


def _parallely_get_relationship_changes(self_entities, self_out_rels, other_out_rels):
    with multiprocessing.Pool() as pool:
        for result in pool.starmap(
            _generate_relation_changes,
            [(e1, self_out_rels, other_out_rels) for e1 in self_entities],
        ):
            if result:
                yield result
