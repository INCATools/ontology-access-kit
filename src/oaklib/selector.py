import logging
import os
from pathlib import Path
from typing import Optional, Type

from oaklib import BasicOntologyInterface
from oaklib import datamodels as datamodels_package
from oaklib.implementations import GildaImplementation
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.ontoportal.agroportal_implementation import (
    AgroPortalImplementation,
)
from oaklib.implementations.ontoportal.bioportal_implementation import (
    BioPortalImplementation,
)
from oaklib.implementations.ontoportal.ecoportal_implementation import (
    EcoPortalImplementation,
)
from oaklib.implementations.ontoportal.matportal_implementation import (
    MatPortalImplementation,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
from oaklib.implementations.sparql.lov_implementation import LovImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph import UbergraphImplementation
from oaklib.implementations.wikidata.wikidata_implementation import (
    WikidataImplementation,
)
from oaklib.interfaces import OntologyInterface
from oaklib.resource import OntologyResource

RDF_SUFFIX_TO_FORMAT = {
    "ttl": "turtle",
    "rdf": "turtle",
    "jsonld": "json-ld",
    "json-ld": "json-ld",
}

# Deprecated?
SCHEME_DICT = {
    "sqlite": SqlImplementation,
    "ubergraph": UbergraphImplementation,
    "ontobee": OntobeeImplementation,
    "lov": LovImplementation,
    "sparql": SparqlImplementation,
    "rdflib": SparqlImplementation,
    "bioportal": BioPortalImplementation,
    "agroportal": AgroPortalImplementation,
    "ecoportal": EcoPortalImplementation,
    "matportal": MatPortalImplementation,
    "wikidata": WikidataImplementation,
    "ols": OlsImplementation,
    "funowl": FunOwlImplementation,
    "pronto": ProntoImplementation,
    "simpleobo": SimpleOboImplementation,
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


def get_implementation_class_from_scheme(scheme: str) -> Type[OntologyInterface]:
    if scheme == "http" or scheme == "https":
        raise NotImplementedError("Web requests not implemented yet")
    else:
        # return SCHEME_DICT[scheme]
        from oaklib.implementations import implementation_resolver

        return implementation_resolver.lookup(scheme)


def get_resource_imp_class_from_suffix_descriptor(
    suffix: str, resource: OntologyResource, descriptor: str
):
    from oaklib.implementations import (
        ProntoImplementation,
        SparqlImplementation,
        SqlImplementation,
    )

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
    elif suffix == "ofn":
        impl_class = FunOwlImplementation
    else:
        resource.local = True
        impl_class = ProntoImplementation

    return impl_class, resource


def get_resource_from_shorthand(
    descriptor: str, format: str = None, import_depth: Optional[int] = None
) -> OntologyResource:
    """
    Maps from a shorthand descriptor to an OntologyResource.

    :param descriptor:
    :param format: file format/syntax, e.g obo, turtle
    :param import_depth: maximum import depth to traverse
    :return:
    """
    from oaklib.implementations import (
        LovImplementation,
        ProntoImplementation,
        SparqlImplementation,
    )

    resource = OntologyResource(format=format)
    resource.import_depth = import_depth
    resource.slug = descriptor
    impl_class: Optional[Type[OntologyInterface]] = None
    if descriptor:
        # Pre-processing
        if descriptor.startswith("datamodel:"):
            # introspect the internal OAK datamodel.
            # the oak data models are intended for programmatic use, but the documentation
            # is also exposed as a pseudo-ontology by default.
            # this allows us to do things such as use the OAK CLI to find all classes
            # or fields in a data model, see their hierarchy, etc
            # this is currently an advanced/experimental feature, if useful
            # it should be exposed in user-facing sphinx docs.
            descriptor = descriptor.replace("datamodel:", "")
            dm_path = os.path.dirname(datamodels_package.__file__)
            descriptor = f"{Path(dm_path)/descriptor}.owl.ttl"
            logging.info(f"Introspecting datamodel from {descriptor}")
            resource.slug = descriptor
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
            elif not impl_class:
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
