from abc import ABC
from typing import Dict, List, Iterable

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE


class DifferInterface(BasicOntologyInterface, ABC):
    """
    Generates descriptions of differences

    TBD: low level diffs vs high level

     See `KGCL <https://github.com/cmungall/knowledge-graph-change-language>`_
    """

    def diff(self, left_ontology_id: CURIE, right_ontology_id: CURIE) -> str:
        """
        Diffs two ontologies - both must be ontologies wrapped by the current implementation

        :param left_ontology_id:
        :param right_ontology_id:
        :return: TBD KGCL?
        """
