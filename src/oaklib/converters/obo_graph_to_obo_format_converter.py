import logging
import sys
from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import Any, Dict, List, Optional, Tuple, Union

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

    use_shorthand: bool = True

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

    def dumps(
        self,
        source: Union[GraphDocument, Graph],
        aux_graphs: Optional[List[Graph]] = None,
        **kwargs,
    ) -> str:
        """
        Dump an OBO Graph Document to a string

        :param source:
        :return:
        """
        obodoc = self.convert(source, aux_graphs=aux_graphs)
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

    def convert(
        self,
        source: Union[GraphDocument, Graph],
        target: OboDocument = None,
        aux_graphs: Optional[List[Graph]] = None,
        **kwargs,
    ) -> OboDocument:
        """
        Convert an OBO Format Document.

        :param source:
        :param target: if None, one will be created
        :param aux_graphs: additional graphs to use for label lookup
        :return:
        """
        if target is None:
            target = OboDocument()
        if isinstance(source, Graph):
            source = GraphDocument(graphs=[source])
        for g in source.graphs:
            logging.info(f"Converting graph {g.id}, nodes: {len(g.nodes)}, edges: {len(g.edges)}")
            self._convert_graph(g, target=target, aux_graphs=aux_graphs)
        logging.info(f"Converted {len(target.stanzas)} stanzas")
        return target

    def _commentify(
        self, curie: CURIE, graph: Graph, aux_graphs: Optional[List[Graph]] = None
    ) -> str:
        graphs = [graph] + (aux_graphs or [])
        for g in graphs:
            for n in g.nodes:
                if n.id == curie and n.lbl:
                    return f"{curie} ! {n.lbl}"
        return curie

    def _id(self, uri_or_curie: CURIE) -> CURIE:
        if not self.curie_converter:
            return uri_or_curie
        return self.curie_converter.compress(uri_or_curie, passthrough=True)

    def _predicate_id(self, uri_or_curie: CURIE, target: OboDocument) -> CURIE:
        curie = self._id(uri_or_curie)
        return target.curie_to_shorthand_map.get(curie, curie)

    def _convert_graph(
        self, source: Graph, target: OboDocument, aux_graphs: Optional[List[Graph]] = None
    ) -> OboDocument:
        edges_by_subject = index_graph_edges_by_subject(source)
        for n in source.nodes:
            if n.type == "PROPERTY" and n.lbl:
                shorthand = n.lbl.replace(" ", "_")
                target.curie_to_shorthand_map[self._id(n.id)] = shorthand
        for n in source.nodes:
            logging.debug(f"Converting node {n.id}")
            self._convert_node(
                n, index=edges_by_subject, target=target, graph=source, aux_graphs=aux_graphs
            )
        for lda in source.logicalDefinitionAxioms:
            defined_class_id = self._id(lda.definedClassId)
            if defined_class_id not in target.stanzas:
                target.add_stanza(Stanza(id=defined_class_id, type="Term"))
            stanza = target.stanzas[defined_class_id]
            for g in lda.genusIds:
                obj = self._id(g)
                obj = self._commentify(obj, source, aux_graphs)
                stanza.add_tag_value(TAG_INTERSECTION_OF, obj)
            for r in lda.restrictions:
                filler = self._id(r.fillerId)
                filler = self._commentify(filler, source, aux_graphs)
                pred = self._id(r.propertyId)
                stanza.add_tag_value_pair(TAG_INTERSECTION_OF, pred, filler)
        return target

    def _convert_node(
        self,
        source: Node,
        index: Dict[CURIE, List[Edge]],
        target: OboDocument,
        graph: Graph = None,
        aux_graphs: Optional[List[Graph]] = None,
    ) -> None:
        id = self._id(source.id)
        shorthand_xref = None
        if id in target.curie_to_shorthand_map:
            shorthand_xref = id
            id = target.curie_to_shorthand_map[id]
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
        if shorthand_xref:
            stanza.add_tag_value(TAG_XREF, shorthand_xref)
        for e in index.get(source.id, []):
            obj = self._id(e.obj)
            obj_labeled = self._commentify(obj, graph, aux_graphs)
            pred = self._predicate_id(e.pred, target)
            if e.pred in DIRECT_PREDICATE_MAP:
                stanza.add_tag_value(DIRECT_PREDICATE_MAP[e.pred], f"{obj_labeled}")
            else:
                stanza.add_tag_value(TAG_RELATIONSHIP, f"{pred} {obj_labeled}")
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
