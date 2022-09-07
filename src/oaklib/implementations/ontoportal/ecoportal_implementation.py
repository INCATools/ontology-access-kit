from dataclasses import dataclass

from ontoportal_client import EcoPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class EcoPortalImplementation(OntoPortalImplementationBase):
    """
    Implementation over ecoportal endpoint

    """

    ontoportal_client_class = EcoPortalClient
