from dataclasses import dataclass

from oaklib.implementations import BioportalImplementation
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, URI
from oaklib.utilities.apikey_manager import get_apikey_value
from oaklib.utilities.rate_limiter import check_limit
from sssom_schema import Mapping

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
