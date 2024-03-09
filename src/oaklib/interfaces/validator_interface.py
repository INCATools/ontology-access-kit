from abc import ABC
from typing import Dict, Iterable

from oaklib.datamodels.validation_datamodel import (
    MappingValidationResult,
    RepairConfiguration,
    RepairOperation,
    ValidationConfiguration,
    ValidationResult,
)
from oaklib.interfaces import MappingProviderInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


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
        for curie in self.entities():
            if self.definition(curie) is None:
                yield curie

    def validate(self, configuration: ValidationConfiguration = None) -> Iterable[ValidationResult]:
        """
        Validate entire ontology or wrapped ontologies.

        Validation results might be implementation specific

        - reasoners will yield logical problems
        - shape checkers or schema checkers like SHACL or LinkML will return closed-world structural violations
        - specialized implementations may yield lexical or other kinds of problems
        :return:
        """
        raise NotImplementedError

    def validate_mappings(
        self,
        entities: Iterable[CURIE] = None,
        adapters: Dict[str, BasicOntologyInterface] = None,
        configuration: ValidationConfiguration = None,
    ) -> Iterable[MappingValidationResult]:
        """
        Validate mappings for a set of entities.

        :param entities:
        :return:
        """
        from oaklib.utilities.mapping.mapping_validation import validate_mappings

        if not isinstance(self, MappingProviderInterface):
            raise ValueError(f"Cannot validate mappings on {self}")
        mappings = list(self.sssom_mappings(entities))
        for errors, m in validate_mappings(mappings, adapters=adapters):
            for error in errors:
                result = MappingValidationResult(
                    subject_id=m.subject_id,
                    object_id=m.object_id,
                    predicate_id=m.predicate_id,
                    info=error,
                )
                yield result

    def repair(
        self, configuration: RepairConfiguration = None, dry_run=False
    ) -> Iterable[RepairOperation]:
        """
        Finds problems and fixes them.

        :param configuration:
        :param dry_run:
        :return:
        """
        raise NotImplementedError

    def check_external_references(self):
        raise NotImplementedError

    def is_coherent(self) -> bool:
        """
        True if the ontology is logically coherent, as determined by deductive reasoning
        (e.g. an OWL reasoner)

        :return: true if coherent
        """
        raise NotImplementedError

    def unsatisfiable_classes(self, exclude_nothing=True) -> Iterable[CURIE]:
        """
        Yields all classes that are unsatisfiable, as determined by deductive reasoning
        (e.g. an OWL reasoner)

        :param exclude_nothing: if True (default) do not include the tautological owl:Nothing
        :return: class curie iterator
        """
        raise NotImplementedError
