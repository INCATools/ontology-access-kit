"""
Adapter for PubMed,

.. warning ::

    this is currently highly incomplete.
"""
import logging
from dataclasses import dataclass

from oaklib.datamodels import obograph
from oaklib.implementations.eutils.eutils_implementation import EUtilsImplementation

__all__ = [
    "PubMedImplementation",
]

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
        local_id = curie.replace("PMID:", "")
        paset = ec.efetch(db=self.database, id=local_id)
        for pa in paset:
            n = obograph.Node(
                id=curie,
                lbl=pa.title,
                meta=obograph.Meta(definition=obograph.DefinitionPropertyValue(val=pa.abstract))
                # TODO: creators, ...
            )
            return n
