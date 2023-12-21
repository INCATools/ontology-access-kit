import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Collection, Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib import BasicOntologyInterface
from oaklib.datamodels.taxon_constraints import SubjectTerm, Taxon, TaxonConstraint
from oaklib.datamodels.vocabulary import (
    IN_TAXON,
    IS_A,
    NEVER_IN_TAXON,
    ONLY_IN_TAXON,
    PRESENT_IN_TAXON,
)
from oaklib.interfaces.obograph_interface import GraphTraversalMethod, OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, TAXON_CURIE

TAXON_PREDICATES = [NEVER_IN_TAXON, ONLY_IN_TAXON, IN_TAXON, PRESENT_IN_TAXON]
NORMALIZE_MAP = {ONLY_IN_TAXON: IN_TAXON}

TERM_TAXON_CONSTRAINTS = Tuple[List[TAXON_CURIE], List[TAXON_CURIE], List[TAXON_CURIE]]


@dataclass
class ConstraintCache:
    term_to_constraints: Dict[CURIE, List[Tuple[PRED_CURIE, TAXON_CURIE]]] = None
    complete: bool = False


def _tc(tc: TaxonConstraint):
    return TaxonConstraint(taxon=tc.taxon, subject=tc.subject, via_terms=tc.via_terms)


def taxon_ids_from_taxon_constraints(tcs: List[TaxonConstraint]) -> List[TAXON_CURIE]:
    return list(set([tc.taxon.id for tc in tcs]))


class TaxonConstraintInterface(BasicOntologyInterface):
    """
    Computes taxon constraints.
    """

    cache: ConstraintCache = None
    subject_graph_traversal_method: Optional[GraphTraversalMethod] = None

    def get_terms_with_taxon_constraints(
        self,
        curies: Iterable[CURIE],
        predicates: List[PRED_CURIE] = None,
        include_redundant=False,
        add_labels=True,
        direct=False,
    ) -> Iterator[SubjectTerm]:
        """
        Generate :ref:`TaxonConstraint`s for a given subject term ID

        This implements taxon constraints using a graph walking strategy rather than a reasoning strategy

        :param curies: subject identifiers
        :param predicates: predicates to traverse from subject term to term with constraint
        :param include_redundant:
        :param add_labels:
        :param direct:
        :return:
        """
        for curie in curies:
            yield self.get_term_with_taxon_constraints(
                curie,
                predicates=predicates,
                include_redundant=include_redundant,
                add_labels=add_labels,
                direct=direct,
            )

    def get_term_with_taxon_constraints(
        self,
        curie: CURIE,
        predicates: List[PRED_CURIE] = None,
        include_redundant=False,
        include_never_in_even_if_redundant_with_only_in=False,
        add_labels=True,
        direct=False,
    ) -> SubjectTerm:
        """
        Generate :ref:`TaxonConstraint`s for a given subject term ID

        This implements taxon constraints using a graph walking strategy rather than a reasoning strategy

         An ontology interface for making label lookups.
        :param curie: subject identifier
        :param predicates: predicates to traverse from subject term to term with constraint
        :param include_redundant:
        :param add_labels:
        :param direct:
        :return:
        """
        label = self.label(curie)
        # if label is None:
        #    raise ValueError(f"Unknown term: {curie}")
        st = SubjectTerm(curie, label=label)
        # find all taxon constraints, including redundant
        traversal_method = self.subject_graph_traversal_method or GraphTraversalMethod.HOP
        logging.info(f"Inferring taxon constraints for {curie} via {traversal_method}")
        subject_ancs = (
            [curie]
            if direct
            else list(
                self.ancestors(
                    curie,
                    predicates,
                    method=traversal_method,
                )
            )
        )
        subject_ancs = list(set(subject_ancs))
        logging.info(f"Ancestors of {curie}: {len(subject_ancs)} via {traversal_method}")
        for anc in subject_ancs:
            logging.debug(f"Checking ancestor {anc} of {curie} over predicates: {predicates}")
            if anc.startswith("NCBITaxon:"):
                continue
            for predicate, taxon in self.get_direct_taxon_constraints(anc):
                logging.debug(f"Direct constraint:{anc} {predicate} to {taxon}")
                tc = TaxonConstraint(
                    taxon=Taxon(taxon),
                    subject=anc,
                    predicate=predicate,
                    redundant=False,  # redundancy will be checked later
                    via_terms=[SubjectTerm(anc)],
                    asserted=anc == curie,
                )
                if predicate == NEVER_IN_TAXON:
                    st.never_in.append(tc)
                elif predicate == IN_TAXON:
                    st.only_in.append(tc)
                elif predicate == PRESENT_IN_TAXON:
                    pass
                    # if anc == curie:
                    #    st.present_in.append(tc)
                else:
                    raise ValueError(f"Unexpected taxon pred: {predicate}")
        for tc in self.calculate_present_in_taxon_constraints(curie, predicates):
            st.present_in.append(tc)
        if not direct:
            self._compute_redundancies(st, predicates)
        logging.info("Filling missing info")
        self._fill_missing(st)
        logging.info("Injecting labels")
        if add_labels:
            self.inject_labels(st)
        logging.info("Getting description")
        st.description = self.get_taxon_constraints_description(st)
        if not include_redundant:
            st.only_in = [tc for tc in st.only_in if not tc.redundant]
            st.never_in = [
                tc
                for tc in st.never_in
                if not tc.redundant
                and (
                    not tc.redundant_with_only_in or include_never_in_even_if_redundant_with_only_in
                )
            ]
            st.present_in = [tc for tc in st.present_in if not tc.redundant]
        return st

    def calculate_present_in_taxon_constraints(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterator[TaxonConstraint]:
        """
        Get all present_in taxon constraints for a given term

        :param curie:
        :return:
        """
        if not isinstance(self, OboGraphInterface):
            raise ValueError("This method requires an OboGraphInterface")
        descendants = list(self.descendants(curie, predicates))
        for s, p, o in self.relationships(descendants, [PRESENT_IN_TAXON]):
            yield TaxonConstraint(
                taxon=Taxon(id=o),
                subject=curie,
                predicate=p,
                via_terms=[SubjectTerm(s)],
                asserted=True,
            )

    def _compute_redundancies(self, st: SubjectTerm, predicates: List[PRED_CURIE] = None):
        logging.info(f"Checking {len(st.only_in)} only-in constraints")
        for tc in st.only_in:
            # calculate redundancy for only-ins
            present_in_taxon_ancs = list(self.ancestors(tc.taxon.id, [IS_A]))
            tc_subject_ancs = list(self.ancestors(tc.subject, predicates))
            for other_tc in st.only_in:
                # check if other TCs are redundant with this one:
                # i.e. the other TC is to a more general taxon
                # e.g. tc=only_in(Mammals), other_tc=only_in(Animals)
                if other_tc.taxon.id in present_in_taxon_ancs:
                    reflexive = tc.taxon.id == other_tc.taxon.id
                    if not reflexive:
                        other_tc.redundant = True
                        other_tc.redundant_with.append(_tc(tc))
                    else:
                        if other_tc.subject in tc_subject_ancs and other_tc.subject != tc.subject:
                            tc.redundant = True
                            tc.comments.append(
                                f"Redundant with constraint on same taxon from more general term {other_tc.subject}"
                            )
                else:
                    if tc.taxon.id not in list(self.ancestors(other_tc.taxon.id, [IS_A])):
                        st.unsatisfiable = True
                        tc.comments.append(
                            (
                                f"Unsatisfiable taxon constraints: {tc.taxon.id} "
                                "and {other_tc.taxon.id} are disjoint"
                            )
                        )
        logging.info(f"Checking {len(st.present_in)} present-in constraints")
        for tc in st.present_in:
            # calculate redundancy for present-ins
            present_in_taxon_ancs = list(self.ancestors(tc.taxon.id, [IS_A]))
            if st.only_in:
                for only_in in st.only_in:
                    only_in_taxon_ancs = list(self.ancestors(only_in.taxon.id, [IS_A]))
                    if (
                        tc.taxon.id not in only_in_taxon_ancs
                        and only_in.taxon.id not in present_in_taxon_ancs
                    ):
                        st.unsatisfiable = True
                        st.description = f"Unsat, present_in {tc.taxon.id} conflict with only_in"
            if any(never_in.taxon.id in present_in_taxon_ancs for never_in in st.never_in):
                st.unsatisfiable = True
                st.description = f"Unsat, present_in {tc.taxon.id} conflict with never_in"
        # TODO: consider adding default to root
        only_nr = {tc.taxon.id: tc for tc in st.only_in if not tc.redundant}
        logging.info(f"Checking {len(st.never_in)} never-in constraints")
        for tc in st.never_in:
            # calculate redundancy for never-ins, and also consistency with only-ins
            present_in_taxon_ancs = list(self.ancestors(tc.taxon.id, [IS_A]))
            # check if this TC is redundant with any others:
            # i.e. the other TC is to a more general taxon
            # e.g. tc=never_in(Mammals), other_tc=never_in(Animals)
            for other_tc in st.never_in:
                if other_tc.taxon.id != tc.taxon.id and other_tc.taxon.id in present_in_taxon_ancs:
                    tc.redundant = True
                    tc.redundant_with.append(_tc(other_tc))
            # check for cross-redundancy
            tc.redundant_with_only_in = True
            if not st.only_in:
                tc.redundant_with_only_in = False
            else:
                for anc in self.ancestors(tc.taxon.id, [IS_A]):
                    if anc in only_nr.keys():
                        # refines an existing taxon constraint
                        tc.redundant_with_only_in = False
                        # tc.redundant_with.append(_tc(only_nr[anc]))
                        break
                for other_tc in only_nr.values():
                    other_tc_ancs = list(self.ancestors(other_tc.taxon.id, [IS_A]))
                    if tc.taxon.id in other_tc_ancs:
                        st.unsatisfiable = True
                        other_tc.contradicted_by.append(tc)

    def precompute_direct_constraint_cache(self):
        cache = ConstraintCache(term_to_constraints={})
        logging.info("Precomputing direct constraint cache")
        for s, pred, taxon in self.relationships(predicates=TAXON_PREDICATES):
            if s not in cache.term_to_constraints:
                cache.term_to_constraints[s] = []
            if pred in NORMALIZE_MAP:
                pred = NORMALIZE_MAP[pred]
            tpl = (pred, taxon)
            if tpl not in cache.term_to_constraints[s]:
                cache.term_to_constraints[s].append(tpl)
        cache.complete = True
        self.cache = cache
        logging.info(f"Precomputed cache for {len(cache.term_to_constraints)} subjects")

    def get_direct_taxon_constraints(
        self,
        curie: CURIE,
    ) -> Iterator[Tuple[PRED_CURIE, TAXON_CURIE]]:
        """
        Given an ID for a SubjectTerm, yield direct taxon constraints for that term.

        :param curie:
        :return:
        """
        yielded = set()
        if self.cache:
            if curie in self.cache.term_to_constraints:
                for pred, taxon in self.cache.term_to_constraints[curie]:
                    yield pred, taxon
            if self.cache.complete:
                return
        logging.info(f"{curie} not in cache")
        for _s, pred, taxon in self.relationships([curie], predicates=TAXON_PREDICATES):
            if pred in NORMALIZE_MAP:
                pred = NORMALIZE_MAP[pred]
            tpl = (pred, taxon)
            if tpl not in yielded:
                yield pred, taxon
                yielded.add(tpl)
                if self.cache:
                    if curie not in self.cache.term_to_constraints:
                        self.cache.term_to_constraints[curie] = []
                    self.cache.term_to_constraints[curie].append(tpl)

    def filter_nr_only(self, taxa: Collection[TAXON_CURIE]) -> List[TAXON_CURIE]:
        exclude = set()
        for t in taxa:
            for parent in self.ancestors(t, predicates=[IS_A]):
                if parent != t:
                    exclude.add(parent)
        return [t for t in taxa if t not in exclude]

    def filter_nr_never(self, taxa: Collection[TAXON_CURIE]) -> List[TAXON_CURIE]:
        include = set()
        for t in taxa:
            for parent in self.ancestors(t, predicates=[IS_A]):
                if parent in taxa:
                    include.add(t)
        return list(include)

    def _fill_missing(self, st: SubjectTerm):
        # fills in trivial inferable information
        for tc in st.only_in:
            if not tc.subject:
                tc.subject = st.id
            tc.predicate = ONLY_IN_TAXON
        for tc in st.never_in:
            if not tc.subject:
                tc.subject = st.id
            tc.predicate = NEVER_IN_TAXON

    def inject_labels(self, st: SubjectTerm):
        if st.label is None:
            st.label = self.label(st.id)
        for r in st.only_in + st.never_in + st.present_in + st.present_in_ancestor_of:
            if r.taxon.label is None:
                r.taxon.label = self.label(r.taxon.id)
            for t in r.via_terms:
                if t.label is None:
                    t.label = self.label(t.id)

    def eval_candidate_taxon_constraint(
        self,
        candidate_st: SubjectTerm,
        predicates: List[PRED_CURIE] = None,
        add_labels=True,
    ) -> SubjectTerm:
        """
        Evaluate a proposed SubjectTerm plus its taxon constraints against the existing database.

        The input SubjectTerm is not modified - instead a fresh instance is created, annotated
        with redundancy statements.

        :param candidate_st:
        :param predicates: predicates to use in evaluation
        :return: An evaluated TaxonConstraint
        """
        # do not mutate: make a copy and initialize candidate status.
        candidate_st = deepcopy(candidate_st)
        for tc in (
            candidate_st.only_in
            + candidate_st.never_in
            + candidate_st.present_in
            + candidate_st.present_in_ancestor_of
        ):
            tc.candidate = True
        self._fill_missing(candidate_st)
        # fetch current taxon constraints
        curr_st = self.get_term_with_taxon_constraints(candidate_st.id, predicates)
        merged_st = deepcopy(candidate_st)  # why do we copy again?
        # trivial direct redundancy checks
        for tc in merged_st.only_in:
            # check for redundancy of only-ins
            for otc in curr_st.only_in:
                if otc.taxon.id == tc.taxon.id:
                    tc.redundant = True
                    tc.redundant_with.append(_tc(otc))
        for tc in merged_st.never_in:
            # check for redundancy of never-ins
            for otc in curr_st.never_in:
                if otc.taxon.id == tc.taxon.id:
                    tc.redundant = True
                    tc.redundant_with.append(_tc(otc))
        merged_st.only_in.extend(curr_st.only_in)
        merged_st.never_in.extend(curr_st.never_in)
        merged_st.present_in.extend(curr_st.present_in)
        merged_st.present_in_ancestor_of.extend(curr_st.present_in_ancestor_of)
        self._compute_redundancies(merged_st, predicates)
        # def _matches(tc1: TaxonConstraint, tc2: TaxonConstraint):
        #    tc1.taxon.id == tc2.taxon.id and tc1.
        merged_st.only_in = [tc for tc in merged_st.only_in if tc.candidate]
        merged_st.never_in = [tc for tc in merged_st.never_in if tc.candidate]
        if add_labels:
            self.inject_labels(merged_st)
        return merged_st

    def get_taxon_constraints_description(self, st: SubjectTerm) -> str:
        def td(t: CURIE) -> str:
            return f'{t} "{self.label(t)}"'

        def tds(ts: List[CURIE]) -> List[str]:
            return [td(t) for t in ts]

        main_desc = f"Term {td(st.id)}"
        if st.unsatisfiable:
            main_desc += " *INCONSISTENT*"
        only_nr = [tc for tc in st.only_in if not tc.redundant]
        if len(only_nr) == 0:
            only_desc = "has no ONLY_IN constraints"
        else:
            taxa = list(set([tc.taxon.id for tc in only_nr]))
            if len(taxa) == 1:
                only_desc = f"is ONLY found in {td(taxa[0])}"
            else:
                only_desc = f'is ONLY found in ALL OF {" AND ".join(tds(taxa))}'
            if all(tc.asserted for tc in only_nr):
                only_desc += " (IS asserted)"
            else:
                orig_subjects = [tc.subject for tc in only_nr]
                only_desc += f' (NOT asserted: original term = {"; ".join(tds(orig_subjects))})'
        never_nr = [tc for tc in st.never_in if not tc.redundant]
        if len(never_nr) == 0:
            never_desc = "no additional constraints"
        else:
            taxa = list(set([tc.taxon.id for tc in never_nr]))
            never_desc = f'is NEVER found in {" OR ".join(tds(taxa))}'
            if all(tc.asserted for tc in never_nr):
                never_desc += " NOT asserted"
            else:
                never_desc += " IS asserted"
        return f"{main_desc} {only_desc}; {never_desc}"
