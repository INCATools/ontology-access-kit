from abc import ABC
from typing import Collection, Iterable, Tuple

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = [
    "EmbeddingProviderInterface",
]


ENTITY_EMBEDDING = Tuple[CURIE, str, Collection[float]]


class EmbeddingProviderInterface(BasicOntologyInterface, ABC):
    """
    Calculates embeddings for entities.
    """

    embedding_strategy: str = None

    def entities_vectors(
        self,
        entities: Iterable[CURIE],
    ) -> Iterable[ENTITY_EMBEDDING]:
        """
        Generate embeddings.

        :param entities: A collection of entities to generate embeddings for.
        :yield: A generator function that yields embedding vectors.
        """
        raise NotImplementedError
