from collections import Iterator, defaultdict
from typing import Dict, List, Tuple

import networkx as nx
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import MappingProviderInterface, RelationGraphInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import PRED_CURIE, CURIE
from oaklib.utilities.graph.networkx_bridge import mappings_to_graph
from sssom import Mapping

DIFF_CATEGORY = CURIE

def get_mappings_between(oi: MappingProviderInterface, external_source: str) -> Iterator[Mapping]:
    prefix = f'{external_source}:'
    for m in oi.all_sssom_mappings():
        if m.object_source == external_source or m.object_id.startswith(prefix):
            yield m

def subject_source(mapping: Mapping) -> str:
    if mapping.subject_source:
        return mapping.subject_source
    return mapping.subject_id.split(':')[0]

def object_source(mapping: Mapping) -> str:
    if mapping.object_source:
        return mapping.object_source
    return mapping.object_id.split(':')[0]

def group_mappings_by_source_pairs(subject_oi: MappingProviderInterface, object_oi: MappingProviderInterface) -> List[Tuple[str, str]]:
    groups: Dict[Tuple[str, str], List[Mapping]] = defaultdict(list)
    for oi in [subject_oi, object_oi]:
        for m in oi.all_sssom_mappings():
            subject_src = subject_source(m)
            object_src = object_source(m)
            groups[(subject_src, object_src)].append(m)
    return groups


def unreciprocated_mappings(subject_oi: MappingProviderInterface, object_oi: MappingProviderInterface,
                            filter_unidirectional: bool = True, both_directions: bool = True) -> Iterator[Mapping]:
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
    for m in subject_oi.all_sssom_mappings():
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
            for m in unreciprocated_mappings(object_oi, subject_oi, filter_unidirectional=filter_unidirectional, both_directions=False):
                yield m

def relation_dict_as_tuples(md: Dict[PRED_CURIE, List[CURIE]]) -> Iterator[PRED_CURIE, CURIE]:
    for pred, parents in md.items():
        for p in  parents:
            yield pred, p

def curie_has_prefix(curie: CURIE, sources: List[str]) -> bool:
    return curie.split(':')[0] in sources

def get_mappings_in(g: nx.Graph, curie: CURIE, sources: List[str]):
    if curie in g:
        return [x for x in g.neighbors(curie) if curie_has_prefix(x, sources)]
    else:
        return []

def caclulate_pairwise_relational_diff(subject_oi: MappingProviderInterface, object_oi: MappingProviderInterface,
                                       sources: List[str]) -> Iterator[DIFF_CATEGORY, CURIE, PRED_CURIE, CURIE, List[CURIE]]:
    g = mappings_to_graph(list(subject_oi.all_sssom_mappings()) + list(object_oi.all_sssom_mappings()))
    if isinstance(subject_oi, OboGraphInterface) and isinstance(object_oi, OboGraphInterface):
        for subject_child in subject_oi.all_entity_curies():
            for pred, subject_parent in relation_dict_as_tuples(subject_oi.get_outgoing_relationships_by_curie(subject_child)):
                has_edge = False
                has_predicate = False
                has_direct_predicate = False
                object_child_list = get_mappings_in(g, subject_child, sources)
                object_parent_list = get_mappings_in(g, subject_parent, sources)
                for object_child in object_child_list:
                    object_child_ancs = list(object_oi.ancestors(object_child))
                    object_child_direct_outgoing = object_oi.get_outgoing_relationships_by_curie(object_child)
                    for object_parent in object_parent_list:
                        #print(f'CHECKING: {object_child} -> {object_parent} // {object_child_ancs}')
                        if object_parent in object_child_ancs:
                            has_edge = True
                            if pred in object_child_direct_outgoing and object_parent in object_child_direct_outgoing[pred]:
                                has_predicate = True
                                has_direct_predicate = True
                            elif isinstance(object_oi, RelationGraphInterface):
                                object_preds = list(object_oi.entailed_relationships_between(object_child, object_parent))
                                if pred in object_preds:
                                    has_predicate = True
                            elif object_parent in list(object_oi.ancestors(object_child, predicates=[pred, IS_A])):
                                has_predicate = True
                if has_edge:
                    if has_direct_predicate:
                        category = 'IDENTICAL'
                    elif has_predicate:
                        category = 'CONSISTENT'
                    else:
                        category = 'OTHER'
                else:
                    category = 'MISSING_EDGE'
                yield category, subject_child, pred, subject_parent, []





