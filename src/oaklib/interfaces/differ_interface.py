import logging
import multiprocessing
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, Tuple

import kgcl_schema.datamodel.kgcl as kgcl
from kgcl_schema.datamodel.kgcl import (
    AddNodeToSubset,
    Change,
    ClassCreation,
    Edge,
    EdgeChange,
    EdgeCreation,
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
    RemoveNodeFromSubset,
    RemoveSynonym,
    SynonymPredicateChange,
)

from oaklib.datamodels.vocabulary import (  # OIO_SYNONYM_TYPE_PROPERTY,
    CLASS_CREATION,
    DEPRECATED_PREDICATE,
    HAS_OBSOLESCENCE_REASON,
    MAPPING_EDGE_DELETION,
    NODE_CREATION,
    NODE_DELETION,
    NODE_TEXT_DEFINITION_CHANGE,
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
        - AddNodeToSubset
        - RemoveNodeFromSubset

        Preferred sequence of changes:
        1. New classes
        2. Label changes
        3. Definition changes
        4. Obsoletions
        5. Added synonyms
        6. Added definitions
        7. Changed relationships
        8. Changed subsets

        :param other_ontology: Ontology to compare against
        :param configuration: Configuration for the differentiation
        :return: A sequence of changes in the form of a dictionary
        """
        if configuration is None:
            configuration = DiffConfiguration()
        # * self => old ontology
        # * other_ontology => latest ontology
        other_ontology_entities = set(list(other_ontology.entities(filter_obsoletes=False)))
        self_entities = set(list(self.entities(filter_obsoletes=False)))
        intersection_of_entities = self_entities.intersection(other_ontology_entities)
        obsolete_nodes = set()

        # ! New classes
        # * other_ontology_entities - self_entities => ClassCreation/NodeCreation
        # * self_entities - other_ontology_entities => NodeDeletion

        # Node/Class Creation
        created_entities = other_ontology_entities - self_entities

        if configuration.yield_individual_changes:
            # Yield each creation individually
            for entity in created_entities:
                types = other_ontology.owl_type(entity)
                if OWL_CLASS in types:
                    yield ClassCreation(id=_gen_id(), about_node=entity)
                # elif OIO_SYNONYM_TYPE_PROPERTY in types:
                #     yield NodeCreation(
                #         id=_gen_id(), about_node=OIO_SYNONYM_TYPE_PROPERTY
                #     )
                else:
                    yield NodeCreation(id=_gen_id(), about_node=entity)
        else:
            # Collect creations and yield at the end
            class_creations = []
            node_creations = []

            for entity in created_entities:
                types = other_ontology.owl_type(entity)
                if OWL_CLASS in types:
                    class_creations.append(ClassCreation(id=_gen_id(), about_node=entity))
                # elif OIO_SYNONYM_TYPE_PROPERTY in types:
                #     node_creations.append(
                #         NodeCreation(id=_gen_id(), about_node=OIO_SYNONYM_TYPE_PROPERTY)
                #     )
                else:
                    node_creations.append(NodeCreation(id=_gen_id(), about_node=entity))

            # Yield collected changes as a dictionary if there are any
            changes = {}
            if class_creations:
                changes[CLASS_CREATION] = class_creations
            if node_creations:
                changes[NODE_CREATION] = node_creations
            if changes:
                yield changes

        # Node Deletion with consideration for yield_individual_changes flag
        nodes_to_delete = self_entities - other_ontology_entities

        if nodes_to_delete:
            if configuration.yield_individual_changes:
                # Yield each deletion individually
                for node in nodes_to_delete:
                    yield NodeDeletion(id=_gen_id(), about_node=node)
            else:
                # Yield all deletions at once in a dictionary
                yield {
                    NODE_DELETION: [
                        NodeDeletion(id=_gen_id(), about_node=node) for node in nodes_to_delete
                    ]
                }

        # ! Obsoletions
        other_ontology_entities_with_obsoletes = set(
            other_ontology.entities(filter_obsoletes=False)
        )
        other_ontology_entities_without_obsoletes = set(
            other_ontology.entities(filter_obsoletes=True)
        )
        other_ontology_obsolete_entities = (
            other_ontology_entities_with_obsoletes - other_ontology_entities_without_obsoletes
        )
        other_ontology_unobsolete_entities = (
            other_ontology_entities_without_obsoletes - other_ontology_entities_with_obsoletes
        )
        possible_obsoletes = self_entities.intersection(other_ontology_obsolete_entities)
        self_ontology_without_obsoletes = set(list(self.entities(filter_obsoletes=True)))
        self_ontology_obsoletes = self_entities - self_ontology_without_obsoletes

        # Find NodeUnobsoletions
        possible_unobsoletes = self_ontology_obsoletes.intersection(
            other_ontology_unobsolete_entities
        )

        obsoletion_generator = _generate_obsoletion_changes(
            possible_obsoletes.union(possible_unobsoletes),
            self.entity_metadata_map,
            other_ontology.entity_metadata_map,
        )

        if configuration.yield_individual_changes:
            # Yield each obsoletion_change object individually
            for obsoletion_change in obsoletion_generator:
                obsolete_nodes.add(obsoletion_change.about_node)
                yield obsoletion_change
        else:
            # Collect all obsoletion_change objects in a dictionary and yield them at the end
            obsoletion_changes = defaultdict(list)
            for obsoletion_change in obsoletion_generator:
                if obsoletion_change:
                    class_name = obsoletion_change.type
                    obsolete_nodes.add(obsoletion_change.about_node)
                    obsoletion_changes.setdefault(class_name, []).append(obsoletion_change)

            if obsoletion_changes:
                yield obsoletion_changes

        # ! Remove obsolete nodes from relevant sets
        intersection_of_entities = self_ontology_without_obsoletes.intersection(
            other_ontology_entities_without_obsoletes
        )

        # Initialize variables for label changes, definition changes, new definitions, and synonyms
        if not configuration.yield_individual_changes:
            label_change_list = []
            definition_changes = defaultdict(list)
            new_definition_list = []
            synonym_changes = defaultdict(list)
            edge_creation_list = []
            edge_deletion_list = []
            edge_change_list = []
            subset_addition_list = []
            subset_removal_list = []

        self_aliases = {}
        other_aliases = {}

        # Loop through each entity once and process
        # ! label changes, definition changes, new definitions, and synonyms
        for entity in intersection_of_entities:
            # Label change
            if self.label(entity) != other_ontology.label(entity):
                node_rename = NodeRename(
                    id=_gen_id(),
                    about_node=entity,
                    old_value=self.label(entity),
                    new_value=other_ontology.label(entity),
                )
                if configuration.yield_individual_changes:
                    yield node_rename
                else:
                    label_change_list.append(node_rename)

            # Definition changes
            old_value = self.definition(entity)
            new_value = other_ontology.definition(entity)
            if old_value != new_value and old_value is not None and new_value is not None:
                change = NodeTextDefinitionChange(
                    id=_gen_id(),
                    about_node=entity,
                    new_value=new_value,
                    old_value=old_value,
                )
                if configuration.yield_individual_changes:
                    yield change
                else:
                    definition_changes[NODE_TEXT_DEFINITION_CHANGE].append(change)

            # New definitions
            if self.definition(entity) is None and other_ontology.definition(entity) is not None:
                new_def = NewTextDefinition(
                    id=_gen_id(),
                    about_node=entity,
                    new_value=other_ontology.definition(entity),
                    old_value=self.definition(entity),
                )
                if configuration.yield_individual_changes:
                    yield new_def
                else:
                    new_definition_list.append(new_def)

            # Synonyms - compute both sets of aliases
            self_aliases[entity] = set(self.alias_relationships(entity, exclude_labels=True))
            other_aliases[entity] = set(
                other_ontology.alias_relationships(entity, exclude_labels=True)
            )

            #  ! Mappings
            self_mappings = set(self.simple_mappings_by_curie(entity))
            other_mappings = set(other_ontology.simple_mappings_by_curie(entity))
            mappings_added_set = other_mappings - self_mappings
            mappings_removed_set = self_mappings - other_mappings
            mapping_changed_set = _find_mapping_changes(self_mappings, other_mappings)
            if mappings_added_set:
                for mapping in mappings_added_set:
                    predicate, xref = mapping
                    edge_created = EdgeCreation(
                        id=_gen_id(),
                        subject=entity,
                        predicate=predicate,
                        object=xref,
                    )
                    if configuration.yield_individual_changes:
                        yield edge_created
                    else:
                        edge_creation_list.append(edge_created)
            if mappings_removed_set:
                for mapping in mappings_removed_set:
                    predicate, xref = mapping
                    deleted_edge = EdgeDeletion(
                        id=_gen_id(),
                        subject=entity,
                        predicate=predicate,
                        object=xref,
                    )
                    if configuration.yield_individual_changes:
                        yield deleted_edge
                    else:
                        edge_deletion_list.append(deleted_edge)
            if mapping_changed_set:
                for changes in mapping_changed_set:
                    object, new_predicate, old_predicate = changes
                    edge_change = EdgeChange(
                        id=_gen_id(),
                        about_edge=Edge(subject=entity, predicate=old_predicate, object=object),
                        old_value=old_predicate,
                        new_value=new_predicate,
                    )

                    if configuration.yield_individual_changes:
                        yield edge_change
                    else:
                        edge_change_list.append(edge_change)

            # ! Subset changes
            self_subsets = set(self.terms_subsets([entity]))
            other_subsets = set(other_ontology.terms_subsets([entity]))
            subsets_added_set = other_subsets - self_subsets
            subsets_removed_set = self_subsets - other_subsets
            if subsets_added_set:
                for _, subset in subsets_added_set:
                    change = AddNodeToSubset(
                        id=_gen_id(),
                        about_node=entity,
                        in_subset=subset,
                    )
                    if configuration.yield_individual_changes:
                        yield change
                    else:
                        subset_addition_list.append(change)
            if subsets_removed_set:
                for _, subset in subsets_removed_set:
                    change = RemoveNodeFromSubset(
                        id=_gen_id(),
                        about_node=entity,
                        in_subset=subset,
                    )
                    if configuration.yield_individual_changes:
                        yield change
                    else:
                        subset_removal_list.append(change)

        # Yield collected changes after processing all entities
        if not configuration.yield_individual_changes:
            if label_change_list:
                yield {NodeRename.__name__: label_change_list}
            if definition_changes[NodeTextDefinitionChange.__name__]:
                yield definition_changes
            if new_definition_list:
                yield {NewTextDefinition.__name__: new_definition_list}
            if edge_creation_list:
                yield {EdgeCreation.__name__: edge_creation_list}
            if edge_deletion_list:
                yield {MAPPING_EDGE_DELETION: edge_deletion_list}
            if edge_change_list:
                yield {EdgeChange.__name__: edge_change_list}
            if subset_addition_list:
                yield {AddNodeToSubset.__name__: subset_addition_list}
            if subset_removal_list:
                yield {RemoveNodeFromSubset.__name__: subset_removal_list}

        # Process synonyms changes after collecting all aliases
        synonyms_generator = _generate_synonym_changes(
            intersection_of_entities, self_aliases, other_aliases
        )
        if configuration.yield_individual_changes:
            # Yield each synonyms_change object individually
            for synonyms_change in synonyms_generator:
                yield synonyms_change
        else:
            # Collect all changes in a defaultdict and yield them at the end
            for synonyms_change in synonyms_generator:
                synonym_changes[synonyms_change.__class__.__name__].append(synonyms_change)
            if synonym_changes:
                yield synonym_changes

        # ! Relationships
        self_out_rels = {
            entity: set(self.outgoing_relationships(entity))
            for entity in self_ontology_without_obsoletes
        }
        other_out_rels = {
            entity: set(other_ontology.outgoing_relationships(entity))
            for entity in self_ontology_without_obsoletes
        }

        # Process the entities in parallel using a generator
        list_of_changes = defaultdict(list) if not configuration.yield_individual_changes else []
        for relationship_changes in _parallely_get_relationship_changes(
            self_ontology_without_obsoletes,
            self_out_rels,
            other_out_rels,
            configuration.yield_individual_changes,
        ):
            for change in relationship_changes:
                if configuration.yield_individual_changes:
                    yield change
                else:
                    # Collect all changes in a defaultdict
                    for change_type, change_list in change.items():
                        list_of_changes.setdefault(change_type, []).extend(change_list)

        if not configuration.yield_individual_changes:
            yield list_of_changes  # Yield the collected changes once at the end

    def diff_summary(
        self,
        other_ontology: BasicOntologyInterface,
        configuration: DiffConfiguration = None,
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
        self,
        other_ontology: BasicOntologyInterface,
        curie: CURIE,
        other_curie: CURIE = None,
    ) -> Any:
        raise NotImplementedError


# ! Helper functions for the diff method
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
    entities, self_entity_metadata_map, other_ontology_entity_metadata_map
):
    self_metadata_map = {entity: self_entity_metadata_map(entity) for entity in entities}
    other_metadata_map = {entity: other_ontology_entity_metadata_map(entity) for entity in entities}

    deprecation_data = [
        (
            entity,
            self_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
            other_metadata_map[entity].get(DEPRECATED_PREDICATE, [False])[0],
            other_metadata_map[entity],
        )
        for entity in entities
    ]

    for item in deprecation_data:
        results = _process_deprecation_data(item)
        for result in results:
            if result:
                yield result


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
        change = NodeMove(id=_gen_id(), about_edge=edge)
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


def _find_mapping_changes(set1, set2):
    # Convert sets to dictionaries for easier lookup
    dict1 = {t[1]: t[0] for t in set1}
    dict2 = {t[1]: t[0] for t in set2}

    # Find changes
    changes = []
    for key in dict1:
        if key in dict2 and dict1[key] != dict2[key]:
            changes.append((key, dict1[key], dict2[key]))
    return changes
