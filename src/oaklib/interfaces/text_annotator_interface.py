from abc import ABC
from typing import Dict, List, Iterable, Iterator

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE

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

    def annotate_text(self, text: TEXT) -> Iterator:
        raise NotImplementedError
