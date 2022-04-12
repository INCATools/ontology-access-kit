from abc import ABC
from dataclasses import dataclass
from typing import Dict, List, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE
from oaklib.datamodels.validation_datamodel import ValidationResult, ValidationConfiguration


class ValidatorInterface(BasicOntologyInterface, ABC):
    """
    Basic ontology QC

    The overall goal is to support the following

    - validating against OntologyMetadata schema
    - lexical checks
    - wrapping reasoning
    - structural graph checks

    Specific implementations may choose to implement efficient methods for this.
    For example, a SQL implementation can quickly determine all terms
    missing definitions with a query over an indexed table.

    Currently the main implementation for this is the SqlDatabase implementation,
    this implements a generic property check using the OntologyMetadata datamodel

    See:

     - `OntologyMetadata <https://incatools.github.io/ontology-access-kit/datamodels/ontology-metadata/>`_
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

    def validate(self, configuration: ValidationConfiguration = None) -> Iterable[ValidationResult]:
        """
        Validate entire ontology or wrapped ontologies

        Validation results might be implementation specific

        - reasoners will yield logical problems
        - shape checkers or schema checkers like SHACL or LinkML will return closed-world structural violations
        - specialized implementations may yield lexical or other kinds of problems
        :return:
        """
        raise NotImplementedError

    def check_external_references(self):
        raise NotImplementedError

