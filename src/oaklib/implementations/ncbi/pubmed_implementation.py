"""
Adapter for PubMed,

.. warning ::

    this is currently highly incomplete.
"""

import logging
import re
from dataclasses import dataclass
from typing import Optional

from oaklib.datamodels import obograph
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, RDFS_LABEL
from oaklib.implementations.ncbi.eutils_implementation import EUtilsImplementation
from oaklib.implementations.ncbi.pubmed_parser import (
    PubmedRecord,
    parse_pubmed_article_set,
)

__all__ = [
    "PubMedImplementation",
]

from oaklib.interfaces.basic_ontology_interface import METADATA_MAP
from oaklib.types import CURIE

logger = logging.getLogger(__name__)

PMID_PATTERN = re.compile(r"[0-9]+")


def _is_foreign_curie(curie: CURIE) -> bool:
    return ":" in curie and not curie.startswith("PMID:")


@dataclass
class PubMedImplementation(EUtilsImplementation):
    """
    Wraps PubMed endpoint.

    """

    database = "pubmed"
    entity_type = "schema:Publication"

    def _fetch_record(self, curie: CURIE) -> Optional[PubmedRecord]:
        local_id = curie.replace("PMID:", "").strip()
        if not PMID_PATTERN.fullmatch(local_id):
            logger.warning(f"Not a valid PubMed identifier: {curie}")
            return None
        # NCBI returns PMIDs without leading zeros
        local_id = str(int(local_id))
        logger.info(f"Fetching {local_id} from {self.database}")
        for record in parse_pubmed_article_set(self._efetch([local_id])):
            if record.pmid == local_id:
                return record
        return None

    def node(
        self,
        curie: CURIE,
        **kwargs,
    ) -> Optional[obograph.Node]:
        if _is_foreign_curie(curie):
            return obograph.Node(id=curie, lbl=curie)
        record = self._fetch_record(curie)
        if record is None:
            return None
        meta = None
        if record.abstract:
            meta = obograph.Meta(definition=obograph.DefinitionPropertyValue(val=record.abstract))
        # TODO: creators, ...
        return obograph.Node(id=curie, lbl=record.title, meta=meta)

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        if _is_foreign_curie(curie):
            return {}
        record = self._fetch_record(curie)
        if record is None:
            return {}
        return {
            "id": curie,
            RDFS_LABEL: record.title,
            HAS_DEFINITION_CURIE: record.abstract,
            "year": record.year,
            "authors": record.authors,
            "mesh_qualifiers": record.mesh_qualifiers,
            "mesh_headings": record.mesh_headings,
        }
