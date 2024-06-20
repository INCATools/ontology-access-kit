import logging
import multiprocessing
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Tuple

import kgcl_schema.datamodel.kgcl as kgcl
from kgcl_schema.datamodel.kgcl import (
    AddNodeToSubset,
    Change,
    ClassCreation,
    Edge,
    EdgeDeletion,
    MappingCreation,
    # MappingReplacement,
    MappingPredicateChange,
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
    RemoveMapping,
    RemoveNodeFromSubset,
    RemoveSynonym,
    RemoveTextDefinition,
    SynonymPredicateChange,
)

from oaklib.datamodels.vocabulary import (  # OIO_SYNONYM_TYPE_PROPERTY,
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

logger = logging.getLogger(__name__)


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

    This uses the KGCL datamodel, see `<https://w3id.org/kgcl/>`_ for more information.
    """

    def changed_nodes(
        self,
        other_ontology: BasicOntologyInterface,
        configuration: DiffConfiguration = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, str]]:
        raise NotImplementedError

    def grouped_diff(
        self,
        *args,
        **kwargs,
    ) -> Iterator[Tuple[str, List[Change]]]:
        """
        Yields changes grouped by type.

        This wraps the :meth:`diff` method and groups the changes by type.

        :param args:
        :param kwargs:
        :return:
        """
        changes = list(self.diff(*args, **kwargs))
        change_map = defaultdict(list)
        for change in changes:
            change_map[change.type].append(change)
        for k, vs in change_map.items():
            yield k, vs

    def diff(
        self,
        other_ontology: BasicOntologyInterface,
        configuration: DiffConfiguration = None,
        **kwargs,
    ) -> Iterator[Change]:
        """
        Diffs two ontologies.

        The changes that are yielded describe transitions from the current ontology to the other ontology.

        Note that this is not guaranteed to diff every axiom in both ontologies. Different implementations
        may implement different subsets.

        Example usage:

        >>> from oaklib import get_adapter
        >>> from linkml_runtime.dumpers import yaml_dumper
        >>> path1 = "simpleobo:tests/input/go-nucleus.obo"
        >>> path2 = "simpleobo:tests/input/go-nucleus-modified.obo"
        >>> ont1 = get_adapter(path1)
        >>> ont2 = get_adapter(path2)
        >>> for change in ont1.diff(ont2):
        ...     print(yaml_dumper.dumps(change))
        <BLANKLINE>
        ...
        type: NodeRename
        old_value: catalytic activity
        new_value: enzyme activity
        about_node: GO:0003824
        ...


        :param other_ontology: Ontology to compare against
        :param configuration: Configuration for the differentiation
        :return: A sequence of changes in the form of a dictionary
        """
        if configuration is None:
            configuration = DiffConfiguration()
        logging.info(f"Configuration: {configuration}")
        # * self => old ontology
        # * other_ontology => latest ontology
        other_ontology_entities = set(list(other_ontology.entities(filter_obsoletes=False)))
        logger.info(f"other_ontology_entities = {len(other_ontology_entities)}")
        self_entities = set(list(self.entities(filter_obsoletes=False)))
        logger.info(f"self_entities = {len(self_entities)}")
        intersection_of_entities = self_entities.intersection(other_ontology_entities)
        obsolete_nodes = set()

        # ! New classes
        # * other_ontology_entities - self_entities => ClassCreation/NodeCreation
        # * self_entities - other_ontology_entities => NodeDeletion

        # Node/Class Creation
        created_entities = other_ontology_entities - self_entities
        logger.info(f"Created = {len(created_entities)}")

        logger.info("finding Creations")
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

        logger.info("finding Deletions")
        nodes_to_delete = self_entities - other_ontology_entities

        if nodes_to_delete:
            for node in nodes_to_delete:
                yield NodeDeletion(id=_gen_id(), about_node=node)

        logger.info("finding Obsoletions")
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

        logger.info("finding Unsoletions")
        possible_unobsoletes = self_ontology_obsoletes.intersection(
            other_ontology_unobsolete_entities
        )

        obsoletion_generator = _generate_obsoletion_changes(
            possible_obsoletes.union(possible_unobsoletes),
            self.entity_metadata_map,
            other_ontology.entity_metadata_map,
        )

        logger.info("Remaining...")
        for obsoletion_change in obsoletion_generator:
            obsolete_nodes.add(obsoletion_change.about_node)
            yield obsoletion_change

        logger.info("Remove obsolete nodes from relevant sets")
        intersection_of_entities = self_ontology_without_obsoletes.intersection(
            other_ontology_entities_without_obsoletes
        )

        logger.info("finding remaining changes")

        self_aliases = {}
        other_aliases = {}

        # Loop through each entity once and process
        logger.info("label changes, definition changes, new definitions, and synonyms")
        for entity in intersection_of_entities:
            # Label change
            if self.label(entity) != other_ontology.label(entity):
                node_rename = NodeRename(
                    id=_gen_id(),
                    about_node=entity,
                    old_value=self.label(entity),
                    new_value=other_ontology.label(entity),
                )
                yield node_rename

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
                yield change

            # New definitions
            if self.definition(entity) is None and other_ontology.definition(entity) is not None:
                new_def = NewTextDefinition(
                    id=_gen_id(),
                    about_node=entity,
                    new_value=other_ontology.definition(entity),
                    old_value=self.definition(entity),
                )
                yield new_def

            # definition removal
            if self.definition(entity) is not None and other_ontology.definition(entity) is None:
                yield RemoveTextDefinition(
                    id=_gen_id(),
                    about_node=entity,
                    old_value=self.definition(entity),
                    new_value=other_ontology.definition(entity),
                )

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
                    mapping_created = MappingCreation(
                        id=_gen_id(),
                        subject=entity,
                        predicate=predicate,
                        object=xref,
                    )
                    yield mapping_created
            if mappings_removed_set:
                for mapping in mappings_removed_set:
                    predicate, xref = mapping
                    deleted_mapping = RemoveMapping(
                        id=_gen_id(),
                        about_node=entity,
                        predicate=predicate,
                        object=xref,
                    )
                    yield deleted_mapping
            if mapping_changed_set:
                for changes in mapping_changed_set:
                    object, new_predicate, old_predicate = changes
                    mapping_change = MappingPredicateChange(
                        id=_gen_id(),
                        about_node=entity,
                        object=object,
                        old_value=old_predicate,
                        new_value=new_predicate,
                    )

                    yield mapping_change

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
                    yield change
            if subsets_removed_set:
                for _, subset in subsets_removed_set:
                    change = RemoveNodeFromSubset(
                        id=_gen_id(),
                        about_node=entity,
                        in_subset=subset,
                    )
                    yield change

        logger.info("Process synonyms changes after collecting all aliases")
        synonyms_generator = _generate_synonym_changes(
            intersection_of_entities, self_aliases, other_aliases
        )
        for synonyms_change in synonyms_generator:
            yield synonyms_change

        logger.info("Relationships")
        self_out_rels = {
            entity: set(self.outgoing_relationships(entity))
            for entity in self_ontology_without_obsoletes
        }
        other_out_rels = {
            entity: set(other_ontology.outgoing_relationships(entity))
            for entity in self_ontology_without_obsoletes
        }

        # Process the entities in parallel using a generator
        yield from _parallely_get_relationship_changes(
            self_ontology_without_obsoletes,
            self_out_rels,
            other_out_rels,
        )

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
                about = change.subject
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
                        logger.warning(
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
        **kwargs,
    ) -> Any:
        raise NotImplementedError


# ! Helper functions for the diff method
def _generate_synonym_changes(self_entities, self_aliases, other_aliases) -> Iterator[Change]:
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


def _process_deprecation_data(deprecation_data_item) -> Iterator[Change]:
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


def _generate_relation_changes(e1, self_out_rels, other_out_rels) -> List[Change]:
    e1_rels = self_out_rels[e1]
    e2_rels = other_out_rels[e1]
    changes = []

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
                changes.append(change)
        else:
            change = EdgeDeletion(id=_gen_id(), subject=e1, predicate=pred, object=alias)
            changes.append(change)

    for rel in e2_rels.difference(e1_rels):
        pred, alias = rel
        edge = Edge(subject=e1, predicate=pred, object=alias)
        change = NodeMove(id=_gen_id(), about_edge=edge)
        changes.append(change)

    return changes


def _parallely_get_relationship_changes(
    self_entities, self_out_rels, other_out_rels
) -> Iterator[Change]:
    with multiprocessing.Pool() as pool:
        results = pool.starmap(
            _generate_relation_changes,
            [(e1, self_out_rels, other_out_rels) for e1 in self_entities],
        )
        for result in results:
            yield from result


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
