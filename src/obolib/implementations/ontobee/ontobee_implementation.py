from abc import ABC
from dataclasses import dataclass

import SPARQLWrapper
from obolib.implementations.ontobee.ontobee import OntobeeProvider
from obolib.implementations.sparql.sparql_implementation import SparqlImplementation
from obolib.resource import OntologyResource


@dataclass
class OntobeeImplementation(SparqlImplementation):
    """
    Wraps the Ontobee sparql endpoint

    See: `<https://www.ontobee.org/>`_
    """

    @classmethod
    def create(cls, resource: OntologyResource = None) -> "OntobeeImplementation":
        """
        An OntobeeImplementation can be initialed by:

        .. code:: python

           >>>  oi = OntobeeImplementation.create()

        The default ontobee endpoint will be assumed

        :param resource: optional
        :return: OntobeeImplementation
        """
        engine = OntobeeProvider.create_engine(resource)
        return OntobeeImplementation(sparql_wrapper=engine)







