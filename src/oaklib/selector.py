import logging
import os
from pathlib import Path
from typing import Optional, Type

from oaklib import BasicOntologyInterface
from oaklib import datamodels as datamodels_package
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.interfaces import OntologyInterface
from oaklib.resource import OntologyResource

RDF_SUFFIX_TO_FORMAT = {
    "ttl": "turtle",
    "nt": "ntriples",
    "rdf": "turtle",
    "jsonld": "json-ld",
    "json-ld": "json-ld",
    "xml": "xml",
    "n3": "n3",
}


def get_adapter(descriptor: str, format: str = None) -> BasicOntologyInterface:
    """
    Gets an adapter (implementation) for a given descriptor.

    OAK allows for multiple different *adapters* (aka *implementations*);
    for example, :ref:`SQLImplementation` and :ref:`BioPortalImplementation`.

    This function allows you to get an adapter for a given descriptor.
    A descriptor combines a *scheme* followed by a colon symbol, and then
    optionally additional information that specifies how to access a particular
    resource or ontology within that scheme.

    Example:

    .. code :: python

        >>> from oaklib import get_adapter
        >>>
        >>> ## Use the simpleobo adapter to read a local OBO file:
        >>> adapter = get_adapter('simpleobo:my-ont.obo')
        >>> for label in oi.label("GO:0005634"):
        >>>     print(label)
        >>>
        >>> ## Use the ubergraph adapter, querying within GO
        >>> adapter = get_adapter('ubergraph:go')
        >>> for label in oi.label("GO:0005634"):
        >>>     print(label)
        >>>
        >>> ## Use the ubergraph adapter, querying within all
        >>> adapter = get_adapter('ubergraph:')
        >>> for label in oi.label("GO:0005634"):
        >>>     print(label)

    If you omit the scheme then OAK will try to guess the scheme based on the
    suffix of the descriptor

    .. code :: python

        >>> from oaklib import get_adapter
        >>>
        >>> ## Use an adapter that is able to read OBO Format:
        >>> ## (currently defaults to pronot)
        >>> adapter = get_adapter('my-ont.obo')
        >>> for label in oi.label("GO:0005634"):
        >>>     print(label)
        >>>
        >>> ## Use an adapter that is able to read SQLIte:
        >>> adapter = get_adapter('my-ont.db')
        >>> for label in oi.label("GO:0005634"):
        >>>     print(label)

    :param descriptor:
    :param format:
    :return:
    """
    res = get_resource_from_shorthand(descriptor, format)
    return res.implementation_class(res)


def get_implementation_from_shorthand(
    descriptor: str, format: str = None
) -> BasicOntologyInterface:
    """
    Gets an adapter (implementation) for a given descriptor.

    NOTE: this is an alias for `get_adapter` - use this instead,
    get_implementation_from_shorthand will be deprecated in future.

    :param descriptor:
    :param format:
    :return:
    """
    return get_adapter(descriptor, format)


def get_implementation_class_from_scheme(scheme: str) -> Type[OntologyInterface]:
    """
    Given a selector schema (e.g. sqlite, ubergraph, pronto, etc.) return the adapter class.

    :param scheme:
    :return: adapter (implementation) class that implements the OntologyInterface
    """
    if scheme == "http" or scheme == "https":
        raise NotImplementedError("Web requests not implemented yet")
    else:
        # return SCHEME_DICT[scheme]
        from oaklib.implementations import get_implementation_resolver

        return get_implementation_resolver().lookup(scheme)


def get_resource_imp_class_from_suffix_descriptor(
    suffix: str, resource: OntologyResource, descriptor: str
):
    from oaklib.implementations import (  # SimpleOboImplementation,
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
    # elif suffix == "obo":
    #     impl_class = SimpleOboImplementation
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

        # Prevent the driveletter from being interpreted as scheme on Windows.
        if ":" in descriptor and not os.path.exists(descriptor):
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
                if resource.slug and resource.slug.endswith(".obo"):
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
