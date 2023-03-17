import logging
import sys
from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import Any, Dict, List, Tuple

import rdflib

from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.datamodels.vocabulary import IS_A, SYNONYM_PRED_TO_SCOPE_MAP
from oaklib.implementations.simpleobo.simple_obo_parser import (
    TAG_DEFINITION,
    TAG_INTERSECTION_OF,
    TAG_INVERSE_OF,
    TAG_IS_A,
    TAG_NAME,
    TAG_RELATIONSHIP,
    TAG_SUBSET,
    TAG_SYNONYM,
    TAG_XREF,
    OboDocument,
    Stanza,
)
from oaklib.types import CURIE
from oaklib.utilities.oboformat_utils import subset_to_shorthand
from oaklib.utilities.obograph_utils import index_graph_edges_by_subject

TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Any]

DIRECT_PREDICATE_MAP = {
    "is_a": TAG_IS_A,
    IS_A: TAG_IS_A,  # sometime obographs use the predicate rather than shorthand
    "subPropertyOf": TAG_IS_A,
    "inverseOf": TAG_INVERSE_OF,
}

typedef_type_map = {
    "CLASS": "Term",
    "PROPERTY": "Typedef",
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
            obodoc.dump(sys.stdout)
        else:
            with open(target, "w", encoding="UTF-8") as f:
                obodoc.dump(f)

    def dumps(self, source: GraphDocument, **kwargs) -> str:
        """
        Dump an OBO Graph Document to a string

        :param source:
        :return:
        """
        obodoc = self.convert(source)
        io = StringIO()
        obodoc.dump(io)
        return io.getvalue()

    def as_bytes_io(self, source: GraphDocument, **kwargs) -> BytesIO:
        """
        Dump an OBO Graph Document to a string

        :param source:
        :return:
        """
        s = self.dumps(source)
        return BytesIO(s.encode("UTF-8"))

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
        for lda in source.logicalDefinitionAxioms:
            defined_class_id = self._id(lda.definedClassId)
            if defined_class_id not in target.stanzas:
                target.add_stanza(Stanza(id=defined_class_id, type="Term"))
            stanza = target.stanzas[defined_class_id]
            for g in lda.genusIds:
                obj = self._id(g)
                stanza.add_tag_value(TAG_INTERSECTION_OF, obj)
            for r in lda.restrictions:
                filler = self._id(r.fillerId)
                pred = self._id(r.propertyId)
                stanza.add_tag_value_pair(TAG_INTERSECTION_OF, pred, filler)
        return target

    def _convert_node(
        self, source: Node, index: Dict[CURIE, List[Edge]], target: OboDocument
    ) -> None:
        id = self._id(source.id)
        logging.debug(f"Converting node {id} from {source}")
        t = source.type
        # if not t:
        #    logging.warning(f"No type for {id}")
        #    return
        if id.startswith("oio:"):
            return
        typedef_type = typedef_type_map.get(t, None)
        if not typedef_type:
            return
        stanza = Stanza(id=id, type=typedef_type)
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
        return

    def _convert_meta(self, source: Node, target: Stanza):
        meta = source.meta
        logging.debug(f"ADDING DEF {target}")
        if meta.definition:
            xrefs = ", ".join(meta.definition.xrefs)
            target.add_tag_value(TAG_DEFINITION, f'"{_escape(meta.definition.val)}" [{xrefs}]')
        if meta.xrefs:
            for x in meta.xrefs:
                target.add_tag_value(TAG_XREF, x.val)
        for x in meta.subsets:
            target.add_tag_value(TAG_SUBSET, subset_to_shorthand(x))
        for s in meta.synonyms:
            xrefs = ", ".join(s.xrefs)
            scope = SYNONYM_PRED_TO_SCOPE_MAP[f"oio:{s.pred}"]
            target.add_tag_value(TAG_SYNONYM, f'"{_escape(s.val)}" {scope} [{xrefs}]')
