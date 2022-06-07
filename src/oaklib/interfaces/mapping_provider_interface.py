import logging
from abc import ABC
from typing import Dict, List, Tuple, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
import sssom
from oaklib.types import CURIE


class MappingProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology provider that provides SSSOM mappings

    TODO: move code from mapping-walker
    """

    def all_sssom_mappings(self) -> Iterable[sssom.Mapping]:
        """
        All SSSOM mappings in the ontology

        The subject_id MUST be a CURIE in the ontology

        :return:
        """
        logging.info(f'Getting all mappings')
        for curie in self.all_entity_curies():
            logging.debug(f'Getting mappings for {curie}')
            for m in self.get_sssom_mappings_by_curie(curie):
                yield m

    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[sssom.Mapping]:
        """
        All SSSOM mappings about a curie

        MUST yield mappings where EITHER subject OR object equals the CURIE

        :param curie:
        :return:
        """
        raise NotImplementedError

    def get_transitive_mappings_by_curie(self, curie: CURIE) -> Iterable[sssom.Mapping]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

