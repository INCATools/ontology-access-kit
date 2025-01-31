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
from oaklib.interfaces.obograph_interface import OboGraphInterface
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

    ignore_invalid_changes: bool = False
    """If True, then invalid changes are ignored. If False, then invalid changes raise an exception"""

    def apply_patch(
        self,
        patch: Change,
        activity: Activity = None,
        metadata: Mapping[PRED_CURIE, Any] = None,
        configuration: Configuration = None,
        strict=False,
    ) -> Optional[Change]:
        """
        Applies a change description

        :param patch: TBD use KGCL
        :param activity:
        :param metadata:
        :param configuration:
        :param strict: if True, raise an exception if the change cannot be applied
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
        self, changes: List[Change], configuration: Configuration = None, apply=False
    ) -> List[Change]:
        """
        Expand a list of complex change objects to a list of atomic changes.

        :param changes:
        :param configuration:
        :param apply: if True, apply the changes
        :return:
        """
        expanded_changes = []
        for c in changes:
            c_expanded = self.expand_change(c, configuration)
            if apply:
                for c2 in c_expanded:
                    self.apply_patch(c2)
            expanded_changes.extend(c_expanded)
        return expanded_changes

    def expand_change(self, change: Change, configuration: Configuration = None) -> List[Change]:
        """
        Expand a complex change object to a list of atomic changes.

        Examples
        --------
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
            if isinstance(self, OboGraphInterface):
                for ldef in self.logical_definitions(self.entities()):
                    if about_node in ldef.genusIds or about_node in [
                        r.fillerId for r in ldef.restrictions
                    ]:
                        message = (
                            f"{about_node} used in logical definition of {ldef.definedClassId}"
                        )
                        if self.ignore_invalid_changes:
                            logging.warning(f"SKIPPING {change}; reason={message}")
                            return []
                        raise ValueError(message)
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
                new_edges = []
                transitive_predicates = [IS_A, PART_OF]
                for s, p1, _ in child_relationships:
                    for _, p2, o in parent_relationships:
                        if p1 == p2 and p1 in transitive_predicates:
                            pred = p1
                        elif p1 == IS_A:
                            pred = p2
                        elif p2 == IS_A:
                            pred = p1
                        else:
                            pred = None
                        if pred:
                            e = (s, pred, o)
                            if e in new_edges:
                                continue
                            if e in self.relationships([s]):
                                # edge previously existed
                                continue
                            new_edges.append(e)
                            desc = f"Rewired from link to {about_node} {self.label(about_node)}"
                            ch = EdgeCreation(
                                generate_change_id(),
                                subject=s,
                                predicate=pred,
                                object=o,
                                change_description=desc,
                            )
                            changes.append(ch)
                            logging.info(f"Rewiring {s} {p1} {about_node} to {s} {pred} {o}")
            # TODO: set this based on configuration
            remove_edges = True
            if remove_edges:
                for s, p, o in child_relationships + parent_relationships:
                    ch = EdgeDeletion(generate_change_id(), subject=s, predicate=p, object=o)
                    logging.info(f"Removing {s} {p} {o}")
                    changes.append(ch)
        return changes

    def undo(self, changes: List[Change], expand=False, strict=True, **kwargs) -> List[Change]:
        """
        Undo a list of changes

        :param changes:
        :param kwargs:
        :return:
        """
        reversed = self.reverse_changes(changes)
        if expand:
            reversed = self.expand_changes(reversed)
        applied_changes = []
        while reversed:
            change = reversed.pop()
            applied_change = self.apply_patch(change, **kwargs)
            if applied_change:
                applied_changes.append(applied_change)
            elif strict:
                raise ValueError(f"Could not apply {change}")
        return applied_changes

    def reverse_changes(self, changes: List[Change]) -> List[Change]:
        """
        Creates reciprocal Undo operations for a list of changes

        :param changes:
        :return:
        """
        raise NotImplementedError

    def add_contributors(self, curie: CURIE, agents: List[CURIE]) -> None:
        raise NotImplementedError

    def set_creator(self, curie: CURIE, agent: CURIE) -> None:
        raise NotImplementedError
