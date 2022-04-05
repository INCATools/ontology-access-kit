from abc import ABC
from typing import Dict, List, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE


class SemanticSimilarityInterface(BasicOntologyInterface, ABC):
    """
    TODO: consider direct use of nxontology
    """

    def most_recent_common_ancestors(self, curie1: CURIE, curie2: CURIE, predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        raise NotImplementedError

    def common_ancestors(self, curie1: CURIE, curie2: CURIE, predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        raise NotImplementedError

    def get_information_content(self, curie: CURIE, background: CURIE = None):
        raise NotImplementedError

