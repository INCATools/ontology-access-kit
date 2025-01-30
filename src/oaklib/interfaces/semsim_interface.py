import logging
import math
import statistics
from abc import ABC
from collections import defaultdict
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib.datamodels.similarity import (
    BestMatch,
    TermInfo,
    TermPairwiseSimilarity,
    TermSetPairwiseSimilarity,
)
from oaklib.datamodels.vocabulary import OWL_THING
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.obograph_utils import as_digraph
from oaklib.utilities.semsim.similarity_utils import (
    load_information_content_map,
    setwise_jaccard_similarity,
)


class SemanticSimilarityInterface(BasicOntologyInterface, ABC):
    """
    An interface for calculating similarity measures between pairs of terms or
    collections of terms
    """

    cached_information_content_map: Dict[CURIE, float] = None
    """Mapping from term to information content"""

    def most_recent_common_ancestors(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        include_owl_thing: bool = True,
    ) -> Iterable[CURIE]:
        """
        Most recent common ancestors (MRCAs) for a pair of entities

        The MRCAs are the set of Common Ancestors (CAs) that are not themselves proper
        ancestors of another CA

        :param subject:
        :param object:
        :param predicates:
        :param include_owl_thing:
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
            n = 0
            for a in common:
                if a not in ancs_of_common:
                    yield a
                    n += 1
            if n == 0:
                yield OWL_THING
        else:
            raise NotImplementedError

    def setwise_most_recent_common_ancestors(
        self,
        subjects: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        include_owl_thing: bool = True,
    ) -> Iterable[CURIE]:
        """
        Most recent common ancestors (MRCAs) for a set of entities

        The MRCAs are the set of Common Ancestors (CAs) that are not themselves proper
        ancestors of another CA

        :param subjects:
        :param predicates:
        :param include_owl_thing:
        :return:
        """
        if not isinstance(self, OboGraphInterface):
            raise NotImplementedError
        ancs = []
        for s in subjects:
            ancs.append(set(self.ancestors([s], predicates)))
        common = set.intersection(*ancs)
        ancs_of_common = []
        for ca in common:
            for caa in self.ancestors(ca, predicates):
                if caa != ca:
                    ancs_of_common.append(caa)
        n = 0
        for a in common:
            if a not in ancs_of_common:
                yield a
                n += 1
        if n == 0 and include_owl_thing:
            yield OWL_THING

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
        graph_adapter = self
        if not isinstance(graph_adapter, OboGraphInterface):
            raise NotImplementedError
        og = graph_adapter.ancestor_graph(subjects, predicates)
        dg = as_digraph(og)
        pairs = []
        subjects = [s for s in subjects if s in dg]
        for s in subjects:
            for o in subjects:
                if asymmetric and s >= o:
                    continue
                pairs.append((s, o))
        for s, o in pairs:
            for mrca in self.most_recent_common_ancestors(s, o, predicates=predicates):
                yield s, o, mrca

    def common_ancestors(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
        include_owl_thing: bool = True,
    ) -> Iterable[CURIE]:
        """
        Common ancestors of a subject-object pair

        :param subject:
        :param object:
        :param predicates:
        :param subject_ancestors: optional pre-generated ancestor list
        :param object_ancestors: optional pre-generated ancestor list
        :param include_owl_thing:
        :return:
        """
        if subject_ancestors is not None and object_ancestors is not None:
            subject_ancestors = set(subject_ancestors)
            object_ancestors = set(object_ancestors)
        elif isinstance(self, OboGraphInterface):
            subject_ancestors = set(self.ancestors(subject, predicates))
            object_ancestors = set(self.ancestors(object, predicates))
        else:
            raise NotImplementedError
        if include_owl_thing:
            subject_ancestors.add(OWL_THING)
            object_ancestors.add(OWL_THING)
        for a in subject_ancestors.intersection(object_ancestors):
            yield a

    def common_descendants(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        include_owl_nothing: bool = False,
    ) -> Iterable[CURIE]:
        raise NotImplementedError

    def load_information_content_scores(self, source: str) -> None:
        """
        Load term information content values from file

        :param source:
        :return:
        """
        self.cached_information_content_map = load_information_content_map(source)

    def set_information_content_scores(self, scores: Iterable[Tuple[CURIE, float]]) -> None:
        """
        Load term information content values from file

        :param source:
        :return:
        """
        self.cached_information_content_map = dict(scores)

    def get_information_content(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Optional[float]:
        """
        Returns the information content of a term.

        IC(t) = -log2(Pr(t))

        :param curie:
        :param predicates:
        :return:
        """
        pairs = list(self.information_content_scores([curie], object_closure_predicates=predicates))
        if pairs:
            if len(pairs) > 1:
                raise ValueError(f"Multiple values for IC for {curie} = {pairs}")
            return pairs[0][1]

    def information_content_scores(
        self,
        curies: Optional[Iterable[CURIE]] = None,
        predicates: List[PRED_CURIE] = None,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
        term_to_entities_map: Dict[CURIE, List[CURIE]] = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Yields entity-score pairs for a given collection of entities.

        The Information Content (IC) score for a term t is determined by:

            IC(t) = -log2(Pr(t))

        Where the probability Pr(t) is determined by the frequency of that term against
        the whole corpus:

            Pr(t) = freq(t)/|items|

        :param curies:
        :param predicates:
        :param object_closure_predicates:
        :param use_associations:
        :param term_to_entities_map:
        :param kwargs:
        :return:
        """
        if curies is None:
            for curie_it in chunk(self.entities()):
                yield from self.information_content_scores(
                    curie_it,
                    predicates=predicates,
                    object_closure_predicates=object_closure_predicates,
                    use_associations=use_associations,
                    term_to_entities_map=term_to_entities_map,
                    **kwargs,
                )
            return
        curies = list(curies)
        if self.cached_information_content_map is None and use_associations:
            logging.info("Calculating and caching IC map from associations")
            from oaklib.interfaces.association_provider_interface import (
                AssociationProviderInterface,
            )

            if not isinstance(self, AssociationProviderInterface):
                raise ValueError(
                    f"unable to retrieve associations from this interface, type {type(self)}"
                )
            self.cached_information_content_map = {}
            all_entities = set()
            for a in self.associations():
                all_entities.add(a.subject)
            num_entities = len(all_entities)
            logging.info(f"num_entities={num_entities}")
            for term, count in self.association_subject_counts(
                predicates=predicates, object_closure_predicates=object_closure_predicates
            ):
                if count > num_entities:
                    raise AssertionError(f"Count {count} > num_entities {num_entities}")
                self.cached_information_content_map[term] = -math.log(
                    count / num_entities
                ) / math.log(2)
            if curies:
                for curie in curies:
                    if curie not in self.cached_information_content_map:
                        self.cached_information_content_map[curie] = 0.0
        if self.cached_information_content_map is not None:
            logging.debug("Using cached IC map")
            for curie in curies:
                if curie in self.cached_information_content_map:
                    yield curie, self.cached_information_content_map[curie]
            return
        logging.info("Calculating and caching IC map from ontology")
        all_entities = list(self.entities())
        num_entities = len(all_entities)
        if not isinstance(self, OboGraphInterface):
            raise NotImplementedError
        yielded_owl_thing = False
        for curie in curies:
            descendants = list(self.descendants([curie], object_closure_predicates))
            yield curie, -math.log(len(descendants) / num_entities)
            if curie == OWL_THING:
                yielded_owl_thing = True
        # inject owl:Thing, which always has zero information
        if (OWL_THING in curies or not curies) and not yielded_owl_thing:
            yield OWL_THING, 0.0

    def pairwise_similarity(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
        min_jaccard_similarity: Optional[float] = None,
        min_ancestor_information_content: Optional[float] = None,
    ) -> Optional[TermPairwiseSimilarity]:
        """
        Pairwise similarity between a pair of ontology terms

        :param subject:
        :param object:
        :param predicates:
        :param subject_ancestors: optional pre-generated ancestor list
        :param object_ancestors: optional pre-generated ancestor list
        :param min_jaccard_similarity: minimum Jaccard similarity for a pair to be considered
        :param min_ancestor_information_content: minimum IC for a common ancestor to be considered
        :return:
        """
        logging.debug(f"Calculating pairwise similarity for {subject} x {object} over {predicates}")
        if subject_ancestors is None and isinstance(self, OboGraphInterface):
            subject_ancestors = list(self.ancestors(subject, predicates=predicates))
        if object_ancestors is None and isinstance(self, OboGraphInterface):
            object_ancestors = list(self.ancestors(object, predicates=predicates))
        if subject_ancestors is not None and object_ancestors is not None:
            jaccard_similarity = setwise_jaccard_similarity(subject_ancestors, object_ancestors)
        if min_jaccard_similarity is not None and jaccard_similarity < min_jaccard_similarity:
            return None
        cas = list(
            self.common_ancestors(
                subject,
                object,
                predicates,
                subject_ancestors=subject_ancestors,
                object_ancestors=object_ancestors,
            )
        )
        if OWL_THING in cas:
            cas.remove(OWL_THING)
        logging.debug(f"Retrieving IC for {len(cas)} common ancestors")
        ics = {
            a: ic
            for a, ic in self.information_content_scores(cas, object_closure_predicates=predicates)
        }
        if len(ics) > 0:
            max_ic = max(ics.values())
            best_mrcas = [a for a in ics.keys() if math.isclose(ics[a], max_ic, rel_tol=0.001)]
            anc = best_mrcas[0]
        else:
            max_ic = 0.0
            anc = None
        if min_ancestor_information_content is not None:
            if max_ic < min_ancestor_information_content:
                return None
        logging.debug(f"MRCA = {anc} with {max_ic}")
        sim = TermPairwiseSimilarity(
            subject_id=subject,
            object_id=object,
            ancestor_id=anc,
            subject_information_content=ics.get(subject, self.get_information_content(subject)),
            object_information_content=ics.get(object, self.get_information_content(object)),
            ancestor_information_content=max_ic,
            jaccard_similarity=jaccard_similarity,
        )
        sim.ancestor_information_content = max_ic

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
        min_jaccard_similarity: Optional[float] = None,
        min_ancestor_information_content: Optional[float] = None,
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
            logging.info(f"Computing pairwise similarity for {s} x {len(objects)} objects")
            for o in objects:
                val = self.pairwise_similarity(
                    s,
                    o,
                    predicates=predicates,
                    min_jaccard_similarity=min_jaccard_similarity,
                    min_ancestor_information_content=min_ancestor_information_content,
                )
                if val:
                    yield val
