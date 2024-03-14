from dataclasses import dataclass, field
from typing import Collection, Dict, Optional

from oaklib.datamodels.obograph import Edge, Graph, Node
from oaklib.transformers.graph_transformer import GraphTransformer
from oaklib.types import PRED_CURIE
from oaklib.utilities.obograph_utils import index_graph_nodes


@dataclass
class Labeler:
    """
    Generates labels and ids for generated nodes
    """

    code: str
    label: str = None
    separator: str = field(default="-")

    def generate(self, node: Node) -> Node:
        """
        Generates a label for a node

        :param node:
        :return:
        """
        if self.label is not None:
            label = self.label
        else:
            label = f"{node.lbl} ({self.code})"
        sep = self.separator
        id = f"{node.id}{sep}{self.code}"
        new_node = Node(id=id, lbl=label, type="CLASS")
        return new_node


@dataclass
class SEPTransformer(GraphTransformer):
    """
    An ontology graph transformer that maps an ontology to a generalized SEP pattern.

    The SEP (Structured-Entities-Parts) pattern is used for partonomies and represents each
    entity E as a triad of terms (S, E, P):

    - S is the union of E and P
    - E is the entity
    - P is a grouping for all parts of E

    The result is a diamond shape, where E is the top node, and S and P are the bottom nodes;
    all the (proper) parts of E are listed under P, and all the subclasses of E are listed under S.

    This transformer implements a generalization of this that generates R1, R2, ... Rn
    nodes for each predicate, in addition to the E node
    """

    structure_labeler: Optional[Labeler] = None
    entity_labeler: Optional[Labeler] = None
    relationship_labelers: Optional[Dict[PRED_CURIE, Labeler]] = None

    include_predicates: Optional[Collection[PRED_CURIE]] = None
    """A collection of predicates to include"""

    make_entity_top_node: Optional[bool] = field(default=True)
    """If true, makes the entity node the top node in the graph"""

    def transform(self, source_ontology: Graph, **kwargs) -> Graph:
        """
        Filters edges from a graph.

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> from oaklib.transformers.sep_transformer import SEPTransformer
        >>> from oaklib.datamodels.vocabulary import PART_OF
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> graph = adapter.as_obograph()
        >>> transformer = SEPTransformer(include_predicates=[PART_OF])
        >>> filtered_graph = transformer.transform(graph)
        >>> nucleus = "GO:0005634"
        >>> nuc_edges = [(e.sub, e.obj) for e in filtered_graph.edges if nucleus in [e.sub, e.obj]]
        >>> for e in sorted(nuc_edges):
        ...    print(e)
        ('GO:0005634', 'GO:0043231-SUB')
        ('GO:0005634-BFO:0000050', 'GO:0005634')
        ('GO:0005634-SUB', 'GO:0005634')

        :param source_ontology:
        :return:

        """
        subsumption_pred = "is_a"
        make_entity_top_node = self.make_entity_top_node
        structure_labeler = self.structure_labeler
        entity_labeler = self.entity_labeler
        nix = index_graph_nodes(source_ontology)
        include_predicates = self.include_predicates
        if structure_labeler is None:
            structure_labeler = Labeler(code="S")
        if entity_labeler is None:
            if make_entity_top_node:
                code = "SUB"
            else:
                code = "E"
            entity_labeler = Labeler(code=code)
        relationship_labelers = self.relationship_labelers
        if relationship_labelers is None:
            relationship_labelers = {}
        for edge in source_ontology.edges:
            pred = edge.pred
            if pred not in relationship_labelers:
                relationship_labelers[pred] = Labeler(code=pred)
        new_edges = []
        new_node_map = {}

        def add_node(n: Node):
            if n.id not in new_node_map:
                new_node_map[n.id] = n

        upper_node_map = {}  # diamond parents
        lower_node_map = {}  # diamond children
        for node in source_ontology.nodes:
            # ensure all original nodes are preserved
            add_node(node)
            if node.type != "CLASS":
                continue
            structure_node = structure_labeler.generate(node)
            entity_node = entity_labeler.generate(node)
            if make_entity_top_node:
                upper_node_map[node.id] = node  # e.g. Nucleus
                lower_node_map[node.id] = entity_node  # e.g. NucleusSubtype
            else:
                upper_node_map[node.id] = structure_node  # e.g. NucleusStructure
                lower_node_map[node.id] = node  # e.g. Nucleus

        for edge in source_ontology.edges:
            pred = edge.pred
            if include_predicates is not None:
                if pred != subsumption_pred and pred not in include_predicates:
                    continue
            orig_parent_node_id = edge.obj
            orig_child_node_id = edge.sub
            upper_node = upper_node_map.get(orig_parent_node_id, None)
            if upper_node is None:
                continue
            e_node = lower_node_map.get(orig_parent_node_id, None)
            if e_node is None:
                continue
            # E is_a S (e.g. Nucleus is_a NucleusStructure)
            new_edges.append((e_node.id, subsumption_pred, upper_node.id))
            orig_parent_node = nix.get(orig_parent_node_id, None)
            if orig_parent_node is None:
                continue
            if pred == subsumption_pred:
                new_edges.append((orig_child_node_id, subsumption_pred, e_node.id))
                add_node(e_node)
            else:
                # e.g. NucleusPart
                p_node = relationship_labelers[pred].generate(orig_parent_node)
                # P is_a S (e.g. NucleusPart is_a NucleusStructure)
                new_edges.append((p_node.id, subsumption_pred, upper_node.id))
                new_edges.append((orig_child_node_id, subsumption_pred, p_node.id))
                add_node(p_node)
        edges = [Edge(sub=s, pred=p, obj=o) for s, p, o in set(new_edges)]
        return Graph(id=source_ontology.id, nodes=list(new_node_map.values()), edges=edges)
