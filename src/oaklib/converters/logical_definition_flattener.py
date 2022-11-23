from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, List, Union

from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.obograph import Graph, GraphDocument, LogicalDefinitionAxiom
from oaklib.types import CURIE

DEFINE_CLASS_FIELD = "defined_class"
GENUS_CLASS_FIELD = "genus_class"


@dataclass(eq=False)
class LogicalDefinitionFlattener(DataModelConverter):
    """Flattens logical definitions to tuples for use in template libraries."""

    def convert(
        self, source: Union[LogicalDefinitionAxiom, Graph, GraphDocument], target: Any = None
    ) -> Union[dict, List[dict]]:
        """
        Convert a logical definition axiom or a graph including logical definition axioms.

        :param source: graph or axiom
        :return:
        """
        if isinstance(source, Graph):
            return [self.convert(lda) for lda in source.logicalDefinitionAxioms]
        if isinstance(source, GraphDocument):
            return [
                self.convert(lda)
                for graph in source.graphs
                for lda in graph.logicalDefinitionAxioms
            ]
        obj = {
            DEFINE_CLASS_FIELD: source.definedClassId,
        }
        if len(source.genusIds) == 1:
            obj[GENUS_CLASS_FIELD] = source.genusIds[0]
        else:
            for i in range(0, len(source.genusIds)):
                obj[f"{GENUS_CLASS_FIELD}_{i+1}"] = source.genusIds[i]
        prop_dict = defaultdict(list)
        for restriction in source.restrictions:
            prop = self._curie(restriction.propertyId)
            prop = self._property_label(prop).replace(" ", "_").replace(":", "_")
            prop_dict[prop].append(restriction.fillerId)
        for prop, values in prop_dict.items():
            if len(values) == 1:
                obj[prop] = values[0]
            else:
                for i in range(0, len(values)):
                    obj[f"{prop}_{i+1}"] = values[i]
        obj = {k: self._curie(v) for k, v in obj.items()}
        return obj

    def _curie(self, iri: str) -> CURIE:
        curie = self.curie_converter.compress(iri)
        return curie if curie else iri

    @lru_cache
    def _property_label(self, predicate: CURIE) -> str:
        lbl = self.labeler(predicate) if self.labeler else None
        return lbl if lbl else predicate
