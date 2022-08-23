from abc import ABC
from typing import Dict

from kgcl_schema.datamodel.kgcl import Change

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class PatcherInterface(BasicOntologyInterface, ABC):
    """
    Applies diffs

    See `KGCL <https://github.com/INCATools/kgcl>`_
    """

    def apply_patch(self, patch: Change) -> None:
        """
        Applies a change description

        :param patch: TBD use KGCL
        :return:
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
        pass
