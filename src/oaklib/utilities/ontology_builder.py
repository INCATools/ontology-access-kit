from dataclasses import dataclass, field
from typing import List

import kgcl_schema.datamodel.kgcl as kgcl

from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.types import CURIE, PRED_CURIE


def _change_id():
    return "_"


@dataclass
class OntologyBuilder:
    """
    A class for creating ontologies that follows the builder pattern

    Under the hood this uses :ref:`KGCL` objects

    Currently this is not yet fully featured, and is recommended mostly for tests
    """

    ontology_interface: PatcherInterface
    """Wrapper ontology interface - cumulative changes are passed here"""

    changes: List[kgcl.Change] = field(default_factory=lambda: [])
    """List of changes to be applied"""

    def _add(self, change: kgcl.Change) -> "OntologyBuilder":
        self.changes.append(change)
        return self

    def add_class(
        self, id: CURIE, name: str = None, is_as: List[CURIE] = None
    ) -> "OntologyBuilder":
        """
        Adds a new class

        :param id:
        :param name:
        :return:
        """
        self._add(kgcl.ClassCreation(_change_id(), node_id=id))
        if name:
            self._add(kgcl.NodeRename(_change_id(), about_node=id, new_value=name))
        if is_as:
            for is_a in is_as:
                self.add_is_a(id, is_a)
        return self

    def add_is_a(self, subject: CURIE, object: CURIE) -> "OntologyBuilder":
        """
        Adds an is-a relationship

        :param subject:
        :param object:
        :return:
        """
        return self.add_relationship(subject, IS_A, object)

    def add_relationship(
        self, subject: CURIE, predicate: PRED_CURIE, object: CURIE
    ) -> "OntologyBuilder":
        """
        Adds a relationship

        See :ref:`Edge`

        :param subject:
        :param predicate:
        :param object:
        :return:
        """
        return self._add(
            kgcl.EdgeCreation(_change_id(), subject=subject, predicate=predicate, object=object)
        )

    def build(self) -> PatcherInterface:
        for change in self.changes:
            self.ontology_interface.apply_patch(change)
        self.changes = []
        return self.ontology_interface
