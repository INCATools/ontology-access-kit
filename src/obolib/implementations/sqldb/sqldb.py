from typing import Any

from obolib.ontology_provider import OntologyProvider
from obolib.resource import OntologyResource
from sqlalchemy import create_engine

class SqlDatabaseProvider(OntologyProvider):

    @classmethod
    def create_engine(cls, resource: OntologyResource = None) -> Any:
        print(f'CREATING: {resource.slug}')
        engine = create_engine(resource.slug) ## TODO
        #Session = sessionmaker(engine)
        return engine




