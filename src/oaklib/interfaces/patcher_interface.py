from abc import ABC
from typing import Any, Dict, List, Mapping, Optional

from kgcl_schema.datamodel.kgcl import (
    Activity,
    Change,
    NameBecomesSynonym,
    NewSynonym,
    NodeRename,
)

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE


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
        self, patch: Change, activity: Activity = None, metadata: Mapping[PRED_CURIE, Any] = None
    ) -> Optional[Change]:
        """
        Applies a change description

        :param patch: TBD use KGCL
        :param activity:
        :param metadata:
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

    def expand_change(self, change: Change) -> List[Change]:
        """
        Expand a change object to a list of atomic changes.

        :param change:
        :return:
        """
        if isinstance(change, NameBecomesSynonym):
            if change.change_1 is None:
                change.change_1 = NodeRename(
                    about_node=change.about_node,
                    old_value=change.old_value,
                    new_value=change.new_value,
                )
            if change.change_2 is None:
                current_label = self.label(change.about_node)
                change.change_2 = NewSynonym(about_node=change.about_node, new_value=current_label)
            return [change.change_1, change.change_2]
        return [change]
