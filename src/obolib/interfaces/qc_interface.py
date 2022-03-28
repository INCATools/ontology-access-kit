from abc import ABC
from typing import Dict, List, Iterable

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE


class QualityControlInterface(BasicOntologyInterface, ABC):
    """
    Basic ontology QC

    In future the following functionality will be defined:

    - validating against OntologyMetadata schema
    - lexical checks
    - wrapping reasoning
    - structural graph checks
    """

    def term_curies_without_definitions(self) -> Iterable[CURIE]:
        for curie in self.all_entity_curies():
            if self.get_definition_by_curie(curie) is None:
                yield curie

    def validate(self):
        raise NotImplementedError()
