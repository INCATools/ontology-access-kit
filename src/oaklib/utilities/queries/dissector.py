import logging
from typing import List, Optional, Union

from pydantic import BaseModel

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import HAS_PART, PART_OF
from oaklib.interfaces import OboGraphInterface
from oaklib.query import Query, ancestor_of, descendant_of, subclass_of
from oaklib.types import CURIE, PRED_CURIE

ITEM = Union[CURIE, str]
PRED_OR_PREDS = Union[PRED_CURIE, list[PRED_CURIE]]


class ClassReference(BaseModel):
    id: CURIE
    label: Optional[str] = None


class DissectedEntity(BaseModel):
    returned_type: ClassReference
    base_type: Optional[ClassReference] = None
    inferred_type: Optional[ClassReference] = None
    found_in: Optional[List[ClassReference]] = None


def dissection_query(
    structure: ITEM,
    dissection_relation: PRED_OR_PREDS = HAS_PART,
    inverse_relation: PRED_OR_PREDS = PART_OF,
    entity_type: ITEM = None,
) -> Query:
    """
    Generate a query for the dissection of a structure.

    >>> from oaklib import get_adapter
    >>> cl = get_adapter("sqlite:obo:cl")
    >>> q = dissection_query("neocortex", entity_type="neuron")
    >>> for cell, name in sorted(q.execute(cl, labels=True)):
    ...     print(cell, name)
    <BLANKLINE>
    ...
    CL:0000598 pyramidal neuron

    :param structure:
    :param dissection_relation:
    :param inverse_relation:
    :param entity_type:
    :return:
    """
    if not isinstance(dissection_relation, list):
        dissection_relation = [dissection_relation]
    if not isinstance(inverse_relation, list):
        inverse_relation = [inverse_relation]
    if isinstance(entity_type, str):
        # if user provides "neuron", assume we mean subtypes of neuron
        entity_type = subclass_of(entity_type)
    dissect_q = ancestor_of(
        descendant_of(structure, predicates=inverse_relation), predicates=dissection_relation
    )
    if entity_type:
        dissect_q = dissect_q & entity_type
    return dissect_q


def dissect(
    adapter: BasicOntologyInterface,
    structure: ITEM,
    dissection_relation: PRED_OR_PREDS = HAS_PART,
    inverse_relation: PRED_OR_PREDS = PART_OF,
    entity_type: ITEM = None,
    complete=True,
    **kwargs,
) -> List[DissectedEntity]:
    """
    Dissect a structure into its parts.

    All parts:

    >>> from oaklib import get_adapter
    >>> cl = get_adapter("sqlite:obo:cl")
    >>> for e in dissect(cl, "alveolus"):
    ...     print(e.returned_type.id, e.returned_type.label)
    <BLANKLINE>
    ...
    GO:0005929 cilium
    ...

    All parts of a certain type:

    >>> from oaklib import get_adapter
    >>> cl = get_adapter("sqlite:obo:cl")
    >>> for e in dissect(cl, "alveolus", entity_type="epithelial cell"):
    ...     print(e.returned_type.id, e.returned_type.label)
    <BLANKLINE>
    ...
    CL:4028002 alveolar capillary type 1 endothelial cell
    ...


    :param structure:
    :param dissection_relation:
    :param inverse_relation:
    :param entity_type:
    :return:
    """
    q = dissection_query(
        structure,
        dissection_relation=dissection_relation,
        inverse_relation=inverse_relation,
        entity_type=entity_type,
    )
    results = []
    for id, name in q.execute(adapter, labels=True, **kwargs):
        if not name:
            logging.info(f"No label found for {id}")
        entity = DissectedEntity(
            returned_type=ClassReference(id=id, label=name),
        )
        results.append(entity)
    if complete:
        if not isinstance(adapter, OboGraphInterface):
            raise NotImplementedError
        # ldefs = list(adapter.logical_definitions())

        # for entity in results:
        #    entity.found_in =
    return results
