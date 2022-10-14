from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from sssom_schema import Mapping

from oaklib.datamodels.obograph import Node
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.validation_datamodel import (
    ValidationConfiguration,
    ValidationResult,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    PRED_CURIE,
    RELATIONSHIP_MAP,
    BasicOntologyInterface,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, SUBSET_CURIE


@dataclass
class AggregatorImplementation(
    ValidatorInterface,
    RdfInterface,
    RelationGraphInterface,
    OboGraphInterface,
    SearchInterface,
    MappingProviderInterface,
):
    """
    Wraps multiple implementations and integrates results together.

    This allows for multiple implementations to be wrapped, with calls to
    the aggregator farming out queries to multiple implementations, and weaving
    the results together.

    Documentation:

    - `Aggregator Implementation <https://incatools.github.io/ontology-access-kit/implementations/aggregator.html>`_
    """

    implementations: List[BasicOntologyInterface] = None

    def _delegate_iterator(self, func: Callable) -> Iterable:
        for i in self.implementations:
            for v in func(i):
                yield v

    def _delegate_simple_tuple_map(self, func: Callable, strict=False) -> Dict[Any, List[Any]]:
        m = defaultdict(list)
        for i in self.implementations:
            for k, vs in func(i).items():
                m[k] += vs
        return m

    def _delegate_first(self, func: Callable, strict=False) -> Optional[Any]:
        for i in self.implementations:
            v = func(i)
            if v is not None:
                return v
        if strict:
            raise ValueError(f"No value for {func}")

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        return self._delegate_iterator(lambda i: i.basic_search(search_term, config=config))

    def validate(self, configuration: ValidationConfiguration = None) -> Iterable[ValidationResult]:
        return self._delegate_iterator(lambda i: i.validate())

    def entities(self, **kwargs) -> Iterable[CURIE]:
        return self._delegate_iterator(lambda i: i.entities(**kwargs))

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._delegate_iterator(lambda i: i.simple_mappings_by_curie(curie))

    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        return self._delegate_iterator(lambda i: i.get_sssom_mappings_by_curie(curie))

    def label(self, curie: CURIE) -> str:
        return self._delegate_first(lambda i: i.label(curie))

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        return self._delegate_simple_tuple_map(lambda i: i.entity_alias_map(curie))

    def subsets(self) -> Iterable[SUBSET_CURIE]:
        return self._delegate_iterator(lambda i: i.subsets())

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        return self._delegate_iterator(lambda i: i.subset_members(subset))

    def node(self, curie: CURIE, strict=False) -> Node:
        # TODO: this implementation is ad-hoc
        # return the first node that has a label populated
        node: Node = None
        for i in self.implementations:
            if isinstance(i, OboGraphInterface):
                node = i.node(curie)
                if node.lbl:
                    return node
        return node

    def outgoing_relationship_map(self, curie: CURIE) -> RELATIONSHIP_MAP:
        return self._delegate_simple_tuple_map(lambda i: i.outgoing_relationship_map(curie))

    def incoming_relationship_map(self, curie: CURIE) -> RELATIONSHIP_MAP:
        return self._delegate_simple_tuple_map(lambda i: i.incoming_relationship_map(curie))
