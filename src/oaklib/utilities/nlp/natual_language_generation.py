from dataclasses import dataclass
from typing import List

import oaklib.datamodels.obograph as og
from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import (
    IN_TAXON,
    IS_A,
    NEVER_IN_TAXON,
    ONLY_IN_TAXON,
    PART_OF,
)
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE

TEXT = str


PREDICATE_TO_TEXT = {
    IS_A: "is a kind of",
    PART_OF: "is part of",
    ONLY_IN_TAXON: "is only found in",
    IN_TAXON: "is only found in",
    NEVER_IN_TAXON: "is never found in",
}


@dataclass
class NaturalLanguageGenerator:
    """
    Generates natural language sentences
    """

    ontology_interface: BasicOntologyInterface
    mask_symbol: str = "[MASK]"

    def render_texts(self, texts: List[TEXT]) -> TEXT:
        texts = [f"{text}." for text in texts]
        return "\n".join(texts)

    def render_entity(self, subject: CURIE) -> TEXT:
        """
        Generate a natural language text description of an entity such as an ontology term

        Text is generated from both logical axioms (edges) and existing textual information
        (such as text definitions and synonyms)

        :param subject:
        :return:
        """
        oi = self.ontology_interface
        texts = []
        lbl = self.render_node_reference(subject)
        texts.append(f"{lbl} has the identifier {subject}")
        defn = oi.definition(subject)
        if defn:
            texts.append(f"{lbl} is defined as {defn}")
        for a in oi.entity_aliases(subject):
            texts.append(f"{lbl} is also known as {a}")
        if isinstance(oi, OboGraphInterface):
            for ldef in oi.logical_definitions([subject]):
                texts.append(self.render_logical_definition(ldef))
            for e in oi.outgoing_relationships(subject):
                texts.append(self.render_edge(og.Edge(subject, *e)))
        return self.render_texts(texts)

    def render_edge(self, edge: og.Edge) -> TEXT:
        """
        Generate natural language text from an edge

        :param edge:
        :return:
        """
        s = self.render_node_reference(edge.sub)
        p = self.render_predicate(edge.pred)
        o = self.render_node_reference(edge.obj)
        return f"every {s} {p} a {o}"

    def render_logical_definition(self, ldef: og.LogicalDefinitionAxiom) -> TEXT:
        """
        Generate natural language text from an edge

        :param ldef:
        :return:
        """
        s = self.render_node_reference(ldef.definedClassId)
        gs = [self.render_node_reference(g) for g in ldef.genusIds]
        genus = " and ".join(gs)
        rs = [
            f"{self.render_predicate(r.propertyId)} a {self.render_node_reference(r.fillerId)}"
            for r in ldef.restrictions
        ]
        rs_str = " and ".join(rs)
        return f"{s} is equivalent to a {genus} that {rs_str}"

    def render_predicate(self, predicate_id: PRED_CURIE) -> TEXT:
        if predicate_id in PREDICATE_TO_TEXT:
            return PREDICATE_TO_TEXT[predicate_id]
        else:
            return self.render_node_reference(predicate_id)

    def render_node_reference(self, node_id: CURIE) -> TEXT:
        lbl = self.ontology_interface.label(node_id)
        if lbl:
            return lbl
        else:
            return node_id
