from abc import ABC
from typing import Dict, List, Iterable

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE


class PatcherInterface(BasicOntologyInterface, ABC):
    """
    Applies diffs

    """

    def apply_patch(self, patch: str) -> None:
        """
        Applies a change description

        :param patch: TBD use KGCL?
        :return:
        """


