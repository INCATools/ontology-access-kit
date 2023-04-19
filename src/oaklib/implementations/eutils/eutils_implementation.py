"""Abstract Base Class Adapter for EUtils."""
import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar, Iterable, Iterator, Optional, Tuple

from eutils import Client

__all__ = [
    "EUtilsImplementation",
]

from oaklib.datamodels.vocabulary import RDF_TYPE
from oaklib.interfaces import OboGraphInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    LANGUAGE_TAG,
    RELATIONSHIP,
)
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)


@dataclass
class EUtilsImplementation(OboGraphInterface, ABC):
    """
    Wraps Eutils endpoint.
    """

    entrez_client: Client = field(default_factory=lambda: Client())

    database: ClassVar[Optional[str]] = None
    entity_type: ClassVar[Optional[str]] = None

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang is not None:
            raise NotImplementedError("lang not implemented for eutils")
        n = self.node(curie)
        if n is not None:
            return n.lbl

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        if not subjects:
            raise NotImplementedError("subjects must be provided")
        for s in subjects:
            yield s, RDF_TYPE, self.entity_type

    def ontologies(self) -> Iterable[CURIE]:
        yield f"infores:{self.database}"

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang is not None:
            raise NotImplementedError("lang not implemented for eutils")
        n = self.node(curie)
        if n is not None:
            return n.meta.definition.val

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        yield from []

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        return {}
