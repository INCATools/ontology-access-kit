import logging
from collections import defaultdict
from copy import deepcopy
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from sssom_schema import Mapping, MappingCardinalityEnum

import oaklib.datamodels.obograph as og
from oaklib import get_adapter
from oaklib.datamodels.vocabulary import HAS_DBXREF, SKOS_EXACT_MATCH
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE
from oaklib.utilities.mapping.cross_ontology_diffs import (
    group_mappings_by_source_pairs,
    object_source,
    subject_source,
)


def _prefix(curie: CURIE) -> str:
    return curie.split(":")[0].lower()


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


def partition_mappings(
    mappings: List[Mapping],
) -> Dict[Tuple[str, str], List[Mapping]]:
    """
    Partition mappings by subject and object prefixes.

    >>> from oaklib import get_adapter
    >>> from oaklib.utilities.mapping.mapping_validation import partition_mappings
    >>> adapter = get_adapter("sqlite:obo:xao")
    >>> mappings = list(adapter.sssom_mappings())
    >>> by_prefixes = partition_mappings(mappings)
    >>> for prefix_pair, mappings in partition_mappings(mappings).items():
    ...     for mapping in mappings:
    ...         print(prefix_pair, mapping.subject_id, mapping.object_id)
    <BLANKLINE>
    ...
    ('xao', 'cl') XAO:0003252 CL:0000311
    ...

    :param mappings:
    :return:
    """
    partitioned = defaultdict(list)
    for m in mappings:
        subject_prefix = _prefix(m.subject_id)
        object_prefix = _prefix(m.object_id)
        k = (subject_prefix, object_prefix)
        partitioned[k].append(m)
    return partitioned


def assign_mapping_cardinalities(
    mappings: List[Mapping],
) -> None:
    groups = partition_mappings(mappings)
    for _, mappings in groups.items():
        s2o = defaultdict(set)
        o2s = defaultdict(set)
        for m in mappings:
            s2o[m.subject_id].add(m.object_id)
            o2s[m.object_id].add(m.subject_id)
        for m in mappings:

            def _card(n: int) -> str:
                if n == 1:
                    return "1"
                elif n == 0:
                    return "0"
                else:
                    return "n"

            card_str = f"{_card(len(s2o[m.subject_id]))}:{_card(len(o2s[m.object_id]))}"
            m.mapping_cardinality = MappingCardinalityEnum(MappingCardinalityEnum[card_str])


# TODO: avoid globals
obsoletes = {}


def _obsoletes(prefix: str, adapters: Optional[Dict[str, BasicOntologyInterface]]) -> List[CURIE]:
    if prefix not in obsoletes:
        adapter = lookup_mapping_adapter(prefix, adapters)
        obsoletes[prefix] = list(adapter.obsoletes(include_merged=True))
    return obsoletes[prefix]


def lookup_mapping_adapter(
    curie: CURIE, adapters: Optional[Dict[str, BasicOntologyInterface]]
) -> Optional[BasicOntologyInterface]:
    """
    Look up an adapter for a given CURIE using a Dict of adapters.

    :param curie:
    :param adapters:
    :return:
    """
    prefix = _prefix(curie)
    if "*" in adapters:
        adapters[prefix] = adapters["*"]
        if prefix not in obsoletes:
            obsoletes[prefix] = list(adapters[prefix].obsoletes(include_merged=True))
    if prefix not in adapters:
        logging.info(f"loading {prefix}")
        try:
            adapters[prefix] = get_adapter(f"sqlite:obo:{prefix}")
        except Exception as e:
            logging.info(f"failed to load {prefix}: {e}")
            adapters[prefix] = None
            obsoletes[prefix] = []
            return None
        obsoletes[prefix] = list(adapters[prefix].obsoletes(include_merged=True))
    return adapters[prefix]


def lookup_mapping_entities(
    mappings: Iterable[Mapping], adapters: Dict[str, OboGraphInterface], **kwargs
) -> og.Graph:
    """
    Look up entities for a list of mappings.

    :param mappings:
    :param adapters:
    :param kwargs:
    :return:
    """
    graph = og.Graph(id="mappings")
    entities = set()
    for m in mappings:
        entities.add(m.subject_id)
        entities.add(m.object_id)
    nmap = {}
    for entity in entities:
        if entity in nmap:
            continue
        prefix = _prefix(entity)
        adapter = lookup_mapping_adapter(entity, adapters)
        if not isinstance(adapter, OboGraphInterface):
            raise ValueError(f"no adapter for {prefix}")
        n = adapter.node(entity, **kwargs)
        nmap[entity] = n
        for rel in adapter.relationships(entity):
            graph.edges.append(og.Edge(subject=rel[0], predicate=rel[1], object=rel[2]))
        graph.nodes.append(n)
    return graph


def validate_mappings(
    mappings: List[Mapping],
    adapters: Optional[Dict[str, BasicOntologyInterface]] = None,
    autolabel: bool = True,
    xref_is_bijective=True,
    inject_comments=True,
) -> Iterator[Tuple[List[str], Mapping]]:
    """
    Validate a list of mappings.

    >>> from oaklib import get_adapter
    >>> from oaklib.utilities.mapping.mapping_validation import validate_mappings
    >>> adapter = get_adapter("sqlite:obo:xao")
    >>> mappings = list(adapter.sssom_mappings())
    >>> for errors, m in validate_mappings(mappings):
    ...     print(errors, m.subject_id, m.object_id)
    <BLANKLINE>
    ...

    The current validation checks include:

    - cardinality checks
    - mappings to obsoletes

    For cardinality checks, the assumption is that if the mapping is not 1:1, AND either the predicate
    is skos:exactMatch OR oio:hasDbXref, then the mapping is invalid. The oio predicate can be
    omitted from this check by setting xref_is_bijective to False.

    Note that for autolabeling and obsoletion checks, it may be necessary to look up
    CURIEs in a variety of different ontolgies. The default assumption here is that there
    exists a resource ``sqlite:obo:{prefix}`` for each prefix in the CURIEs. This may not always
    hold (the xref may not always be to an ontology in the registry), so if no such adapter is found,
    the autolabeling and obsoletion checks will be skipped for that CURIE.

    The caller has the option of providing more fine-grained control over the adapters used by
    passing an ``adapters`` dict which maps prefixes to ontology adapters.

    The ``adapters`` dict has a special value "*" which will match any prefix -- this can be used in the case
    of application ontologies that merge multiple ontologies together.

    :param mappings: mappings to validate
    :param adapters: a mapping from prefix to ontology adapter. If not provided, will be created
    :param autolabel: if True, will attempt to autolabel the yielded mappings
    :param xref_is_bijective: if True (default), then mappings to oio:hasDbXref are considered bijective
    :param inject_comments: if True (default), then validation comments will be injected into the mapping
    :return: yields all (copy of) mappings that do not validate together with list of problems
    """
    if adapters is None:
        adapters = {}

    mappings = deepcopy(mappings)
    assign_mapping_cardinalities(mappings)

    for m in mappings:
        subject_prefix = _prefix(m.subject_id)
        object_prefix = _prefix(m.object_id)
        if subject_prefix == "_" or object_prefix == "_":
            continue
        subject_adapter = lookup_mapping_adapter(m.subject_id, adapters)
        object_adapter = lookup_mapping_adapter(m.object_id, adapters)
        comments = []
        subject_is_obsolete = m.subject_id in _obsoletes(subject_prefix, adapters)
        object_is_obsolete = m.object_id in _obsoletes(object_prefix, adapters)
        if subject_is_obsolete and not object_is_obsolete:
            comments.append("subject is obsolete")
        if object_is_obsolete and not subject_is_obsolete:
            comments.append("object is obsolete")
        if subject_is_obsolete and object_is_obsolete:
            logging.info(
                f"both {m.subject_id} and {m.object_id} are obsolete, but this is not a violation"
            )
        if m.mapping_cardinality != MappingCardinalityEnum(MappingCardinalityEnum["1:1"]):
            if m.predicate_id == SKOS_EXACT_MATCH or (
                m.predicate_id == HAS_DBXREF and xref_is_bijective
            ):
                comments.append(f"cardinality is {m.mapping_cardinality}")
        if object_adapter:
            object_label = object_adapter.label(m.object_id)
            if not object_label:
                comments.append("no label for object")
            elif m.object_label and m.object_label != object_label:
                comments.append("object label mismatch")
        if comments:
            if autolabel:
                if not m.subject_label and subject_adapter:
                    m.subject_label = subject_adapter.label(m.subject_id)
                if not m.object_label and object_adapter:
                    m.object_label = object_adapter.label(m.object_id)
            if inject_comments:
                m.comment = " | ".join(comments)
            yield comments, m
