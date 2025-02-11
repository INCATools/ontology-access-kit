"""
Utilities for writing out obo graphs

"""

import logging
from typing import Optional, TextIO, Union

from linkml_runtime.dumpers import json_dumper, yaml_dumper

from oaklib import OntologyResource
from oaklib.converters.obo_graph_to_cx_converter import OboGraphToCXConverter
from oaklib.converters.obo_graph_to_rdf_owl_converter import OboGraphToRdfOwlConverter
from oaklib.datamodels.obograph import Graph, GraphDocument
from oaklib.implementations import ProntoImplementation
from oaklib.utilities.obograph_utils import graph_to_image

OG_FORMATS = ["json", "yaml", "obojson", "obograph"]
RENDER_FORMATS = ["png", "svg", "dot"]

logger = logging.getLogger(__name__)


def write_graph_document(
    doc: GraphDocument,
    output: Optional[Union[str, TextIO]] = None,
    format: str = None,
    view: Optional[bool] = None,
    **kwargs,
):
    logger.info(f"Writing graph document to {output} in format {format} // v={view}")
    if view and not format:
        format = "png"
    if (not format or format in OG_FORMATS) and not view:
        if output:
            json_dumper.dump(doc, to_file=output, inject_type=False)
        else:
            print(json_dumper.dumps(doc))
    else:
        if len(doc.graphs) != 1:
            raise ValueError("Can only write a single graph to a file")
        write_graph(doc.graphs[0], output, format, view=view, **kwargs)


def write_graph(
    graph: Graph,
    output: Optional[Union[str, TextIO]] = None,
    format: str = None,
    view: Optional[bool] = None,
    **kwargs,
):
    """
    Writes an obo graph to a file-like object in a specified format

    :param graph:
    :param output:
    :param format:
    :return:
    """
    if view or format in RENDER_FORMATS:
        graph_to_image(
            graph,
            imgfile=output,
            format=format,
            view=view,
            **kwargs,
        )
    elif format in OG_FORMATS:
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
    elif format == "turtle":
        converter = OboGraphToRdfOwlConverter()
        converter.dump(graph, output)
    elif format == "cx":
        converter = OboGraphToCXConverter()
        converter.dump(graph, output)
    else:
        raise ValueError(f"Do not know how to write: {format}")
