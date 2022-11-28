from dataclasses import dataclass
from typing import Iterable, List

from oaklib import BasicOntologyInterface
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResult
from oaklib.types import CURIE


@dataclass
class OntologyRule:
    """Base class for all ontology rules."""

    name: str
    results: List[ValidationResult] = None
    severity = SeverityOptions(SeverityOptions.WARNING)

    def evaluate(
        self, oi: BasicOntologyInterface, entities: Iterable[CURIE] = None
    ) -> Iterable[ValidationResult]:
        """
        Evaluate the rule.

        :param oi:
        :param entities:
        :return:
        """
        raise NotImplementedError

    def add_result(
        self, subject=None, info=None, typ=None, severity=None, object=None
    ) -> ValidationResult:
        """
        Register an additional validation result.

        :param subject:
        :param info:
        :param typ:
        :param severity:
        :return:
        """
        if typ is None:
            cls = type(self)
            typ = f"oaklib:{cls.__name__}"
        if severity is None:
            severity = self.severity
        vr = ValidationResult(
            subject=subject, object=object, info=info, type=typ, severity=severity
        )
        if self.results is None:
            self.results = []
        self.results.append(vr)
        return vr
