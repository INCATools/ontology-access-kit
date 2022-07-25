from typing import List, Tuple, Union

from linkml_runtime.linkml_model import SlotDefinitionName
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib import BasicOntologyInterface


def add_labels_to_object(
    oi: BasicOntologyInterface,
    obj: YAMLRoot,
    pairs: List[Tuple[Union[SlotDefinitionName, str], Union[SlotDefinitionName, str]]],
) -> None:
    """
    Adds labels to an object, for a set of id-label relation pairs

    :param oi: An ontology interface for making label lookups.
    :param obj: object to be filled
    :param pairs: list of slot name pairs
    :return: None
    """
    for curie_slot, label_slot in pairs:
        curie = getattr(obj, curie_slot, None)
        if curie is not None:
            label = oi.label(curie)
            if label is not None:
                setattr(obj, label_slot, label)
