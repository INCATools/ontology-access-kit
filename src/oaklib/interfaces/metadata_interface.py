from abc import ABC
from typing import Iterable, Iterator, List, Optional, Tuple

import oaklib.datamodels.ontology_metadata as om
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class MetadataInterface(BasicOntologyInterface, ABC):
    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        raise NotImplementedError

    def definition_with_annotations(
        self, curie: CURIE
    ) -> Optional[Tuple[str, List[om.Annotation]]]:
        """
        Get the definition of a term, if it exists, along with any annotations.

        :param curie:
        :return:
        """
        for ax in self.statements_with_annotations(curie):
            if ax.annotatedProperty == HAS_DEFINITION_CURIE:
                return ax.annotatedTarget, ax.annotations

    def definitions_with_annotations(
        self, curies: Iterable[CURIE]
    ) -> Iterator[Tuple[str, List[om.Annotation]]]:
        """
        Get the definitions of a set of terms, if they exist, along with any annotations.

        :param curies:
        :return:
        """
        for curie in curies:
            defn_obj = self.definition_with_annotations(curie)
            if defn_obj:
                yield curie, defn_obj[0], defn_obj[1]
            else:
                yield curie, None, None
