from obolib.implementations.sparql.sparql import SparqlEndpointProvider


class UbergraphProvider(SparqlEndpointProvider):

    @classmethod
    def _default_url(cls) -> str:
        return "https://ubergraph.apps.renci.org/sparql"
