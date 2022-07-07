from dataclasses import dataclass

from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.owl_interface import OwlInterface


@dataclass
class OwleryImplementation(OwlInterface, AbstractSparqlImplementation):
    """
    Wraps an owlery endpoint

     See `<https://github.com/phenoscape/owlery>`_

    .. warning ::

      Not implemented
    """
