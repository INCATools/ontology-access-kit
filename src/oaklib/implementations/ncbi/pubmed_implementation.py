"""
Adapter for PubMed,

.. warning ::

    this is currently highly incomplete.
"""

import logging
from dataclasses import dataclass

from oaklib.datamodels import obograph
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, RDFS_LABEL
from oaklib.implementations.ncbi.eutils_implementation import EUtilsImplementation

__all__ = [
    "PubMedImplementation",
]

from oaklib.interfaces.basic_ontology_interface import METADATA_MAP
from oaklib.types import CURIE

logger = logging.getLogger(__name__)


@dataclass
class PubMedImplementation(EUtilsImplementation):
    """
    Wraps PubMed endpoint.

    """

    database = "pubmed"
    entity_type = "schema:Publication"

    def node(
        self,
        curie: CURIE,
        **kwargs,
    ) -> obograph.Node:
        ec = self.entrez_client
        if ":" in curie and not curie.startswith("PMID:"):
            return obograph.Node(id=curie, lbl=curie)
        local_id = curie.replace("PMID:", "")
        logger.info(f"Fetching {local_id} from {self.database}")
        paset = ec.efetch(db=self.database, id=local_id)
        for pa in paset:
            n = obograph.Node(
                id=curie,
                lbl=pa.title,
                meta=obograph.Meta(definition=obograph.DefinitionPropertyValue(val=pa.abstract)),
                # TODO: creators, ...
            )
            return n

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        ec = self.entrez_client
        if ":" in curie and not curie.startswith("PMID:"):
            return {}
        local_id = curie.replace("PMID:", "")
        logger.info(f"Fetching {local_id} from {self.database}")
        paset = ec.efetch(db=self.database, id=local_id)
        for pa in paset:
            m = {
                "id": curie,
                RDFS_LABEL: pa.title,
                HAS_DEFINITION_CURIE: pa.abstract,
                "year": pa.year,
                "authors": pa.authors,
                "mesh_qualifiers": pa.mesh_qualifiers,
                "mesh_headings": pa.mesh_headings,
            }
            return m
