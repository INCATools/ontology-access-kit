from abc import ABC
from dataclasses import dataclass

from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.interfaces.search_interface import SearchInterface


@dataclass
class OntobeeImplementation(SparqlImplementation, SearchInterface):
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









