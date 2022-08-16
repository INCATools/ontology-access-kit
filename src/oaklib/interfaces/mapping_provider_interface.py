import logging
from abc import ABC
from typing import Iterable, Optional

from deprecation import deprecated
from sssom_schema import Mapping

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class MappingProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology provider that provides SSSOM mappings

    TODO: move code from mapping-walker
    """

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        for mapping in mappings:
            if not mapping.subject_label:
                mapping.subject_label = self.label(mapping.subject_id)
            if not mapping.object_label:
                mapping.object_label = self.label(mapping.object_id)

    def sssom_mappings_by_source(
        self, subject_or_object_source: Optional[str] = None
    ) -> Iterable[Mapping]:
        """
        All SSSOM mappings in the ontology

        The subject_id MUST be a CURIE in the ontology

        :param object_source:
        :return:
        """
        logging.info("Getting all mappings")
        for curie in self.entities():
            logging.debug(f"Getting mappings for {curie}")
            for m in self.get_sssom_mappings_by_curie(curie):
                if subject_or_object_source:
                    if (
                        m.object_source != subject_or_object_source
                        and m.subject_source != subject_or_object_source
                    ):
                        continue
                yield m

    @deprecated("Replaced by sssom_mappings()")
    def all_sssom_mappings(
        self, subject_or_object_source: Optional[str] = None
    ) -> Iterable[Mapping]:
        return self.sssom_mappings_by_source(subject_or_object_source)

    @deprecated("Use sssom_mappings()")
    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        """
        All SSSOM mappings about a curie

        MUST yield mappings where EITHER subject OR object equals the CURIE

        :param curie:
        :return:
        """
        raise NotImplementedError

    def sssom_mappings(
        self, curie: Optional[CURIE] = None, source: Optional[str] = None
    ) -> Iterable[Mapping]:
        """
        returns all sssom mappings matching filter conditions

        :param curie:
        :param source:
        :return:
        """
        logging.info("Getting all mappings")
        if curie:
            it = [curie]
        else:
            it = self.entities()
        for curie in it:
            logging.debug(f"Getting mappings for {curie}")
            for m in self.get_sssom_mappings_by_curie(curie):
                if source:
                    if m.object_source != source and m.subject_source != source:
                        continue
                yield m

    def get_transitive_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError
