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
    -------
    .. packages :: python

        >>> from oaklib.implementations.ontoportal.bioportal_implementation import BioPortalImplementation
        >>> from oaklib.implementations.ontoportal.ontoportal_implementation_base import get_apikey_value
        >>> api_key = get_apikey_value(BioPortalImplementation.ontoportal_client_class.name)
        >>> oi = BioPortalImplementation(api_key=api_key)
        >>> text = "increased expression of Shh in interneuron populations in the forebrain"
        >>> for ann in oi.annotate_text(text):
        ...     print(ann.subject_start, ann.subject_end, ann.object_id, ann.object_label)
        <BLANKLINE>
        ...
        1 9 PATO:0000470 increased amount
        ...
        63 71 FMA:61992 Forebrain
        ...

    See `<https://data.bioontology.org/documentation>`_

    """

    ontoportal_client_class = BioPortalClient
