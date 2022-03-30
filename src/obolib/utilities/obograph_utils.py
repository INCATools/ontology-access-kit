import json
import logging
import shutil
import subprocess
import tempfile
from typing import Dict, Any

import yaml
from linkml_runtime.dumpers import json_dumper
from obolib.vocabulary.obograph import Graph


def graph_as_dict(graph: Graph) -> Dict[str, Any]:
    obj = json_dumper.to_dict(graph)
    for n in obj['nodes']:
        if 'label' in n:
            # annoying mutation: the json format uses 'lbl' not label
            n['lbl'] = n['label']
            del n['label']
    return obj

def draw_graph(graph: Graph, seeds = None, configure = None, stylemap = None) -> None:
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
        pngfile = f'{temp_file_name}.png'
        style_json = json.dumps(style).replace("'", "\\'")
        logging.debug(f'Style = {style_json}')
        cmdtoks = [EXEC, '-S', style_json, '-t', 'png', temp_file_name, '-o', pngfile]
        if stylemap is not None:
            cmdtoks += ['-s', stylemap]
        logging.debug(f'Run: {cmdtoks}')
        subprocess.run(cmdtoks)
        subprocess.run(['open', pngfile])