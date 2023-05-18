"""Rust implementation of semantic similarity measures."""
import inspect
import logging
import math
from dataclasses import dataclass
from typing import ClassVar, List

from semsimian import (
    max_information_content,
    relationships_to_closure_table,
    semantic_jaccard_similarity,
)

from oaklib.datamodels.similarity import TermPairwiseSimilarity
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

        rels = [r for r in self.wrapped_adapter.relationships(include_entailed=True)]
        self._rust_closure_table = relationships_to_closure_table(rels)
        # TODO: eliminate the need for this
        self._entities = {r[0] for r in rels}

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
        sim = TermPairwiseSimilarity(
            subject_id=subject,
            object_id=object,
            ancestor_id=None,
            ancestor_information_content=None,
        )
        if subject not in self._entities or object not in self._entities:
            logging.debug(f"Unknown entity in {subject} x {object}")
            if subject == object:
                sim.jaccard_similarity = 1.0
            else:
                sim.jaccard_similarity = 0.0
            sim.ancestor_information_content = 0.0
            return sim

        if predicates:
            predicates = set(predicates)
        sim.jaccard_similarity = semantic_jaccard_similarity(
            self._rust_closure_table, subject, object, predicates
        )
        sim.ancestor_information_content = max_information_content(
            self._rust_closure_table, subject, object, predicates
        )
        sim.phenodigm_score = math.sqrt(sim.jaccard_similarity * sim.ancestor_information_content)
        return sim
