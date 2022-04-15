import logging
from collections import defaultdict
from typing import List, Iterator, Tuple, Collection

from oaklib.datamodels.taxon_constraints import SubjectTerm, TaxonConstraint, Taxon
from oaklib.datamodels.vocabulary import IS_A, NEVER_IN_TAXON, ONLY_IN_TAXON, IN_TAXON
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, TAXON_CURIE

TAXON_PREDICATES = [NEVER_IN_TAXON, ONLY_IN_TAXON, IN_TAXON]

TERM_TAXON_CONSTRAINTS = Tuple[List[TAXON_CURIE], List[TAXON_CURIE]]


def get_direct_taxon_constraints(oi: OboGraphInterface, curie: CURIE) -> Iterator[Tuple[PRED_CURIE, TAXON_CURIE]]:
    for pred, taxons in oi.get_outgoing_relationships_by_curie(curie).items():
        if pred in TAXON_PREDICATES:
            if pred == ONLY_IN_TAXON:
                pred = IN_TAXON
            for taxon in taxons:
                yield pred, taxon

def all_term_taxon_constraints(oi: OboGraphInterface, curie: CURIE, predicates: List[PRED_CURIE] = None) -> TERM_TAXON_CONSTRAINTS:
    never = set()
    only = set()
    for anc in oi.ancestors(curie, predicates):
        if anc.startswith('NCBITaxon:'):
            continue
        for predicate, taxon in get_direct_taxon_constraints(oi, anc):
            if predicate == NEVER_IN_TAXON:
                never.add(taxon)
            elif predicate == IN_TAXON:
                only.add(taxon)
            else:
                raise ValueError(f'Unexpected taxon pred: {predicate}')
    return list(never), list(only)

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

def nr_term_taxon_constraints_simple(oi: OboGraphInterface, curie: CURIE, predicates: List[PRED_CURIE] = None) -> TERM_TAXON_CONSTRAINTS:
    never, only = all_term_taxon_constraints(oi, curie, predicates)
    never, only = filter_nr_never(oi, never), filter_nr_only(oi, only)
    return never, only

def get_term_with_taxon_constraints(oi: OboGraphInterface, curie: CURIE, predicates: List[PRED_CURIE] = None,
                                    include_redundant=False, add_labels=True) -> SubjectTerm:
    st = SubjectTerm(curie, label=oi.get_label_by_curie(curie))
    never = defaultdict(list)
    only = defaultdict(list)
    for anc in oi.ancestors(curie, predicates):
        logging.debug(f'Checking ancestor {anc} of {curie} using {predicates}')
        if anc.startswith('NCBITaxon:'):
            continue
        for predicate, taxon in get_direct_taxon_constraints(oi, anc):
            if predicate == NEVER_IN_TAXON:
                #never.add(taxon)
                never[taxon].append(anc)
            elif predicate == IN_TAXON:
                #only.add(taxon)
                only[taxon].append(anc)
            else:
                raise ValueError(f'Unexpected taxon pred: {predicate}')
    def make_taxon(t: CURIE):
        if add_labels:
            return Taxon(t, oi.get_label_by_curie(t))
        else:
            return Taxon(t)
    never_nr, only_nr = filter_nr_never(oi, never), filter_nr_only(oi, only)
    st.never_in = [TaxonConstraint(redundant=False, taxon=make_taxon(t)) for t in never_nr]
    st.only_in = [TaxonConstraint(redundant=False, taxon=make_taxon(t)) for t in only_nr]
    if include_redundant:
        st.never_in += [TaxonConstraint(redundant=True, taxon=make_taxon(t)) for t in never if t not in never_nr]
        st.only_in += [TaxonConstraint(redundant=True, taxon=make_taxon(t)) for t in only if t not in only_nr]
    for tc in st.only_in:
        tc.via_terms += [SubjectTerm(t) for t in only[tc.taxon.id]]
    for tc in st.never_in:
        tc.via_terms += [SubjectTerm(t) for t in never[tc.taxon.id]]
        for anc in oi.ancestors(curie, predicates):
            if anc in only_nr:
                tc.redundant_with_only_in = True
    return st



