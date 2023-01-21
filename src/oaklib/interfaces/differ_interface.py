import logging
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, Tuple

import kgcl_schema.datamodel.kgcl as kgcl
from kgcl_schema.datamodel.kgcl import Change, ClassCreation, NodeCreation, NodeDeletion

from oaklib.datamodels.vocabulary import (
    DEPRECATED_PREDICATE,
    HAS_OBSOLESCENCE_REASON,
    OWL_CLASS,
    TERM_REPLACED_BY,
    TERMS_MERGED,
)
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.kgcl_utilities import generate_change_id

TERM_LIST_DIFF = Tuple[CURIE, CURIE]
RESIDUAL_KEY = "__RESIDUAL__"


@dataclass
class DiffConfiguration:
    """Configuration for the differ."""

    simple: bool = False
    group_by_property: PRED_CURIE = None


def _gen_id():
    return generate_change_id()


class DifferInterface(BasicOntologyInterface, ABC):
    """
    Generates Change objects between one ontology and another.

    This uses the KGCL datamodel, see :ref:`kgcl-datamodel` for more information.
    """

    def diff(
        self, other_ontology: BasicOntologyInterface, configuration: DiffConfiguration = None
    ) -> Iterator[Change]:
        """
        Diffs two ontologies.

        The changes that are yielded describe transitions from the current ontology to the other ontology.

        Note that this is not guaranteed to diff every axiom in both ontologies. Only a subset of KGCL change
        types are supported:

        - NodeCreation
        - NodeDeletion
        - NodeMove
        - NodeRename
        - PredicateChange

        :param other_ontology:
        :param configuration:
        :return: KGCL change object
        """
        if configuration is None:
            configuration = DiffConfiguration()
        other_ontology_entities = set(list(other_ontology.entities(filter_obsoletes=False)))
        self_entities = set(list(self.entities(filter_obsoletes=False)))
        logging.info(f"Comparing {len(self_entities)} terms in this ontology")
        for e1 in self_entities:
            # e1_types = self.owl_type(e1)
            # is_class = OWL_CLASS in e1_types
            logging.debug(f"Comparing e1 {e1}")
            if e1 not in other_ontology_entities:
                yield NodeDeletion(id=_gen_id(), about_node=e1)
                continue
            if configuration.simple:
                continue
            e1_metadata = self.entity_metadata_map(e1)
            e2_metadata = other_ontology.entity_metadata_map(e1)
            metadata_props = set(e1_metadata.keys()).union(e2_metadata.keys())
            if DEPRECATED_PREDICATE in metadata_props:
                e1_dep = e1_metadata.get(DEPRECATED_PREDICATE, [False])[0]
                e2_dep = e2_metadata.get(DEPRECATED_PREDICATE, [False])[0]
                if e1_dep != e2_dep:
                    # TODO: bundle associated changes
                    if e1_dep and not e2_dep:
                        yield kgcl.NodeUnobsoletion(id=_gen_id(), about_node=e1)
                    elif not e1_dep and e2_dep:
                        if TERM_REPLACED_BY in e2_metadata:
                            if TERMS_MERGED in e2_metadata.get(HAS_OBSOLESCENCE_REASON, []):
                                yield kgcl.NodeDirectMerge(
                                    id=_gen_id(),
                                    about_node=e1,
                                    has_direct_replacement=e2_metadata[TERM_REPLACED_BY][0],
                                )
                            else:
                                yield kgcl.NodeObsoletionWithDirectReplacement(
                                    id=_gen_id(),
                                    about_node=e1,
                                    has_direct_replacement=e2_metadata[TERM_REPLACED_BY][0],
                                )
                        else:
                            yield kgcl.NodeObsoletion(id=_gen_id(), about_node=e1)
            differs = self.different_from(e1, other_ontology)
            if differs is not None and not differs:
                continue
            e1_arels = set(self.alias_relationships(e1, exclude_labels=True))
            e2_arels = set(other_ontology.alias_relationships(e1, exclude_labels=True))
            for arel in e1_arels.difference(e2_arels):
                pred, alias = arel
                switches = {r[0] for r in e2_arels if r[1] == alias}
                if len(switches) == 1:
                    e2_arels = set([x for x in e2_arels if x[1] != alias])
                    # TODO: KGCL model needs to include predicates
                    yield kgcl.SynonymPredicateChange(id=_gen_id(), about_node=e1, old_value=alias)
                else:
                    yield kgcl.RemoveSynonym(id=_gen_id(), about_node=e1, old_value=alias)
            for arel in e2_arels.difference(e1_arels):
                pred, alias = arel
                yield kgcl.NewSynonym(id=_gen_id(), about_node=e1, new_value=alias)
            e1_label = self.label(e1)
            e2_label = other_ontology.label(e1)
            if e1_label != e2_label:
                yield kgcl.NodeRename(
                    id=_gen_id(), about_node=e1, old_value=e1_label, new_value=e2_label
                )
            e1_rels = set(self.outgoing_relationships(e1))
            e2_rels = set(other_ontology.outgoing_relationships(e1))
            for rel in e1_rels.difference(e2_rels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                switches = list({r[0] for r in e2_rels if r[1] == filler})
                if len(switches) == 1:
                    e2_rels = set([x for x in e2_rels if x[1] != filler])
                    if pred != switches[0]:
                        yield kgcl.PredicateChange(
                            id=_gen_id(), about_edge=edge, old_value=pred, new_value=switches[0]
                        )
                else:
                    yield kgcl.NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
            for rel in e2_rels.difference(e1_rels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                yield kgcl.NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
        logging.info(f"Comparing {len(other_ontology_entities)} terms in other ontology")
        for e2 in other_ontology_entities:
            logging.debug(f"Comparing e2 {e2}")
            if e2 not in self_entities:
                e2_types = other_ontology.owl_type(e2)
                is_class = OWL_CLASS in e2_types
                if is_class:
                    yield ClassCreation(id=_gen_id(), about_node=e2)
                else:
                    yield NodeCreation(id=_gen_id(), about_node=e2)
                continue

    def diff_summary(
        self, other_ontology: BasicOntologyInterface, configuration: DiffConfiguration = None
    ) -> Dict[str, Any]:
        """
        Provides high level summary of differences.

        The result is a two-level dictionary

        - the first level is the grouping key
        - the second level is the type of change

        The value of the second level is a count of the number of changes of that type.



        :param other_ontology:
        :param configuration:
        :return:
        """
        summary = {}
        for change in self.diff(other_ontology, configuration):
            if isinstance(change, kgcl.NodeChange):
                about = change.about_node
            elif isinstance(change, kgcl.EdgeChange):
                about = change.about_edge.subject
            else:
                about = None
            partition = RESIDUAL_KEY
            if about and configuration.group_by_property:
                md = self.entity_metadata_map(about)
                if not md or configuration.group_by_property not in md:
                    md = other_ontology.entity_metadata_map(about)
                if configuration.group_by_property in md:
                    v = md[configuration.group_by_property]
                    if len(v) == 1:
                        partition = v[0]
                    else:
                        logging.warning(
                            f"Multiple values for {configuration.group_by_property} = {v}"
                        )
            if partition not in summary:
                summary[partition] = {}
            typ = type(change).__name__
            if typ not in summary[partition]:
                summary[partition][typ] = 0
            summary[partition][typ] += 1
        return dict(summary)

    def different_from(
        self, entity: CURIE, other_ontology: BasicOntologyInterface
    ) -> Optional[bool]:
        return None

    def compare_ontology_term_lists(
        self, other_ontology: BasicOntologyInterface
    ) -> Iterator[Change]:
        """
        Provides high level summary of differences

        :param other_ontology:
        :return:
        """
        this_terms = set(self.entities())
        other_terms = set(other_ontology.entities())
        for t in this_terms.difference(other_terms):
            yield NodeDeletion(
                id="x",
                # type='NodeDeletion',
                about_node=t,
            )
        for t in other_terms.difference(this_terms):
            yield NodeCreation(id="x", about_node=t)

    def compare_term_in_two_ontologies(
        self, other_ontology: BasicOntologyInterface, curie: CURIE, other_curie: CURIE = None
    ) -> Any:
        raise NotImplementedError
