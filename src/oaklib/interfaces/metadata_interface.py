import logging
from abc import ABC
from typing import Dict, Iterable, List, Optional, Tuple

import sssom

import oaklib.datamodels.ontology_metadata as om
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, IS_A
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class MetadataInterface(BasicOntologyInterface, ABC):
    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        raise NotImplementedError

    def definition_with_annotations(
        self, curie: CURIE
    ) -> Optional[Tuple[str, List[om.Annotation]]]:
        for ax in self.statements_with_annotations(curie):
            if ax.annotatedProperty == HAS_DEFINITION_CURIE:
                return ax.annotatedTarget, ax.annotations
