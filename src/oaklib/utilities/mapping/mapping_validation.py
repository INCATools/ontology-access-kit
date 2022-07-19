from typing import Iterator

from sssom_schema import Mapping

from oaklib.interfaces import MappingProviderInterface
from oaklib.utilities.mapping.cross_ontology_diffs import (
    group_mappings_by_source_pairs,
    object_source,
    subject_source,
)


def unreciprocated_mappings(
    subject_oi: MappingProviderInterface,
    object_oi: MappingProviderInterface,
    filter_unidirectional: bool = True,
    both_directions: bool = True,
) -> Iterator[Mapping]:
    """
    yields all mappings from all terms in subject ontology where the object
    is in the object ontology, and the object does not have the reciprocal mapping

    in some cases, no reciprocal mappings are expected - if filter_unidirectional is set
    then exclude from the report any mapping between sources where there exist no mappings
    between those sources

    So for example, if Uberon has xrefs to XAO, and XAO has xrefs to Uberon, then we expect
    all mappings to be reciprocated. But if ubeorn has xrefs to EMAPA, and EMAPA has no mappings
    to Uberon, we expect the mappings to be unidirectional

    :param subject_oi:
    :param object_oi:
    :param filter_unidirectional: if True (default), include only where reciprocals are expected
    :param both_directions: if True (default) also calculate from object to subject
    :return:
    """
    groups = group_mappings_by_source_pairs(subject_oi, object_oi)
    for m in subject_oi.sssom_mappings_by_source():
        subject_src = subject_source(m)
        object_src = object_source(m)
        subject_id = m.subject_id
        object_id = m.object_id
        if filter_unidirectional:
            if (object_src, subject_src) not in groups:
                return
        is_reciprocated = False
        for rm in object_oi.get_sssom_mappings_by_curie(object_id):
            if rm.object_id == subject_id:
                is_reciprocated = True
                break
        if not is_reciprocated:
            yield m
    if both_directions:
        if subject_oi != object_oi:
            for m in unreciprocated_mappings(
                object_oi,
                subject_oi,
                filter_unidirectional=filter_unidirectional,
                both_directions=False,
            ):
                yield m
