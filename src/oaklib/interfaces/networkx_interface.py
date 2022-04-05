from abc import ABC
from typing import Dict, List

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, LABEL, URI

# Deprecate? Just use utility class?
class NetworkxInterface(BasicOntologyInterface, ABC):
    """
    TODO: consider direct use of nxontology
    """