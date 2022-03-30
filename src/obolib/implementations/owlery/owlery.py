from obolib.implementations.sparql.sparql import SparqlEndpointProvider
from obolib.resource import OntologyResource
from pronto import Ontology


class OwleryProvider(SparqlEndpointProvider):

    @classmethod
    def _default_url(cls) -> str:
        return "http://sparql.hegroup.org/sparql"

