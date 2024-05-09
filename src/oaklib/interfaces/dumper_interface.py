import logging
from abc import ABC
from typing import Any, Dict

from linkml_runtime.dumpers import json_dumper

from oaklib.converters.obo_graph_to_cx_converter import OboGraphToCXConverter
from oaklib.converters.obo_graph_to_fhir_converter import OboGraphToFHIRConverter
from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.converters.obo_graph_to_rdf_owl_converter import OboGraphToRdfOwlConverter
from oaklib.datamodels.obograph import GraphDocument
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface

SUMMARY_STATISTICS_MAP = Dict[str, Any]

OBOGRAPH_CONVERTERS = {
    "obo": OboGraphToOboFormatConverter,
    "fhirjson": OboGraphToFHIRConverter,
    "owl": OboGraphToRdfOwlConverter,
    "turtle": OboGraphToRdfOwlConverter,
    "rdf": OboGraphToRdfOwlConverter,
    "rdfxml": (OboGraphToRdfOwlConverter, {"format": "xml"}),
    "cx": OboGraphToCXConverter,
    "obojson": None,
    "json": None,
}

FORMAT_SYNONYMS = {
    "json": "obojson",
    "obographs": "obojson",
}


class DumperInterface(BasicOntologyInterface, ABC):
    """
    An OntologyInterface that is capable of exporting entire contents.
    """

    def dump(
        self, path: str = None, syntax: str = None, enforce_canonical_ordering=False, **kwargs
    ):
        """
        Exports current contents.

        :param path: Path to file to write to. If None, then write to stdout.
        :param syntax: Syntax to use. If None, then use the default syntax.
        :param enforce_canonical_ordering:
        :param kwargs: Additional arguments to pass to the dumper
        :return:
        """
        logging.info(f"Dumping graph to {path} in {syntax}")
        if not syntax:
            raise ValueError(f"Unknown syntax: {syntax}")
        if syntax in FORMAT_SYNONYMS:
            syntax = FORMAT_SYNONYMS[syntax]
        if syntax not in OBOGRAPH_CONVERTERS:
            raise ValueError(f"Cannot handle syntax: {syntax}")
        if not isinstance(self, OboGraphInterface):
            raise ValueError(f"Cannot handle interface: {self}")
        og = self.as_obograph()
        ogdoc = GraphDocument(graphs=[og])
        converter_class = OBOGRAPH_CONVERTERS.get(syntax, None)
        if not converter_class:
            json_str = json_dumper.dumps(ogdoc, inject_type=False)
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(json_str)
            else:
                print(json_str)
        else:
            if isinstance(converter_class, tuple):
                converter_class, converter_kwargs = converter_class
                kwargs.update(converter_kwargs)
            converter = converter_class()
            converter.enforce_canonical_ordering = enforce_canonical_ordering
            logging.info(f"Using {converter}, kwargs={kwargs}")
            converter.curie_converter = self.converter
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            if "format" not in kwargs:
                kwargs["format"] = syntax
            converter.dump(ogdoc, target=path, **kwargs)
