from abc import ABC
from typing import Iterable, Optional

from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = [
    "TEXT",
    "nen_annotation",
    "TextAnnotatorInterface",
]

TEXT = str


def nen_annotation(text: str, curie: CURIE, label: str) -> TextAnnotation:
    """Return an annotation appropriate for a grounding."""
    return TextAnnotation(
        subject_start=1,
        subject_end=len(text),
        object_id=curie,
        object_label=label,
    )


class TextAnnotatorInterface(BasicOntologyInterface, ABC):
    """
    Performs Named Entity Recognition on texts

    Currently this is only partially implemented by :class:`.BioportalInterface`

    potential implementations:

    - zooma
    - scigraph-annotator
    - ontorunner
    - spacy
    """

    def annotate_text(
        self, text: TEXT, configuration: Optional[TextAnnotationConfiguration] = None
    ) -> Iterable[TextAnnotation]:
        """
        Annotate a piece of text

        .. note ::

           the signature of this method may change

        :param text:
        :param configuration:
        :return:
        """
        if not configuration:
            raise NotImplementedError("Missing text annotation configuration")
        if not configuration.matches_whole_text:
            raise NotImplementedError(
                f"{self.__class__.__name__} can't be used to match partial text"
            )
        if not isinstance(self, SearchInterface):
            raise TypeError(
                f"{self.__class__.__name__} needs to inherit from {SearchInterface} "
                f"to use the default annotate_text() implementation"
            )
        for object_id in self.basic_search(text):
            label = self.label(object_id)
            # amap = self.alias_map_by_curie(object_id)
            yield nen_annotation(text=text, curie=object_id, label=label)
