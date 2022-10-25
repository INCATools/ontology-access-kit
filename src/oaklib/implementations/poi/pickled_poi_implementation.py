import inspect
import logging
import math
import pickle
from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar, List, Iterable, Dict, Iterator, Union, Tuple

from oaklib.constants import OAKLIB_MODULE
from oaklib.datamodels import obograph, ontology_metadata
from oaklib.datamodels.association import Association
from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.similarity import TermPairwiseSimilarity, TermSetPairwiseSimilarity, TermInfo
from oaklib.datamodels.vocabulary import (
    ALL_MATCH_PREDICATES,
    DEPRECATED_PREDICATE,
    DISJOINT_WITH,
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    HAS_EXACT_SYNONYM,
    HAS_SYNONYM_TYPE,
    IN_CATEGORY_PREDS,
    IN_SUBSET,
    IS_A,
    LABEL_PREDICATE,
    OWL_NOTHING,
    OWL_THING,
    RDF_TYPE,
    SEMAPV,
    SYNONYM_PREDICATES,
    omd_slots, PART_OF,
)
from oaklib.implementations.poi.poi_implementation import PoiImplementation
from oaklib.implementations.poi.intset_ontology_index import IntSetOntologyIndex
from oaklib.implementations.poi.bitwise_utils import bitmap_from_list, BITMAP, POS, map_bitmap_to_ints, \
    bitmap_cardinality
from oaklib.implementations.sqldb import SEARCH_CONFIG
from oaklib.interfaces import SubsetterInterface, TextAnnotatorInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    METADATA_MAP,
    PRED_CURIE,
    PREFIX_MAP,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
    BasicOntologyInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CATEGORY_CURIE, CURIE, SUBSET_CURIE
from oaklib.utilities.basic_utils import get_curie_prefix, pairs_as_dict




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

