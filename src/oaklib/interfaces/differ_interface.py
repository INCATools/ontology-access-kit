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
    OBSOLETE_SUBSTRING,
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
    yield_individual_changes: bool = True


def _gen_id():
    return generate_change_id()


class DifferInterface(BasicOntologyInterface, ABC):
    """
    Generates Change objects between one ontology and another.

    This uses the KGCL datamodel, see :ref:`kgcl-datamodel` for more information.
    """

    def diff(
        self,
        other_ontology: BasicOntologyInterface,
        configuration: DiffConfiguration = None,
    ) -> Iterator[Dict[str, Any]]:
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

        Preferred sequence of changes:
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
        intersection_of_entities = self_entities.intersection(other_ontology_entities)

        # ! New classes
        # * other_ontology_entities - self_entities => ClassCreation/NodeCreation
        # * self_entities - other_ontology_entities => NodeDeletion

        # Node/Class Creation
        if other_ontology_entities - self_entities:
            list_of_created_nodes = list(other_ontology_entities - self_entities)
            dict_nodes_or_classes = {
                ent: other_ontology.owl_type(ent) for ent in list_of_created_nodes
            }

            class_creations = []
            node_creations = []

            # Instead of checking all() twice, iterate once and classify each node
            for node, types in dict_nodes_or_classes.items():
                if OWL_CLASS in types:
                    if configuration.yield_individual_changes:
                        yield ClassCreation(id=_gen_id(), about_node=node)
                    else:
                        class_creations.append(ClassCreation(id=_gen_id(), about_node=node))
                else:
                    if configuration.yield_individual_changes:
                        yield NodeCreation(id=_gen_id(), about_node=node)
                    else:
                        node_creations.append(NodeCreation(id=_gen_id(), about_node=node))

            # Now yield based on the flag and whether there are items in the lists
            if not configuration.yield_individual_changes:
                changes = {}
                if class_creations:
                    changes[CLASS_CREATION] = class_creations
                if node_creations:
                    changes[NODE_CREATION] = node_creations
                if changes:
                    yield changes

        # Node Deletion with consideration for yield_individual_changes flag
        nodes_to_delete = self_entities - other_ontology_entities

        if configuration.yield_individual_changes:
            for node in nodes_to_delete:
                yield NodeDeletion(id=_gen_id(), about_node=node)
        else:
            yield {
                NODE_DELETION: [
                    NodeDeletion(id=_gen_id(), about_node=node) for node in nodes_to_delete
                ]
            }

        # ! Obsoletions
        obsoletion_generator = _generate_obsoletion_changes(
            self_entities,
            self.entity_metadata_map,
            other_ontology.entity_metadata_map,
        )

        if configuration.yield_individual_changes:
            # Yield each obsoletion_change object individually
            for obsoletion_change in obsoletion_generator:
                yield obsoletion_change
        else:
            # Collect all obsoletion_change objects in a dictionary and yield them at the end
            obsoletion_changes = defaultdict(list)
            for obsoletion_change in obsoletion_generator:
                if obsoletion_change:
                    class_name = obsoletion_change.__class__.__name__
                    obsoletion_changes.setdefault(class_name, []).append(obsoletion_change)

            if obsoletion_changes:
                yield obsoletion_changes

        # ! Label changes
        if not configuration.yield_individual_changes:
            label_change_list = []
        for entity in intersection_of_entities:
            if self.label(entity) != other_ontology.label(entity) and not (
                other_ontology.label(entity).startswith(OBSOLETE_SUBSTRING)
                or other_ontology.label(entity).startswith(OBSOLETE_SUBSTRING.upper())
            ):
                node_rename = NodeRename(
                    id=_gen_id(),
                    about_node=entity,
                    old_value=self.label(entity),
                    new_value=other_ontology.label(entity),
                )
                if configuration.yield_individual_changes:
                    # Yield NodeRename objects individually if the flag is True
                    yield node_rename
                else:
                    # Collect NodeRename objects in a list if the flag is False
                    label_change_list.append(node_rename)

        # If the flag is False and there are collected changes, yield them as a dictionary
        if not configuration.yield_individual_changes and label_change_list:
            yield {NODE_RENAME: label_change_list}

        # ! Definition changes
        for entity in intersection_of_entities:
            old_value = self.definition(entity)
            new_value = other_ontology.definition(entity)

            if (
                old_value != new_value
                and old_value is not None
                and new_value is not None
                and not (
                    new_value.startswith(OBSOLETE_SUBSTRING)
                    or new_value.startswith(OBSOLETE_SUBSTRING.upper())
                )
            ):
                change = NodeTextDefinitionChange(
                    id=_gen_id(),
                    about_node=entity,
                    new_value=new_value,
                    old_value=old_value,
                )

                if configuration.yield_individual_changes:
                    yield change
                else:
                    # If we're not yielding individually, collect changes in a generator
                    definition_change_gen = (change for _ in [None])  # Generator with one item

                    # Yield the collected changes as a dictionary when the first change occurs
                    yield {NODE_TEXT_DEFINITION_CHANGE: list(definition_change_gen)}
                    break  # Exit the loop after yielding the dictionary

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
        if configuration.yield_individual_changes:
            # Yield each synonyms_change object individually
            for synonyms_change in synonyms_generator:
                yield synonyms_change
        else:
            # Collect all changes in a defaultdict and yield them at the end
            synonym_changes = defaultdict(list)
            for synonyms_change in synonyms_generator:
                synonym_changes[synonyms_change.__class__.__name__].append(synonyms_change)

            if synonym_changes:
                yield synonym_changes

        # ! New definitions
        if configuration.yield_individual_changes:
            # Yield each NewTextDefinition object individually
            for entity in intersection_of_entities:
                if (
                    self.definition(entity) is None
                    and other_ontology.definition(entity) is not None
                ):
                    yield NewTextDefinition(
                        id=_gen_id(),
                        about_node=entity,
                        new_value=other_ontology.definition(entity),
                        old_value=self.definition(entity),
                    )
        else:
            # Collect all NewTextDefinition objects in a list and yield them at once
            new_definition_list = [
                NewTextDefinition(
                    id=_gen_id(),
                    about_node=entity,
                    new_value=other_ontology.definition(entity),
                    old_value=self.definition(entity),
                )
                for entity in intersection_of_entities
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
        for relationship_changes in _parallely_get_relationship_changes(
            self_entities,
            self_out_rels,
            other_out_rels,
            configuration.yield_individual_changes,
        ):
            for change in relationship_changes:
                if configuration.yield_individual_changes:
                    yield change
                else:
                    # Collect all changes in a defaultdict and yield them at the end
                    for change_type, change_list in change.items():
                        if change_list:
                            yield {change_type: change_list}

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


# ! Helper functions for the diff method
# def _create_obsoletion_object(e1, e1_dep, e2_dep, e2_meta):
#     if not e1_dep and e2_dep:
#         term_replaced_by = e2_meta.get(TERM_REPLACED_BY)
#         if term_replaced_by is None:
#             return NodeObsoletion(id=_gen_id(), about_node=e1)
#         else:
#             has_obsolescence_reason = e2_meta.get(HAS_OBSOLESCENCE_REASON, [])
#             if TERMS_MERGED in has_obsolescence_reason:
#                 return NodeDirectMerge(
#                     id=_gen_id(),
#                     about_node=e1,
#                     has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
#                 )
#             else:
#                 return NodeObsoletionWithDirectReplacement(
#                     id=_gen_id(),
#                     about_node=e1,
#                     has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
#                 )
#     else:
#         return NodeUnobsoletion(id=_gen_id(), about_node=e1)


def _generate_synonym_changes(self_entities, self_aliases, other_aliases):
    for e1 in self_entities:
        e1_arels = self_aliases[e1]
        e2_arels = other_aliases[e1]

        # Pre-calculate the differences
        e1_diff = e1_arels.difference(e2_arels)
        e2_diff = e2_arels.difference(e1_arels)

        for arel in e1_diff:
            pred, alias = arel
            switches = {r[0] for r in e2_arels if r[1] == alias}
            if len(switches) == 1:
                # Update e2_arels to remove the alias
                e2_arels = {x for x in e2_arels if x[1] != alias}
                synonym_change = SynonymPredicateChange(
                    id=_gen_id(),
                    about_node=e1,
                    target=alias,
                    old_value=pred,
                    new_value=switches.pop(),
                )
            else:
                # ! Remove obsoletes
                if not (
                    alias.startswith(OBSOLETE_SUBSTRING)
                    or alias.startswith(OBSOLETE_SUBSTRING.upper())
                ):
                    synonym_change = RemoveSynonym(id=_gen_id(), about_node=e1, old_value=alias)

            yield synonym_change

        for arel in e2_diff:
            pred, alias = arel
            synonym_change = NewSynonym(
                id=_gen_id(), about_node=e1, new_value=alias, predicate=pred
            )
            yield synonym_change


def _process_deprecation_data(deprecation_data_item):
    e1, e1_dep, e2_dep, e2_meta = deprecation_data_item
    if e1_dep != e2_dep:
        #     kgcl_obj = _create_obsoletion_object(e1, e1_dep, e2_dep, e2_meta)
        #     if kgcl_obj:
        #         return kgcl_obj.__class__.__name__, kgcl_obj
        # return None
        if not e1_dep and e2_dep:
            term_replaced_by = e2_meta.get(TERM_REPLACED_BY)
            if term_replaced_by is None:
                yield NodeObsoletion(id=_gen_id(), about_node=e1)
            else:
                has_obsolescence_reason = e2_meta.get(HAS_OBSOLESCENCE_REASON, [])
                if TERMS_MERGED in has_obsolescence_reason:
                    yield NodeDirectMerge(
                        id=_gen_id(),
                        about_node=e1,
                        has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
                    )
                else:
                    yield NodeObsoletionWithDirectReplacement(
                        id=_gen_id(),
                        about_node=e1,
                        has_direct_replacement=e2_meta[TERM_REPLACED_BY][0],
                    )
        else:
            yield NodeUnobsoletion(id=_gen_id(), about_node=e1)


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

    for item in deprecation_data:
        results = _process_deprecation_data(item)
        for result in results:
            if result:
                yield result

    # with multiprocessing.Pool() as pool:
    #     results = pool.map(_process_deprecation_data, deprecation_data)

    # if yield_individual_changes:
    #     # Yield individual KGCL objects if the flag is set
    #     for result in results:
    #         if result:
    #             _, kgcl_obj = result
    #             yield kgcl_obj
    # else:
    #     # Initialize the dictionary to collect obsoletion changes
    #     obsoletion_changes = {}

    #     for result in results:
    #         if result:
    #             class_name, kgcl_obj = result
    #             # Aggregate changes by class name
    #             obsoletion_changes.setdefault(class_name, []).append(kgcl_obj)

    #     # Yield the aggregated changes if we're not yielding individual changes
    #     if obsoletion_changes:
    #         yield obsoletion_changes


def _generate_relation_changes(e1, self_out_rels, other_out_rels, yield_individual_changes):
    e1_rels = self_out_rels[e1]
    e2_rels = other_out_rels[e1]
    changes = [] if yield_individual_changes else defaultdict(list)

    for rel in e1_rels.difference(e2_rels):
        pred, alias = rel
        edge = Edge(subject=e1, predicate=pred, object=alias)
        switches = list({r[0] for r in e2_rels if r[1] == alias})
        if len(switches) == 1:
            e2_rels.discard((switches[0], alias))
            if pred != switches[0]:
                change = PredicateChange(
                    id=_gen_id(), about_edge=edge, old_value=pred, new_value=switches[0]
                )
                if yield_individual_changes:
                    changes.append(change)
                else:
                    changes.setdefault(PredicateChange.__name__, []).append(change)
        else:
            change = EdgeDeletion(id=_gen_id(), subject=e1, predicate=pred, object=alias)
            if yield_individual_changes:
                changes.append(change)
            else:
                changes.setdefault(EdgeDeletion.__name__, []).append(change)

    for rel in e2_rels.difference(e1_rels):
        pred, alias = rel
        edge = Edge(subject=e1, predicate=pred, object=alias)
        change = NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
        if yield_individual_changes:
            changes.append(change)
        else:
            changes.setdefault(NodeMove.__name__, []).append(change)

    # If not yielding individual changes and there are changes, return them as a dictionary
    if not yield_individual_changes and changes:
        return [changes]

    # Otherwise, return the list of changes
    return changes


def _parallely_get_relationship_changes(
    self_entities, self_out_rels, other_out_rels, yield_individual_changes
):
    with multiprocessing.Pool() as pool:
        results = pool.starmap(
            _generate_relation_changes,
            [(e1, self_out_rels, other_out_rels, yield_individual_changes) for e1 in self_entities],
        )
        for result in results:
            if result:
                yield result
