from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional

import pystow
import requests
import requests_cache


@dataclass
class PubDBWrapper(ABC):

    name: ClassVar[str] = "__generic__"

    cache_path: Optional[str] = None

    session: requests.Session = field(default_factory=lambda: requests.Session())

    api_key: Optional[str] = None

    email: Optional[str] = None

    _uses_cache: bool = False

    def __post_init__(self):
        cache_path = self.cache_path
        if not cache_path:
            cache_path = pystow.join("oaklib", "session_cache", self.name, ensure_exists=True)
        self.set_cache(cache_path)

    def set_cache(self, name: str) -> None:
        self.session = requests_cache.CachedSession(name)
        self._uses_cache = True

    @abstractmethod
    def objects_by_ids(self, object_ids: List[str]) -> List[Dict]:
        raise NotImplementedError
