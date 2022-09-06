from dataclasses import dataclass

from ontoportal_client import AgroPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class AgroPortalImplementation(OntoPortalImplementationBase):
    """
    Implementation over agroportal endpoint

    """

    ontoportal_client_class = AgroPortalClient
