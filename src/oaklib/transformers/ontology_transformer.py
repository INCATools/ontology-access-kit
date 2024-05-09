from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class OntologyTransformer(ABC):  # noqa
    """
    A class for transforming ontologies
    """

    def transform(self, source_ontology: Any, **kwargs) -> Any:
        """
        Transforms an ontology into another ontology

        :param source_ontology:
        :param kwargs: additional configuration arguments
        :return:
        """
        raise NotImplementedError
