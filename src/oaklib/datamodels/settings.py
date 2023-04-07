from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Settings:
    impl: Any = None
    autosave: bool = False
    associations_type: Optional[str] = None
    preferred_language: Optional[str] = None
    other_languages: Optional[List[str]] = None
