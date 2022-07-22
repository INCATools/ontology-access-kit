from dataclasses import dataclass

from ontoportal_client import BioPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class BioportalImplementation(OntoPortalImplementationBase):
    """
    Implementation over bioportal endpoint

    See `<https://data.bioontology.org/documentation>`_
    """

    OntoPortalClientClass = BioPortalClient
    api_key_name = "bioportal"
