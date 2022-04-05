"""
Utilities for the OBOGraph Datamodel
------------------------------------

See :ref:`datamodels`

"""
import json
import logging
import os
import shutil
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Dict, Any, List

import yaml
from linkml_runtime.dumpers import json_dumper
from oaklib.types import PRED_CURIE
from oaklib.datamodels.obograph import Graph
import networkx as nx
# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
from oaklib import conf as conf_package

DEFAULT_STYLEMAP = 'obograph-style.json'

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
    return Graph(graph_id, nodes=deepcopy(graph.nodes))

def as_multi_digraph(graph: Graph, reverse: bool = True) -> nx.MultiDiGraph:
    """
    Convert to a networkx :class:`.MultiDiGraph`

    :param graph: OBOGraph
    :param reverse:
    :return:
    """
    mdg = nx.MultiDiGraph()
    for edge in graph.edges:
        edge_attrs = {"predicate": edge.pred}
        if reverse:
            mdg.add_edge(edge.obj, edge.sub, **edge_attrs)
        else:
            mdg.add_edge(edge.sub, edge.obj, **edge_attrs)
    return mdg
