"""A persistent local cache of entity embeddings, backed by sqlite."""

import logging
import sqlite3
import time
from pathlib import Path
from typing import Callable, Dict, Iterable, Optional, Union

import numpy as np

from oaklib.types import CURIE

__all__ = [
    "EmbeddingCache",
]

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS embedding (
    source TEXT NOT NULL,
    model TEXT NOT NULL,
    entity TEXT NOT NULL,
    vector BLOB,
    fetched_at REAL NOT NULL,
    PRIMARY KEY (source, model, entity)
)
"""


class EmbeddingCache:
    """
    Stores vectors keyed by (source, model, entity).

    Entities that the source does not know about are cached as misses (a ``None``
    vector) so that they are not requested again.

    >>> cache = EmbeddingCache(":memory:")
    >>> cache.put("ols", "m1", {"X:1": np.array([1.0, 2.0]), "X:2": None})
    >>> sorted(cache.get("ols", "m1", ["X:1", "X:2", "X:3"]).items())
    [('X:1', array([1., 2.], dtype=float32)), ('X:2', None)]
    """

    def __init__(self, path: Union[str, Path], is_stale: Optional[Callable[[float], bool]] = None):
        """
        :param path: path to the sqlite file, or ``:memory:``
        :param is_stale: if set, called with the time (seconds since the epoch) an entry
            was cached; entries for which it returns True are treated as absent.
            :meth:`CachePolicy.refresh` can be passed here.
        """
        self.path = str(path)
        self.is_stale = is_stale
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path)
        self._connection.execute(_SCHEMA)
        self._connection.commit()

    def get(
        self, source: str, model: str, entities: Iterable[CURIE]
    ) -> Dict[CURIE, Optional[np.ndarray]]:
        """
        Look up cached vectors.

        :return: mapping for every cached entity; the value is None for cached misses
        """
        results = {}
        entities = list(entities)
        for i in range(0, len(entities), 500):
            batch = entities[i : i + 500]
            placeholders = ",".join("?" * len(batch))
            rows = self._connection.execute(
                f"SELECT entity, vector, fetched_at FROM embedding "  # noqa: S608
                f"WHERE source = ? AND model = ? AND entity IN ({placeholders})",
                [source, model, *batch],
            )
            for entity, blob, fetched_at in rows:
                if self.is_stale is not None and self.is_stale(fetched_at):
                    continue
                results[entity] = None if blob is None else np.frombuffer(blob, dtype=np.float32)
        return results

    def put(self, source: str, model: str, vectors: Dict[CURIE, Optional[np.ndarray]]) -> None:
        """Store vectors (None records a miss)."""
        now = time.time()
        rows = [
            (
                source,
                model,
                entity,
                None if v is None else np.asarray(v, dtype=np.float32).tobytes(),
                now,
            )
            for entity, v in vectors.items()
        ]
        self._connection.executemany(
            "INSERT OR REPLACE INTO embedding VALUES (?, ?, ?, ?, ?)", rows
        )
        self._connection.commit()

    def clear(self, source: Optional[str] = None, model: Optional[str] = None) -> None:
        """Remove cached entries, optionally restricted to a source and/or model."""
        clauses, params = [], []
        if source is not None:
            clauses.append("source = ?")
            params.append(source)
        if model is not None:
            clauses.append("model = ?")
            params.append(model)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        self._connection.execute(f"DELETE FROM embedding{where}", params)  # noqa: S608
        self._connection.commit()
