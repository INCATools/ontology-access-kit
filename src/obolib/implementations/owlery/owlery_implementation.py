from abc import ABC
from dataclasses import dataclass

from obolib.implementations.sparql.sparql_implementation import SparqlImplementation
from obolib.interfaces.owl_interface import OwlInterface
from obolib.resource import OntologyResource


@dataclass
class OwleryImplementation(OwlInterface, SparqlImplementation):
    """
    Wraps an owlery endpoint

     See `<https://github.com/phenoscape/owlery>`_

    .. warning ::

      Not implemented
    """


    @classmethod
    def create(cls, resource: OntologyResource = None) -> "OwleryImplementation":
        """

        """
        engine = OwleryProvider.create_engine(resource)
        return OwleryImplementation(engine)







