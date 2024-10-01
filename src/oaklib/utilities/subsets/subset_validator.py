from typing import List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE


class SubsetValidationConfig(BaseModel):
    subset_name: Optional[str] = None
    subset_description: Optional[str] = None
    subset_terms: Optional[list[CURIE]] = None
    predicates: Optional[list[PRED_CURIE]] = None
    exclude_terms: Optional[List[CURIE]] = None
    ic_score_adapter_name: Optional[str] = None


class TermPair(BaseModel):
    left_term: CURIE
    right_term: CURIE
    left_term_label: Optional[str] = None
    right_term_label: Optional[str] = None


class SubsetValidationResultComponent(BaseModel):
    min_ic_dist: float
    min_ic_dist_term_pairs: Optional[List[TermPair]] = None
    min_j_dist: float
    min_j_dist_term_pairs: Optional[List[TermPair]] = None
    avg_min_ic_dist_by_term: float
    avg_min_j_by_term: float


class SubsetValidationResult(BaseModel):
    subset_name: Optional[str] = None
    configuration: Optional[SubsetValidationConfig] = None
    combined_score: Optional[float] = None
    terms_used: Optional[list[CURIE]] = None
    ignored_terms: Optional[list[CURIE]] = None
    overall: Optional[SubsetValidationResultComponent] = None
    sibling_pairs: Optional[SubsetValidationResultComponent] = None
    ancestor_pairs: Optional[SubsetValidationResultComponent] = None
    leaf_pairs: Optional[SubsetValidationResultComponent] = None


def set_labels(adapter: BasicOntologyInterface, term_pair: TermPair):
    term_pair.left_term_label = adapter.label(term_pair.left_term)
    term_pair.right_term_label = adapter.label(term_pair.right_term)


def validate_subset(
    adapter: SemanticSimilarityInterface, configuration: Optional[SubsetValidationConfig] = None
) -> SubsetValidationResult:
    """
    Validate a subset of terms and predicates

    :param adapter:
    :param configuration:
    :return:
    """
    graph_adapter = adapter
    if not isinstance(graph_adapter, OboGraphInterface):
        raise ValueError("Adapter must implement OboGraphInterface")
    if configuration is None:
        configuration = SubsetValidationConfig()
    if not configuration.subset_terms:
        if not configuration.subset_name:
            raise ValueError("No subset name or terms provided")
        configuration.subset_terms = list(adapter.subset_members(configuration.subset_name))
    if not configuration.predicates:
        configuration.predicates = [IS_A, PART_OF]
    if configuration.ic_score_adapter_name:
        ic_adapter = get_adapter(configuration.ic_score_adapter_name)
        if not isinstance(ic_adapter, SemanticSimilarityInterface):
            raise ValueError(
                "Information content adapter must implement SemanticSimilarityInterface"
            )
        scores = ic_adapter.information_content_scores(predicates=configuration.predicates)
        adapter.set_information_content_scores(scores)
    terms = configuration.subset_terms
    pairs = []
    t2score = {t: adapter.get_information_content(t) for t in terms}
    t2score = {t: s for t, s in t2score.items() if s is not None}
    max_score = max(t2score.values())
    ic_factor = 1.0 / (max_score * 2)
    terms = [t for t in terms if t in t2score and t2score[t] > 0.0]
    if not terms:
        raise ValueError("No terms found with information content")
    result = SubsetValidationResult(
        subset_name=configuration.subset_name,
        configuration=configuration,
        terms_used=terms,
        ignored_terms=[t for t in configuration.subset_terms if t not in terms],
    )
    if len(terms) < 2:
        result.combined_score = 0.0
        return result
    non_leaf_terms = set()
    for i, term_i in enumerate(terms):
        term_i_ancs = set(
            graph_adapter.ancestors(term_i, configuration.predicates, reflexive=False)
        )
        non_leaf_terms.update(term_i_ancs)
        for j, term_j in enumerate(terms):
            if i >= j:
                continue
            term_j_ancs = set(graph_adapter.ancestors(term_j, configuration.predicates))
            sim = adapter.pairwise_similarity(term_i, term_j, configuration.predicates)
            # If the term pair are in separate branches or subgraphs, ignore them;
            # this is either if the universal root term (which has zero information content) is the ancestor,
            # of if the ancestor is in the set of excluded terms (e.g. upper ontology groupings)
            if sim.jaccard_similarity == 0.0:
                continue
            anc_ic = sim.ancestor_information_content
            if np.isclose(anc_ic, 0.0):
                continue
            if configuration.exclude_terms and sim.ancestor_id in configuration.exclude_terms:
                continue
            left_ic_diff = abs(sim.subject_information_content - anc_ic)
            right_ic_diff = abs(sim.object_information_content - anc_ic)
            ic_diff = left_ic_diff + right_ic_diff

            if term_i in term_j_ancs:
                rel = 1
            elif term_j in term_i_ancs:
                rel = -1
            else:
                rel = 0
            pair = {
                "term_i": term_i,
                "term_j": term_j,
                "rel": rel,
                "j": 1 - sim.jaccard_similarity,
                "ic_distance": ic_diff * ic_factor,
            }
            pairs.append(pair)
            from copy import copy

            rev_pair = copy(pair)
            rev_pair["term_i"] = term_j
            rev_pair["term_j"] = term_i
            pairs.append(rev_pair)

    leaf_terms = {t for t in terms if t not in non_leaf_terms}
    df = pd.DataFrame(pairs)
    df_sibs = df[df["rel"] == 0]
    df_ancs = df[df["rel"] != 0]
    df_all = df
    df_leafs = df[df["term_i"].isin(leaf_terms) & df["term_j"].isin(leaf_terms)]

    overall_score = 0.0
    n = 0
    for cn, df in [
        ("overall", df_all),
        ("sibling_pairs", df_sibs),
        ("ancestor_pairs", df_ancs),
        ("leaf_pairs", df_leafs),
    ]:
        min_ic_dist = df["ic_distance"].min()
        min_j = df["j"].min()
        # Get witnesses for min_ic_dist
        min_ic_dist_rows = df[np.isclose(df["ic_distance"], min_ic_dist)]
        min_ic_dist_pairs = []
        for _i, row in min_ic_dist_rows.iterrows():
            min_ic_dist_pair = TermPair(left_term=row["term_i"], right_term=row["term_j"])
            set_labels(adapter, min_ic_dist_pair)
            min_ic_dist_pairs.append(min_ic_dist_pair)

        # Get witnesses for min_j
        # these are floats so we don't expect exact - get approximate
        min_j_rows = df[np.isclose(df["j"], min_j)]
        # min_j_rows = df[df['j'] == min_j]
        min_j_pairs = []
        for _i, row in min_j_rows.iterrows():
            min_j_pair = TermPair(left_term=row["term_i"], right_term=row["term_j"])
            set_labels(adapter, min_j_pair)
            min_j_pairs.append(min_j_pair)

        for metric in ["ic_distance", "j"]:
            min_agg_metric = f"min_{metric}"
            df[min_agg_metric] = df[[metric]].min(axis=1)
        component = SubsetValidationResultComponent(
            min_ic_dist=min_ic_dist,
            min_ic_dist_term_pairs=min_ic_dist_pairs,
            min_j_dist=min_j,
            min_j_dist_term_pairs=min_j_pairs,
            avg_min_ic_dist_by_term=df["min_ic_distance"].mean(),
            avg_min_j_by_term=df["min_j"].mean(),
        )
        if not np.isnan(min_ic_dist):
            overall_score += component.min_ic_dist + component.avg_min_ic_dist_by_term
            n += 2
        setattr(result, cn, component)
    result.combined_score = overall_score / n
    return result
