from abc import ABC
from typing import Iterator, List, Tuple

from oaklib.datamodels.obograph import DefinitionPropertyValue
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = [
    "OntologyGenerationInterface",
]


class OntologyGenerationInterface(BasicOntologyInterface, ABC):
    """
    Interface for generation of ontologies and ontology terms.
    """

    def generate_definitions(
        self, curies: List[CURIE], style_hints="", **kwargs
    ) -> Iterator[Tuple[CURIE, DefinitionPropertyValue]]:
        """
        Generate text definitions for a list of curies.

        :param curies:
        :param style_hints:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()
