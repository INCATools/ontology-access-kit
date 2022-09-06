from dataclasses import dataclass

from ontoportal_client import BioPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class BioPortalImplementation(OntoPortalImplementationBase):
    """
    Implementation over bioportal endpoint

    See `<https://data.bioontology.org/documentation>`_
    """

    ontoportal_client_class = BioPortalClient
