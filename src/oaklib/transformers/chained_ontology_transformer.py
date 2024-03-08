from dataclasses import dataclass
from typing import Any, Collection

from oaklib.transformers.ontology_transformer import OntologyTransformer


@dataclass
class ChainedOntologyTransformer(OntologyTransformer):
    """
    An ontology graph transformer that chains multiple other transformers
    """

    chained_transformers: Collection[OntologyTransformer]

    def transform(self, source_ontology: Any, **kwargs) -> Any:
        for transformer in self.chained_transformers:
            source_ontology = transformer.transform(source_ontology, **kwargs)
        return source_ontology
