import logging
from collections import defaultdict
from collections.abc import Iterator
from copy import deepcopy
from typing import Dict, Iterable, List, Optional, Tuple

import networkx as nx
from sssom import Mapping

from oaklib.datamodels.cross_ontology_diff import (
    DiffCategory,
    MappingCardinalityEnum,
    RelationalDiff,
)
from oaklib.datamodels.vocabulary import IS_A, SEMAPV, SKOS_EXACT_MATCH
from oaklib.interfaces import MappingProviderInterface, RelationGraphInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.networkx_bridge import mappings_to_graph
from oaklib.utilities.label_utilities import add_labels_to_object

ONE_TO_ZERO = MappingCardinalityEnum(MappingCardinalityEnum["1:0"])
ONE_TO_MANY = MappingCardinalityEnum(MappingCardinalityEnum["1:n"])

DIFF_CATEGORY = CURIE
ANALOGOUS_RELATION = Tuple[DIFF_CATEGORY, CURIE, PRED_CURIE, CURIE, List[CURIE]]


def get_mappings_between(oi: MappingProviderInterface, external_source: str) -> Iterator[Mapping]:
    prefix = f"{external_source}:"
    for m in oi.sssom_mappings_by_source():
        if m.object_source == external_source or m.object_id.startswith(prefix):
            yield m


def subject_source(mapping: Mapping) -> str:
    if mapping.subject_source:
        return mapping.subject_source
    return mapping.subject_id.split(":")[0]


def object_source(mapping: Mapping) -> str:
    if mapping.object_source:
        return mapping.object_source
    return mapping.object_id.split(":")[0]


def group_mappings_by_source_pairs(
    subject_oi: MappingProviderInterface, object_oi: MappingProviderInterface
) -> Dict[Tuple[str, str], Mapping]:
    groups: Dict[Tuple[str, str], List[Mapping]] = defaultdict(list)
    for oi in [subject_oi, object_oi]:
        for m in oi.sssom_mappings_by_source():
            subject_src = subject_source(m)
            object_src = object_source(m)
            groups[(subject_src, object_src)].append(m)
    return groups


def relation_dict_as_tuples(md: Dict[PRED_CURIE, List[CURIE]]) -> Iterator[PRED_CURIE, CURIE]:
    for pred, parents in md.items():
        for p in parents:
            yield pred, p


def curie_has_prefix(curie: CURIE, sources: Optional[List[str]]) -> bool:
    return sources is None or curie.split(":")[0] in sources


def get_mappings_in(g: nx.Graph, curie: CURIE, sources: List[str]):
    if curie in g:
        return list(set([x for x in g.neighbors(curie) if curie_has_prefix(x, sources)]))
    else:
        return []


def calculate_pairwise_relational_diff(
    left_oi: OboGraphInterface,
    right_oi: OboGraphInterface,
    sources: List[str],
    entities: Optional[Iterable[CURIE]] = None,
    mappings: Optional[List[Mapping]] = None,
    predicates: Optional[List[PRED_CURIE]] = None,
    include_identity=False,
    include_reflexive=False,
    add_labels=False,
) -> Iterator[RelationalDiff]:
    """
    Calculates a relational diff between ontologies in two sources using the combined mappings
    from both

    E.g. use MP and HP mappings to give a report on how these ontologies are structurally different.

    :param left_oi:
    :param right_oi:
    :param sources:
    :param entities:
    :param mappings: if None, then mappings are extracted from both sources
    :param predicates:
    :param include_identity: include identity relations to mappings (useful for comparing versions)
    :param include_reflexive: include reflexive relations such as A part-of A; excluded by default
    :param add_labels:
    :return:
    """
    if include_identity:
        if mappings is None:
            mappings = []
        for x in set(left_oi.entities(filter_obsoletes=False)).intersection(
            right_oi.entities(filter_obsoletes=False)
        ):
            m = Mapping(
                subject_id=x,
                object_id=x,
                predicate_id=SKOS_EXACT_MATCH,
                mapping_justification=SEMAPV.LexicalMatching.value,
            )
            mappings.append(m)
        logging.info(f"Identity mappings: {len(mappings)}")
    if mappings is None:
        logging.info("No mappings provided -- using mappings embedded in both ontologies")
        mappings = []
        at_least_one = False
        if isinstance(left_oi, MappingProviderInterface):
            mappings += list(left_oi.sssom_mappings_by_source())
            at_least_one = True
        if isinstance(right_oi, MappingProviderInterface):
            mappings += list(right_oi.sssom_mappings_by_source())
            at_least_one = True
        if not at_least_one:
            raise NotImplementedError(
                "One of left and right inputs must implement MappingProvider if mappings "
                "are not specified"
            )
        if not mappings:
            logging.warning("No mappings found in either left or right")
    if entities is not None:
        entities = list(entities)
        if False:
            logging.info(
                f"Filtering {len(mappings)} mappings to entity set of size {len(entities)}"
            )
            mappings = [m for m in mappings if m.subject_id in entities or m.object_id in entities]
            if not mappings:
                logging.warning("No mappings present after filtering: consider expanding entities")
    logging.info(f"Converting all {len(mappings)} mappings to networkx, sources={sources}")
    g = mappings_to_graph(mappings)
    logging.info("Completed conversion to nx")
    if isinstance(left_oi, OboGraphInterface) and isinstance(right_oi, OboGraphInterface):
        if entities is not None:
            left_oi_entities = entities
        else:
            left_oi_entities = left_oi.entities()
        for subject_child in left_oi_entities:
            logging.info(f"Subject child: {subject_child}")
            if not curie_has_prefix(subject_child, sources):
                continue
            for pred, subject_parent in relation_dict_as_tuples(
                left_oi.outgoing_relationship_map(subject_child)
            ):
                if entities is not None:
                    if subject_child not in entities and subject_parent not in entities:
                        continue
                if predicates and pred not in predicates:
                    continue
                if not curie_has_prefix(subject_parent, sources):
                    continue
                if not include_reflexive and subject_child == subject_parent:
                    continue
                for r in calculate_pairwise_relational_diff_for_edge(
                    left_oi,
                    right_oi,
                    sources,
                    g,
                    subject_child,
                    pred,
                    subject_parent,
                    predicates=predicates,
                    include_reflexive=include_reflexive,
                ):
                    if add_labels:
                        add_labels_to_object(
                            left_oi,
                            r,
                            [
                                ("left_subject_id", "left_subject_label"),
                                ("left_object_id", "left_object_label"),
                            ],
                        )
                        add_labels_to_object(
                            right_oi,
                            r,
                            [
                                ("right_subject_id", "right_subject_label"),
                                ("right_object_id", "right_object_label"),
                            ],
                        )
                    yield r
    else:
        raise NotImplementedError


def _mapping_cardinality(opposite_nodes: List[CURIE]) -> Optional[MappingCardinalityEnum]:
    if len(opposite_nodes) == 0:
        return ONE_TO_ZERO
    elif len(opposite_nodes) > 1:
        return ONE_TO_MANY
    else:
        return None


def calculate_pairwise_relational_diff_for_edge(
    left_oi: OboGraphInterface,
    right_oi: OboGraphInterface,
    sources: List[str],
    nx_graph: nx.Graph,
    left_subject: CURIE,
    left_predicate: PRED_CURIE,
    left_object: CURIE,
    predicates: Optional[List[PRED_CURIE]] = None,
    include_reflexive=False,
) -> Iterator[RelationalDiff]:
    """
    Given an edge from the left-side ontology, determine if an analogous edge can be found
    on the right side. If it exists, check it for consistency.

    See the cross-ontology diff datamodel for more details

    :param left_oi:
    :param right_oi:
    :param sources:
    :param nx_graph:
    :param left_subject:
    :param left_predicate:
    :param left_object:
    :param predicates:
    :param include_reflexive:
    :return: iterator over differences
    """
    logging.debug(f"Checking for analog of {left_subject} {left_predicate} {left_object}")
    rdiff = RelationalDiff(
        left_subject_id=left_subject,
        left_predicate_id=left_predicate,
        left_object_id=left_object,
    )
    # candidate right edges are drawn from the cross-product of mappings
    # of the left subject and left object
    right_subject_list = get_mappings_in(nx_graph, left_subject, sources)
    right_object_list = get_mappings_in(nx_graph, left_object, sources)
    rdiff.subject_mapping_cardinality = _mapping_cardinality(right_subject_list)
    candidates: List[RelationalDiff] = []
    for right_subject in right_subject_list:
        right_subject_ancs = list(right_oi.ancestors(right_subject, predicates=predicates))
        # logging.debug(f"RIGHT: {right_subject} // ANCS[{predicates}] = {right_subject_ancs}")
        right_subject_parents = []
        right_subject_direct_outgoing = defaultdict(list)
        for p, o in right_oi.outgoing_relationships(right_subject):
            right_subject_parents.append(o)
            right_subject_direct_outgoing[p].append(o)
        # right_subject_direct_outgoing = right_oi.get_outgoing_relationship_map_by_curie(
        #    right_subject
        # )
        for right_object in right_object_list:
            if not include_reflexive and right_subject == right_object:
                continue
            candidate = deepcopy(rdiff)
            candidate.right_subject_id = right_subject
            candidate.right_object_id = right_object
            rdiff.object_mapping_cardinality = _mapping_cardinality(right_subject_list)
            is_direct = right_object in right_subject_parents
            if right_object == right_subject:
                candidate.category = DiffCategory.RightNodesAreIdentical
            elif right_object in right_subject_ancs:
                if (
                    left_predicate in right_subject_direct_outgoing
                    and right_object in right_subject_direct_outgoing[left_predicate]
                ):
                    candidate.category = DiffCategory.Identical
                    candidate.right_predicate_ids = [left_predicate]
                elif isinstance(right_oi, RelationGraphInterface):
                    candidate.right_predicate_ids = list(
                        right_oi.entailed_relationships_between(right_subject, right_object)
                    )
                    if left_predicate in candidate.right_predicate_ids:
                        candidate.category = DiffCategory.LeftEntailedByRight
                    else:
                        candidate.category = DiffCategory.NonEntailedRelationship
                elif right_object in list(
                    right_oi.ancestors(right_subject, predicates=[left_predicate, IS_A])
                ):
                    if is_direct:
                        candidate.category = DiffCategory.MoreSpecificPredicateOnRight
                    else:
                        candidate.category = DiffCategory.IndirectFormOfEdgeOnRight
                else:
                    candidate.category = DiffCategory.NonEntailedRelationship
            else:
                candidate.category = DiffCategory.NoRelationship
            assert candidate.category
            # TODO
            candidate.category = DiffCategory(candidate.category)
            candidates.append(candidate)
    # TODO: allow caller to bypass filtering
    candidates = _filter_candidates(candidates, rdiff)
    for candidate in candidates:
        yield candidate


def _filter_candidates(
    candidates: List[RelationalDiff], base: RelationalDiff
) -> List[RelationalDiff]:
    if len(candidates) == 0:
        base.category = DiffCategory(DiffCategory.MissingMapping)
        return [base]
    by_cat = defaultdict(list)
    for d in candidates:
        by_cat[str(d.category)].append(d)
    # TODO: introspect rankings in schema for this
    priority_ranking = [
        DiffCategory.Identical,
        DiffCategory.LessSpecificPredicateOnRight,
        DiffCategory.MoreSpecificPredicateOnRight,
        DiffCategory.IndirectFormOfEdgeOnRight,
        DiffCategory.LeftEntailedByRight,
        DiffCategory.RightEntailedByLeft,
        DiffCategory.NonEntailedRelationship,
        DiffCategory.RightNodesAreIdentical,
        DiffCategory.NoRelationship,
        DiffCategory.MissingMapping,
    ]
    for c in priority_ranking:
        n = str(DiffCategory(c))
        if n in by_cat:
            return by_cat[n]
    raise ValueError(f"Unexpected category: {list(by_cat.keys())}")
