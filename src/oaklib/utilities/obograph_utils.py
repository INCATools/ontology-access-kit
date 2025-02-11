"""
Utilities for the OBOGraph Datamodel
------------------------------------

See :ref:`datamodels`

"""

import io
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from copy import copy, deepcopy
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, TextIO, Tuple, Union

import networkx as nx
import yaml
from curies import Converter
from linkml_runtime.dumpers import json_dumper
from pydantic import BaseModel

# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
from oaklib import conf as conf_package
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument, Node
from oaklib.datamodels.vocabulary import IS_A, PART_OF, RDF_TYPE
from oaklib.types import CURIE, PRED_CURIE

DEFAULT_STYLEMAP = "obograph-style.json"

# TODO: use the style map
DEFAULT_PREDICATE_CODE_MAP = {IS_A: "i", PART_OF: "p", RDF_TYPE: "t"}

PREDICATE_WEIGHT_MAP = Dict[PRED_CURIE, float]

PREDICATE_MAP = {"is_a": IS_A}


class TreeFormatEnum(Enum):
    markdown = "md"
    text = "text"


def graph_node_ids_from_subject_and_objects(g: Graph) -> List[CURIE]:
    node_ids = set()
    for edge in g.edges:
        node_ids.add(edge.sub)
        node_ids.add(edge.obj)
    return list(node_ids)


def remove_unlabeled_nodes(g: Union[GraphDocument, Graph], rescue_connected_nodes=True) -> None:
    if isinstance(g, GraphDocument):
        for graph in g.graphs:
            remove_unlabeled_nodes(graph, rescue_connected_nodes=rescue_connected_nodes)
    else:
        if rescue_connected_nodes:
            rescued = graph_node_ids_from_subject_and_objects(g)
            g.nodes = [n for n in g.nodes if n.lbl is not None or n.id in rescued]
        else:
            g.nodes = [n for n in g.nodes if n.lbl is not None]


def load_obograph_document(path: Union[str, Path]) -> GraphDocument:
    """
    Load an OBOGraph document from a file.

    Example:

        >>> from oaklib.utilities.obograph_utils import load_obograph_document
        >>> doc = load_obograph_document("tests/input/go-nucleus.json")
        >>> g = doc.graphs[0]
        >>> nucleus_terms = [n for n in g.nodes if n.lbl == "nucleus"]
        >>> len(nucleus_terms)
        1

    :param path:
    :return:
    """
    raw_obj = json.load(open(path))
    if "@type" in raw_obj:
        del raw_obj["@type"]
    for g in raw_obj["graphs"]:
        for n in g["nodes"]:
            # workaround for json_loader issue
            if len(n.keys()) == 1 and "id" in n:
                n["lbl"] = None
    return GraphDocument(**raw_obj)
    # return json_loader.load(str(path), target_class=GraphDocument)


def default_stylemap_path():
    conf_path = os.path.dirname(conf_package.__file__)
    return str(Path(conf_path) / DEFAULT_STYLEMAP)


def graph_as_dict(graph: Graph) -> Dict[str, Any]:
    """
    Serialize graph nodes to a dict.

    Example:

        >>> from oaklib.utilities.obograph_utils import load_obograph_document
        >>> doc = load_obograph_document("tests/input/go-nucleus.json")
        >>> g = doc.graphs[0]
        >>> obj = graph_as_dict(g)
        >>> node_map = {n["id"]: n for n in obj["nodes"]}
        >>> assert len(node_map) > 20

    :param graph:
    """
    obj = json_dumper.to_dict(graph)
    for n in obj.get("nodes", []):
        # normalization: no longer needed?
        if "label" in n:
            # annoying mutation: the json format uses 'lbl' not label
            n["lbl"] = n["label"]
            del n["label"]
    return obj


def draw_graph(graph: Graph, seeds=None, configure=None, stylemap=None, imgfile=None) -> None:
    """
    Generates an image from a graph using :ref:`graph_to_image` then open for display

    :param graph:
    :param seeds:
    :param configure:
    :param stylemap:
    :param imgfile:
    :return:
    """
    imgfile = graph_to_image(graph, seeds, configure=configure, stylemap=stylemap, imgfile=imgfile)
    subprocess.run(["open", imgfile])


def graph_to_image(
    graph: Graph,
    seeds: Optional[list[str]] = None,
    configure: Optional[str] = None,
    stylemap: Optional[str] = None,
    imgfile: Optional[str] = None,
    view: bool = None,
    format="png",
) -> None:
    """
    Renders a graph to png using obographviz.

        >>> from oaklib.utilities.obograph_utils import load_obograph_document
        >>> doc = load_obograph_document("tests/input/go-nucleus.json")
        >>> g = doc.graphs[0]
        >>> graph_to_image(g, imgfile="tests/output/go-nucleus-for-g2i.png")

    :param graph: OboGraph object to visualize
    :param seeds: list of node ids to highlight
    :param configure: yaml string to configure the graph
    :param stylemap: path to stylemap file following kgviz data model
    :param imgfile: path to image file to write
    :param view:
    :param format: defaults to png
    :return:
    """
    if format is None:
        format = "png"
    g = {"graphs": [graph_as_dict(graph)]}
    logging.debug(f"graph = {g}")
    exec = "og2dot"
    if shutil.which(exec) is None:
        logging.error(f"No {exec}")
        print("You need to install a node package to be able to visualize results")
        print("")
        print("npm install -g obographviz")
        print("Then set your path to include og2dot")
        raise Exception(
            f"Cannot find {exec} on path. Install from https://github.com/INCATools/obographviz"
        )
    with tempfile.NamedTemporaryFile(mode="w") as tmpfile:
        style = {}
        logging.info(f"Seed nodes: {seeds}")
        # if seeds is not None:
        #    style["highlightIds"] = seeds
        if configure is not None:
            configure_obj = yaml.safe_load(configure)
            for k, v in configure_obj.items():
                style[k] = v
        temp_file_name = tmpfile.name
        logging.info(f"Writing to {temp_file_name}")
        json_dump = json.dumps(g)
        tmpfile.write(json_dump)
        logging.debug(f"JSON {json_dump}")
        tmpfile.flush()

        if imgfile is None:
            imgfile = f"{temp_file_name}.{format}"
        style_json = json.dumps(style).replace("'", "\\'")
        logging.debug(f"Style = {style_json}")
        cmdtoks = [exec, "-S", style_json, "-t", format, temp_file_name, "-o", imgfile]
        if stylemap is not None:
            cmdtoks += ["-s", stylemap]
        if seeds is not None:
            for seed in seeds:
                cmdtoks += ["-H", seed]
        if sys.platform == "win32":
            cmdtoks = ["cmd.exe", "/c"] + cmdtoks
            opencmd = ["cmd.exe", "/c", "start", imgfile]
        else:
            opencmd = ["open", imgfile]
        logging.debug(f"Run: {cmdtoks}")
        subprocess.run(cmdtoks)

        if view and format != "dot":
            logging.debug(f"Run: {opencmd}")
            subprocess.run(opencmd)


def filter_by_predicates(graph: Graph, predicates: List[PRED_CURIE], graph_id: str = None) -> Graph:
    """
    Create a subgraph that has only edges whose predicates are in the predicate list

    :param graph:
    :param predicates:
    :param graph_id:
    :return:
    """
    if graph_id is None:
        graph_id = graph.id
    edges = [edge for edge in graph.edges if PREDICATE_MAP.get(edge.pred, edge.pred) in predicates]
    return Graph(graph_id, nodes=deepcopy(graph.nodes), edges=edges)


def as_multi_digraph(
    graph: Graph,
    reverse: bool = True,
    filter_reflexive: bool = True,
    predicates: Optional[List[PRED_CURIE]] = None,
) -> nx.MultiDiGraph:
    """
    Convert to a networkx :class:`.MultiDiGraph`

    :param graph: OBOGraph
    :param filter_reflexive: if true, remove edges where sub == obj
    :param predicates: if not None, only include edges with these predicates
    :return: networkx MultiDiGraph
    """
    mdg = nx.MultiDiGraph()
    for edge in graph.edges:
        if filter_reflexive and reflexive(edge):
            continue
        if predicates is not None and edge.pred not in predicates:
            continue
        edge_attrs = {"predicate": edge.pred}
        if reverse:
            mdg.add_edge(edge.obj, edge.sub, **edge_attrs)
        else:
            mdg.add_edge(edge.sub, edge.obj, **edge_attrs)
    return mdg


def as_digraph(
    graph: Graph,
    reverse: bool = True,
    filter_reflexive: bool = True,
    predicates: Optional[List[PRED_CURIE]] = None,
) -> nx.MultiDiGraph:
    """
    Convert to a networkx :class:`.DiGraph`

    :param graph: OBOGraph
    :param reverse:
    :return:
    """
    dg = nx.MultiDiGraph()
    for edge in graph.edges:
        if predicates is not None and edge.pred not in predicates:
            continue
        if filter_reflexive and reflexive(edge):
            continue
        edge_attrs = {"predicate": edge.pred}
        if reverse:
            dg.add_edge(edge.obj, edge.sub, **edge_attrs)
        else:
            dg.add_edge(edge.sub, edge.obj, **edge_attrs)
    return dg


def as_graph(
    graph: Graph,
    reverse: bool = True,
    filter_reflexive: bool = True,
    predicate_weights: PREDICATE_WEIGHT_MAP = None,
    default_weight=1.0,
) -> nx.Graph:
    """
    Convert to a networkx :class:`.DiGraph`

    :param graph: OBOGraph
    :param reverse:
    :return:
    """
    dg = nx.Graph()
    for edge in graph.edges:
        if filter_reflexive and reflexive(edge):
            continue
        edge_attrs = {"predicate": edge.pred}
        if predicate_weights is not None:
            if edge.pred in predicate_weights:
                w = predicate_weights[edge.pred]
            else:
                w = default_weight
            edge_attrs["weight"] = w
        dg.add_edge(edge.sub, edge.obj, **edge_attrs)
    return dg


def ancestors_with_stats(graph: Graph, curies: List[CURIE]) -> Dict[CURIE, Dict[str, Any]]:
    """
    Given an OBO Graph, and a list of start/seed curies, calculate
    various statistics about each graph node.

    The current stats for each ancestor node are:

    - visited (int): number of seed nodes underneath that node
    - distance (int): the shortest distance from that ancestor node to a seed node

    :param graph:
    :param curies:
    :return:
    """
    dg = as_digraph(graph)
    counts = defaultdict(int)
    logging.info("Calculating visits")
    for curie in curies:
        for a in set(list(nx.ancestors(dg, curie)) + [curie]):
            counts[a] += 1
    logging.info("Calculating distance matrix")
    splens = dict(nx.all_pairs_shortest_path_length(dg))
    logging.info("Getting final stats")
    stats = {}
    for node in dg.nodes:
        stats[node] = dict(
            visits=counts[node],
            distance=min([dist for k, dist in splens[node].items() if k in curies]),
        )
    return stats


def shortest_paths(
    graph: Graph,
    start_curies: List[CURIE],
    end_curies: Optional[List[CURIE]] = None,
    predicate_weights: Optional[PREDICATE_WEIGHT_MAP] = None,
    directed=False,
) -> Iterator[Tuple[CURIE, CURIE, List[CURIE]]]:
    """
    Finds all shortest paths from a set of start nodes to a set of end nodes

    :param graph: OboGraph object
    :param start_curies:
    :param end_curies: if None, then compute for all proper ancestors
    :param predicate_weights: an optional map of predicates to weights
    :return:
    """
    if directed:
        dg = as_digraph(graph, reverse=False)
    else:
        dg = as_graph(graph, predicate_weights=predicate_weights)
    logging.info(f"Calculating paths, starts={start_curies}")
    for start_curie in start_curies:
        if not dg.has_node(start_curie):
            logging.info(f"Skipping {start_curie} because it is not in the graph")
            continue
        if end_curies:
            this_end_curies = end_curies
        else:
            this_end_curies = list(nx.ancestors(dg, start_curie))
        logging.info(f"Calculating distances for {start_curie}")
        for end_curie in set(this_end_curies):
            if not dg.has_node(end_curie):
                logging.info(f"Skipping {end_curie} because it is not in the graph")
                continue
            logging.debug(f"COMPUTING {start_curie} to {end_curie}")
            try:
                if directed:
                    paths = nx.all_simple_paths(dg, source=start_curie, target=end_curie)
                else:
                    paths = nx.all_shortest_paths(
                        dg,
                        source=start_curie,
                        target=end_curie,
                        weight="weight",
                        method="bellman-ford",
                    )
                for path in paths:
                    yield start_curie, end_curie, path
            except nx.NetworkXNoPath:
                logging.info(f"No path between {start_curie} and {end_curie}")


def edges_from_tree(tree: dict, pred=IS_A) -> List[Edge]:
    """
    Given a parent node and a list of children, return a list of edges

    >>> from oaklib.utilities.obograph_utils import edges_from_tree
    >>> for e in edges_from_tree({1: {2: [3, 4]}}):
    ...    print(e.sub, e.obj)
    2 1
    3 2
    4 2

    :param tree:
    :param pred: defaults to IS_A
    :return:
    """
    edges = []

    def _safe(x: Any):
        return str(x)

    def _edge(s: Any, o: Any) -> None:
        edges.append(Edge(sub=str(s), pred=pred, obj=str(o)))

    for parent, children in tree.items():
        if isinstance(children, list):
            # leaf nodes
            for child in children:
                _edge(child, parent)
        else:
            # non-leaf nodes
            for child, grandchildren in children.items():
                _edge(child, parent)
                edges.extend(edges_from_tree({child: grandchildren}, pred=pred))
    return edges


def depth_first_ordering(
    graph: Graph, predicates: Optional[List[PRED_CURIE]] = None
) -> List[CURIE]:
    """
    Return a depth-first ordering of the nodes in the graph.

    >>> from oaklib.datamodels.obograph import Graph
    >>> from oaklib.utilities.obograph_utils import depth_first_ordering, edges_from_tree
    >>> ## Chains have a deterministic DF ordering
    >>> edges = edges_from_tree({1: {2: [3]}})
    >>> list(depth_first_ordering(Graph("test", edges=edges)))
    ['1', '2', '3']
    >>> list(depth_first_ordering(Graph("test", edges=list(reversed(edges)))))
    ['1', '2', '3']
    >>> edges2 = edges_from_tree({5: [3, 4]})
    >>> ordered = list(depth_first_ordering(Graph("test", edges=edges + edges2)))
    >>> assert ordered.index('1') < ordered.index('2')

    :param graph: OBOGraph
    :param predicates:
    :return:
    """
    g = as_digraph(graph, predicates=predicates)
    roots = [n for n, d in g.in_degree() if d == 0]
    ordered = []
    for root in roots:
        for n in nx.dfs_preorder_nodes(g, root):
            if n not in ordered:
                ordered.append(n)
    return ordered
    six = index_graph_edges_by_subject(graph)
    oix = index_graph_edges_by_object(graph)
    stack = list(set(oix.keys()) - set(six.keys()))
    visited = []
    while stack:
        node = stack.pop()
        visited.append(node)
        for edge in oix[node]:
            if edge.sub not in visited and edge.sub not in stack:
                stack.append(edge.sub)
    return visited


def remove_nodes_from_graph(graph: Graph, node_ids: List[CURIE]):
    """
    Remove the specified nodes from the graph, and cascade to any edges
    that reference these nodes

    Mutates the graph in-place
    :param graph:
    :param node_ids:
    :return: None
    """
    graph.nodes = [n for n in graph.nodes if n.id not in node_ids]
    graph.edges = [
        e
        for e in graph.edges
        if e.sub not in node_ids and e.obj not in node_ids and e.pred not in node_ids
    ]


def trim_graph(
    graph: Graph, seeds: List[CURIE], distance: int = 0, include_intermediates=False
) -> Graph:
    """
    Remove all nodes more than a specified distance from a set of seed nodes

    For each node in the graph, if the minimum distance between that node and one of the seed nodes
    is greater than the distance threshold, then remove it

    By default, this is determined using the ancestor relationship

    :param graph: input graph (will not be modified)
    :param seeds: seed nodes used to calculate distance for each ancestor
    :param distance: threshold for minimum distance
    :param include_intermediates: if true, always include nodes that are between two seed nodes
    :return: trimmed graph
    """
    dg = as_digraph(graph)
    all_ancs = set()
    intermediates = set()
    for seed in seeds:
        ancs = list(nx.ancestors(dg, seed))
        all_ancs.update(ancs)
        for anc in ancs:
            if anc in seeds:
                intermediates.add(anc)
            for anc_of_anc in nx.ancestors(dg, anc):
                if anc_of_anc in seeds:
                    intermediates.add(anc)
    splens = dict(nx.all_pairs_shortest_path_length(dg))
    nodes_to_trim = set()
    for anc in all_ancs:
        if include_intermediates and anc in intermediates:
            continue
        all_dists = [dist for k, dist in splens[anc].items() if k in seeds]
        logging.debug(f"Anc: {anc} distances={all_dists}")
        if all_dists:
            min_dist = min(all_dists)
            if min_dist > distance:
                nodes_to_trim.add(anc)
    new_graph = deepcopy(graph)
    remove_nodes_from_graph(new_graph, list(nodes_to_trim))
    return new_graph


def merge_graphs(source: Graph, target: Graph, replace: bool = False) -> Graph:
    """
    Merge two graphs into a single graph

    :param source: source graph
    :param target: target graph
    :param replace: if true, replace nodes that share the same id
    :return: merged graph
    """
    new_graph = deepcopy(target)
    nix = index_graph_nodes(target)
    for node in source.nodes:
        if replace or node.id not in nix:
            new_graph.nodes.append(node)
        else:
            nix[node.id] = merge_graph_nodes(nix[node.id], node)
    for edge in source.edges:
        if edge not in target.edges:
            new_graph.edges.append(edge)
    return new_graph


def merge_graph_nodes(target: Node, source: Node) -> Node:
    """
    Merge two nodes into a single node

    :param target:
    :param source:
    :return:
    """
    new_node = Node(id=target.id, lbl=target.lbl, type=target.type, meta=target.meta)
    if source.lbl:
        new_node.lbl = source.lbl
    if not new_node.meta:
        new_node.meta = source.meta
        return new_node
    source_meta = source.meta
    if not source_meta:
        return new_node
    if source_meta.definition:
        new_node.meta.definition = source_meta.definition
    if source_meta.synonyms:
        for s in source_meta.synonyms:
            if s not in new_node.meta.synonyms:
                new_node.meta.synonyms.append(s)
    if source_meta.xrefs:
        for x in source_meta.xrefs:
            if x not in new_node.meta.xrefs:
                new_node.meta.xrefs.append(x)
    if source_meta.subsets:
        for s in source_meta.subsets:
            if s not in new_node.meta.subsets:
                new_node.meta.subsets.append(s)
    return new_node


def index_graph_nodes(graph: Graph) -> Dict[CURIE, Node]:
    """
    Returns an index of all nodes key by node id

    :param graph:
    :return: node by id index
    """
    return {n.id: n for n in graph.nodes}


def index_graph_edges_by_subject(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by subject id

    :param graph:
    :return: edges by subject index
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.sub].append(e)
    return d


def index_graph_edges_by_subject_object(graph: Graph) -> Dict[Tuple[CURIE, CURIE], List[Edge]]:
    """
    Returns an index of lists of edges keyed by subject and object

    :param graph:
    :return: edges by subject-object pair index
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[(e.sub, e.obj)].append(e)
    return d


def index_graph_edges_by_object(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by object id

    :param graph:
    :return: edges by object index
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.obj].append(e)
    return d


def index_graph_edges_by_predicate(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by predicate id

    :param graph:
    :return: edges by predicate index
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.pred].append(e)
    return d


def topological_sort(graph: Graph, predicates: Optional[List[PRED_CURIE]]) -> List[CURIE]:
    """
    Returns a topological sort of the graph.

    A topological sort is a nonunique permutation of the nodes of a
    directed graph such that an edge from u to v implies that u
    appears before v in the topological sort order. This ordering is
    valid only if the graph has no directed cycles.

    :param graph:
    :param predicates:
    :return:
    """
    dg = as_multi_digraph(graph, predicates=predicates)
    return nx.topological_sort(dg)


def graph_info(graph: Graph) -> str:
    return f"{graph.id} nodes: {len(graph.nodes)} edges: {len(graph.edges)}"


def reflexive(edge: Edge) -> bool:
    return edge.sub == edge.obj


def graph_to_tree_display(
    graph: Graph,
    predicates: List[PRED_CURIE] = None,
    skip: List[CURIE] = None,
    output: TextIO = None,
    start_curies: List[CURIE] = None,
    seeds: List[CURIE] = None,
    format: str = None,
    max_paths: int = 10,
    predicate_code_map=DEFAULT_PREDICATE_CODE_MAP,
    display_options: Optional[List[str]] = None,
    stylemap=None,
) -> Optional[str]:
    """
    Translate a graph to a textual tree representation

    :param graph: input graph
    :param predicates: predicates to traverse over
    :param skip: omit paths that include this entity
    :param output: where to write tree text
    :param start_curies: seed nodes
    :param seeds: nodes to highlight
    :param format: markdown or text
    :param max_paths: upper limit on number of distinct paths to show
    :param predicate_code_map: mapping between predicates and codes/acronyms
    :param display_options: list of display options, as per info writer
    :param stylemap: kgviz stylemap (not yet used)
    :return:
    """
    # TODO: refactor this to use graph_to_tree_structure
    if not display_options:
        display_options = []
    show_all = "all" in display_options
    if seeds is None:
        seeds = []
    if output is None:
        output = io.StringIO()
        is_str = True
    else:
        is_str = False
    logging.info(f"graph = {graph_info(graph)}")
    nix = index_graph_nodes(graph)
    if predicates is not None:
        subgraph = filter_by_predicates(graph, predicates)
    else:
        subgraph = graph
    logging.info(f"Subgraph = {graph_info(subgraph)}, filtered by {predicates}")
    children_ix = index_graph_edges_by_object(subgraph)
    dg = as_multi_digraph(subgraph, filter_reflexive=True)
    if start_curies is None:
        roots = [n for n, d in dg.in_degree if d == 0]
    else:
        roots = start_curies
    logging.info(f"Roots={roots}")
    if format is None or format == TreeFormatEnum.markdown.value:
        indent = 4 * " "
    else:
        indent = "."
    todo = [([], "", n) for n in roots]
    counts = defaultdict(int)
    while len(todo) > 0:
        stack, rel, n = todo.pop()
        depth = len(stack)
        counts[n] += 1
        logging.debug(f"Visited {n} {counts[n]} times (max = {max_paths})")
        if counts[n] > max_paths:
            logging.info(f"Reached {counts[n]} for node {n};; truncating rest")
            break
        rel_pred = PREDICATE_MAP.get(rel, rel)
        if rel_pred in predicate_code_map:
            code = predicate_code_map[rel_pred]
        elif rel in nix:
            code = nix[rel].lbl
            if code is None:
                code = rel
        else:
            code = rel
        output.write(depth * indent)
        output.write(f"* [{code}] ")
        node_info = f"{n}"
        if n in nix:
            obj = nix[n]
            if obj.lbl:
                node_info += f" ! {obj.lbl}"
            if obj.meta:
                meta = obj.meta
                if (show_all or "d" in display_options) and meta.definition:
                    node_info += f' "{meta.definition.val}"'
                if (show_all or "x" in display_options) and meta.xrefs:
                    node_info += " ["
                    for x in meta.xrefs:
                        node_info += f" {x.val}"
                    node_info += " ]"
        if n in seeds:
            node_info = f"**{node_info}**"
        output.write(node_info)
        output.write("\n")
        child_edges = children_ix.get(n, [])
        for child_edge in child_edges:
            if skip and child_edge.sub in skip:
                continue
            if not reflexive(child_edge):
                if child_edge.sub not in stack:
                    todo.append((stack + [n], child_edge.pred, child_edge.sub))
    if is_str:
        return output.getvalue()


class TreeNode(BaseModel):
    id: Optional[CURIE] = (None,)
    lbl: Optional[str] = None
    meta: Optional[dict] = None
    children: Dict[PRED_CURIE, List["TreeNode"]] = {}
    parent_id: Optional[str] = None
    parent_relation: Optional[PRED_CURIE] = None
    path_to_root: List[CURIE] = []


def graph_to_tree_structure(
    graph: Graph,
    predicates: List[PRED_CURIE] = None,
    skip: List[CURIE] = None,
    start_curies: List[CURIE] = None,
    predicate_label_map: Dict[PRED_CURIE, str] = None,
    max_paths: int = 10,
) -> List[TreeNode]:
    """
    Linearizes a graph to a list of trees.

    The list will contain one element for each root
    :param graph:
    :param predicates:
    :param skip:
    :param start_curies:
    :param max_paths:
    :return:
    """
    logging.info(f"graph = {graph_info(graph)}")
    if not predicate_label_map:
        predicate_label_map = {
            IS_A: "subtypes",
            PART_OF: "parts",
        }
    nix = index_graph_nodes(graph)
    if predicates is not None:
        subgraph = filter_by_predicates(graph, predicates)
    else:
        subgraph = graph
    logging.info(f"Subgraph = {graph_info(subgraph)}, filtered by {predicates}")
    children_ix = index_graph_edges_by_object(subgraph)
    dg = as_multi_digraph(subgraph, filter_reflexive=True)
    if start_curies is None:
        root_ids = [n for n, d in dg.in_degree if d == 0]
    else:
        root_ids = start_curies
    logging.info(f"Roots={root_ids}")
    stack = [TreeNode(id=n) for n in root_ids]
    tree_roots = copy(stack)
    counts = defaultdict(int)

    pointer = 0
    while len(stack) > pointer:
        next_node = stack[pointer]
        next_node_id = next_node.id
        pointer += 1
        counts[next_node_id] += 1
        logging.debug(f"Visited {next_node_id} {counts[next_node_id]} times (max = {max_paths})")
        if max_paths is not None and counts[next_node_id] > max_paths:
            logging.info(
                f"Reached {counts[next_node_id]} for node {next_node_id};; truncating rest"
            )
            break
        if next_node_id in nix:
            next_node_obj = nix[next_node_id]
            next_node.lbl = next_node_obj.lbl
            # TODO: meta
        child_edges = children_ix.get(next_node_id, [])
        for child_edge in child_edges:
            pred = child_edge.pred
            pred = predicate_label_map.get(pred, pred)
            if skip and child_edge.sub in skip:
                continue
            if not reflexive(child_edge):
                if child_edge.sub in next_node.path_to_root:
                    continue
                child_node = TreeNode(
                    id=child_edge.sub, parent_id=next_node_id, parent_relation=pred
                )
                child_node.path_to_root = next_node.path_to_root + [next_node_id]
                if pred not in next_node.children:
                    next_node.children[pred] = []
                next_node.children[pred].append(child_node)
                stack.append(child_node)

    return tree_roots


def graph_to_d3viz_objects(
    graph: Graph,
    predicates: List[PRED_CURIE] = None,
    relations_as_nodes=False,
    **kwargs,
) -> List[Dict]:
    roots = graph_to_tree_structure(graph, predicates=predicates, **kwargs)
    return [
        tree_node_to_d3viz_object(root, relations_as_nodes=relations_as_nodes) for root in roots
    ]


def tree_node_to_d3viz_object(tree_node: TreeNode, relations_as_nodes=False) -> Dict:
    obj = {"name": tree_node.lbl, "parent": tree_node.parent_id}
    if tree_node.children:
        obj["children"] = []
        if relations_as_nodes:
            for pred, children in tree_node.children.items():
                pred_node = {
                    "name": pred,
                    "parent": tree_node.id,
                    "children": [tree_node_to_d3viz_object(child, True) for child in children],
                }
                obj["children"].append(pred_node)
        else:
            for children in tree_node.children.values():
                for child in children:
                    obj["children"].append(tree_node_to_d3viz_object(child))
    return obj


def expand_all_graph_ids(graph: Union[Graph, GraphDocument], converter: Converter) -> None:
    def _expand(x):
        try:
            return converter.expand(x)
        except Exception:
            return x

    mutate_graph_ids(graph, _expand)


def compress_all_graph_ids(graph: Union[Graph, GraphDocument], converter: Converter) -> None:
    def _compress(x):
        try:
            return converter.compress(x)
        except Exception:
            return x

    mutate_graph_ids(graph, _compress)


def mutate_graph_ids(graph: Union[Graph, GraphDocument], func: Callable) -> None:
    """
    Iterate over the ids in a graph and modify them.

    :param graph:
    :param func:
    :return:
    """
    if isinstance(graph, GraphDocument):
        for g in graph.graphs:
            mutate_graph_ids(g, func)
        return
    for n in graph.nodes:
        n.id = func(n.id)
    for e in graph.edges:
        e.sub = func(e.sub)
        e.pred = func(e.pred)
        e.obj = func(e.obj)
    for ld in graph.logicalDefinitionAxioms:
        ld.definedClassId = func(ld.definedClassId)
        ld.genusIds = [func(x) for x in ld.genusIds]
        for r in ld.restrictions:
            r.propertyId = func(r.propertyId)
            r.fillerId = func(r.fillerId)
    graph.equivalentNodesSets = [func(x) for x in graph.equivalentNodesSets]


def graph_id_iterator(graph: Union[Graph, GraphDocument]) -> Iterator[CURIE]:
    """
    Iterate over the ids in a graph

    :param graph:
    :return:
    """
    if isinstance(graph, GraphDocument):
        for g in graph.graphs:
            yield from graph_id_iterator(g)
        return
    for n in graph.nodes:
        yield n.id
    for e in graph.edges:
        yield from [e.sub, e.obj, e.pred]
    for ld in graph.logicalDefinitionAxioms:
        yield ld.definedClassId
        yield from ld.genusIds
        for r in ld.restrictions:
            yield r.propertyId
            yield r.fillerId
    for ns in graph.equivalentNodesSets:
        yield from ns.nodeIds


def graph_ids(graph: Union[Graph, GraphDocument]) -> Iterator[CURIE]:
    """
    Return a set of all ids in a graph

    :param graph:
    :return:
    """
    yield from list(set(graph_id_iterator(graph)))


def induce_graph_prefix_map(
    graph: Union[Graph, GraphDocument], converter: Converter
) -> Dict[str, str]:
    def _id_to_prefix(id: CURIE) -> Optional[str]:
        pfx, _ = converter.parse_uri(id)
        if pfx:
            return pfx
        parts = id.split(":")
        if len(parts) > 1:
            return parts[0]
        return None

    prefixes = {_id_to_prefix(id) for id in graph_ids(graph)}
    return {p: converter.expand_pair(p, "") for p in prefixes if p}
