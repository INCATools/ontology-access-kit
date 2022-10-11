from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Type, Union

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
    """Name or path of ontology resource"""

    directory: Optional[str] = None
    """For local resources, the directory where the serialization is found"""

    scheme: Optional[str] = None
    """The scheme of the resource, e.g pronto, sqlite"""

    format: Optional[str] = None
    """For serialized resources, the serialization format"""

    url: Optional[str] = None
    """For remote resources, the URL from which it can be obtained"""

    readonly: Optional[bool] = False
    """Typically true for remote resources"""

    provider: Optional[str] = None

    local: Optional[bool] = False
    """Is the resource locally on disk or remote?"""

    in_memory: Optional[bool] = False

    data: Optional[str] = None

    implementation_class: Optional[Union[Type]] = None

    import_depth: Optional[int] = None
    """If set, this determines the maximum depth in the import tree to follow"""

    @property
    def local_path(self) -> Optional[Path]:
        if self.slug:
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
        from .implementations import SqlImplementation, get_implementation_resolver

        implementation_resolver = get_implementation_resolver()
        cls = implementation_resolver.lookup(implementation, default=SqlImplementation)
        return implementation_resolver.make(cls, kwargs, resource=self)
