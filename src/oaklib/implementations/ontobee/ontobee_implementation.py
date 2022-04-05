from abc import ABC
from dataclasses import dataclass

from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation


@dataclass
class OntobeeImplementation(SparqlImplementation):
    """
    Wraps the Ontobee sparql endpoint

    An OntobeeImplementation can be initialed by:

        .. code:: python

           >>>  oi = OntobeeImplementation.create()

        The default ontobee endpoint will be assumed

    See: `<https://www.ontobee.org/>`_
    """

    def _default_url(self) -> str:
        return "http://sparql.hegroup.org/sparql"









