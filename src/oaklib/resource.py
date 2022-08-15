from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Type, Union

from class_resolver import HintOrType

if TYPE_CHECKING:
    from .interfaces import OntologyInterface

__all__ = [
    "OntologyResource",
]


@dataclass
class OntologyResource:
    """
    A representation of an ontology resource.

    This may be a local or remote file, or an ontology name that is part of a remote service
    """

    slug: str = None
    directory: str = None
    scheme: str = None
    format: str = None
    url: str = None
    readonly: bool = False
    provider: str = None
    local: bool = False
    in_memory: bool = False
    data: str = None
    implementation_class: Union[Type] = None

    @property
    def local_path(self) -> Path:
        if self.directory:
            return Path(self.directory) / self.slug
        else:
            return Path(self.slug)

    def valid(self) -> bool:
        return self.slug is not None or self.url is not None

    def materialize(
        self, implementation: HintOrType["OntologyInterface"] = None, **kwargs
    ) -> "OntologyInterface":
        """Materialize the ontology resource with the given implementation."""
        from .implementations import SqlImplementation, implementation_resolver

        cls = implementation_resolver.lookup(implementation, default=SqlImplementation)
        return implementation_resolver.make(cls, kwargs, resource=self)
