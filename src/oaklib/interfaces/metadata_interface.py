import logging
from abc import ABC
from typing import Dict, List, Tuple, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
import oaklib.datamodels.ontology_metadata as om
import sssom
from oaklib.types import CURIE


class MetadataInterface(BasicOntologyInterface, ABC):

    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        raise NotImplementedError

