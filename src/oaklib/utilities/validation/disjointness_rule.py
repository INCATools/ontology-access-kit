import logging
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Tuple

from oaklib import BasicOntologyInterface
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResult
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.types import CURIE
from oaklib.utilities.validation.ontology_rule import OntologyRule


@dataclass
class DisjointnessRule(OntologyRule):
    """
    disjointness axioms should be declared.

    UndeclaredDisjointness(c1, c2) =

     - c1 and c2 are NOT declared or inferred disjoint
     - AND there is no a such that a sub c1 and a sub c2
     - AND for each c in c1, c2, |desc(c)| / |all(c)| > threshold

    """

    name: str = "Undeclared Disjointness Ontology Rule"
    severity = SeverityOptions(SeverityOptions.INFO)
    min_descendants: int = field(default=40)
    labelled_only = True
    max_siblings = 30

    def evaluate(
        self, oi: BasicOntologyInterface, entities: Iterable[CURIE] = None
    ) -> Iterable[ValidationResult]:
        """
        Implements the OntologyRule.evaluate() method.

        :param oi:
        :param entities:
        :return:
        """
        if not isinstance(oi, OboGraphInterface):
            raise ValueError("UndeclaredDisjointnessOntologyRule requires an OboGraphInterface")
        for c1, c2 in self._get_candidate_pairs(oi, entities):
            if c1 >= c2:
                continue
            c1_label = oi.label(c1)
            c2_label = oi.label(c2)
            if self.labelled_only and (c1_label is None or c2_label is None):
                continue
            logging.info(f"Candidate: {c1} '{c1_label}' vs {c2} '{c2_label}'")
            if isinstance(oi, OwlInterface):
                has_disjointness = oi.is_disjoint(c1, c2)
            else:
                raise ValueError("UndeclaredDisjointnessOntologyRule requires an OwlInterface")
            c1_desc_count = oi.descendant_count(c1, predicates=[IS_A])
            if c1_desc_count < self.min_descendants:
                continue
            c2_desc_count = oi.descendant_count(c2, predicates=[IS_A])
            if c2_desc_count < self.min_descendants:
                continue
            cds = list(oi.common_descendants(c1, c2, predicates=[IS_A]))
            has_underlap = len(cds) > 0
            if has_underlap:
                if has_disjointness:
                    yield self.add_result(
                        subject=c1,
                        object=c2,
                        info=f"disjointness axiom violated between {c1} and {c2}",
                    )
            else:
                if not has_disjointness:
                    yield self.add_result(
                        subject=c1,
                        object=c2,
                        info=(
                            f"{c1} {c2_label} (|D|={c1_desc_count}) and {c2} {c2_label} (|D|={c2_desc_count}"
                            "are not declared disjoint, but they have no common descendants"
                        ),
                    )

    def _get_candidate_pairs(
        self, oi: OboGraphInterface, entities: Iterable[CURIE] = None
    ) -> Iterator[Tuple[CURIE, CURIE]]:
        if entities is None:
            entities = oi.entities()
        entities = list(entities)
        roots = []
        candidates = []
        logging.info(f"Selecting candidates from {len(entities)} entities")
        for e in entities:
            children = [r[1] for r in oi.incoming_relationships(e, predicates=[IS_A])]
            if len(children) > self.max_siblings:
                continue
            parents = [r[1] for r in oi.outgoing_relationships(e, predicates=[IS_A])]
            if not parents and children:
                roots.append(e)
            for c1 in children:
                for c2 in children:
                    candidates.append((c1, c2))
        for r1 in roots:
            for r2 in roots:
                candidates.append((r1, r2))
        for c1, c2 in candidates:
            yield c1, c2

    def exhaustive_evaluate(
        self, oi: BasicOntologyInterface, entities: Iterable[CURIE] = None
    ) -> Iterable[ValidationResult]:
        """
        Implements the OntologyRule.evaluate() method.

        :param oi:
        :param entities:
        :return:
        """
        if not isinstance(oi, OboGraphInterface):
            raise ValueError("UndeclaredDisjointnessOntologyRule requires an OboGraphInterface")
        roots = list(oi.roots(predicates=[IS_A]))
        stack = []
        for i in roots:
            for j in roots:
                if i <= j:
                    stack.append((i, j))
        visited = set()
        while stack:
            c1, c2 = stack[0]
            stack = stack[1:]
            if (c1, c2) in visited or (c2, c1) in visited:
                continue
            visited.add((c1, c2))
            if c1 > c2:
                continue
            c1_label = oi.label(c1)
            c2_label = oi.label(c2)
            if self.labelled_only and (c1_label is None or c2_label is None):
                continue
            c1_children = [r[1] for r in oi.incoming_relationships(c1, predicates=[IS_A])]
            c2_children = [r[1] for r in oi.incoming_relationships(c2, predicates=[IS_A])]
            if c1 in list(oi.ancestors(c2, predicates=[IS_A], reflexive=False)):
                stack.extend([(c1c, c2) for c1c in c1_children])
                continue
            if c2 in list(oi.ancestors(c1, predicates=[IS_A], reflexive=False)):
                stack.extend([(c1, c2c) for c2c in c2_children])
                continue
            logging.info(
                f"Candidate: {c1} '{c1_label}' vs {c2} '{c2_label}', visited={len(visited)}"
            )
            if isinstance(oi, OwlInterface):
                has_disjointness = oi.is_disjoint(c1, c2)
            else:
                raise ValueError("UndeclaredDisjointnessOntologyRule requires an OwlInterface")
            if not c1_children or not c2_children:
                continue
            c1_desc_count = oi.descendant_count(c1, predicates=[IS_A])
            if c1_desc_count < self.min_descendants:
                continue
            c2_desc_count = oi.descendant_count(c2, predicates=[IS_A])
            if c2_desc_count < self.min_descendants:
                continue
            if c1 == c2:
                has_underlap = True
            else:
                cds = list(oi.common_descendants(c1, c2, predicates=[IS_A]))
                has_underlap = len(cds) > 0
            if has_underlap:
                stack.extend([(i, j) for i in c1_children + [c1] for j in c2_children + [c2]])
                if has_disjointness:
                    yield self.add_result(
                        subject=c1,
                        object=c2,
                        info=f"disjointness axiom violated between {c1} and {c2}",
                    )
            else:
                if not has_disjointness:
                    yield self.add_result(
                        subject=c1,
                        object=c2,
                        info=(
                            f"{c1} (|D|={c1_desc_count}) and {c2} (|D|={c2_desc_count}"
                            "are not declared disjoint, but they have no common descendants"
                        ),
                    )
