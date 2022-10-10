import logging
from abc import ABC
from typing import Iterable, Optional

from oaklib.datamodels.lexical_index import LexicalIndex
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

__all__ = [
    "TEXT",
    "nen_annotation",
    "TextAnnotatorInterface",
]

from oaklib.utilities.lexical.lexical_indexer import create_lexical_index

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

    lexical_index: Optional[LexicalIndex] = None
    """If present, some implementations may choose to use this"""

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
            configuration = TextAnnotationConfiguration()
        if configuration.matches_whole_text:
            if isinstance(self, SearchInterface):
                for object_id in self.basic_search(text):
                    label = self.label(object_id)
                    # amap = self.alias_map_by_curie(object_id)
                    yield nen_annotation(text=text, curie=object_id, label=label)
            else:
                raise NotImplementedError(
                    f"{self.__class__.__name__} can't be used to match partial text"
                )
        else:
            logging.info("using highly inefficient annotation method")
            if not self.lexical_index:
                self.lexical_index = create_lexical_index(self)
            logging.info("Performing naive search using lexical index")
            li = self.lexical_index
            text_lower = text.lower()
            for k, grouping in li.groupings.items():
                if k in text_lower:
                    ix = text_lower.index(k)
                    for r in grouping.relationships:
                        ann = TextAnnotation(
                            subject_start=ix + 1,
                            subject_end=ix + len(k) - 1,
                            predicate_id=r.predicate,
                            object_id=r.element,
                            object_label=r.element_term,
                            match_string=text[ix : ix + len(k)],
                        )
                        yield ann
