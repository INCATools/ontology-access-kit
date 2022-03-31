from abc import ABC
from typing import Dict, List

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE, LABEL, URI

# Deprecate? Just use utility class?
class NetworkxInterface(BasicOntologyInterface, ABC):
    """
    TODO: consider direct use of nxontology
    """