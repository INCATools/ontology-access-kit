from dataclasses import dataclass
from typing import Iterator, List, Optional, Iterable

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import LogicalDefinitionAxiom
from oaklib.datamodels.validation_datamodel import SeverityOptions, ValidationResult
from oaklib.datamodels.vocabulary import HAS_DBXREF
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE
from oaklib.utilities.validation.ontology_rule import OntologyRule


def _index(text: str, markers: List[str]) -> Optional[int]:
    for m in markers:
        m = f" {m} "
        if m in text:
            return text.index(m)


@dataclass
class ProcessedTextDefinition:
    """
    A processed textual definition.

    Assumes structures laid out in <https://philpapers.org/archive/SEPGFW.pdf>_
    """

    original_definition: str
    """The unprocessed definition."""

    main_definition: str
    """The core part of the definition, before the period."""

    gloss: Optional[str] = None
    """The part of the definition after the period (if present)."""

    definiendum: Optional[str] = None
    """The name of the thing being defined. E.g. 'A <difinendium> is a <genus> that <differentia>"""

    genus_text: Optional[str] = None
    """If the definition follows 'A <genus> that <differentia>, this is the genus"""

    differentia_text: Optional[str] = None
    """If the definition follows 'A <genus> that <differentia>, this is the differentia"""

    that_marker_index: Optional[int] = None
    """If the definition follows genus-differentia form, this is the position of the that/which."""


@dataclass
class TextAndLogicalDefinitionMatchOntologyRule(OntologyRule):
    """
    Text and logical definitions should match.

    This is a highly sensitive test and many textual definitions
    are expected not to conform due to natural lexical variation.

    The tests are based on a subset of the criteria in, in particular:

    - S1: conform to conventions (do not include definiendum)
    - S3: Use the genus differentia form
    - S7: Avoid circularity
    - S11: Match text and logical definitions

    """

    name: str = "text and logical definition match rule"
    severity = SeverityOptions(SeverityOptions.INFO)
    skip_text_annotation: bool = False

    def process_text_definition(self, tdef: str) -> ProcessedTextDefinition:
        """
        Parse a textual definition.

        :param tdef:
        :return:
        """
        parts = tdef.split(".")
        main_def = parts[0]
        ptd = ProcessedTextDefinition(original_definition=tdef, main_definition=main_def)
        # parts = [p.strip() for p in parts[1:]]
        parts = parts[1:]
        if parts:
            ptd.gloss = ".".join(parts).strip()
        for marker in [" that ", " which "]:
            subparts = main_def.split(marker)
            if len(subparts) > 1:
                ptd.genus_text = subparts[0]
                ptd.differentia_text = marker.join(subparts[1:])
                ptd.that_marker_index = main_def.index(marker)
                break
        if ptd.genus_text:
            if " is " in ptd.genus_text:
                subparts = ptd.genus_text.split(" is ")
                ptd.definiendum = subparts[0]
                ptd.genus_text = " is ".join(subparts[1:])
            genus_words = ptd.genus_text.split(" ")
            if genus_words[0].lower() in ["a", "the", "an"]:
                ptd.genus_text = " ".join(genus_words[1:])
        return ptd

    def check_against_logical_definition(
        self,
        oi: BasicOntologyInterface,
        pdef: ProcessedTextDefinition,
        ldef: LogicalDefinitionAxiom,
    ) -> Iterator[ValidationResult]:
        """
        Check a text definition against a logical definition.

        :param oi:
        :param pdef:
        :param ldef:
        :return:
        """
        subject = ldef.definedClassId
        if isinstance(oi, TextAnnotatorInterface) and not self.skip_text_annotation:
            anns = list(oi.annotate_text(pdef.main_definition))
            anns_by_object = {ann.object_id: ann for ann in anns}

            def _check(
                expected_id: CURIE, expected_in_text: str, is_genus=False
            ) -> Iterator[ValidationResult]:
                if expected_id in anns_by_object:
                    if not expected_in_text:
                        pass
                    else:
                        ann = anns_by_object[expected_id]
                        if ann.match_string in expected_in_text:
                            if is_genus and len(ann.match_string) < len(expected_in_text):
                                yield ValidationResult(
                                    type="S3",
                                    subject=subject,
                                    info=f"Did not match whole text: {ann.match_string} < {expected_in_text}",
                                )
                        else:
                            yield ValidationResult(
                                type="S11.WrongPlace", subject=subject, info="Wrong position"
                            )
                else:
                    yield ValidationResult(
                        type="S11.NotFound", subject=subject, info=f"Not found: {expected_id}"
                    )

            for genus in ldef.genusIds:
                for result in _check(genus, pdef.genus_text, is_genus=True):
                    yield result
            for restr in ldef.restrictions:
                for result in _check(restr.fillerId, pdef.differentia_text):
                    yield result
            if subject in anns_by_object:
                yield ValidationResult(
                    type="S7",
                    subject=subject,
                    info=f"Circular, {anns_by_object[subject].match_string} in definition",
                )

    def evaluate(self, oi: BasicOntologyInterface, entities: Iterable[CURIE] = None) -> Iterable[ValidationResult]:
        """
        Implements the OntologyRule.evaluate() method.

        :param oi:
        :param entities:
        :return:
        """
        if entities is None:
            entities = oi.entities(filter_obsoletes=True)
        for subject in entities:
            problem_count = 0
            # TODO: leakage of quoted URIs into CURIEs should be fixed upstream.
            # these currently come from SWRL URIs from rdftab
            if subject.startswith("<"):
                continue
            tdef = oi.definition(subject)
            if tdef:
                pdef = self.process_text_definition(tdef)
                if not pdef.genus_text or not pdef.differentia_text:
                    yield ValidationResult(
                        subject=subject,
                        severity=SeverityOptions(SeverityOptions.WARNING),
                        predicate=HAS_DBXREF,
                        type="S3",
                        info=f'Cannot parse genus and differentia for "{tdef}"',
                    )
                    problem_count += 1
            else:
                pdef = None
                yield ValidationResult(
                    subject=subject,
                    severity=SeverityOptions(SeverityOptions.ERROR),
                    predicate=HAS_DBXREF,
                    type="S0",
                    info=f'Missing text definition for "{subject}"',
                )
                problem_count += 1
            if isinstance(oi, OboGraphInterface):
                for ldef in oi.logical_definitions([subject]):
                    if pdef:
                        for result in self.check_against_logical_definition(oi, pdef, ldef):
                            yield result
                            problem_count += 1
                    if len(ldef.genusIds) != 1:
                        yield ValidationResult(
                            subject=subject,
                            type="S3.1",
                            info=f"expected one genus; got {len(ldef.genusIds)}.",
                        )
                        problem_count += 1
            else:
                raise NotImplementedError(f"Not implemented for {type(oi)}")
            if problem_count == 0:
                yield ValidationResult(
                    subject=subject,
                    severity=SeverityOptions(SeverityOptions.INFO),
                    predicate=HAS_DBXREF,
                    type="S.*",
                    info=f'No problems with: "{tdef}"',
                )
