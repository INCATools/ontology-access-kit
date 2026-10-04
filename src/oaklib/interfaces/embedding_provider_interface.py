import statistics
from abc import ABC
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

import numpy as np
import pandas as pd

from oaklib.datamodels.similarity import (
    BestMatch,
    TermInfo,
    TermPairwiseSimilarity,
    TermSetPairwiseSimilarity,
)
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE
from oaklib.utilities.embeddings.closure_embeddings import closure_embeddings
from oaklib.utilities.embeddings.vector_utils import similarity_matrix

__all__ = [
    "EmbeddingProviderInterface",
    "CLOSURE_MODEL",
]

CLOSURE_MODEL = "closure"
"""Pseudo-model that encodes each term as a multi-hot vector of its reflexive ancestors."""


class EmbeddingProviderInterface(BasicOntologyInterface, ABC):
    """
    Provides vector embeddings for entities, and operations over them.

    The core method is :meth:`entity_embeddings`, which returns a numpy matrix with one
    row per entity. Similarity, nearest-neighbour search and set-wise (best match)
    comparison are derived from it, so a backend only needs to supply vectors;
    backends that can do more natively (e.g. server-side vector search) override
    the relevant methods.

    Each backend offers one or more named *models* (see :meth:`embedding_models`).
    Vectors from different models are not comparable.

    Any adapter that also implements :class:`OboGraphInterface` additionally supports
    the ``closure`` pseudo-model, in which each term is a multi-hot vector of its
    reflexive ancestors. This makes classic ontology-based similarity directly
    comparable with learned embeddings:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("tests/input/go-nucleus.db")
    >>> ids, m = adapter.entity_embeddings(["GO:0005634", "GO:0005635"], model="closure")
    >>> m.shape[0]
    2
    >>> round(adapter.embedding_similarity("GO:0005634", "GO:0005634", model="closure"), 3)
    1.0
    """

    default_embedding_model = None
    """Model used when none is specified."""

    closure_embedding_predicates = None
    """Predicates traversed by the ``closure`` model; None means is_a only."""

    # ---------------------------------------------------------------
    # Backend hooks
    # ---------------------------------------------------------------

    def _fetch_embeddings(
        self, curies: List[CURIE], model: str
    ) -> Dict[CURIE, Optional[np.ndarray]]:
        """
        Fetch vectors for entities from the backend.

        Implementations should return a mapping containing an entry for every entity
        that has a vector; entities without vectors may be omitted or mapped to None.

        :param curies: entities to fetch
        :param model: the model name
        :return: mapping from entity to vector
        """
        raise NotImplementedError(f"{type(self).__name__} does not provide model {model}")

    # ---------------------------------------------------------------
    # Core API
    # ---------------------------------------------------------------

    def embedding_models(self) -> List[str]:
        """
        Names of the models this adapter can provide embeddings for.

        :return: list of model names
        """
        if isinstance(self, OboGraphInterface):
            return [CLOSURE_MODEL]
        return []

    def _resolve_model(self, model: Optional[str]) -> str:
        if model:
            return model
        if self.default_embedding_model:
            return self.default_embedding_model
        models = self.embedding_models()
        if not models:
            raise ValueError(f"{type(self).__name__} does not provide any embedding models")
        return models[0]

    def entity_embeddings(
        self, curies: Iterable[CURIE], model: Optional[str] = None
    ) -> Tuple[List[CURIE], np.ndarray]:
        """
        Embed a collection of entities as a matrix.

        Entities for which no vector is available are dropped; the returned list
        gives the entity for each row, in input order.

        :param curies: entities to embed
        :param model: model name; defaults to the adapter's default model
        :return: tuple of (curies, matrix with one row per curie)
        """
        model = self._resolve_model(model)
        curies = list(dict.fromkeys(curies))
        if model == CLOSURE_MODEL:
            if not isinstance(self, OboGraphInterface):
                raise NotImplementedError(f"{type(self).__name__} cannot compute closures")
            ids, _, matrix = closure_embeddings(
                self, curies, predicates=self.closure_embedding_predicates
            )
            return ids, matrix
        vectors = self._fetch_embeddings(curies, model)
        ids = [c for c in curies if vectors.get(c) is not None]
        if not ids:
            return [], np.zeros((0, 0), dtype=np.float32)
        return ids, np.vstack([vectors[c] for c in ids])

    def entity_embedding(self, curie: CURIE, model: Optional[str] = None) -> Optional[np.ndarray]:
        """
        Embed a single entity.

        Note that for the ``closure`` model the vector dimensions depend on the set of
        entities embedded together, so use :meth:`entity_embeddings` to compare.

        :param curie: entity to embed
        :param model: model name
        :return: vector, or None if the entity has no embedding
        """
        ids, matrix = self.entity_embeddings([curie], model=model)
        return matrix[0] if ids else None

    def embeddings_dataframe(
        self, curies: Iterable[CURIE], model: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Embed a collection of entities as a DataFrame indexed by entity.

        :param curies: entities to embed
        :param model: model name
        :return: DataFrame with one row per entity and one column per dimension
        """
        ids, matrix = self.entity_embeddings(curies, model=model)
        df = pd.DataFrame(matrix, index=pd.Index(ids, name="id"))
        return df

    def text_embedding(self, text: str, model: Optional[str] = None) -> np.ndarray:
        """
        Embed arbitrary text, using the same space as the entity embeddings.

        :param text: text to embed
        :param model: model name
        :return: vector
        """
        raise NotImplementedError(f"{type(self).__name__} cannot embed arbitrary text")

    # ---------------------------------------------------------------
    # Derived operations
    # ---------------------------------------------------------------

    def embedding_similarity_matrix(
        self,
        subjects: Iterable[CURIE],
        objects: Optional[Iterable[CURIE]] = None,
        model: Optional[str] = None,
        metric: str = "cosine",
    ) -> pd.DataFrame:
        """
        All-by-all similarity between two sets of entities.

        Entities without embeddings are omitted from the result.

        :param subjects: row entities
        :param objects: column entities; defaults to subjects
        :param model: model name
        :param metric: ``cosine`` (default) or ``jaccard``
        :return: DataFrame indexed by subject, with a column per object
        """
        subjects = list(subjects)
        objects = subjects if objects is None else list(objects)
        # embed together so that closure vectors share dimensions
        ids, matrix = self.entity_embeddings(subjects + objects, model=model)
        row_ix = {c: i for i, c in enumerate(ids)}
        s_ids = [c for c in dict.fromkeys(subjects) if c in row_ix]
        o_ids = [c for c in dict.fromkeys(objects) if c in row_ix]
        if not s_ids or not o_ids:
            return pd.DataFrame(index=s_ids, columns=o_ids, dtype=float)
        sims = similarity_matrix(
            matrix[[row_ix[c] for c in s_ids]], matrix[[row_ix[c] for c in o_ids]], metric=metric
        )
        return pd.DataFrame(sims, index=s_ids, columns=o_ids)

    def embedding_similarity(
        self,
        subject: CURIE,
        object: CURIE,
        model: Optional[str] = None,
        metric: str = "cosine",
    ) -> Optional[float]:
        """
        Similarity between a pair of entities.

        :param subject: first entity
        :param object: second entity
        :param model: model name
        :param metric: ``cosine`` (default) or ``jaccard``
        :return: similarity score, or None if either entity has no embedding
        """
        df = self.embedding_similarity_matrix([subject], [object], model=model, metric=metric)
        if df.empty:
            return None
        return float(df.iloc[0, 0])

    def embedding_pairwise_similarity(
        self, subject: CURIE, object: CURIE, model: Optional[str] = None
    ) -> Optional[TermPairwiseSimilarity]:
        """
        Pairwise similarity as a :class:`TermPairwiseSimilarity` object.

        Only the ``cosine_similarity`` slot is populated. This allows embedding-based
        scores to be used anywhere semantic similarity results are expected.

        :param subject: first entity
        :param object: second entity
        :param model: model name
        :return: similarity object, or None if either entity has no embedding
        """
        score = self.embedding_similarity(subject, object, model=model)
        if score is None:
            return None
        return TermPairwiseSimilarity(subject_id=subject, object_id=object, cosine_similarity=score)

    def embedding_termset_similarity(
        self,
        subjects: List[CURIE],
        objects: List[CURIE],
        model: Optional[str] = None,
        labels: bool = False,
    ) -> TermSetPairwiseSimilarity:
        """
        Compare two sets of entities using best-match average over cosine similarity.

        This is the embedding analog of
        :meth:`SemanticSimilarityInterface.termset_pairwise_similarity`; the score of
        each best match is a cosine similarity.

        :param subjects: first set of entities (e.g. a patient's phenotypes)
        :param objects: second set of entities (e.g. a disease's phenotypes)
        :param model: model name
        :param labels: if True, populate labels
        :return: set-wise similarity, with ``average_score`` as the best-match average
        """
        df = self.embedding_similarity_matrix(subjects, objects, model=model)
        sim = TermSetPairwiseSimilarity()
        for x in subjects:
            sim.subject_termset[x] = TermInfo(x)
        for x in objects:
            sim.object_termset[x] = TermInfo(x)
        scores = []
        if not df.empty:
            for best_matches, frame in (
                (sim.subject_best_matches, df),
                (sim.object_best_matches, df.T),
            ):
                for source, row in frame.iterrows():
                    target = row.idxmax()
                    score = float(row[target])
                    pair = (source, target) if frame is df else (target, source)
                    best_matches[source] = BestMatch(
                        source,
                        match_target=target,
                        score=score,
                        similarity=TermPairwiseSimilarity(
                            subject_id=pair[0], object_id=pair[1], cosine_similarity=score
                        ),
                    )
                    scores.append(score)
        if not scores:
            scores = [0.0]
        sim.average_score = statistics.mean(scores)
        sim.best_score = max(scores)
        if labels:
            curies = set(subjects) | set(objects)
            label_ix = dict(self.labels(curies))
            for x in list(sim.subject_termset.values()) + list(sim.object_termset.values()):
                x.label = label_ix.get(x.id)
            for x in list(sim.subject_best_matches.values()) + list(
                sim.object_best_matches.values()
            ):
                x.match_source_label = label_ix.get(x.match_source)
                x.match_target_label = label_ix.get(x.match_target)
        return sim

    def nearest_entities(
        self,
        curie: CURIE,
        limit: int = 10,
        model: Optional[str] = None,
        candidates: Optional[Iterable[CURIE]] = None,
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Find the entities whose embeddings are most similar to that of a given entity.

        The default implementation is a brute-force comparison against ``candidates``
        (by default, all entities in the adapter). Backends with a vector index
        override this.

        :param curie: query entity
        :param limit: maximum number of results
        :param model: model name
        :param candidates: entities to search over
        :return: iterator of (entity, score) tuples, best first (excluding the query entity)
        """
        if candidates is None:
            candidates = self.entities(filter_obsoletes=True)
        candidates = [c for c in candidates if c != curie]
        df = self.embedding_similarity_matrix([curie], candidates, model=model)
        if df.empty:
            return
        row = df.iloc[0].drop(curie, errors="ignore").sort_values(ascending=False)
        for c, score in row.head(limit).items():
            yield c, float(score)

    def nearest_entities_to_vector(
        self,
        vector: np.ndarray,
        limit: int = 10,
        model: Optional[str] = None,
        candidates: Optional[Iterable[CURIE]] = None,
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Find the entities whose embeddings are most similar to a given vector.

        :param vector: query vector, in the space of ``model``
        :param limit: maximum number of results
        :param model: model name
        :param candidates: entities to search over
        :return: iterator of (entity, score) tuples, best first
        """
        if candidates is None:
            candidates = self.entities(filter_obsoletes=True)
        ids, matrix = self.entity_embeddings(candidates, model=model)
        if not ids:
            return
        vector = np.asarray(vector)
        if matrix.shape[1] != vector.shape[0]:
            raise ValueError(
                f"Query vector has {vector.shape[0]} dimensions but {model} embeddings "
                f"have {matrix.shape[1]}"
            )
        scores = similarity_matrix(vector[None, :], matrix)[0]
        for i in np.argsort(-scores)[:limit]:
            yield ids[i], float(scores[i])

    def nearest_entities_to_text(
        self,
        text: str,
        limit: int = 10,
        model: Optional[str] = None,
        candidates: Optional[Iterable[CURIE]] = None,
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Find the entities whose embeddings are most similar to an embedding of some text.

        :param text: query text
        :param limit: maximum number of results
        :param model: model name
        :param candidates: entities to search over
        :return: iterator of (entity, score) tuples, best first
        """
        vector = self.text_embedding(text, model=model)
        yield from self.nearest_entities_to_vector(
            vector, limit=limit, model=model, candidates=candidates
        )
