import urllib

import requests
import logging
from dataclasses import dataclass, field
from typing import Any, List, Dict, Union, Iterator, Iterable, Tuple

from oaklib.datamodels import oxo
from oaklib.datamodels.oxo import ScopeEnum
from oaklib.datamodels.text_annotator import TextAnnotation
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.ols.oxo_utils import load_oxo_payload
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, PRED_CURIE
from sssom import Mapping
from sssom.sssom_datamodel import MatchTypeEnum
from sssom.sssom_document import MappingSetDocument

ANNOTATION = Dict[str, Any]

oxo_pred_mappings = {
    ScopeEnum.EXACT.text: 'skos:exactMatch',
    ScopeEnum.BROADER.text: 'skos:broadMatch',
    ScopeEnum.NARROWER.text: 'skos:narrowMatch',
    ScopeEnum.RELATED.text: 'skos:closeMatch',
}


@dataclass
class OlsImplementation(TextAnnotatorInterface, SearchInterface, MappingProviderInterface):
    """
    Implementation over OLS and OxO APIs

    .. note::


    """
    ols_api_key: str = None
    label_cache: Dict[CURIE, str] = field(default_factory=lambda: {})
    base_url = "https://www.ebi.ac.uk/spot/oxo/api/mappings"
    ols_base_url = "https://www.ebi.ac.uk/ols/api/ontologies/"
    prefix_map: Dict[str, str] = field(default_factory=lambda: {})
    focus_ontology: str = None

    def __post_init__(self):
        if self.focus_ontology is None:
            if self.resource:
                self.focus_ontology = self.resource.slug

    def add_prefix(self, curie: str, uri: str):
        [pfx, local] = curie.split(':', 2)
        if pfx not in self.prefix_map:
            self.prefix_map[pfx] = uri.replace(local, '')

    def get_prefix_map(self) -> PREFIX_MAP:
        return self.prefix_map

    def get_labels_for_curies(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        raise NotImplementedError

    def annotate_text(self, text: str) -> Iterator[TextAnnotation]:
        raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def ancestors(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        query = 'hierarchicalAncestors'
        if predicates:
            if predicates == [IS_A]:
                query = 'ancestors'
            elif IS_A not in predicates:
                raise NotImplementedError(f'OLS always include {IS_A}, you selected: {predicates}')
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        ancs = set()
        ontology = self.focus_ontology
        for curie in start_curies:
            term_id = self.curie_to_uri(curie)
            # must be double encoded https://www.ebi.ac.uk/ols/docs/api
            term_id_quoted = urllib.parse.quote(term_id, safe='')
            term_id_quoted = urllib.parse.quote(term_id_quoted, safe='')
            url = f'{self.ols_base_url}{ontology}/terms/{term_id_quoted}/{query}'
            logging.debug(f'URL={url}')
            result = requests.get(url)
            obj = result.json()
            if result.status_code == 200 and '_embedded' in obj:
                ancs.update([x['obo_id'] for x in obj['_embedded']['terms']])
            else:
                logging.debug(f'No ancestors for {url} (maybe ontology not indexed in OLS?)')
                ancs = []
        return list(ancs)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[Mapping]:
        result = requests.get(self.base_url, params=dict(fromId=curie))
        obj = result.json()
        container = load_oxo_payload(obj)
        return self.convert_payload(container)

    def convert_payload(self, container: oxo.Container) -> Iterator[Mapping]:
        oxo_mappings = container._embedded.mappings
        mappings: Mapping = []
        for oxo_mapping in oxo_mappings:
            oxo_s = oxo_mapping.fromTerm
            oxo_o = oxo_mapping.toTerm
            mapping = Mapping(subject_id=oxo_s.curie,
                              subject_label=oxo_s.label,
                              subject_source=oxo_s.datasource.prefix if oxo_s.datasource else None,
                              predicate_id=oxo_pred_mappings[str(oxo_mapping.scope)],
                              match_type=MatchTypeEnum.Unspecified,
                              object_id=oxo_o.curie,
                              object_label=oxo_o.label,
                              object_source=oxo_o.datasource.prefix if oxo_o.datasource else None,
                              mapping_provider=oxo_mapping.datasource.prefix)
            self.add_prefix(oxo_s.curie, oxo_s.uri)
            self.add_prefix(oxo_o.curie, oxo_o.uri)
            yield mapping

    def fill_gaps(self, msdoc: MappingSetDocument, confidence: float = 1.0) -> int:
        curie_map = curie_to_uri_map(msdoc)
        inv_map = {v: k for k, v in curie_map.items()}
        n = 0
        for curie, uri in curie_map.items():
            pfx, _ = curie.split(':', 2)
            ancs = self.get_ancestors(uri, ontology=pfx.lower())
            logging.debug(f'{curie} ANCS = {ancs}')
            for anc in ancs:
                if anc in curie_map:
                    m = Mapping(subject_id=curie,
                                object_id=anc,
                                predicate_id='rdfs:subClassOf',
                                confidence=confidence,
                                match_type=MatchTypeEnum.HumanCurated
                                )
                    logging.info(f'Gap filled link: {m}')
                    msdoc.mapping_set.mappings.append(m)
                    n += 1
        return n

