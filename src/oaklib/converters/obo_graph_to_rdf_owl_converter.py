from dataclasses import dataclass
from typing import Any, Tuple, Union

import rdflib
from rdflib import OWL, RDFS

from oaklib import BasicOntologyInterface
from oaklib.converters.data_model_converter import DataModelConverter
from oaklib.datamodels.obograph import (
    RDF,
    Edge,
    Graph,
    GraphDocument,
    Meta,
    Node,
    PropertyValue,
)
from oaklib.datamodels.vocabulary import (
    HAS_BROAD_SYNONYM,
    HAS_DBXREF,
    HAS_DEFINITION_URI,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_RELATED_SYNONYM,
)
from oaklib.types import CURIE

TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Any]

DIRECT_PREDICATE_MAP = {
    "is_a": RDFS.subClassOf,
    "subPropertyOf": RDFS.subPropertyOf,
    "inverseOf": OWL.inverseOf,
}

SCOPE_MAP = {
    "hasBroadSynonym": HAS_BROAD_SYNONYM,
    "hasExactSynonym": HAS_EXACT_SYNONYM,
    "hasNarrowSynonym": HAS_NARROW_SYNONYM,
    "hasRelatedSynonym": HAS_RELATED_SYNONYM,
}


@dataclass
class OboGraphToRdfOwlConverter(DataModelConverter):
    """Converts from OboGraph to OWL layered on RDF."""

    def dump(self, source: GraphDocument, target: str = None) -> None:
        """
        Dump an OBO Graph Document to a FHIR CodeSystem

        :param source:
        :param target:
        :return:
        """
        g = self.convert(source)
        if target is None:
            print(g.serialize(format="turtle"))
        else:
            g.serialize(format="turtle", destination=target)

    def convert(self, source: GraphDocument, target: rdflib.Graph = None) -> rdflib.Graph:
        """
        Convert an OBO GraphDocument.

        :param source:
        :param target: if None, one will be created
        :return:
        """
        if target is None:
            target = rdflib.Graph()
        for g in source.graphs:
            self._convert_graph(g, target=target)
        return target

    def _convert_graph(self, source: Graph, target: rdflib.Graph) -> rdflib.Graph:
        for n in source.nodes:
            self._convert_node(n, target=target)
        for e in source.edges:
            self._convert_edge(e, target=target)
        return target

    def _convert_node(self, source: Node, target: rdflib.Graph) -> rdflib.Graph:
        uri = self._uri_ref(source.id)
        if not source.type or source.type == "CLASS":
            target.add((uri, RDF.type, OWL.Class))
        if source.lbl:
            target.add((uri, RDFS.label, rdflib.Literal(source.lbl)))
        if source.meta:
            self._convert_meta(uri, source.meta, target=target)
        return target

    def _convert_meta(self, uri: rdflib.URIRef, source: Meta, target: rdflib.Graph) -> rdflib.Graph:
        if source.definition:
            self._add_statement(uri, HAS_DEFINITION_URI, source.definition, target=target)
        for x in source.xrefs:
            self._add_statement(uri, HAS_DBXREF, x, target=target)
        for x in source.synonyms:
            pred = SCOPE_MAP[x.pred]
            self._add_statement(uri, pred, x, target=target)
        return target

    def _convert_edge(self, source: Edge, target: rdflib.Graph) -> rdflib.Graph:
        subject = self._uri_ref(source.sub)
        object = self._uri_ref(source.obj)
        if source.pred in DIRECT_PREDICATE_MAP:
            target.add((subject, DIRECT_PREDICATE_MAP[source.pred], object))
        else:
            bnode = rdflib.BNode()
            target.add((subject, RDFS.subClassOf, bnode))
            target.add((bnode, RDF.type, OWL.Restriction))
            target.add((bnode, OWL.onProperty, self._uri_ref(source.pred)))
            target.add((bnode, OWL.someValuesFrom, object))
        return target

    def _add_statement(
        self,
        uri: rdflib.URIRef,
        pred: Union[str, rdflib.URIRef],
        pv: PropertyValue,
        target: rdflib.Graph,
    ):
        if not isinstance(pred, rdflib.URIRef):
            pred = self._uri_ref(pred)
        triple = uri, pred, rdflib.Literal(pv.val)
        target.add(triple)
        for x in pv.xrefs:
            self._add_reified(triple, HAS_DBXREF, x, target=target)

    def _add_reified(
        self, triple: TRIPLE, pred: Union[str, rdflib.URIRef], val: Any, target: rdflib.Graph
    ):
        if not isinstance(pred, rdflib.URIRef):
            pred = self._uri_ref(pred)
        bnode = rdflib.BNode()
        target.add((bnode, RDF.type, OWL.Axiom))
        target.add((bnode, OWL.annotatedSource, triple[0]))
        target.add((bnode, OWL.annotatedProperty, triple[1]))
        target.add((bnode, OWL.annotatedTarget, triple[2]))
        target.add((bnode, pred, rdflib.Literal(val)))
        target.add((pred, RDF.type, OWL.AnnotationProperty))

    def _uri_ref(self, curie: CURIE) -> rdflib.URIRef:
        if self.curie_converter is None:
            self.curie_converter = BasicOntologyInterface().converter
        uri = self.curie_converter.expand(curie)
        if uri is None:
            uri = curie
        return rdflib.URIRef(uri)
