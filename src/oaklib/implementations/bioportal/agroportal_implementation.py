from dataclasses import dataclass

from ontoportal_client import AgroPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import OntoPortalImplementationBase


@dataclass
class AgroportalImplementation(OntoPortalImplementationBase):
    """
    Implementation over agroportal endpoint

    """

    OntoPortalClientClass = AgroPortalClient
    api_key_name = "agroportal"
