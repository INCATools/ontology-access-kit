from abc import ABC
from typing import Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

#TODO: Does this class need to exist, it doesn't look like it's being used anywhere
#as an abstract class.

class SkosInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple SKOS vocabularies

    `SKOS <https://www.w3.org/2004/02/skos/>`_
    """

    def concepts(self) -> Iterable[CURIE]:
        """
        Concepts (put here for pydoc).

        :return:
        """
        raise NotImplementedError

    def broader(self, curie: CURIE) -> Iterable[CURIE]:
        """
        Broader (put here for pydoc).

        :param curie:
        :return:
        """
        raise NotImplementedError

    def narrower(self, curie: CURIE) -> Iterable[CURIE]:
        """
        Narrower (put here for pydoc).

        :param curie:
        :return:
        """
        raise NotImplementedError

    def exact(self, curie: CURIE) -> Iterable[CURIE]:
        """
        Exact (put here for pydoc).

        :param curie:
        :return:
        """
        raise NotImplementedError

    def related(self, curie: CURIE) -> Iterable[CURIE]:
        """
        Get related.

        :param curie:
        :return:
        """
        raise NotImplementedError
