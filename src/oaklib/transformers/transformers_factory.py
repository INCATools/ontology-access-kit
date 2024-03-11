import importlib
import re
from typing import Optional, Type, Union

from oaklib.datamodels.obograph import GraphDocument
from oaklib.implementations.obograph.obograph_implementation import (
    OboGraphImplementation,
)
from oaklib.interfaces import OboGraphInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.transformers.graph_transformer import GraphTransformer
from oaklib.transformers.ontology_transformer import OntologyTransformer


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_ontology_transformer(
    name: Union[str, Type], package: Optional[str] = None, **kwargs
) -> OntologyTransformer:
    if isinstance(name, str):
        if package is None:
            snakecase = camel_to_snake(name)
            package = f"oaklib.transformers.{snakecase}"
        package_obj = importlib.import_module(package)
        # instantiate the class
        class_obj = getattr(package_obj, name)
    else:
        class_obj = name
    return class_obj(**kwargs)


def apply_ontology_transformation(
    impl, transformer: Union[str, Type, OntologyTransformer], **kwargs
) -> DumperInterface:
    if not isinstance(transformer, OntologyTransformer):
        transformer = get_ontology_transformer(transformer, **kwargs)
    if isinstance(transformer, GraphTransformer):
        if not isinstance(impl, OboGraphInterface):
            raise NotImplementedError
        graph = impl.as_obograph()
        new_graph = transformer.transform(graph)
        gdoc = GraphDocument(graphs=[new_graph])
        new_impl = OboGraphImplementation(obograph_document=gdoc)
        return new_impl
    else:
        raise NotImplementedError
