import logging
from dataclasses import dataclass, field
from typing import Iterable, List, Type

from oaklib import BasicOntologyInterface
from oaklib.datamodels.validation_datamodel import ValidationResult
from oaklib.utilities.validation.definition_ontology_rule import (
    TextAndLogicalDefinitionMatchOntologyRule,
)
from oaklib.utilities.validation.disjointness_rule import DisjointnessRule
from oaklib.utilities.validation.ontology_rule import OntologyRule

RULES = [TextAndLogicalDefinitionMatchOntologyRule, DisjointnessRule]


@dataclass
class RuleRunner:
    rules: List[Type[OntologyRule]] = field(default_factory=lambda: RULES)

    def run(self, oi: BasicOntologyInterface) -> Iterable[ValidationResult]:
        """
        Run all rules

        :param oi:
        :return:
        """
        for rule_cls in self.rules:
            rule = rule_cls()
            logging.info(f"Running: {rule}")
            for result in rule.evaluate(oi):
                yield result

    def set_rules(self, rule_names: Iterable[str]) -> None:
        """
        Set the rules to run

        :param rules:
        :return:
        """
        rule_dict = {rule.__name__: rule for rule in RULES}
        self.rules = [rule_dict[name] for name in rule_names]
        logging.info(f"Set rules: {self.rules}")
