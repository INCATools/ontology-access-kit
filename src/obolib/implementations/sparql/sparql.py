from typing import Union

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.ontology_provider import OntologyProvider
from obolib.resource import OntologyResource
from pronto import Ontology
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph


class SparqlEndpointProvider(OntologyProvider):

    @classmethod
    def create_engine(cls, resource: OntologyResource = None) -> Union[SPARQLWrapper, Graph]:
        if resource is None:
            resource = OntologyResource(url=cls._default_url())
        if resource.local:
            g = Graph()
            return g.parse(resource.local_path)
        else:
            print(f'URL = {resource.url}')
            return SPARQLWrapper(resource.url)

    @classmethod
    def dump(cls, ontology: Ontology, resource: OntologyResource):
        raise NotImplementedError

