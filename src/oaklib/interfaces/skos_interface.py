from abc import ABC
from typing import Dict, List, Tuple, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, LABEL, URI
from rdflib import Graph


class SkosInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple SKOS vocabularies

    `SKOS <https://www.w3.org/2004/02/skos/>`_
    """

    def concepts(self) -> Iterable[CURIE]:
        """

        :return:
        """
        raise NotImplementedError

    def broader(self, curie: CURIE) -> Iterable[CURIE]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

    def narrower(self, curie: CURIE) -> Iterable[CURIE]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

    def exact(self, curie: CURIE) -> Iterable[CURIE]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

    def related(self, curie: CURIE) -> Iterable[CURIE]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError


