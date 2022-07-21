from dataclasses import dataclass

from ontoportal_client import AgroPortalClient

from oaklib.interfaces.ontoportal_interface import OntoPortalInterface


@dataclass
class AgroportalImplementation(OntoPortalInterface):
    """
    Implementation over agroportal endpoint

    """

    OntoPortalClientClass = AgroPortalClient
    api_key_name = "agroportal"
