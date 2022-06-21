from dataclasses import dataclass

from oaklib.implementations import BioportalImplementation
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, URI


@dataclass
class AgroportalImplementation(
    BioportalImplementation, TextAnnotatorInterface, SearchInterface, MappingProviderInterface
):
    """
    Implementation over agroportal endpoint

    """

    @property
    def _base_url(self) -> str:
        return "http://data.agroportal.lirmm.fr/"

    def load_bioportal_api_key(self, path: str = None) -> None:
        self.bioportal_api_key = "1de0a270-29c5-4dda-b043-7c3580628cd5"
