"""Rust implementation of semantic similarity measures."""

import inspect
import logging
import math
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from oaklib.datamodels.similarity import (
    BestMatch,
    TermInfo,
    TermPairwiseSimilarity,
    TermSetPairwiseSimilarity,
)
from oaklib.datamodels.vocabulary import OWL_THING
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.interfaces.association_provider_interface import AssociationProviderInterface
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
class SemSimianImplementation(
    SearchInterface, SemanticSimilarityInterface, OboGraphInterface, AssociationProviderInterface
):
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
        AssociationProviderInterface.associations,
        AssociationProviderInterface.add_associations,
    ]

    custom_ic_map_path: str = None

    semsimian_object_cache: Dict[Tuple[PRED_CURIE], Optional["Semsimian"]] = field(default_factory=dict)  # type: ignore # noqa

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

        self.term_pairwise_similarity_attributes = [
            attr
            for attr in vars(TermPairwiseSimilarity)
            if not any(attr.startswith(s) for s in ["class_", "_"])
        ]
        self.termset_pairwise_similarity_attributes = [
            attr
            for attr in vars(TermSetPairwiseSimilarity)
            if not any(attr.startswith(s) for s in ["class_", "_"])
        ]

    def _get_semsimian_object(
        self,
        predicates: List[PRED_CURIE] = None,
        attributes: List[str] = None,
        resource_path: str = None,
        custom_ic_map_path: str = None,
    ) -> "Semsimian":  # type: ignore # noqa
        """
        Get Semsimian object from "semsimian_object_cache" or add a new one.

        :param predicates: collection of predicates, defaults to None
        :return: A Semsimian object.
        """
        from semsimian import Semsimian

        predicates = tuple(sorted(predicates))

        if custom_ic_map_path is not None:
            logging.info(f"Using custom IC map with Semsimian: {custom_ic_map_path}")

        if predicates not in self.semsimian_object_cache:
            # spo = [
            #     r
            #     for r in self.wrapped_adapter.relationships(
            #         include_entailed=True, predicates=predicates
            #     )
            # ]
            if isinstance(self.wrapped_adapter, SqlImplementation):
                self.resource_path = str(self.wrapped_adapter.engine.url).lstrip("sqlite:")
            else:
                self.resource_path = str(self.wrapped_adapter.engine.url)

            self.semsimian_object_cache[predicates] = Semsimian(
                spo=None,
                predicates=predicates,
                pairwise_similarity_attributes=attributes,
                resource_path=self.resource_path,
                custom_ic_map_path=self.custom_ic_map_path,
            )

        return self.semsimian_object_cache[predicates]

    def load_information_content_scores(self, source: str) -> None:
        """
        Load information content from a source.

        :param source: The source of information content.
        """
        self.custom_ic_map_path = source

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
        semsimian = self._get_semsimian_object(
            predicates=predicates,
            attributes=self.term_pairwise_similarity_attributes,
            custom_ic_map_path=self.custom_ic_map_path,
        )

        jaccard_val = semsimian.jaccard_similarity(subject, object)

        if math.isnan(jaccard_val):
            return None

        if min_jaccard_similarity is not None and jaccard_val < min_jaccard_similarity:
            return None

        _, ancestor_information_content_val = semsimian.resnik_similarity(subject, object)

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
        semsimian = self._get_semsimian_object(
            predicates=predicates,
            attributes=self.term_pairwise_similarity_attributes,
            custom_ic_map_path=self.custom_ic_map_path,
        )
        all_results = semsimian.all_by_all_pairwise_similarity(
            subject_terms=set(subjects),
            object_terms=set(objects),
            minimum_jaccard_threshold=min_jaccard_similarity,
            minimum_resnik_threshold=min_ancestor_information_content,
            # predicates=set(predicates) if predicates else None,
        )

        logging.info("Post-processing results from semsimian")
        for term1_key, values in all_results.items():
            for term2_key, result in values.items():
                # Remember the _ here is cosine_similarity which we do not use at the moment.
                jaccard, resnik, phenodigm_score, _, ancestor_set = result
                if len(ancestor_set) > 0:
                    sim = TermPairwiseSimilarity(
                        subject_id=term1_key,
                        object_id=term2_key,
                        ancestor_id=next(
                            iter(ancestor_set)
                        ),  # TODO: Change this: gets first element of the set
                    )

                else:
                    sim = TermPairwiseSimilarity(
                        subject_id=term1_key, object_id=term2_key, ancestor_id=OWL_THING
                    )
                sim.jaccard_similarity = jaccard if jaccard is not None else 0.0
                sim.ancestor_information_content = resnik if resnik is not None else 0.0
                sim.phenodigm_score = phenodigm_score if phenodigm_score is not None else 0.0

                yield sim

    def termset_pairwise_similarity(
        self,
        subjects: List[CURIE],
        objects: List[CURIE],
        score_metric: str = None,
        predicates: List[PRED_CURIE] = None,
        labels=False,
    ) -> TermSetPairwiseSimilarity:
        """
        Return TermSetPairwiseSimilarity object.

        :param subjects: List of subject nodes.
        :param objects: List of object nodes.
        :param predicates: List of predicates, defaults to None
        :param labels: Boolean to get labels for all nodes from resource, defaults to False
        :return: TermSetPairwiseSimilarity object
        """
        semsimian = self._get_semsimian_object(
            predicates=predicates, attributes=self.termset_pairwise_similarity_attributes
        )
        sim = TermSetPairwiseSimilarity()
        semsimian_tsps = semsimian.termset_pairwise_similarity(
            set(subjects), set(objects), score_metric
        )

        # Assuming all keys for the dict semsimian_tsps are attributes for the class TermSetPairwiseSimilarity,
        # populate the object `sim`
        for attribute, value in semsimian_tsps.items():
            if isinstance(value, list):
                setattr(
                    sim,
                    attribute,
                    {
                        k: TermInfo(id=v["id"], label=v["label"])
                        for term_dict in value
                        for k, v in term_dict.items()
                    },
                )
            elif isinstance(value, dict) and str(attribute).endswith("best_matches"):
                best_match_dict = {}
                for k, v in value.items():
                    if k != "similarity":
                        v["similarity"] = value["similarity"][k]
                        v = self._regain_element_formats(v)
                        best_match_object: BestMatch = BestMatch(**v)
                        best_match_dict[k] = best_match_object

                setattr(sim, attribute, best_match_dict)
            else:
                value = self._regain_element_formats(value)
                setattr(sim, attribute, value)

        if labels:
            logging.warning("Adding labels not yet implemented in SemsimianImplementation.")

        return sim

    def _regain_element_formats(self, value: str) -> Union[str, float]:
        """Check if value is a float/str/NaN and format them accordingly."""
        if isinstance(value, dict):
            for key in value:
                value[key] = self._regain_element_formats(value[key])
        else:
            try:
                if value == "NaN":
                    value = None
                else:
                    value = float(value)
            except ValueError:
                try:
                    value = int(value)
                except ValueError:
                    pass
        return value
