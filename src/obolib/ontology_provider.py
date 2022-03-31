from typing import Any

from obolib.resource import OntologyResource

# TODO: deprecate this
class OntologyProvider:

    @classmethod
    def create_engine(cls, resource: OntologyResource) -> Any:
        raise NotImplementedError

