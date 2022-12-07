import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import rdflib

from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.datamodels.vocabulary import (
    HAS_BROAD_SYNONYM,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_RELATED_SYNONYM,
)
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_DEFINITION,
    TAG_INVERSE_OF,
    TAG_IS_A,
    TAG_NAME,
    TAG_RELATIONSHIP,
    OboDocument,
    Stanza,
)
from oaklib.types import CURIE
from oaklib.utilities.obograph_utils import index_graph_edges_by_subject

TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Any]

DIRECT_PREDICATE_MAP = {
    "is_a": TAG_IS_A,
    "subPropertyOf": TAG_IS_A,
    "inverseOf": TAG_INVERSE_OF,
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
class OboGraphToOboFormatConverter(DataModelConverter):
    """Converts from OboGraph to OBO Format."""

    def dump(self, source: GraphDocument, target: str = None, **kwargs) -> None:
        """
        Dump an OBO Graph Document to a FHIR CodeSystem

        :param source:
        :param target:
        :return:
        """
        obodoc = self.convert(source)
        if target is None:
            print(obodoc.dump())
        else:
            with open(target, "w", encoding="UTF-8") as f:
                obodoc.dump(f)

    def convert(self, source: GraphDocument, target: OboDocument = None, **kwargs) -> OboDocument:
        """
        Convert an OBO Format Document.

        :param source:
        :param target: if None, one will be created
        :return:
        """
        if target is None:
            target = OboDocument()
        for g in source.graphs:
            self._convert_graph(g, target=target)
        return target

    def _id(self, uri: CURIE) -> CURIE:
        if not self.curie_converter:
            return uri
        curie = self.curie_converter.compress(uri)
        if curie is None:
            return uri
        else:
            return curie

    def _convert_graph(self, source: Graph, target: OboDocument) -> OboDocument:
        edges_by_subject = index_graph_edges_by_subject(source)
        for n in source.nodes:
            logging.debug(f"Converting node {n.id}")
            self._convert_node(n, index=edges_by_subject, target=target)
        return target

    def _convert_node(
        self, source: Node, index: Dict[CURIE, List[Edge]], target: OboDocument
    ) -> OboDocument:
        id = self._id(source.id)
        logging.debug(f"Converting node {id} from {source}")
        stanza = Stanza(id=id, type="Term")
        target.add_stanza(stanza)
        if source.lbl:
            stanza.add_tag_value(TAG_NAME, source.lbl)
        if source.meta:
            self._convert_meta(source, target=stanza)
        for e in index.get(source.id, []):
            obj = self._id(e.obj)
            pred = self._id(e.pred)
            if e.pred in DIRECT_PREDICATE_MAP:
                stanza.add_tag_value(DIRECT_PREDICATE_MAP[e.pred], obj)
            else:
                stanza.add_tag_value(TAG_RELATIONSHIP, f"{pred} {obj}")
        return target

    def _convert_meta(self, source: Node, target: Stanza):
        meta = source.meta
        if meta.definition:
            xrefs = ", ".join(meta.definition.xrefs)
            target.add_tag_value(TAG_DEFINITION, f'"{_escape(meta.definition.val)}" [{xrefs}]')
