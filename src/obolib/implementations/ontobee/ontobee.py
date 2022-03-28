from obolib.implementations.sparql.sparql import SparqlEndpointProvider
from obolib.resource import OntologyResource
from pronto import Ontology


class OntobeeProvider(SparqlEndpointProvider):

    @classmethod
    def _default_url(cls) -> str:
        return "http://sparql.hegroup.org/sparql"

    def dump(cls, ontology: Ontology, resource: OntologyResource):
        pass