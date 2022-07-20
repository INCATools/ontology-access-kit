import logging
from copy import deepcopy
from typing import Collection, Iterator, List, TextIO, Tuple

from oaklib.datamodels.taxon_constraints import SubjectTerm, Taxon, TaxonConstraint
from oaklib.datamodels.vocabulary import (
    IN_TAXON,
    IS_A,
    NEVER_IN_TAXON,
    ONLY_IN_TAXON,
    PRESENT_IN_TAXON,
)
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, TAXON_CURIE

TAXON_PREDICATES = [NEVER_IN_TAXON, ONLY_IN_TAXON, IN_TAXON, PRESENT_IN_TAXON]

TERM_TAXON_CONSTRAINTS = Tuple[List[TAXON_CURIE], List[TAXON_CURIE], List[TAXON_CURIE]]


def _taxon_ids(tcs: List[TaxonConstraint]) -> List[TAXON_CURIE]:
    return list(set([tc.taxon.id for tc in tcs]))


def get_direct_taxon_constraints(
    oi: OboGraphInterface, curie: CURIE
) -> Iterator[Tuple[PRED_CURIE, TAXON_CURIE]]:
    for pred, taxons in oi.outgoing_relationship_map(curie).items():
        if pred in TAXON_PREDICATES:
            if pred == ONLY_IN_TAXON:
                pred = IN_TAXON
            for taxon in taxons:
                yield pred, taxon


def all_term_taxon_constraints(
    oi: OboGraphInterface, curie: CURIE, predicates: List[PRED_CURIE] = None
) -> TERM_TAXON_CONSTRAINTS:
    st = get_term_with_taxon_constraints(oi, curie, predicates)
    return _taxon_ids(st.never_in), _taxon_ids(st.only_in), _taxon_ids(st.present_in)


def filter_nr_only(oi: OboGraphInterface, taxa: Collection[TAXON_CURIE]) -> List[TAXON_CURIE]:
    exclude = set()
    for t in taxa:
        for parent in oi.ancestors(t, predicates=[IS_A]):
            if parent != t:
                exclude.add(parent)
    return [t for t in taxa if t not in exclude]


def filter_nr_never(oi: OboGraphInterface, taxa: Collection[TAXON_CURIE]) -> List[TAXON_CURIE]:
    include = set()
    for t in taxa:
        for parent in oi.ancestors(t, predicates=[IS_A]):
            if parent in taxa:
                include.add(t)
    return list(include)


def _fill_missing(st: SubjectTerm):
    for tc in st.only_in:
        if not tc.subject:
            tc.subject = st.id
        tc.predicate = ONLY_IN_TAXON
    for tc in st.never_in:
        if not tc.subject:
            tc.subject = st.id
        tc.predicate = NEVER_IN_TAXON


def inject_labels(oi: OboGraphInterface, st: SubjectTerm):
    if st.label is None:
        st.label = oi.label(st.id)
    for r in st.only_in + st.never_in + st.present_in + st.present_in_ancestor_of:
        if r.taxon.label is None:
            r.taxon.label = oi.label(r.taxon.id)
        for t in r.via_terms:
            if t.label is None:
                t.label = oi.label(t.id)


def eval_candidate_taxon_constraint(
    oi: OboGraphInterface,
    candidate_st: SubjectTerm,
    predicates: List[PRED_CURIE] = None,
    add_labels=True,
):
    """
    Evaluate a proposed SubjectTerm plus its taxon constraints against the existing database

    :param oi: An ontology interface for making label lookups.
    :param candidate_st:
    :param predicates:
    :return:
    """
    candidate_st = deepcopy(candidate_st)
    _fill_missing(candidate_st)
    curr_st = get_term_with_taxon_constraints(oi, candidate_st.id, predicates)
    # curr_only = [tc.taxon.id for tc in curr_st.only_in]
    curr_never = [tc.taxon.id for tc in curr_st.never_in]
    # candidate_only = [tc.taxon.id for tc in candidate_st.only_in]
    candidate_never = [tc.taxon.id for tc in candidate_st.never_in]
    # msgs = []
    for candidate_tc in candidate_st.only_in:
        if not oi.label(candidate_tc.taxon.id):
            raise ValueError(f"Unknown taxon: {candidate_tc.taxon.id}")
        if not candidate_tc.redundant:
            for other_candidate_tc in candidate_st.only_in:
                if candidate_tc != other_candidate_tc:
                    if candidate_tc.taxon.id in oi.ancestors(
                        other_candidate_tc.taxon.id, predicates
                    ):
                        candidate_tc.redundant = True
                        candidate_tc.redundant_with.append(other_candidate_tc)
                        candidate_tc.comments.append(
                            f"Redundant with other candidate {other_candidate_tc.subject}"
                        )
                        break
        if not candidate_tc.redundant:
            for existing_candidate_tc in curr_st.only_in:
                if not existing_candidate_tc.redundant:
                    if candidate_tc.taxon.id in oi.ancestors(
                        existing_candidate_tc.taxon.id, predicates
                    ):
                        candidate_tc.redundant = True
                        candidate_tc.redundant_with.append(existing_candidate_tc)
                        candidate_tc.comments.append(
                            f"Redundant with pre-existing constraint \
                            {existing_candidate_tc.subject} // {existing_candidate_tc.taxon}"
                        )
                        break
    # check for inconsistencies
    for pos_tc in (
        candidate_st.only_in
        + candidate_st.present_in
        + candidate_st.present_in_ancestor_of
        + curr_st.only_in
        + curr_st.present_in
        + curr_st.present_in_ancestor_of
    ):
        for anc in oi.ancestors(pos_tc.taxon.id, predicates):
            for neg_tc in curr_st.never_in + candidate_st.never_in:
                if anc == neg_tc.taxon.id:
                    pos_tc.contradicted_by.append(neg_tc)
                    candidate_st.unsatisfiable = True
    for pos_tc in candidate_st.only_in + curr_st.only_in:
        ancs = list(oi.ancestors(pos_tc.taxon.id, predicates))
        for tc in candidate_st.present_in_ancestor_of:
            if tc.taxon.id in ancs:
                tc.comments.append(
                    f"Inconsistent with only-in {pos_tc.subject} to {pos_tc.taxon.id}"
                )
                candidate_st.unsatisfiable = True
                tc.contradicted_by(pos_tc)
    for candidate_tc in candidate_st.never_in:
        if not oi.label(candidate_tc.taxon.id):
            raise ValueError(f"Unknown taxon: {candidate_tc.taxon.id}")
        if not candidate_tc.redundant:
            for anc in oi.ancestors(candidate_tc.taxon.id, predicates):
                if anc in curr_never:
                    candidate_tc.redundant = True
                    candidate_tc.comments.append(f"Redundant with existing TC to {anc}")
                    break
                if anc in candidate_never and anc != candidate_tc.taxon.id:
                    candidate_tc.redundant = True
                    candidate_tc.comments.append(f"Redundant with candidate TC to {anc}")
                    break
        if not candidate_tc.redundant_with_only_in and not candidate_st.unsatisfiable:
            candidate_tc.redundant_with_only_in = True  # assume true

            for anc in oi.ancestors(candidate_tc.taxon.id, predicates):
                for only_tc in curr_st.only_in + candidate_st.only_in:
                    # print(f'{candidate_tc.taxon.id} anc: {anc} / {only_tc.taxon.id}')
                    if not only_tc.redundant and anc == only_tc.taxon.id:
                        candidate_tc.redundant_with_only_in = False
    if add_labels:
        inject_labels(oi, candidate_st)
    return candidate_st


def get_term_with_taxon_constraints(
    oi: OboGraphInterface,
    curie: CURIE,
    predicates: List[PRED_CURIE] = None,
    include_redundant=False,
    add_labels=True,
) -> SubjectTerm:
    """
    Generate :ref:`TaxonConstraint`s for a given subject term ID

    This implements taxon constraints using a graph walking strategy rather than a reasoning strategy

     An ontology interface for making label lookups.
    :param curie: subject identifier
    :param predicates: predicates to traverse from subject term to term with constraint
    :param include_redundant:
    :param add_labels:
    :return:
    """
    label = oi.label(curie)
    st = SubjectTerm(curie, label=label)
    if label is None:
        raise ValueError(f"Unknown term: {curie}")
    # find all taxon constraints, including redundant
    logging.info(f"Inferring taxon constraints for {curie}")
    subject_ancs = list(oi.ancestors(curie, predicates))
    for anc in subject_ancs:
        logging.debug(f"Checking ancestor {anc} of {curie} over predicates: {predicates}")
        if anc.startswith("NCBITaxon:"):
            continue
        for predicate, taxon in get_direct_taxon_constraints(oi, anc):
            logging.debug(f"Direct constraint: {predicate} to {taxon}")
            tc = TaxonConstraint(
                taxon=Taxon(taxon),
                subject=anc,
                predicate=predicate,
                redundant=False,
                via_terms=[SubjectTerm(anc)],
                asserted=anc == curie,
            )
            if predicate == NEVER_IN_TAXON:
                st.never_in.append(tc)
            elif predicate == IN_TAXON:
                st.only_in.append(tc)
            elif predicate == PRESENT_IN_TAXON:
                if anc == curie:
                    st.present_in.append(tc)
            else:
                raise ValueError(f"Unexpected taxon pred: {predicate}")
    for tc in st.only_in:
        ancs = oi.ancestors(tc.taxon.id, [IS_A])
        tc_subject_ancs = list(oi.ancestors(tc.subject, predicates))
        for anc in ancs:
            reflexive = anc == tc.taxon.id
            # check if other TCs are redundant with this one:
            # i.e. the other TC is to a more general taxon
            # e.g. tc=only_in(Mammals), other_tc=only_in(Animals)
            for other_tc in st.only_in:
                if other_tc.taxon.id == anc:
                    if not reflexive:
                        other_tc.redundant = True
                        other_tc.redundant_with.append(tc)
                    else:
                        if other_tc.subject in tc_subject_ancs and other_tc.subject != tc.subject:
                            # pass
                            tc.redundant = True
                            tc.comments.append(
                                f"Redundant with constraint on same taxon from more general term {other_tc.subject}"
                            )
                            # tc.redundant_with.append(other_tc)

    # TODO: consider adding default to root
    only_nr = {tc.taxon.id: tc for tc in st.only_in if not tc.redundant}
    for tc in st.never_in:
        ancs = oi.ancestors(tc.taxon.id, [IS_A])
        # check if this TC is redundant with any others:
        # i.e. the other TC is to a more general taxon
        # e.g. tc=never_in(Mammals), other_tc=never_in(Animals)
        for other_tc in st.never_in:
            if other_tc.taxon.id != tc.taxon.id and other_tc.taxon.id in ancs:
                tc.redundant = True
                tc.redundant_with.append(other_tc)
        # check for cross-redundancy
        tc.redundant_with_only_in = True
        if not st.only_in:
            tc.redundant_with_only_in = False
        else:
            for anc in oi.ancestors(tc.taxon.id, [IS_A]):
                if anc in only_nr.keys():
                    # refines an existing taxon constraint
                    tc.redundant_with_only_in = False
                    tc.redundant_with.append(only_nr[anc])
                    break
            for other_tc in only_nr.values():
                if tc.taxon.id in oi.ancestors(other_tc.taxon.id, [IS_A]):
                    st.unsatisfiable = True
                    other_tc.contradicted_by.append(tc)
    _fill_missing(st)
    if add_labels:
        inject_labels(oi, st)
    st.description = get_taxon_constraints_description(oi, st)
    return st


def parse_gain_loss_file(file: TextIO) -> Iterator[SubjectTerm]:
    """
    Parses a file containing gains and losses

    See `<https://github.com/geneontology/go-ontology/issues/16298>`_

    :param file:
    :return:
    """
    for line in file.readlines():
        [term, event_text] = line.strip().split(",")
        st = SubjectTerm(term)
        parts = event_text.split(";")
        if parts[-1] == "":
            parts.pop()
        curr = None
        curr_category = None
        for part in parts:
            if not part:
                logging.error(f"Blank element in line {line}")
                continue
            if "|" in part:
                [category, taxon] = part.split("|")
                curr_category = category
                if category == "Gain":
                    curr = st.only_in
                elif category == ">Loss":
                    curr = st.never_in
                else:
                    raise ValueError(f"Unknown directive: {category}")
            else:
                taxon = part
            if curr is None:
                raise ValueError("Need to specify directive")
            import re

            match = re.search(r"(\S+)\((.*)\)", taxon)
            if match:
                taxon_id, taxon_label = match.group(1, 2)
            else:
                raise ValueError(f"Could not parse taxon {taxon}")
            curr.append(
                TaxonConstraint(taxon=Taxon(taxon_id, label=taxon_label), evolutionary=True)
            )
            if curr_category == "Gain":
                curr = st.present_in
        yield st


def get_taxon_constraints_description(oi: OboGraphInterface, st: SubjectTerm) -> str:
    def td(t: CURIE) -> str:
        return f'{t} "{oi.label(t)}"'

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
