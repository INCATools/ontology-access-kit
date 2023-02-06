import inspect
import logging
from dataclasses import dataclass, field

from oaklib import OntologyResource
from oaklib.implementations.poi.poi_implementation import PoiImplementation


@dataclass
class PickledPoiImplementation(PoiImplementation):
    """
    A BitwiseImplementation that is restored from a pickled index.

    To create an index on the command line:

    .. code-block:: bash

        runoak -i poi:sqlite:obo:hp dump -o /tmp/hp.pkl

    To retrieve:

    .. code-block:: base

        runoak -i pickledpoi:/tmp/hp.pkl termset-similarity HP:0000023 HP:0000024 HP:0000013 @ HP:0000016 HP:0000036
    """
    pickle_path: str = None

    def __post_init__(self):
        if self.pickle_path is None:
            self.pickle_path = self.resource.slug
        self.load(self.pickle_path)
        resource = OntologyResource(slug=self.ontology_index.source)
        from oaklib.selector import get_implementation_from_shorthand

        slug = resource.slug
        logging.info(f"Wrapping an existing OAK implementation to fetch {slug}")
        inner_oi = get_implementation_from_shorthand(slug)
        self.wrapped_adapter = inner_oi
        # delegation magic
        methods = dict(inspect.getmembers(self.wrapped_adapter))
        for m in self.delegated_methods:
            mn = m if isinstance(m, str) else m.__name__
            setattr(PoiImplementation, mn, methods[mn])
