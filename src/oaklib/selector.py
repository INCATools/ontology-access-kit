import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Optional, Type

from oaklib import BasicOntologyInterface
from oaklib.implementations import GildaImplementation
from oaklib.implementations.bioportal.agroportal_implementation import (
    AgroportalImplementation,
)
from oaklib.implementations.bioportal.bioportal_implementation import (
    BioportalImplementation,
)
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.lov_implementation import LovImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph import UbergraphImplementation
from oaklib.implementations.wikidata.wikidata_implementation import (
    WikidataImplementation,
)
from oaklib.interfaces import OntologyInterface
from oaklib.resource import OntologyResource

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("oakext_") or name.startswith("oakx_")
}

RDF_SUFFIX_TO_FORMAT = {
    "ttl": "turtle",
    "rdf": "turtle",
    "jsonld": "json-ld",
    "json-ld": "json-ld",
}

SCHEME_DICT = {
    "sqlite": SqlImplementation,
    "ubergraph": UbergraphImplementation,
    "ontobee": OntobeeImplementation,
    "lov": LovImplementation,
    "sparql": SparqlImplementation,
    "rdflib": SparqlImplementation,
    "bioportal": BioportalImplementation,
    "agroportal": AgroportalImplementation,
    "wikidata": WikidataImplementation,
    "ols": OlsImplementation,
    "funowl": FunOwlImplementation,
    "pronto": ProntoImplementation,
    "obolibrary": ProntoImplementation,
    "prontolib": ProntoImplementation,
    "gilda": GildaImplementation,
}


def get_implementation_from_shorthand(
    descriptor: str, format: str = None
) -> BasicOntologyInterface:
    """
    See :ref:`get_resource_from_shorthand`

    Example:

    .. code :: python

        >>> oi = get_implementation_from_shorthand('my-ont.owl')
        >>> for term in oi.all_entities():
        >>>     ...

    :param descriptor:
    :param format:
    :return:
    """
    res = get_resource_from_shorthand(descriptor, format)
    return res.implementation_class(res)


def get_implementation_class_from_scheme(scheme: str):
    if scheme == "http" or scheme == "https":
        raise NotImplementedError("Web requests not implemented yet")
    else:
        return SCHEME_DICT[scheme]


def get_resource_imp_class_from_suffix_descriptor(
    suffix: str, resource: OntologyResource, descriptor: str
):

    if suffix == "db" or (resource.format and resource.format == "sqlite"):
        impl_class = SqlImplementation
        resource.slug = f"sqlite:///{Path(descriptor).absolute()}"
    elif resource.format and resource.format in RDF_SUFFIX_TO_FORMAT.values():
        impl_class = SparqlImplementation
    elif suffix in RDF_SUFFIX_TO_FORMAT:
        impl_class = SparqlImplementation
        resource.format = RDF_SUFFIX_TO_FORMAT[suffix]
    elif suffix == "owl":
        impl_class = SparqlImplementation
        resource.format = "xml"
        logging.warning("Using rdflib rdf/xml parser; this behavior may change in future")
    else:
        resource.local = True
        impl_class = ProntoImplementation

    return impl_class, resource


def get_resource_from_shorthand(descriptor: str, format: str = None) -> OntologyResource:
    """
    Maps from a shorthand descriptor to an OntologyResource.

    :param descriptor:
    :param format:
    :return:
    """
    resource = OntologyResource(format=format)
    resource.slug = descriptor
    impl_class: Optional[Type[OntologyInterface]] = None
    if descriptor:
        if ":" in descriptor:
            toks = descriptor.split(":")
            scheme = toks[0]
            resource.scheme = scheme
            rest = ":".join(toks[1:])
            if not rest:
                rest = None
            resource.slug = rest
            # Get impl_class based on scheme.
            impl_class = get_implementation_class_from_scheme(scheme)

            if impl_class == LovImplementation:
                logging.warning("lov scheme may become plugin in future")
            elif impl_class == SparqlImplementation:
                resource.url = rest
                resource.slug = None
            elif impl_class == ProntoImplementation:
                if resource.slug.endswith(".obo"):
                    resource.format = "obo"
                if scheme == "prontolib":
                    resource.local = False
                else:
                    resource.local = True
                resource.slug = rest
            else:
                for ext_name, ext_module in discovered_plugins.items():
                    try:
                        if scheme in ext_module.schemes:
                            impl_class = ext_module.schemes[scheme]
                            break
                    except AttributeError:
                        logging.info(f"Plugin {ext_name} does not declare schemes")
                if not impl_class:
                    raise ValueError(f"Scheme {scheme} not known")
        else:
            logging.info(f"No schema: assuming file path {descriptor}")
            suffix = descriptor.split(".")[-1]
            impl_class, resource = get_resource_imp_class_from_suffix_descriptor(
                suffix, resource, descriptor
            )
    else:
        raise ValueError("No descriptor")

    resource.implementation_class = impl_class
    return resource
