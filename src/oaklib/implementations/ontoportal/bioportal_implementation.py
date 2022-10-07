from dataclasses import dataclass

from ontoportal_client import BioPortalClient

from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)


@dataclass
class BioPortalImplementation(OntoPortalImplementationBase):
    """
    A :ref:`OntoPortal` implementation that connects to a bioportal endpoint.

    Example:

    .. code :: python

        >>> api_key = get_apikey_value(BioPortalImplementation.ontoportal_client_class.name)
        >>> oi = BioPortalImplementation(api_key=api_key)
        >>> text = "increased expression of Shh in interneuron populations in the forebrain"
        >>> for ann in oi.annotate_text(text)
        >>>     ...

    See `<https://data.bioontology.org/documentation>`_
    """

    ontoportal_client_class = BioPortalClient
