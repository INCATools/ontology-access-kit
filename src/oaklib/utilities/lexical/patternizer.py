"""Detect logical definitions from lexical elements in an ontology."""

import logging
import urllib
from typing import Dict, Iterator, List, Optional

import yaml
from pydantic import BaseModel

import oaklib.datamodels.obograph as obograph
from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE


class LexicalPattern(BaseModel):
    """
    A lexical pattern is a string that is used to detect a logical definition.

    The data model here is similar to DOSDPs, but is geared towards parsing of lexical elements
    in ontologies.
    """

    name: str
    """Name of lexical pattern. Typically corresponds to pattern."""

    pattern: Optional[str] = None
    """String pattern to match. If None, defaults to name."""

    is_regex: Optional[bool] = False
    """If True, pattern is a regular expression.
    If False, pattern is a string. Defaults to False. NOT IMPLEMENTED YET."""

    pattern_position: Optional[int] = None
    """If 0, then pattern must be at the beginning of the label.
    If -1, then pattern must be at the end of the label.
    If None, then pattern can be anywhere in the label.
    No other options are supported. Defaults to None."""

    description: Optional[str] = None
    """Description of pattern."""

    curie: Optional[CURIE] = None
    """If the pattern maps to a logical definition, then this is the curie
    of the term that is a fixed element of the definition (genus or differentia filler)."""

    curie_is_genus: Optional[bool] = True
    """If True, then the curie is the genus and the extracted term is the differentia filler."""

    differentia_predicate: Optional[CURIE] = None
    """If the pattern maps to a logical definition, then this is the predicate
    that is used in the differentia."""


class Differentia(BaseModel):
    """Discriminating relationship in a logical definition."""

    predicate: CURIE
    filler: CURIE


class LogicalDefinition(BaseModel):
    """Logical definition of a term, following genus-differentia format."""

    genus: CURIE
    differentia: List[Differentia]


class Term(BaseModel):
    curie: CURIE
    label: str
    logical_definition: Optional[LogicalDefinition] = None
    pattern: Optional[str] = None
    genus_not_in_descendants: Optional[bool] = False
    differentia_not_in_descendants: Optional[bool] = False


class ExtractedConcept(BaseModel):
    """
    A concept extracted from a lexical pattern.

    For example, in a pattern like "nuclear X", the concept is "X".
    """

    label: str
    curies: List[CURIE]
    in_ontology: Optional[bool] = None
    instances: Dict[str, Optional[Term]]


class LexicalPatternCollection(BaseModel):
    """Collection of lexical patterns"""

    patterns: List[LexicalPattern]


def match_and_extract(pattern: LexicalPattern, label: str) -> Optional[str]:
    """
    Given a lexical pattern and a label, return the label with the pattern removed.

    >>> from oaklib.utilities.lexical.patternizer import LexicalPattern, match_and_extract
    >>> pattern = LexicalPattern(name="nuclear X", pattern="nuclear")
    >>> print(match_and_extract(pattern, "nuclear membrane"))
    membrane

    :param pattern:
    :param label:
    :return:
    """
    if pattern.pattern in label:
        if pattern.pattern_position is not None:
            if pattern.pattern_position == 0:
                if not label.startswith(pattern.pattern):
                    return None
            elif pattern.pattern_position == -1:
                if not label.endswith(pattern.pattern):
                    return None
            else:
                raise NotImplementedError("Pattern position must be 0 or -1.")
        return label.replace(pattern.pattern, "").strip()


def lexical_pattern_instances(
    adapter: BasicOntologyInterface,
    patterns: List[LexicalPattern],
    curies: Optional[List[CURIE]] = None,
    new_concept_prefix=None,
    strict=False,
) -> List[ExtractedConcept]:
    """
    Given a list of lexical patterns, return a list of ExtractedConcepts.

    Each ExtractedConcepts contains a label and a dictionary of instances, keyed by the pattern name.

    :param adapter:
    :param patterns:
    :param curies:
    :param new_concept_prefix:
    :return:
    """
    if curies is None:
        curies = list(adapter.entities())
    id_labels = list(adapter.labels(curies, allow_none=False))
    ecs = {}
    injected_curies = []
    for pattern in patterns:
        if pattern.pattern is None:
            pattern.pattern = pattern.name
        logging.info(f"Processing pattern {pattern.name} on {len(id_labels)} labels.")
        for id, label in id_labels:
            concept_label = match_and_extract(pattern, label)
            if concept_label:
                # concept_label = label.replace(pattern.pattern, "").strip()
                if concept_label not in ecs:
                    concept_ids = adapter.curies_by_label(concept_label)
                    if len(concept_ids) > 1:
                        candidate_concept_ids = [id for id in concept_ids if id in curies]
                        if len(candidate_concept_ids) > 0:
                            concept_ids = candidate_concept_ids
                    in_ontology = len(concept_ids) == 1
                    if not concept_ids:
                        if new_concept_prefix:
                            # make label safe by url encoding using library
                            concept_ids = [
                                f"{new_concept_prefix}:{urllib.parse.quote(concept_label)}"
                            ]
                            injected_curies.append(concept_ids[0])
                    ecs[concept_label] = ExtractedConcept(
                        label=concept_label,
                        curies=concept_ids,
                        in_ontology=in_ontology,
                        instances={},
                    )
                concept_ids = ecs[concept_label].curies
                if pattern.curie is not None and not concept_ids and strict:
                    raise ValueError(
                        f"Pattern {pattern.name} matched {concept_label} but no curie was found."
                    )
                if pattern.curie is not None and concept_ids:
                    if pattern.curie_is_genus:
                        genus = pattern.curie
                        differentia = concept_ids[0]
                    else:
                        genus = concept_ids[0]
                        differentia = pattern.curie
                    ldef = LogicalDefinition(
                        genus=genus,
                        differentia=[
                            Differentia(predicate=pattern.differentia_predicate, filler=differentia)
                        ],
                    )
                else:
                    ldef = None
                term = Term(curie=id, label=label, logical_definition=ldef, pattern=pattern.name)
                if ldef:
                    if isinstance(adapter, OboGraphInterface):
                        if ldef.genus not in injected_curies:
                            if ldef.genus not in adapter.ancestors(id, [IS_A]):
                                term.genus_not_in_descendants = True
                        differentia0 = ldef.differentia[0]
                        filler = differentia0.filler
                        if filler not in injected_curies:
                            # pred_closure = [IS_A, differentia0.predicate]
                            pred_closure = None
                            if filler not in adapter.ancestors(id, pred_closure):
                                term.differentia_not_in_descendants = True
                ecs[concept_label].instances[pattern.name] = term
    return list(ecs.values())


def as_matrix(
    ecs: List[ExtractedConcept],
    pattern_collection: Optional[LexicalPatternCollection] = None,
    fields: Optional[List[str]] = None,
) -> Iterator[dict]:
    """
    Given a list of ExtractedConcepts, a matrix representation as a list of dicts.

    Each row is an ExtractedConcept, and each column is a pattern.

    :param ecs:
    :return:
    """
    if not fields:
        if pattern_collection:
            fields = [p.name for p in pattern_collection.patterns]
    if not fields:
        fields = set()
        for ec in ecs:
            fields.update(ec.instances.keys())
        fields = list(fields)

    def cell_value(ec: ExtractedConcept, field: str) -> Optional[str]:
        if field in ec.instances:
            inst = ec.instances[field]
            v = inst.curie
            if inst.genus_not_in_descendants:
                v = f"*{v}/GEN"
            if inst.differentia_not_in_descendants:
                v = f"+{v}/DF"
        else:
            v = ""
        return v

    for ec in ecs:
        curie = ec.curies[0] if ec.curies else None
        row = {"id": curie, "label": ec.label, **{f: cell_value(ec, f) for f in fields}}
        n = len([v for v in row.values() if v]) - 1
        row["num_concepts"] = n
        yield row


def as_logical_definitions(
    ecs: List[ExtractedConcept],
) -> Iterator[obograph.LogicalDefinitionAxiom]:
    """
    Given a list of ExtractedConcepts, return a list of LogicalDefinitionAxioms.

    :param ecs:
    :return:
    """
    for ec in ecs:
        for instance in ec.instances.values():
            if instance.logical_definition is not None:
                yield obograph.LogicalDefinitionAxiom(
                    definedClassId=instance.curie,
                    genusIds=[instance.logical_definition.genus],
                    restrictions=[
                        obograph.ExistentialRestrictionExpression(
                            propertyId=r.predicate, fillerId=r.filler
                        )
                        for r in instance.logical_definition.differentia
                    ],
                )


def load_pattern_collection(patterns_file: str):
    """
    Load a pattern collection from a file.

    :param patterns_file:
    :return:
    """
    return LexicalPatternCollection(**yaml.safe_load(open(patterns_file)))
