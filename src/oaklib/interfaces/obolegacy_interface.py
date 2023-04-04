from abc import ABC
from typing import Union

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import PRED_CURIE

PRED_CODE = Union[str, PRED_CURIE]


class OboLegacyInterface(BasicOntologyInterface, ABC):
    """
    A BasicOntologyInterface that provides a bridge to legacy OBO Format concepts

    See <https://owlcollab.github.io/oboformat/doc/obo-syntax.html>_
    """

    def map_shorthand_to_curie(self, rel_code: PRED_CODE) -> PRED_CURIE:
        """
        Maps either a true relationship type CURIE or a shorthand packages to a CURIE.

        See `section 5.9 <https://owlcollab.github.io/oboformat/doc/obo-syntax.html#5.9>`_

        :param rel_code:
        :return:
        """
        raise NotImplementedError

    def map_curie_to_shorthand(self, rel_type: PRED_CURIE) -> PRED_CODE:
        """
        Reciprocal of `_get_relationship_type_curie`

        :param rel_type:
        :return:
        """
        raise NotImplementedError
