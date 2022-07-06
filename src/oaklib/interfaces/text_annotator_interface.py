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
        if configuration and configuration.matches_whole_text:
            if isinstance(self, SearchInterface):
                curies: Iterable[CURIE] = self.basic_search(text)
                for object_id in curies:
                    label = self.get_label_by_curie(object_id)
                    # amap = self.alias_map_by_curie(object_id)
                    ann = nen_annotation(text, object_id, label)
                    yield ann
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
