from abc import ABC
from typing import Dict, List, Iterable, Iterator

from oaklib.datamodels.text_annotator import TextAnnotation
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface

TEXT = str

class TextAnnotatorInterface(BasicOntologyInterface, ABC):
    """
    Annotates texts

    Note yet implemented; potential implementations:

    - bioportal
    - zooma
    - scigraph-annotator
    - ontorunner
    - spacy
    """

    def annotate_text(self, text: TEXT) -> Iterator[TextAnnotation]:
        raise NotImplementedError
