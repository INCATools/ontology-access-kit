from abc import ABC
from dataclasses import dataclass
from typing import Dict, List, Iterable

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE
from obolib.vocabulary.validation_datamodel import ValidationResult


class ValidatorInterface(BasicOntologyInterface, ABC):
    """
    Basic ontology QC

    In future the following functionality will be defined:

    - validating against OntologyMetadata schema
    - lexical checks
    - wrapping reasoning
    - structural graph checks
    """

    def term_curies_without_definitions(self) -> Iterable[CURIE]:
        """
        TODO: decide whether to write highly specific methods or use a generic validate method
        :return:
        """
        # Implementations are advise to implement more efficient interfaces for their back-end
        for curie in self.all_entity_curies():
            if self.get_definition_by_curie(curie) is None:
                yield curie

    def validate(self) -> Iterable[ValidationResult]:
        """
        Validate entire ontology or wrapped ontologies

        Validation results might be implementation specific

        - reasoners will yield logical problems
        - shape checkers or schema checkers like SHACL or LinkML will return closed-world structural violations
        - specialized implementations may yield lexical or other kinds of problems
        :return:
        """
        raise NotImplementedError()
