from obolib.implementations.sparql.sparql import SparqlEndpointProvider


class OntobeeProvider(SparqlEndpointProvider):

    @classmethod
    def _default_url(cls) -> str:
        return "http://sparql.hegroup.org/sparql"
