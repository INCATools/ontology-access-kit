import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import rdflib
from linkml_runtime.dumpers import json_dumper

from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.fhir import CodeSystem, Concept, ConceptProperty
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.datamodels.vocabulary import (
    HAS_BROAD_SYNONYM,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_RELATED_SYNONYM,
)
from oaklib.types import CURIE
from oaklib.utilities.obograph_utils import index_graph_edges_by_subject

TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Any]

DIRECT_PREDICATE_MAP = {
    "is_a": "parent",
}

SCOPE_MAP = {
    "hasBroadSynonym": HAS_BROAD_SYNONYM,
    "hasExactSynonym": HAS_EXACT_SYNONYM,
    "hasNarrowSynonym": HAS_NARROW_SYNONYM,
    "hasRelatedSynonym": HAS_RELATED_SYNONYM,
}


def _escape(s: str) -> str:
    return s.replace('"', '\\"').replace("\n", "\\n")


@dataclass
class OboGraphToFHIRConverter(DataModelConverter):
    """Converts from OboGraph to FHIR."""

    def dump(self, source: GraphDocument, target: str = None) -> None:
        """
        Dump an OBO Graph Document to a FHIR CodeSystem

        :param source:
        :param target:
        :return:
        """
        cs = self.convert(source)
        json_str = json_dumper.dumps(cs)
        if target is None:
            print(json_str)
        else:
            with open(target, "w", encoding="UTF-8") as f:
                f.write(json_str)

    def convert(self, source: GraphDocument, target: CodeSystem = None) -> CodeSystem:
        """
        Convert an OBO Graph Document to a FHIR CodingSystem

        :param source:
        :param target: if None, one will be created
        :return:
        """
        if target is None:
            target = CodeSystem()
        target.resourceType = CodeSystem.__name__
        for g in source.graphs:
            self._convert_graph(g, target=target)
        return target

    def code(self, uri: CURIE) -> str:
        if not self.curie_converter:
            return uri
        curie = self.curie_converter.compress(uri)
        if curie is None:
            return uri
        else:
            return curie

    def _convert_graph(self, source: Graph, target: CodeSystem) -> CodeSystem:
        target.id = source.id
        edges_by_subject = index_graph_edges_by_subject(source)
        for n in source.nodes:
            logging.debug(f"Converting node {n.id}")
            self._convert_node(n, index=edges_by_subject, target=target)
        return target

    def _convert_node(
        self, source: Node, index: Dict[CURIE, List[Edge]], target: CodeSystem
    ) -> Concept:
        id = self.code(source.id)
        logging.debug(f"Converting node {id} from {source}")
        concept = Concept(code=id, display=source.lbl)
        target.concept.append(concept)
        if source.meta:
            self._convert_meta(source, concept)
        for e in index.get(source.id, []):
            obj = self.code(e.obj)
            if e.pred in DIRECT_PREDICATE_MAP:
                concept.property.append(
                    ConceptProperty(code=DIRECT_PREDICATE_MAP[e.pred], valueCode=obj)
                )
        return concept

    def _convert_meta(self, source: Node, concept: Concept):
        meta = source.meta
        if meta.definition:
            # xrefs = ", ".join(meta.definition.xrefs)
            concept.definition = meta.definition.val
