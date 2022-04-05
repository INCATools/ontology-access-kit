from abc import ABC
from typing import Dict, List, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE


class PatcherInterface(BasicOntologyInterface, ABC):
    """
    Applies diffs

    See `KGCL <https://github.com/cmungall/knowledge-graph-change-language>`_
    """

    def apply_patch(self, patch: str) -> None:
        """
        Applies a change description

        :param patch: TBD use KGCL?
        :return:
        """


