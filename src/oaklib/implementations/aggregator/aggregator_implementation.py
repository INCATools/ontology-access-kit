import logging
from collections import defaultdict
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple, Type

from sssom_schema import Mapping

from oaklib.datamodels.obograph import Node
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.datamodels.validation_datamodel import (
    ValidationConfiguration,
    ValidationResult,
)
from oaklib.interfaces.association_provider_interface import AssociationProviderInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    DEFINITION,
    PRED_CURIE,
    RELATIONSHIP_MAP,
    BasicOntologyInterface,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TEXT, TextAnnotatorInterface
from oaklib.interfaces.usages_interface import UsagesInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, SUBSET_CURIE


@dataclass
class AggregatorImplementation(
    AssociationProviderInterface,
    ValidatorInterface,
    RdfInterface,
    RelationGraphInterface,
    OboGraphInterface,
    SearchInterface,
    MappingProviderInterface,
    TextAnnotatorInterface,
    UsagesInterface,
):
    """
    An OAK adapter that wraps multiple implementations and integrates results together.

    This allows for multiple implementations to be wrapped, with calls to
    the aggregator farming out queries to multiple implementations, and weaving
    the results together.

    Example:

        >>> from oaklib import get_adapter
        >>> from oaklib.implementations import AggregatorImplementation
        >>> from oaklib.datamodels.search import SearchConfiguration, SearchTermSyntax
        >>> hp = get_adapter("sqlite:obo:hp")
        >>> mp = get_adapter("sqlite:obo:mp")
        >>> cfg = SearchConfiguration(syntax=SearchTermSyntax.REGULAR_EXPRESSION)
        >>> agg = AggregatorImplementation(implementations=[hp, mp])
        >>> for entity in sorted(agg.basic_search("parathyroid", config=cfg)):
        ...     print(entity, agg.label(entity))
        <BLANKLINE>
        ...
        HP:0000860 Parathyroid hypoplasia
        ...
        MP:0000680 absent parathyroid glands
        ...

    Command Line Usage
    ------------------

    Use the :code:`--add` (:code:`-a`) option before the main command to add additional implementations.

    E.g

    .. code::

        runoak -i db/mp.db -a db/hp.db COMMAND [COMMAND OPTIONS]


    """

    implementations: List[BasicOntologyInterface] = None

    @property
    def implementation_name(self):
        impl_names = []
        for i in self.implementations:
            impl_names.append(i.implementation_name)
        return "-".join(impl_names)

    def _delegate_iterator(
        self, func: Callable, interface: Optional[Type[BasicOntologyInterface]] = None
    ) -> Iterator:
        for i in self.implementations:
            if interface is None or isinstance(i, interface):
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

    def relationships(self, *args, **kwargs) -> Iterable[CURIE]:
        return self._delegate_iterator(lambda i: i.relationships(*args, **kwargs))

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._delegate_iterator(lambda i: i.simple_mappings_by_curie(curie))

    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        return self._delegate_iterator(
            lambda i: i.get_sssom_mappings_by_curie(curie), MappingProviderInterface
        )

    def sssom_mappings(self, *args, **kwargs) -> Iterable[Mapping]:
        return self._delegate_iterator(
            lambda i: i.sssom_mappings(*args, **kwargs), MappingProviderInterface
        )

    def label(self, curie: CURIE, **kwargs) -> str:
        return self._delegate_first(lambda i: i.label(curie, **kwargs))

    def set_label(self, curie: CURIE, label: str) -> None:
        logging.debug(f"Assuming {curie} is in first aggregated resource, label={label}")
        return self._delegate_first(lambda i: i.set_label(curie, label))

    def curies_by_label(self, label: str) -> List[CURIE]:
        return list(self._delegate_iterator(lambda i: i.curies_by_label(label)))

    def definition(self, curie: CURIE, **kwargs) -> str:
        return self._delegate_first(lambda i: i.definition(curie, **kwargs))

    def definitions(self, curies: Iterable[CURIE], **kwargs) -> Iterator[DEFINITION]:
        return self._delegate_iterator(lambda i: i.definitions(curies, **kwargs))

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

    def associations(self, *args, **kwargs) -> Iterable[CURIE]:
        return self._delegate_iterator(
            lambda i: i.associations(*args, **kwargs), AssociationProviderInterface
        )

    def annotate_text(
        self, text: TEXT, configuration: Optional[TextAnnotationConfiguration] = None
    ) -> Iterable[TextAnnotation]:
        return self._delegate_iterator(lambda i: i.annotate_text(text, configuration))

    def annotate_file(
        self,
        text_file: TextIOWrapper,
        configuration: TextAnnotationConfiguration = None,
    ) -> Iterator[TextAnnotation]:
        return self._delegate_iterator(lambda i: i.annotate_file(text_file, configuration))
