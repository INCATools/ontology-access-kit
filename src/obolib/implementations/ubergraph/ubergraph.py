from obolib.implementations.sparql.sparql import SparqlEndpointProvider
from obolib.resource import OntologyResource
from pronto import Ontology


class UbergraphProvider(SparqlEndpointProvider):

    @classmethod
    def _default_url(cls) -> str:
        return "https://ubergraph.apps.renci.org/sparql"

    def dump(cls, ontology: Ontology, resource: OntologyResource):
        pass