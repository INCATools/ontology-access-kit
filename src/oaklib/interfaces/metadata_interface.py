import logging
from abc import ABC
from typing import Dict, List, Tuple, Iterable, Optional

from oaklib.datamodels.vocabulary import IS_A, HAS_DEFINITION_CURIE
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
import oaklib.datamodels.ontology_metadata as om
import sssom
from oaklib.types import CURIE


class MetadataInterface(BasicOntologyInterface, ABC):

    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        raise NotImplementedError

    def definition_with_annotations(self, curie: CURIE) -> Optional[Tuple[str, List[om.Annotation]]]:
        for ax in self.statements_with_annotations(curie):
            if ax.annotatedProperty == HAS_DEFINITION_CURIE:
                return ax.annotatedTarget, ax.annotations

