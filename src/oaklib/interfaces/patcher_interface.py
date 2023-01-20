import logging
from abc import ABC
from typing import Any, Dict, List, Mapping, Optional

from kgcl_schema.datamodel.kgcl import (
    Activity,
    Change,
    Configuration,
    EdgeCreation,
    EdgeDeletion,
    NameBecomesSynonym,
    NewSynonym,
    NodeObsoletion,
    NodeRename,
)

from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.kgcl_utilities import generate_change_id


class PatcherInterface(BasicOntologyInterface, ABC):
    """
    Applies diffs

    See `KGCL <https://github.com/INCATools/kgcl>`_
    """

    auto_add_contributor_using: PRED_CURIE = None
    """If provided, then any creators of or contributors on a Change object are
       propagated to the entity after application of that change, using this property.
       If this is set then the recommended value is dct:contributor"""

    def apply_patch(
        self,
        patch: Change,
        activity: Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: Configuration = None,
    ) -> Optional[Change]:
        """
        Applies a change description

        :param patch: TBD use KGCL
        :param activity:
        :param metadata:
        :param configuration:
        :return: if successful, return copy of change object with additional metadata attached
        """
        raise NotImplementedError

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        """
        Rewire an ontology replacing all usages of some CURIEs

        :param curie_map:
        :return:
        """
        raise NotImplementedError

    def save(self):
        """
        Commits all changes

        :return:
        """

    def expand_changes(
        self, changes: List[Change], configuration: Configuration = None
    ) -> List[Change]:
        """
        Expand a list of complex change objects to a list of atomic changes.

        :param changes:
        :param configuration:
        :return:
        """
        return [c for change in changes for c in self.expand_change(change, configuration)]

    def expand_change(self, change: Change, configuration: Configuration = None) -> List[Change]:
        """
        Expand a complex change object to a list of atomic changes.

        Examples:

        - An obsoletion command may also generate a label change and removal or rewiring of edges
        - A NameBecomesSynonym may generate a NewSynonym and a NodeRename

        :param change:
        :param configuration:
        :return:
        """
        changes = [change]
        if isinstance(change, NameBecomesSynonym):
            logging.info(f"Expanding {type(change)}")
            if change.change_1 is None:
                change.change_1 = NodeRename(
                    about_node=change.about_node,
                    old_value=change.old_value,
                    new_value=change.new_value,
                )
            if change.change_2 is None:
                current_label = self.label(change.about_node)
                change.change_2 = NewSynonym(
                    generate_change_id(), about_node=change.about_node, new_value=current_label
                )
            return [change.change_1, change.change_2]
        if isinstance(change, NodeObsoletion):
            logging.info(f"Expanding {type(change)}")
            about_node = change.about_node
            changes = [change]
            old_label = self.label(change.about_node)
            obsolete_node_label_prefix = "obsolete "
            # TODO: do this with new version of kgcl
            # if configuration and configuration.obsolete_node_label_prefix is not None:
            #     obsolete_node_label_prefix = configuration.obsolete_node_label_prefix
            new_label = f"{obsolete_node_label_prefix}{old_label}"
            changes.append(
                NodeRename(
                    generate_change_id(),
                    about_node=about_node,
                    old_value=old_label,
                    new_value=new_label,
                )
            )
            parent_relationships = list(self.relationships([about_node]))
            child_relationships = list(self.relationships(objects=[about_node]))
            # TODO: set this based on configuration
            rewire = True
            if rewire:
                rewire_predicates = [IS_A, PART_OF]
                for pred in rewire_predicates:
                    for s, p1, _ in child_relationships:
                        if p1 == pred:
                            for _, p2, o in parent_relationships:
                                if p2 == pred:
                                    ch = EdgeCreation(
                                        generate_change_id(), subject=s, predicate=p2, object=o
                                    )
                                    changes.append(ch)
                                    logging.info(f"Rewiring {s} {p1} {about_node} to {s} {p2} {o}")
            # TODO: set this based on configuration
            remove_edges = True
            if remove_edges:
                for s, p, o in child_relationships + parent_relationships:
                    ch = EdgeDeletion(generate_change_id(), subject=s, predicate=p, object=o)
                    changes.append(ch)
        return changes
