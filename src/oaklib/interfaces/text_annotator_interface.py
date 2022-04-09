from abc import ABC
from typing import Iterator

from oaklib.datamodels.text_annotator import TextAnnotation
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

    def annotate_text(self, text: TEXT) -> Iterator[TextAnnotation]:
        """
        Annotate a piece of text

        .. note ::

           the signature of this method may change

        :param text:
        :return:
        """
        raise NotImplementedError
