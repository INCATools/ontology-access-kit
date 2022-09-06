from dataclasses import dataclass

from ontoportal_client import MatPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class MatPortalImplementation(OntoPortalImplementationBase):
    """
    Implementation over matportal endpoint

    """

    ontoportal_client_class = MatPortalClient
