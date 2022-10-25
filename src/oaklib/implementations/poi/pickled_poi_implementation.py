import inspect
import logging
from dataclasses import dataclass, field

from oaklib.implementations.poi.poi_implementation import PoiImplementation


@dataclass
class PickledPoiImplementation(
    PoiImplementation
):
    """
    A BitwiseImplementation that is restored from a pickled index.
    """
    def __post_init__(self):
        if self.wrapped_adapter is None:
            from oaklib.selector import get_implementation_from_shorthand

            slug = self.resource.slug
            logging.info(f"Wrapping an existing OAK implementation to fetch {slug}")
            inner_oi = get_implementation_from_shorthand(slug)
            self.wrapped_adapter = inner_oi
        # delegation magic
        methods = dict(inspect.getmembers(self.wrapped_adapter))
        for m in self.delegated_methods:
            mn = m if isinstance(m, str) else m.__name__
            setattr(PoiImplementation, mn, methods[mn])
        self.build_index()

