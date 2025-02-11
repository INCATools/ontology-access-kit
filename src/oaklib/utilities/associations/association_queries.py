import itertools
import logging
from typing import Iterator, List, Optional

from oaklib.datamodels.association import Association
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
    SubjectOrObjectRole,
)
from oaklib.types import CURIE, PRED_CURIE


def get_association_iterator(
    impl: AssociationProviderInterface,
    curies: List[CURIE],
    terms_role: Optional[str] = None,
    association_predicates: Optional[List[PRED_CURIE]] = None,
    ontology_predicates: Optional[List[PRED_CURIE]] = None,
    **kwargs,
) -> Iterator[Association]:
    """
    Query associations for a list of curies.

    :param impl:
    :param curies: Query terms
    :param terms_role: are the query terms subjects (e.g. genes; default) or objects (e.g. terms)?
    :param association_predicates:  if provided, filters the associations by these predicates (e.g. involved-in)
    :param ontology_predicates: (recommended) ontology closure predicates
    :param kwargs:
    :return:
    """
    qs_it = impl.associations(
        curies,
        predicates=association_predicates,
        subject_closure_predicates=ontology_predicates,
        **kwargs,
    )
    qo_it = impl.associations(
        objects=curies,
        predicates=association_predicates,
        object_closure_predicates=ontology_predicates,
        **kwargs,
    )
    if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
        it = qs_it
    elif terms_role == SubjectOrObjectRole.OBJECT.value:
        it = qo_it
    else:
        logging.info("Using query terms to query both subject and object")
        it = itertools.chain(qs_it, qo_it)
    return it
