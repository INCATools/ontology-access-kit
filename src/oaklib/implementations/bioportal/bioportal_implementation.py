from dataclasses import dataclass

from ontoportal_client import BioPortalClient

from oaklib.interfaces.ontoportal_interface import OntoPortalInterface


@dataclass
class BioportalImplementation(OntoPortalInterface):
    """
    Implementation over bioportal endpoint

    See `<https://data.bioontology.org/documentation>`_
    """

    OntoPortalClientClass = BioPortalClient
    api_key_name = "bioportal"
