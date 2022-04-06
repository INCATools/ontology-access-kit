import requests
import logging
from dataclasses import dataclass, field
from typing import Any, List, Dict, Union, Iterator, Iterable, Tuple

from oaklib.datamodels.text_annotator import TextAnnotation
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP
from oaklib.interfaces.search_interface import SearchInterface, SearchConfiguration
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE
from oaklib.utilities.apikey_manager import get_apikey_value

REST_URL = "http://data.bioontology.org"

ANNOTATION = Dict[str, Any]


@dataclass
class BioportalImplementation(TextAnnotatorInterface, SearchInterface):
    """
    Implementation over bioportal endpoint

    See `<https://data.bioontology.org/documentation>`_
    """
    bioportal_api_key: str = None
    label_cache: Dict[CURIE, str] = field(default_factory=lambda: {})

    def get_prefix_map(self) -> PREFIX_MAP:
        # TODO
        return {}

    def load_bioportal_api_key(self, path: str = None) -> None:
        self.bioportal_api_key = get_apikey_value('bioportal')

    def _headers(self) -> dict:
        return {'Authorization': 'apikey token=' + self.bioportal_api_key}

    def get_labels_for_curies(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        label_cache = self.label_cache
        for curie in curies:
            logging.debug(f'LOOKUP: {curie}')
            if curie in label_cache:
                yield curie, label_cache[curie]
            else:
                label = self.get_label_by_curie(curie)
                label_cache[curie] = label
                yield curie, label


    def annotate_text(self, text: str) -> Iterator[TextAnnotation]:
        logging.info(f'Annotating text: {text}')
        #include =['prefLabel', 'synonym', 'definition', 'semanticType', 'cui']
        include =['prefLabel', 'semanticType', 'cui']
        require_exact_match = True
        include_str = ','.join(include)
        params = {'include':  include_str,
                  'require_exact_match': require_exact_match,
                  'text': text}
        if self.bioportal_api_key is  None:
            self.load_bioportal_api_key()
        r = requests.get(REST_URL + '/annotator',
                         headers=self._headers(),
                         params=params)
        return self.json_to_results(r.json(), text)

    def json_to_results(self, json_list: List[Any], text: str) -> Iterator[TextAnnotation]:
        results = []
        seen = {}
        for obj in json_list:
            ac_obj = obj['annotatedClass']
            for x in obj['annotations']:
                ann = TextAnnotation(subject_start=x['from'],
                                     subject_end=x['to'],
                                     subject_label=x['text'],
                                     object_id=self.uri_to_curie(ac_obj['@id']),
                                     object_label=ac_obj['prefLabel'],
                                     object_source=ac_obj['links']['ontology'],
                                     match_type=x['matchType'],
                                     #info=str(obj)
                                     )
                uid = ann.subject_start, ann.subject_end, ann.object_id
                if uid in seen:
                    logging.debug(f'Skipping duplicative annotation to {ann.object_source}')
                    continue
                seen[uid] = True
                yield ann

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        if self.bioportal_api_key is  None:
            self.load_bioportal_api_key()
        r = requests.get(REST_URL + '/search',
                         headers=self._headers(),
                         params={'q': search_term, 'include': ['prefLabel']})
        obj = r.json()
        #print(obj)
        collection = obj['collection']
        while len(collection) > 0:
            result = collection[0]
            curie = self.uri_to_curie(result['@id'])
            label = result['prefLabel']
            self.label_cache[curie] = label
            logging.debug(f'M: {curie} => {label}')
            yield curie
            collection = collection[1:]
            if len(collection) == 0:
                next_page = obj['links']['nextPage']
                #print(f'NEXT={next_page}')
                if next_page:
                    r = requests.get(next_page, headers=self._headers())
                    obj = r.json()
                    collection = obj['collection']



