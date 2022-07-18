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
import tempfile
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, TextIO, Tuple

import networkx as nx
import yaml
from linkml_runtime.dumpers import json_dumper

# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
from oaklib import conf as conf_package
from oaklib.datamodels.obograph import Edge, Graph, Node
from oaklib.datamodels.vocabulary import IS_A, PART_OF, RDF_TYPE
from oaklib.types import CURIE, PRED_CURIE

DEFAULT_STYLEMAP = "obograph-style.json"

# TODO: use the style map
DEFAULT_PREDICATE_CODE_MAP = {IS_A: "i", PART_OF: "p", RDF_TYPE: "t"}

PREDICATE_WEIGHT_MAP = Dict[PRED_CURIE, float]


class TreeFormatEnum(Enum):
    markdown = "md"
    text = "text"


def default_stylemap_path():
    conf_path = os.path.dirname(conf_package.__file__)
    return str(Path(conf_path) / DEFAULT_STYLEMAP)


def graph_as_dict(graph: Graph) -> Dict[str, Any]:
    """
    Convert an OBOGraph representation to a dictionary representation isomorphic to the
    OBOGraphs json standard.

    Note: in the python datamodel we use "label", this is converted to "lbl" for the standard

    :param graph:
    :return:
    """
    obj = json_dumper.to_dict(graph)
    for n in obj["nodes"]:
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


def graph_to_image(graph: Graph, seeds=None, configure=None, stylemap=None, imgfile=None) -> str:
    """
    Renders a graph to png using obographviz

    :param graph:
    :param seeds:
    :param configure:
    :param stylemap:
    :return:
    """
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
    with tempfile.NamedTemporaryFile(dir="/tmp", mode="w") as tmpfile:
        style = {}
        logging.info(f"Seed nodes: {seeds}")
        # if seeds is not None:
        #    style["highlightIds"] = seeds
        if configure is not None:
            configure_obj = yaml.safe_load(configure)
            for k, v in configure_obj.items():
                style[k] = v
        # style['styles'] = ['filled', 'rounded']
        # style['prefixProperties'] = {
        #    "CL": {"fillcolor": "yellow"},
        #    "GO": {"fillcolor": "#ff7f00"}
        # }
        temp_file_name = tmpfile.name
        logging.info(f"Writing to {temp_file_name}")
        json_dump = json.dumps(g)
        tmpfile.write(json_dump)
        logging.debug(f"JSON {json_dump}")
        tmpfile.flush()
        if imgfile is None:
            imgfile = f"{temp_file_name}.png"
        style_json = json.dumps(style).replace("'", "\\'")
        logging.debug(f"Style = {style_json}")
        cmdtoks = [exec, "-S", style_json, "-t", "png", temp_file_name, "-o", imgfile]
        if stylemap is not None:
            cmdtoks += ["-s", stylemap]
        if seeds is not None:
            for seed in seeds:
                cmdtoks += ["-H", seed]
        logging.debug(f"Run: {cmdtoks}")
        subprocess.run(cmdtoks)
        return imgfile


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
    edges = [edge for edge in graph.edges if edge.pred in predicates]
    return Graph(graph_id, nodes=deepcopy(graph.nodes), edges=edges)


def as_multi_digraph(
    graph: Graph, reverse: bool = True, filter_reflexive: bool = True
) -> nx.MultiDiGraph:
    """
    Convert to a networkx :class:`.MultiDiGraph`

    :param graph: OBOGraph
    :param reverse:
    :return:
    """
    mdg = nx.MultiDiGraph()
    for edge in graph.edges:
        if filter_reflexive and reflexive(edge):
            continue
        edge_attrs = {"predicate": edge.pred}
        if reverse:
            mdg.add_edge(edge.obj, edge.sub, **edge_attrs)
        else:
            mdg.add_edge(edge.sub, edge.obj, **edge_attrs)
    return mdg


def as_digraph(
    graph: Graph, reverse: bool = True, filter_reflexive: bool = True
) -> nx.MultiDiGraph:
    """
    Convert to a networkx :class:`.DiGraph`

    :param graph: OBOGraph
    :param reverse:
    :return:
    """
    dg = nx.DiGraph()
    for edge in graph.edges:
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
) -> nx.MultiDiGraph:
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
) -> Iterator[Tuple[CURIE, CURIE, List[CURIE]]]:
    """
    Finds all shortest paths from a set of start nodes to a set of end nodes

    :param graph: OboGraph object
    :param start_curies:
    :param end_curies: if None, then compute for all proper ancestors
    :param predicate_weights: an optional map of predicates to weights
    :return:
    """
    dg = as_graph(graph, predicate_weights=predicate_weights)
    logging.info(f"Calculating paths, starts={start_curies}")
    for start_curie in start_curies:
        if end_curies:
            this_end_curies = end_curies
        else:
            this_end_curies = list(nx.ancestors(dg, start_curie))
        logging.info(f"Calculating distances for {start_curie}")
        for end_curie in set(this_end_curies):
            logging.debug(f"COMPUTING {start_curie} to {end_curie}")
            try:
                paths = nx.all_shortest_paths(
                    dg, source=start_curie, target=end_curie, weight="weight", method="bellman-ford"
                )
                for path in paths:
                    yield start_curie, end_curie, path
            except nx.NetworkXNoPath:
                logging.info(f"No path between {start_curie} and {end_curie}")


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


def topological_sort(graph: Graph, predicates: List[PRED_CURIE]) -> List[CURIE]:
    dg = as_multi_digraph(graph)
    return nx.topological_sort(dg)


def graph_info(graph: Graph) -> str:
    return f"{graph.id} nodes: {len(graph.nodes)} edges: {len(graph.edges)}"


def reflexive(edge: Edge) -> bool:
    return edge.sub == edge.obj


def graph_to_tree(
    graph: Graph,
    predicates: List[PRED_CURIE] = None,
    output: TextIO = None,
    start_curies: List[CURIE] = None,
    seeds: List[CURIE] = None,
    format: str = None,
    max_paths: int = 10,
    predicate_code_map=DEFAULT_PREDICATE_CODE_MAP,
    stylemap=None,
) -> Optional[str]:
    """
    Translate a graph to a textual tree representation

    :param graph: input graph
    :param predicates: predicates to traverse over
    :param output: where to write tree text
    :param start_curies: seed nodes
    :param seeds: nodes to highlight
    :param format: markdown or text
    :param max_paths: upper limit on number of distinct paths to show
    :param predicate_code_map: mapping between predicates and codes/acronyms
    :param stylemap: kgviz stylemap (not yet used)
    :return:
    """
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
        if rel in predicate_code_map:
            code = predicate_code_map[rel]
        elif rel in nix:
            code = nix[rel].lbl
            if code is None:
                code = rel
        else:
            code = rel
        output.write(depth * indent)
        output.write(f"* [{code}] ")
        node_info = f"{n}"
        if n in nix and nix[n].lbl:
            node_info += f" ! {nix[n].lbl}"
        if n in seeds:
            node_info = f"**{node_info}**"
        output.write(node_info)
        output.write("\n")
        child_edges = children_ix.get(n, [])
        for child_edge in child_edges:
            if not reflexive(child_edge):
                if child_edge.sub not in stack:
                    todo.append((stack + [n], child_edge.pred, child_edge.sub))
    if is_str:
        return output.getvalue()
