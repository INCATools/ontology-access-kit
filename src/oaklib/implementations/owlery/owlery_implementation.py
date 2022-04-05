from dataclasses import dataclass

from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.interfaces.owl_interface import OwlInterface


@dataclass
class OwleryImplementation(OwlInterface, SparqlImplementation):
    """
    Wraps an owlery endpoint

     See `<https://github.com/phenoscape/owlery>`_

    .. warning ::

      Not implemented
    """







