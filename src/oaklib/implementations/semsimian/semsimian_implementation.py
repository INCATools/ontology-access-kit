"""Rust implementation of semantic similarity measures."""
import inspect
import logging
import math
from dataclasses import dataclass
from typing import ClassVar, Iterable, Iterator, List, Optional

from semsimian import Semsimian

from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.datamodels.vocabulary import OWL_THING
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE

wrapped_adapter: BasicOntologyInterface = None

__all__ = [
    "SemSimianImplementation",
]


@dataclass
class SemSimianImplementation(SearchInterface, SemanticSimilarityInterface, OboGraphInterface):
    """Rust implementation of semantic similarity measures."""

    delegated_methods: ClassVar[List[str]] = [
        BasicOntologyInterface.label,
        BasicOntologyInterface.labels,
        BasicOntologyInterface.entities,
        BasicOntologyInterface.curie_to_uri,
        BasicOntologyInterface.uri_to_curie,
        BasicOntologyInterface.ontologies,
        BasicOntologyInterface.obsoletes,
        BasicOntologyInterface.definition,
        BasicOntologyInterface.definitions,
        SearchInterface.basic_search,
        OboGraphInterface.node,
        OboGraphInterface.ancestors,
        OboGraphInterface.descendants,
        SemanticSimilarityInterface.get_information_content,
        SemanticSimilarityInterface.information_content_scores,
    ]

    def __post_init__(self):
        slug = self.resource.slug
        from oaklib.selector import get_adapter

        slug = slug.replace("semsimian:", "")
        logging.info(f"Wrapping an existing OAK implementation to fetch {slug}")
        self.wrapped_adapter = get_adapter(slug)
        methods = dict(inspect.getmembers(self.wrapped_adapter))
        for m in self.delegated_methods:
            mn = m if isinstance(m, str) else m.__name__
            setattr(SemSimianImplementation, mn, methods[mn])

        spo = [r for r in self.wrapped_adapter.relationships(include_entailed=True)]
        self.semsimian = Semsimian(spo)

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
        :param min_jaccard_similarity: optional minimum jaccard similarity
        :param min_ancestor_information_content: optional minimum ancestor information content
        :return:
        """
        logging.debug(f"Calculating pairwise similarity for {subject} x {object} over {predicates}")

        jaccard_val = self.semsimian.jaccard_similarity(subject, object, set(predicates))

        if math.isnan(jaccard_val):
            return None

        if min_jaccard_similarity is not None and jaccard_val < min_jaccard_similarity:
            return None

        _, ancestor_information_content_val = self.semsimian.resnik_similarity(
            subject, object, set(predicates)
        )

        if math.isnan(ancestor_information_content_val):
            return None

        if (
            min_ancestor_information_content is not None
            and ancestor_information_content_val < min_ancestor_information_content
        ):
            return None

        sim = TermPairwiseSimilarity(
            subject_id=subject,
            object_id=object,
            ancestor_id=None,
            ancestor_information_content=None,
        )

        sim.jaccard_similarity = jaccard_val
        sim.ancestor_information_content = ancestor_information_content_val

        sim.phenodigm_score = math.sqrt(sim.jaccard_similarity * sim.ancestor_information_content)

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
        logging.info(f"Calculating all-by-all pairwise similarity for {len(objects)} objects")
        all_results = self.semsimian.all_by_all_pairwise_similarity(
            subject_terms=set(subjects),
            object_terms=set(objects),
            minimum_jaccard_threshold=min_jaccard_similarity,
            minimum_resnik_threshold=min_ancestor_information_content,
            predicates=set(predicates) if predicates else None,
        )
        logging.info("Post-processing results from semsimian")
        for term1_key, values in all_results.items():
            for term2_key, result in values.items():
                jaccard, resnik, phenodigm_score, ancestor_set = result
                if len(ancestor_set) > 0:
                    sim = TermPairwiseSimilarity(
                        subject_id=term1_key,
                        object_id=term2_key,
                        ancestor_id=next(
                            iter(ancestor_set)
                        ),  # TODO: Change this: gets first element of the set
                    )
                    sim.jaccard_similarity = jaccard
                    sim.ancestor_information_content = resnik
                    sim.phenodigm_score = phenodigm_score
                else:
                    sim = TermPairwiseSimilarity(
                        subject_id=term1_key, object_id=term2_key, ancestor_id=OWL_THING
                    )
                    sim.jaccard_similarity = 0
                    sim.ancestor_information_content = 0
                yield sim
