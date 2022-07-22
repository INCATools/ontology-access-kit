"""
Utilities for writing out obo graphs

"""
from typing import Optional, TextIO, Union

from linkml_runtime.dumpers import json_dumper, yaml_dumper

from oaklib import OntologyResource
from oaklib.datamodels.obograph import Graph
from oaklib.implementations import ProntoImplementation


def write_graph(
    graph: Graph,
    output: Optional[Union[str, TextIO]] = None,
    format: str = None,
):
    """
    Writes an obo graph to a file-like object in a specified format

    :param graph:
    :param output:
    :param format:
    :return:
    """
    if format == "json":
        if output:
            json_dumper.dump(graph, to_file=output, inject_type=False)
        else:
            print(json_dumper.dumps(graph))
    elif format == "yaml":
        if output:
            yaml_dumper.dump(graph, to_file=output, inject_type=False)
        else:
            print(yaml_dumper.dumps(graph))
    elif format == "obo":
        output_oi = ProntoImplementation()
        output_oi.load_graph(graph, replace=True)
        output_oi.store(OntologyResource(slug=output, local=True, format="obo"))
    else:
        raise ValueError(f"Do not know how to write: {format}")
