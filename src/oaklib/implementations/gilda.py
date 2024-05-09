"""A text annotator based on Gilda."""

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterator

from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.text_annotator_interface import TEXT, nen_annotation

if TYPE_CHECKING:
    import gilda

__all__ = [
    "GildaImplementation",
]


@dataclass
class GildaImplementation(TextAnnotatorInterface):
    """
    Perform named entity normalization on text strings with Gilda [gyori2021]_.

    .. [gyori2021] Benjamin M Gyori, Charles Tapley Hoyt, Albert Steppi (2021)
        `Gilda: biomedical entity text normalization with machine-learned
        disambiguation as a service <https://doi.org/10.1093/bioadv/vbac034>`_,
        *Bioinformatics Advances*, Volume 2, Issue 1, 2022, vbac034,
    """

    grounder: "gilda.Grounder" = None
    """A grounder used by Gilda.

    This is instantiated in one of the following ways:

    1. It can be passed directly during instantiation of the
       :class:`GildaImplementation` class.
    2. If not passed and this implementation's ``slug`` attribute is set
       to a path to a gzipped term TSV file, it gets instantiated with the
       custom index
    3. Otherwise, it gets instantiated with the default Gilda term index
    """

    def __post_init__(self):
        if self.grounder is None:
            from gilda.grounder import Grounder

            # The slug corresponds to the path to a gzipped terms TSV
            # when parsed from a descriptor like ``gilda:<path>` via
            # :func:`get_resource_from_shorthand`. If no <path> was
            # given, then this will default to the default Gilda index
            try:
                self.grounder = Grounder(terms=self.resource.slug)
            except AttributeError:  # i.e., there's no slug
                logging.warning("Gilda grounder will use default term index.")
                self.grounder = Grounder()

    def annotate_text(
        self, text: TEXT, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        """
        Implements annotate_text from text_annotator_interface by calling the
        `annotate` endpoint using gilda client.

        :param text: Text to be annotated.
        :param configuration: Text annotation configuration.
        :yield: A generator function that returns annotated results.
        """
        if not configuration:
            raise NotImplementedError("Missing text annotation configuration")
        if configuration.matches_whole_text:
            yield from self._ground(text)
        else:
            yield from self._gilda_annotate(text)

    def _gilda_annotate(self, text: str) -> Iterator[TextAnnotation]:
        from gilda.ner import annotate

        for match_text, match, start, end in annotate(text, grounder=self.grounder):
            yield TextAnnotation(
                subject_start=start,
                subject_end=end,
                subject_label=match_text,
                object_id=match.term.get_curie(),
                object_label=match.term.entry_name,
                matches_whole_text=start == 0 and end == len(text),
            )

    def _ground(self, text: str) -> Iterator[TextAnnotation]:
        for match in self.grounder.ground(text):
            yield nen_annotation(
                text=text,
                object_id=match.term.get_curie(),
                object_label=match.term.entry_name,
            )
