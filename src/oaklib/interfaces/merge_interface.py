import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.utilities.basic_utils import pairs_as_dict, triples_as_dict
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.obograph_utils import merge_graphs


@dataclass
class MergeConfiguration:
    """
    Configuration for merging
    """

    allow_lossy_merge: bool = field(default=True)
    """
    If True, then merges are not guaranteed to include all information from all sources.
    """

    replace_entities: bool = field(default=False)
    """
    If True, then entities with the same IDs are replaced.
    """


class MergeInterface(BasicOntologyInterface, ABC):
    """
    An OntologyInterface that is capable of merging information from other interfaces.
    """

    def merge(
        self,
        sources: List[BasicOntologyInterface],
        configuration: Optional[MergeConfiguration] = None,
        **kwargs,
    ):
        """
        Merges from multiple sources into current adapter.

        :param sources:
        :param configuration:
        :param kwargs:
        :return:
        """
        if not configuration:
            configuration = MergeConfiguration()
        from oaklib.interfaces.obograph_interface import OboGraphInterface

        if isinstance(self, OboGraphInterface) and all(
            isinstance(s, OboGraphInterface) for s in sources
        ):
            self._merge_as_obograph(sources, configuration)
        else:
            self._merge_simple(sources, configuration)

    def _merge_simple(
        self, sources: List[BasicOntologyInterface], configuration: MergeConfiguration
    ):
        if not configuration.allow_lossy_merge:
            raise NotImplementedError("Cannot handle non-lossy merge")
        for source in sources:
            logging.info(f"Merging from {type(source)}")
            for entity_it in chunk(source.entities()):
                entities = list(entity_it)
                labels = pairs_as_dict(source.labels(entities))
                relationships = triples_as_dict(source.relationships(entities))
                for e in entities:
                    self.create_entity(
                        e,
                        label=labels[e][0],
                        relationships=pairs_as_dict(relationships.get(e, [])),
                        replace=configuration.replace_entities,
                    )

    def _merge_as_obograph(
        self, sources: List[BasicOntologyInterface], configuration: MergeConfiguration
    ):
        from oaklib.interfaces.obograph_interface import OboGraphInterface

        if not isinstance(self, OboGraphInterface):
            raise AssertionError(f"Expected OboGraphInterface {type(self)}")
        target_graph = self.as_obograph()
        for source in sources:
            if not isinstance(source, OboGraphInterface):
                raise AssertionError(f"Expected OboGraphInterface {type(source)}")
            target_graph = merge_graphs(
                target_graph, source.as_obograph(), replace=configuration.replace_entities
            )
        self.load_graph(target_graph, replace=True)
