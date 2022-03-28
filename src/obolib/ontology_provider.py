from typing import Any

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.resource import OntologyResource


class OntologyProvider:

    @classmethod
    def create_engine(cls, resource: OntologyResource) -> Any:
        raise NotImplementedError

    def get_basic_ontology_interface(self) -> BasicOntologyInterface:
        pass

    def get_owl_facade(self):
        pass

    def get_obo_graph_facade(self):
        pass

