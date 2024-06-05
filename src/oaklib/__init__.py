"""
Oaklib
------
"""

__version__ = "0.1.0"

from oaklib.interfaces import BasicOntologyInterface  # noqa:F401
from oaklib.query import onto_query  # noqa:F401  # noqa:F401
from oaklib.resource import OntologyResource  # noqa:F401
from oaklib.selector import get_adapter, get_implementation_from_shorthand  # noqa:F401

schemes = {}
