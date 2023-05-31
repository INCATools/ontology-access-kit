import logging
from dataclasses import dataclass
from typing import Iterator

from funowl import Axiom

from oaklib import BasicOntologyInterface
from oaklib.inference.reasoner import Reasoner

logger = logging.getLogger(__name__)


@dataclass
class OwlReasoner(Reasoner):
    """
    A reasoner that computes entailed axioms.

    .. warning::

        This is a stub implementation that does not do any reasoning.
        TODO: decide whether to use robot+py4j vs whelk...
    """

    ontology_adapter: BasicOntologyInterface
    """The ontology to reason over"""

    def entailed_axioms(self) -> Iterator[Axiom]:
        """
        Computes the entailed axioms of the ontology.

        :return:
        """
        raise NotImplementedError
