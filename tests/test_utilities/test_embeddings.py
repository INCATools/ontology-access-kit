import math
import time
import unittest

import numpy as np

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces.embedding_provider_interface import (
    CLOSURE_MODEL,
    EmbeddingProviderInterface,
)
from oaklib.utilities.embeddings.closure_embeddings import closure_embeddings
from oaklib.utilities.embeddings.embedding_cache import EmbeddingCache
from oaklib.utilities.embeddings.vector_utils import (
    cosine_similarity_matrix,
    jaccard_similarity_matrix,
)
from tests import IMBO, INPUT_DIR, NUCLEAR_ENVELOPE, NUCLEUS, VACUOLE

DB = INPUT_DIR / "go-nucleus.db"


class TestVectorUtils(unittest.TestCase):
    def test_cosine(self):
        a = np.array([[1.0, 0.0], [0.0, 2.0], [0.0, 0.0]])
        m = cosine_similarity_matrix(a)
        self.assertAlmostEqual(m[0, 0], 1.0)
        self.assertAlmostEqual(m[0, 1], 0.0)
        self.assertAlmostEqual(m[2, 2], 0.0)

    def test_jaccard(self):
        a = np.array([[1, 1, 1, 0]])
        b = np.array([[1, 1, 0, 0], [0, 0, 0, 1]])
        m = jaccard_similarity_matrix(a, b)
        self.assertAlmostEqual(m[0, 0], 2 / 3)
        self.assertAlmostEqual(m[0, 1], 0.0)


class TestEmbeddingCache(unittest.TestCase):
    def test_roundtrip(self):
        cache = EmbeddingCache(":memory:")
        cache.put("src", "m1", {"X:1": np.array([0.5, 1.5]), "X:2": None})
        cache.put("src", "m2", {"X:1": np.array([9.0])})
        got = cache.get("src", "m1", ["X:1", "X:2", "X:3"])
        np.testing.assert_array_almost_equal(got["X:1"], [0.5, 1.5])
        self.assertIsNone(got["X:2"])
        self.assertNotIn("X:3", got)
        cache.clear(model="m1")
        self.assertEqual(cache.get("src", "m1", ["X:1"]), {})
        self.assertIn("X:1", cache.get("src", "m2", ["X:1"]))

    def test_staleness(self):
        cache = EmbeddingCache(":memory:", is_stale=lambda then: time.time() - then > 3600)
        cache.put("src", "m", {"X:1": np.array([1.0])})
        self.assertIn("X:1", cache.get("src", "m", ["X:1"]))
        cache.is_stale = lambda then: True
        self.assertEqual(cache.get("src", "m", ["X:1"]), {})


class TestClosureEmbeddings(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = get_adapter(str(DB))

    def test_interface(self):
        self.assertIsInstance(self.adapter, EmbeddingProviderInterface)
        self.assertIn(CLOSURE_MODEL, self.adapter.embedding_models())

    def test_closure_vectors(self):
        ids, vocab, m = closure_embeddings(self.adapter, [NUCLEUS, VACUOLE])
        self.assertEqual(ids, [NUCLEUS, VACUOLE])
        self.assertEqual(m.shape, (2, len(vocab)))
        nucleus_ancs = set(self.adapter.ancestors(NUCLEUS, predicates=[IS_A], reflexive=True))
        self.assertEqual({vocab[i] for i in np.nonzero(m[0])[0]}, nucleus_ancs - {"owl:Thing"})

    def test_jaccard_matches_semsim(self):
        """Jaccard over closure vectors is the same as classic ancestor-set Jaccard."""
        for s, o in [(NUCLEUS, VACUOLE), (NUCLEUS, NUCLEAR_ENVELOPE), (IMBO, VACUOLE)]:
            vec_sim = self.adapter.embedding_similarity(s, o, metric="jaccard")
            classic = self.adapter.pairwise_similarity(s, o, predicates=[IS_A])
            self.assertAlmostEqual(vec_sim, classic.jaccard_similarity, places=6)

    def test_similarity_matrix(self):
        df = self.adapter.embedding_similarity_matrix([NUCLEUS, VACUOLE], [NUCLEUS, "X:UNKNOWN"])
        self.assertEqual(list(df.index), [NUCLEUS, VACUOLE])
        self.assertAlmostEqual(df.loc[NUCLEUS, NUCLEUS], 1.0)
        self.assertTrue(0 < df.loc[VACUOLE, NUCLEUS] < 1)

    def test_dataframe(self):
        df = self.adapter.embeddings_dataframe([NUCLEUS, VACUOLE])
        self.assertEqual(list(df.index), [NUCLEUS, VACUOLE])
        self.assertTrue(set(np.unique(df.values)) <= {0.0, 1.0})

    def test_pairwise_similarity_object(self):
        sim = self.adapter.embedding_pairwise_similarity(NUCLEUS, VACUOLE)
        self.assertEqual(sim.subject_id, NUCLEUS)
        self.assertTrue(0 < sim.cosine_similarity < 1)

    def test_nearest_entities(self):
        results = list(self.adapter.nearest_entities(NUCLEUS, limit=3))
        self.assertEqual(len(results), 3)
        self.assertNotIn(NUCLEUS, [c for c, _ in results])
        scores = [s for _, s in results]
        self.assertEqual(scores, sorted(scores, reverse=True))
        # IMBO is the direct parent of nucleus
        self.assertEqual(results[0][0], IMBO)

    def test_nearest_entities_to_vector(self):
        ids, m = self.adapter.entity_embeddings([NUCLEUS, VACUOLE])
        results = list(
            self.adapter.nearest_entities_to_vector(m[0], limit=1, candidates=[NUCLEUS, VACUOLE])
        )
        self.assertEqual(results[0][0], NUCLEUS)
        # closure dimensions depend on the terms embedded together
        with self.assertRaises(ValueError):
            list(self.adapter.nearest_entities_to_vector(m[0], candidates=[NUCLEAR_ENVELOPE]))

    def test_termset_similarity(self):
        sim = self.adapter.embedding_termset_similarity(
            [NUCLEUS, VACUOLE], [NUCLEAR_ENVELOPE, NUCLEUS], labels=True
        )
        self.assertAlmostEqual(sim.subject_best_matches[NUCLEUS].score, 1.0)
        self.assertEqual(sim.subject_best_matches[NUCLEUS].match_target, NUCLEUS)
        self.assertEqual(sim.object_best_matches[NUCLEAR_ENVELOPE].match_source, NUCLEAR_ENVELOPE)
        self.assertEqual(sim.subject_termset[NUCLEUS].label, "nucleus")
        self.assertTrue(0 < sim.average_score <= 1)
        self.assertAlmostEqual(sim.best_score, 1.0)
        self.assertFalse(math.isnan(sim.average_score))
