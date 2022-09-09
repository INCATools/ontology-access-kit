import logging
import math
import statistics
from abc import ABC
from collections import defaultdict
from typing import Iterable, Iterator, List, Tuple

import networkx as nx

from oaklib.datamodels.similarity import (
    BestMatch,
    TermInfo,
    TermPairwiseSimilarity,
    TermSetPairwiseSimilarity,
)
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.obograph_utils import as_digraph
from oaklib.utilities.semsim.similarity_utils import setwise_jaccard_similarity


class SemanticSimilarityInterface(BasicOntologyInterface, ABC):
    """
    An interface for calculating similarity measures between pairs of terms or
    collections of terms
    """

    def most_recent_common_ancestors(
        self, subject: CURIE, object: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        """
        Most recent common ancestors (MRCAs) for a pair of entities

        The MRCAs are the set of Common Ancestors (CAs) that are not themselves proper
        ancestors of another CA

        :param subject:
        :param object:
        :param predicates:
        :return:
        """
        if isinstance(self, OboGraphInterface):
            s_ancs = set(self.ancestors([subject], predicates))
            o_ancs = set(self.ancestors([object], predicates))
            common = s_ancs.intersection(o_ancs)
            ancs_of_common = []
            for ca in common:
                for caa in self.ancestors(ca, predicates):
                    if caa != ca:
                        ancs_of_common.append(caa)
            for a in common:
                if a not in ancs_of_common:
                    yield a
        else:
            raise NotImplementedError

    def multiset_most_recent_common_ancestors(
        self, subjects: List[CURIE], predicates: List[PRED_CURIE] = None, asymmetric=True
    ) -> Iterable[Tuple[CURIE, CURIE, CURIE]]:
        """
        All pairwise common ancestors for all pairs in a set of terms

        :param subjects:
        :param predicates:
        :param asymmetric:
        :return:
        """
        if isinstance(self, OboGraphInterface):
            og = self.ancestor_graph(subjects, predicates)
            dg = as_digraph(og)
            pairs = []
            subjects = [s for s in subjects if s in dg]
            for s in subjects:
                for o in subjects:
                    if asymmetric and s >= o:
                        continue
                    pairs.append((s, o))
            for (s, o), lca in nx.all_pairs_lowest_common_ancestor(dg, pairs=pairs):
                yield s, o, lca
        else:
            raise NotImplementedError

    def common_ancestors(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
    ) -> Iterable[CURIE]:
        """
        Common ancestors of a subject-object pair

        :param subject:
        :param object:
        :param predicates:
        :param subject_ancestors: optional pre-generated ancestor list
        :param object_ancestors: optional pre-generated ancestor list
        :return:
        """
        if subject_ancestors is not None and object_ancestors is not None:
            for a in set(subject_ancestors).intersection(set(object_ancestors)):
                yield a
        elif isinstance(self, OboGraphInterface):
            s_ancs = set(self.ancestors(subject, predicates))
            o_ancs = set(self.ancestors(object, predicates))
            for a in s_ancs.intersection(o_ancs):
                yield a
        else:
            raise NotImplementedError

    def get_information_content(
        self, curie: CURIE, background: CURIE = None, predicates: List[PRED_CURIE] = None
    ) -> float:
        """
        Returns the information content of a term

        IC(t) = -log2(Pr(t))

        :param curie:
        :param background:
        :param predicates:
        :return:
        """
        raise NotImplementedError

    def pairwise_similarity(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
    ) -> TermPairwiseSimilarity:
        """
        Pairwise similarity between a pair of ontology terms

        :param subject:
        :param object:
        :param predicates:
        :param subject_ancestors: optional pre-generated ancestor list
        :param object_ancestors: optional pre-generated ancestor list
        :return:
        """
        logging.info(f"Calculating pairwise similarity for {subject} x {object} over {predicates}")
        cas = list(
            self.common_ancestors(
                subject,
                object,
                predicates,
                subject_ancestors=subject_ancestors,
                object_ancestors=object_ancestors,
            )
        )
        ics = {a: self.get_information_content(a, predicates) for a in cas}
        if len(ics) > 0:
            max_ic = max(ics.values())
            best_mrcas = [a for a in cas if ics[a] == max_ic]
            anc = best_mrcas[0]
        else:
            max_ic = 0
            anc = None
        sim = TermPairwiseSimilarity(
            subject_id=subject,
            object_id=object,
            ancestor_id=anc,
            ancestor_information_content=max_ic,
        )
        sim.ancestor_information_content = max_ic
        if subject_ancestors is None and isinstance(self, OboGraphInterface):
            subject_ancestors = self.ancestors(subject, predicates=predicates)
        if object_ancestors is None and isinstance(self, OboGraphInterface):
            object_ancestors = self.ancestors(object, predicates=predicates)
        if subject_ancestors is not None and object_ancestors is not None:
            sim.jaccard_similarity = setwise_jaccard_similarity(subject_ancestors, object_ancestors)
        if sim.ancestor_information_content and sim.jaccard_similarity:
            sim.phenodigm_score = math.sqrt(
                sim.jaccard_similarity * sim.ancestor_information_content
            )
        return sim

    def termset_pairwise_similarity(
        self,
        subjects: List[CURIE],
        objects: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        labels=False,
    ) -> TermSetPairwiseSimilarity:
        curies = set(subjects + objects)
        pairs = list(self.all_by_all_pairwise_similarity(subjects, objects, predicates=predicates))
        bm_subject_score = defaultdict(float)
        bm_subject = {}
        bm_subject_sim = {}
        bm_object_score = defaultdict(float)
        bm_object = {}
        bm_object_sim = {}
        sim = TermSetPairwiseSimilarity()
        for x in subjects:
            sim.subject_termset[x] = TermInfo(x)
        for x in objects:
            sim.object_termset[x] = TermInfo(x)
        for pair in pairs:
            st = pair.subject_id
            ot = pair.object_id
            if pair.ancestor_information_content > bm_subject_score[st]:
                bm_subject_score[st] = pair.ancestor_information_content
                bm_subject[st] = ot
                bm_subject_sim[st] = pair
                curies.add(ot)
                curies.add(pair.ancestor_id)
            if pair.ancestor_information_content > bm_object_score[ot]:
                bm_object_score[ot] = pair.ancestor_information_content
                bm_object[ot] = st
                bm_object_sim[ot] = pair
                curies.add(ot)
                curies.add(pair.ancestor_id)
        scores = []
        for s, t in bm_subject.items():
            score = bm_subject_score[s]
            sim.subject_best_matches[s] = BestMatch(
                s, match_target=t, score=score, similarity=bm_subject_sim[s]
            )
            scores.append(score)
        for s, t in bm_object.items():
            score = bm_object_score[s]
            sim.object_best_matches[s] = BestMatch(
                s, match_target=t, score=score, similarity=bm_object_sim[s]
            )
            scores.append(score)
        if not scores:
            scores = [0.0]
        sim.average_score = statistics.mean(scores)
        sim.best_score = max(scores)
        if labels:
            label_ix = {k: v for k, v in self.labels(curies)}
            for x in list(sim.subject_termset.values()) + list(sim.object_termset.values()):
                x.label = label_ix.get(x.id, None)
            for x in list(sim.subject_best_matches.values()) + list(
                sim.object_best_matches.values()
            ):
                x.match_target_label = label_ix.get(x.match_target, None)
                x.match_source_label = label_ix.get(x.match_source, None)
                x.similarity.ancestor_label = label_ix.get(x.similarity.ancestor_id, None)

        return sim

    def all_by_all_pairwise_similarity(
        self,
        subjects: Iterable[CURIE],
        objects: Iterable[CURIE],
        predicates: List[PRED_CURIE] = None,
    ) -> Iterator[TermPairwiseSimilarity]:
        """
        Compute similarity for all combinations of terms in subsets vs all terms in objects

        :param subjects:
        :param objects:
        :param predicates:
        :return:
        """
        objects = list(objects)
        for s in subjects:
            for o in objects:
                yield self.pairwise_similarity(s, o, predicates=predicates)
