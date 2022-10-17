"""Base class for all mappers."""
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Tuple

from curies import Converter
from sssom_schema import SEMAPV, Mapping

from oaklib.datamodels.vocabulary import SKOS_EXACT_MATCH
from oaklib.types import CURIE, URI


@dataclass
class Mapper(ABC):
    """
    Abstract base class for all mappers.

    Mappers map between source CURIEs or URIs and target CURIEs or URIs
    """

    mappings: List[Mapping]
    """SSSOM mappings used as source."""

    curie_converter: Converter = None
    """Converter to go between CURIEs and URIs."""

    _mappings_by_source: Dict[CURIE, List[CURIE]] = None

    def __post_init__(self):
        self._mappings_by_source = defaultdict(list)
        self.add_mappings(self.mappings)
        self._index()

    def add_mapping(self, subject: CURIE, object: CURIE):
        m = Mapping(
            subject_id=subject,
            predicate_id=SKOS_EXACT_MATCH,
            object_id=object,
            mapping_justification=SEMAPV.RegularExpressionReplacement.value,
        )
        self.mappings.append(m)
        self._index()

    def add_mappings(self, mappings: List[Mapping]):
        """Adds more mappings."""
        self.mappings += mappings
        self._index()

    def _index(self):
        for m in self.mappings:
            if m.object_id not in self._mappings_by_source[m.subject_id]:
                self._mappings_by_source[m.subject_id].append(m.object_id)

    def map_curies(self, curies: Iterable[CURIE], strict=False) -> Iterator[Tuple[CURIE, CURIE]]:
        """
        Maps a collection of CURIEs.

        :param curies:
        :param strict:
        :return:
        """
        for curie in curies:
            for o in self._mappings_by_source.get(curie, []):
                yield curie, o

    def map_uris(self, uris: Iterable[URI], strict=False) -> Iterator[Tuple[URI, URI]]:
        """
        Maps a collection of URIs.

        :param uris:
        :param strict:
        :return:
        """
        for uri in uris:
            curie = self.curie_converter.compress(uri)
            for _, mapped_curie in self.map_curies([curie], strict=strict):
                yield uri, self.curie_converter.expand(mapped_curie)

    def map_curie(
        self, curie: CURIE, strict=False, unmapped_reflexive=True, single_valued=False
    ) -> List[CURIE]:
        """
        Maps an individual CURIE.

        :param curie:
        :param strict:
        :param unmapped_reflexive: if True, then an unmappable ID should map to itself
        :param single_valued: forces results to be single-valued
        :return:
        """
        objects = list(self.map_curies([curie], strict=strict))
        if not objects and unmapped_reflexive:
            objects = [(curie, curie)]
        if single_valued and len(objects) != 1:
            raise ValueError(f"Not single-valued for {curie} => {objects}")
        return [o for _, o in objects]

    def direct_map_curie(self, curie: CURIE) -> CURIE:
        """
        Returns single valued mapped curie

        if no mapping, returns self

        :param curie:
        :return:
        """
        return self.map_curie(curie, unmapped_reflexive=True)[0]

    def direct_map_uri(self, uri: URI) -> URI:
        """
        Returns single valued mapped uri

        if no mapping, returns self

        :param curie:
        :return:
        """
        uris = self.map_uris(uri)
        if uris:
            if len(uris) > 1:
                raise ValueError(f"Multiple mappings for {uri} = {uris}")
            return uris[0]
        else:
            return uri
