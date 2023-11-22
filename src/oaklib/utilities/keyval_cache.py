from typing import Any, Dict

from pydantic import BaseModel

from oaklib.types import CURIE


class KeyValCache(BaseModel):
    """
    Key-value cache for storing arbitrary data.
    """

    cache: Dict[str, Dict[str, Any]] = {}

    def add(self, curie: CURIE, property: CURIE, value: Any):
        """
        Add a key-value pair to the cache.
        """
        if property not in self.cache:
            self.cache[property] = {}
        self.cache[property][curie] = value

    def get(self, curie: CURIE, property: CURIE) -> Any:
        """
        Get a value from the cache.
        """
        if property not in self.cache:
            return None
        if curie not in self.cache[property]:
            return None
        return self.cache[property][curie]

    def contains(self, curie: CURIE, property: CURIE) -> Any:
        """
        Check if a value is in the cache.
        """
        if property not in self.cache:
            return False
        return curie in self.cache[property]
