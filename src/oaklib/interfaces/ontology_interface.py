from dataclasses import dataclass
from typing import List

from oaklib.resource import OntologyResource


@dataclass
class OntologyInterface:
    """
    An abstract parent for an ontology interface.
    """

    # engine: Any = None  ## implementation object
    resource: OntologyResource = None
    strict: bool = False

    @property
    def implementation_name(self):
        n = type(self).__name__
        if self.resource.slug:
            n += "-" + self.resource.slug
        return n

    @classmethod
    def create(cls, resource: OntologyResource) -> "OntologyInterface":
        """
        Creates a new ontology interface from a resource

        :param resource:
        :return:
        """
        raise NotImplementedError

    def interfaces_implemented(self) -> List:
        """
        For any given instance of this interface, find all interfaces implemented

        :return:
        """
        return list(type(self).__bases__)
