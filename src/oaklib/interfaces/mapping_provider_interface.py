import logging
from abc import ABC
from typing import Iterable

import sssom

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class MappingProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology provider that provides SSSOM mappings

    TODO: move code from mapping-walker
    """

    def all_sssom_mappings(self, subject_or_object_source: str = None) -> Iterable[sssom.Mapping]:
        """
        All SSSOM mappings in the ontology

        The subject_id MUST be a CURIE in the ontology

        :param object_source:
        :return:
        """
        logging.info("Getting all mappings")
        for curie in self.all_entity_curies():
            logging.debug(f"Getting mappings for {curie}")
            for m in self.get_sssom_mappings_by_curie(curie):
                if subject_or_object_source:
                    if (
                        m.object_source != subject_or_object_source
                        and m.subject_source != subject_or_object_source
                    ):
                        continue
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
