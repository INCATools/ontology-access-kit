from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.ontology_provider import OntologyProvider
from obolib.resource import OntologyResource
from pronto import Ontology


class ProntoProvider(OntologyProvider):

    @classmethod
    def create_engine(cls, resource: OntologyResource = None) -> Ontology:
        if resource is None:
            ontology = Ontology()
        elif resource.local:
            ontology = Ontology(str(resource.local_path))
        else:
            ontology = Ontology.from_obo_library(resource.slug)
        return ontology

    def get_basic_ontology_interface(self) -> BasicOntologyInterface:
        pass

    @classmethod
    def dump(cls, ontology: Ontology, resource: OntologyResource):
        if resource.local:
            with open(str(resource.local_path), 'wb') as f:
                ontology.dump(f, format=resource.format)
        else:
            raise NotImplementedError(f'Cannot dump to {resource}')

