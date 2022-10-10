from dataclasses import dataclass
from typing import ClassVar, Iterable, List, Type

from oaklib import BasicOntologyInterface
from oaklib.datamodels.validation_datamodel import ValidationResult
from oaklib.utilities.validation.definition_ontology_rules import (
    TextAndLogicalDefinitionMatchOntologyRule,
)
from oaklib.utilities.validation.ontology_rule import OntologyRule


@dataclass
class RuleRunner:
    rules: ClassVar[List[Type[OntologyRule]]] = [TextAndLogicalDefinitionMatchOntologyRule]

    def run(self, oi: BasicOntologyInterface) -> Iterable[ValidationResult]:
        """
        Run all rules

        :param oi:
        :return:
        """
        for rule_cls in self.rules:
            rule = rule_cls()
            for result in rule.evaluate(oi):
                yield result
