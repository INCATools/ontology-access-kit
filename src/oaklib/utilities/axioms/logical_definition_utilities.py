from typing import List, Optional

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import LogicalDefinitionAxiom
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE


def logical_definition_matches(
    ldef: LogicalDefinitionAxiom,
    subjects: Optional[List[CURIE]] = None,
    predicates: Optional[List[PRED_CURIE]] = None,
    objects: Optional[List[CURIE]] = None,
) -> bool:
    """
    Check if a logical definition matches a filter criteria.

    >>> from oaklib.datamodels.obograph import LogicalDefinitionAxiom, ExistentialRestrictionExpression
    >>> from oaklib.utilities.axioms.logical_definition_utilities import logical_definition_matches
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> differentia1 = ExistentialRestrictionExpression(propertyId="R:1", fillerId="X:Filler1")
    >>> differentia2 = ExistentialRestrictionExpression(propertyId="R:1", fillerId="X:Filler2")
    >>> ldef = LogicalDefinitionAxiom(definedClassId="X:1",
    ...            genusIds=["X:Genus"], restrictions=[differentia1, differentia2])
    >>> logical_definition_matches(ldef)
    True
    >>> logical_definition_matches(ldef, subjects=["X:Genus"])
    False
    >>> logical_definition_matches(ldef, objects=["X:Genus"])
    True
    >>> logical_definition_matches(ldef, subjects=["X:Filler1"])
    False
    >>> logical_definition_matches(ldef, predicates=["R:1"])
    True
    >>> logical_definition_matches(ldef, predicates=[IS_A])
    True
    >>> logical_definition_matches(ldef, objects=["X:Filler1"])
    True

    :param ldef:
    :param subjects: if specified, the logical definition must have one of these subjects
    :param predicates: if specified, the logical definition must have one of these predicates
    :param objects: if specified, the logical definition must have one of these objects
    :return:
    """
    if predicates or objects:
        class_signature = set(ldef.genusIds + [r.fillerId for r in ldef.restrictions])
        pred_signature = set([r.propertyId for r in ldef.restrictions])
        if ldef.genusIds:
            pred_signature.add(IS_A)
        if predicates:
            if not pred_signature.intersection(predicates):
                return False
        if objects:
            if not class_signature.intersection(objects):
                return False
    if subjects:
        if ldef.definedClassId not in subjects:
            return False
    return True


def roll_up_to_genus(
    term: CURIE, adapter: BasicOntologyInterface, predicates: List[PRED_CURIE]
) -> CURIE:
    """
    Walks up the genus hierarchy.

    This can be used to extract the "meaningful" genus of a compositional term

    :param term:
    :param adapter:
    :param predicates:
    :return:
    """
    if not isinstance(adapter, OboGraphInterface):
        raise NotImplementedError
    replacement = None
    for ldef in adapter.logical_definitions([term]):
        if len(ldef.restrictions) == 1 and len(ldef.genusIds) == 1:
            restr = ldef.restrictions[0]
            if restr.propertyId in predicates:
                replacement = ldef.genusIds[0]
    if replacement:
        return roll_up_to_genus(replacement, adapter, predicates)
    else:
        return term
