from abc import ABC
from typing import Iterator

from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface

TEXT = str


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
        self, text: TEXT, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
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
                for object_id in self.basic_search(text):
                    label = self.get_label_by_curie(object_id)
                    # amap = self.alias_map_by_curie(object_id)
                    ann = TextAnnotation(
                        subject_start=1,
                        subject_end=len(text),
                        object_id=object_id,
                        object_label=label,
                    )
                    yield ann
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
