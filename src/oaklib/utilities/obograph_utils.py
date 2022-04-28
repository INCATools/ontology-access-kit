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
from typing import Dict, Any, List, TextIO, Optional

import yaml
from linkml_runtime.dumpers import json_dumper
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.types import PRED_CURIE, CURIE
from oaklib.datamodels.obograph import Graph, Node, Edge
import networkx as nx
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
from oaklib import conf as conf_package

DEFAULT_STYLEMAP = 'obograph-style.json'

DEFAULT_PREDICATE_CODE_MAP = {
    IS_A: 'i',
    PART_OF: 'p'
}

class TreeFormatEnum(Enum):
    markdown = 'md'
    text = 'text'

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
    for n in obj['nodes']:
        if 'label' in n:
            # annoying mutation: the json format uses 'lbl' not label
            n['lbl'] = n['label']
            del n['label']
    return obj

def draw_graph(graph: Graph, seeds = None, configure = None, stylemap = None, imgfile = None) -> None:
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
    subprocess.run(['open', imgfile])

def graph_to_image(graph: Graph, seeds = None, configure = None, stylemap = None, imgfile = None) -> str:
    """
    Renders a graph to png using obographviz

    :param graph:
    :param seeds:
    :param configure:
    :param stylemap:
    :return:
    """
    g = {"graphs": [graph_as_dict(graph)]}
    logging.debug(f'graph = {g}')
    EXEC = 'og2dot.js'
    if shutil.which(EXEC) is None:
        logging.error(f'No {EXEC}')
        print('You need to install a node package to be able to visualize results')
        print('')
        print('npm install -g obographviz')
        print('Then set your path to include og2dot')
        raise Exception(f'Cannot find {EXEC} on path. Install from https://github.com/cmungall/obographviz')
    with tempfile.NamedTemporaryFile(dir='/tmp', mode='w') as tmpfile:
        style = {}
        if seeds is not None:
            style['highlightIds'] = seeds
        if configure is not None:
            configure_obj = yaml.safe_load(configure)
            for k,v in configure_obj.items():
                style[k] = v
        #style['styles'] = ['filled', 'rounded']
        #style['prefixProperties'] = {
        #    "CL": {"fillcolor": "yellow"},
        #    "GO": {"fillcolor": "#ff7f00"}
        #}
        temp_file_name = tmpfile.name
        logging.info(f'Writing to {temp_file_name}')
        json_dump = json.dumps(g)
        tmpfile.write(json_dump)
        logging.debug(f'JSON {json_dump}')
        tmpfile.flush()
        if imgfile is None:
            imgfile = f'{temp_file_name}.png'
        style_json = json.dumps(style).replace("'", "\\'")
        logging.debug(f'Style = {style_json}')
        cmdtoks = [EXEC, '-S', style_json, '-t', 'png', temp_file_name, '-o', imgfile]
        if stylemap is not None:
            cmdtoks += ['-s', stylemap]
        logging.debug(f'Run: {cmdtoks}')
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

def as_multi_digraph(graph: Graph, reverse: bool = True, filter_reflexive: bool = True) -> nx.MultiDiGraph:
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

def index_graph_nodes(graph: Graph) -> Dict[CURIE, Node]:
    """
    Returns an index of all nodes key by node id
    :param graph:
    :return:
    """
    return {n.id: n for n in graph.nodes}


def index_graph_edges_by_subject(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by predicate id

    :param graph:
    :return:
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.sub].append(e)
    return d

def index_graph_edges_by_predicate(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by predicate id

    :param graph:
    :return:
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.pred].append(e)
    return d

def index_graph_edges_by_object(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by object id

    :param graph:
    :return:
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.obj].append(e)
    return d

def index_graph_edges_by_predicate(graph: Graph) -> Dict[CURIE, List[Edge]]:
    """
    Returns an index of lists of edges keyed by predicate id

    :param graph:
    :return:
    """
    d = defaultdict(list)
    for e in graph.edges:
        d[e.pred].append(e)
    return d


def topological_sort(graph: Graph, predicates: List[PRED_CURIE]) -> List[CURIE]:
    dg = as_multi_digraph(graph)
    return nx.topological_sort(dg)


def graph_info(graph: Graph) -> str:
    return f'{graph.id} nodes: {len(graph.nodes)} edges: {len(graph.edges)}'


def reflexive(edge: Edge) -> bool:
    return edge.sub == edge.obj


def graph_to_tree(graph: Graph, predicates: List[PRED_CURIE] = None, output: TextIO = None,
                  start_curies: List[CURIE] = None, seeds: List[CURIE] = [],
                  format: str = None, max_paths: int = 10,
                  predicate_code_map=DEFAULT_PREDICATE_CODE_MAP,
                  stylemap = None) -> Optional[str]:
    if output is None:
        output = io.StringIO()
        is_str = True
    else:
        is_str = False
    logging.info(f'graph = {graph_info(graph)}')
    nix = index_graph_nodes(graph)
    if predicates is not None:
        subgraph = filter_by_predicates(graph, predicates)
    else:
        subgraph = graph
    logging.info(f'Subgraph = {graph_info(subgraph)}, filtered by {predicates}')
    children_ix = index_graph_edges_by_object(subgraph)
    dg = as_multi_digraph(subgraph, filter_reflexive=True)
    if start_curies is None:
        roots = [n for n, d in dg.in_degree if d == 0]
    else:
        roots = start_curies
    logging.info(f'Roots={roots}')
    if format is None or format == TreeFormatEnum.markdown.value:
        indent = 4 * ' '
    else:
        indent = '.'
    todo = [(0, '', n) for n in roots]
    counts = defaultdict(int)
    while len(todo) > 0:
        depth, rel, n = todo.pop()
        counts[n] += 1
        logging.debug(f'Visited {n} {counts[n]} times (max = {max_paths})')
        if counts[n] > max_paths:
            logging.info(f'Reached {counts[n]} for node {n};; truncating rest')
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
        output.write(f'* [{code}] ')
        node_info = f'{n} ! {nix[n].lbl}'
        if n in seeds:
            node_info = f'**{node_info}**'
        output.write(node_info)
        output.write('\n')
        child_edges = children_ix.get(n, [])
        for child_edge in child_edges:
            if not reflexive(child_edge):
                todo.append((depth+1, child_edge.pred, child_edge.sub))
    if is_str:
        return output.getvalue()



