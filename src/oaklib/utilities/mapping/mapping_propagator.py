from typing import Iterator, List

from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE

PREDICATE = [IS_A]


def propagate_terms_over_mappings(
    oi: MappingProviderInterface, curies: List[CURIE], predicates: List[PRED_CURIE] = PREDICATE
) -> Iterator:
    if isinstance(oi, OboGraphInterface):
        for curie in curies:
            for anc in oi.ancestors(curie, predicates):
                if isinstance(oi, MappingProviderInterface):
                    for m in oi.get_sssom_mappings_by_curie(curie):
                        yield curie, anc, m.object_id
