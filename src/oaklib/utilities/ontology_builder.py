from dataclasses import dataclass, field
from typing import List

import kgcl_schema.datamodel.kgcl as kgcl

from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.types import CURIE


def _change_id():
    return "_"


@dataclass
class OntologyBuilder:

    ontology_interface: PatcherInterface

    changes: List[kgcl.Change] = field(default_factory=lambda: [])

    def _add(self, change: kgcl.Change):
        self.changes.append(change)

    def add_class(self, id: CURIE, name: str = None, **kwargs) -> "OntologyBuilder":
        self._add(kgcl.ClassCreation(_change_id(), node_id=id))
        if name:
            self._add(kgcl.NodeRename(_change_id(), about_node=id, new_value=name))
        return self

    def build(self) -> PatcherInterface:
        for change in self.changes:
            print(change)
            self.ontology_interface.apply_patch(change)
        self.changes = []
        return self.ontology_interface

