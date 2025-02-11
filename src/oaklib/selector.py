import gzip
import io
import logging
import os
from pathlib import Path
from typing import List, Optional, Type, TypeVar, Union

import requests
from deprecation import deprecated
from linkml_runtime.loaders import yaml_loader

from oaklib import BasicOntologyInterface
from oaklib import datamodels as datamodels_package
from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels.input_specification import InputSpecification, Normalizer
from oaklib.implementations import GildaImplementation
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.obograph.obograph_implementation import OboGraphImplementation
from oaklib.interfaces import OntologyInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
    EntityNormalizer,
)
from oaklib.parsers.association_parser_factory import get_association_parser
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


ASSOCIATION_REGISTRY = {
    "hpoa": ([], "hpoa", "http://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa", False),
    "hpoa_g2p": (
        [],
        "hpoa_g2p",
        "http://purl.obolibrary.org/obo/hp/hpoa/genes_to_phenotype.txt",
        False,
    ),
    "hpoa_g2d": (
        [],
        "hpoa_g2d",
        "http://purl.obolibrary.org/obo/hp/hpoa/genes_to_disease.txt",
        False,
    ),
    "gaf": (["group"], "gaf", "http://current.geneontology.org/annotations/{group}.gaf.gz", True),
    "gaf_archive": (
        ["date", "group"],
        "gaf",
        "http://release.geneontology.org/{date}/annotations/{group}.gaf.gz",
        True,
    ),
    "gencc": (
        [],
        "gencc",
        "https://search.thegencc.org/download/action/submissions-export-csv",
        False,
    ),
    "medgen_mim_g2d": (
        [],
        "medgen_mim_g2d",
        "http://ftp.ncbi.nih.gov/gene/DATA/mim2gene_medgen",
        False,
    ),
}

T = TypeVar("T", bound=BasicOntologyInterface)


def get_adapter(
    descriptor: Union[str, Path, InputSpecification],
    format: str = None,
    implements: Optional[Type[T]] = None,
    **kwargs,
) -> T:
    """
    Gets an adapter (implementation) for a given descriptor.

    OAK allows for multiple different *adapters* (aka *implementations*);
    for example, :ref:`SQLImplementation` and :ref:`BioPortalImplementation`.

    This function allows you to get an adapter for a given descriptor.
    A descriptor combines a *scheme* followed by a colon symbol, and then
    optionally additional information that specifies how to access a particular
    resource or ontology within that scheme.

    Example:
    -------
    .. packages :: python

        >>> from oaklib import get_adapter
        >>>
        >>> ## Use the simpleobo adapter to read a local OBO file:
        >>> adapter = get_adapter('simpleobo:tests/input/go-nucleus.obo')
        >>> print(adapter.label("GO:0005634"))
        nucleus
        >>> ## Use the ubergraph adapter, querying within GO
        >>> adapter = get_adapter('ubergraph:go')
        >>> print(adapter.label("GO:0005634"))
        nucleus
        >>> ## Use the ubergraph adapter, querying within all
        >>> adapter = get_adapter('ubergraph:')
        >>> print(adapter.label("GO:0005634"))
        nucleus

    If you omit the scheme then OAK will try to guess the scheme based on the
    suffix of the descriptor

    .. packages :: python

        >>> from oaklib import get_adapter
        >>> ## Use an adapter that is able to read OBO Format:
        >>> ## (currently defaults to pronot)
        >>> adapter = get_adapter('tests/input/go-nucleus.obo')
        >>> print(adapter.label("GO:0005634"))
        nucleus
        >>> ## Use an adapter that is able to read SQLIte:
        >>> adapter = get_adapter('tests/input/go-nucleus.obo')
        >>> print(adapter.label("GO:0005634"))
        nucleus

    If you want to pass extra information through to the implementation
    class, you can do so with keyword arguments:

    .. packages :: python

        >>> from oaklib import get_adapter
        >>> from gilda import get_grounder
        >>> grounder = get_grounder()
        >>> adapter = get_adapter("gilda:", grounder=grounder)
        >>> annotations = adapter.annotate_text("nucleus")

    :param descriptor:
        The input specification, path to a YAML describing an input specification,
        or a shorthand string for instantiating an ontology interface
    :param format: file format/syntax, e.g obo, turtle
    :param kwargs: Keyword arguments to pass through to the implementation class
    :return: An instantiated interface

    """
    if isinstance(descriptor, InputSpecification):
        return _get_adapter_from_specification(descriptor)
    if isinstance(descriptor, Path):
        descriptor = str(descriptor)
    if descriptor.endswith(".yaml"):
        input_specification = yaml_loader.load(open(descriptor), InputSpecification)
        return get_adapter(input_specification)
    res = get_resource_from_shorthand(descriptor, format)
    return res.implementation_class(res, **kwargs)


def _get_adapter_from_specification(
    input_specification: InputSpecification,
) -> BasicOntologyInterface:
    """
    Gets an adapter (implementation) for a given input specification.

    :param input_specification:
    :return:
    """
    if not input_specification.ontology_resources:
        raise ValueError("No ontology resources specified")
    if len(input_specification.ontology_resources) == 1:
        r = list(input_specification.ontology_resources.values())[0]
        adapter = get_adapter(str(r.selector))
    else:
        from oaklib.implementations import AggregatorImplementation

        adapter = AggregatorImplementation(
            implementations=[
                get_adapter(r.selector) for r in input_specification.ontology_resources.values()
            ]
        )
    if input_specification.association_resources:
        if not isinstance(adapter, AssociationProviderInterface):
            raise ValueError(f"Adapter {adapter} does not support associations")
        for r in input_specification.association_resources.values():
            normalizers = [
                EntityNormalizer(
                    adapter=get_adapter(n.selector),
                    source_prefixes=n.source_prefixes,
                    target_prefixes=n.target_prefixes,
                    slots=n.slots,
                    prefix_alias_map={str(k): str(v.alias) for k, v in n.prefix_alias_map.items()},
                )
                for n in r.normalizers
            ]
            logging.info(f"Normalizers: {normalizers}")
            add_associations(
                adapter,
                r.selector,
                r.format,
                normalizers,
                primary_knowledge_source=r.primary_knowledge_source,
                aggregator_knowledge_source=r.aggregator_knowledge_source,
            )
    return adapter


def add_associations(
    adapter: AssociationProviderInterface,
    descriptor: str,
    format: str = None,
    normalizers: Optional[List[Normalizer]] = None,
    primary_knowledge_source: Optional[str] = None,
    aggregator_knowledge_source: Optional[str] = None,
) -> None:
    """
    Adds associations to an adapter.

    :param adapter:
    :param descriptor:
    :param format:
    :param normalizers:
    :return:
    """
    logging.info(
        f"Adding associations from {descriptor} ({primary_knowledge_source}) using {format} format"
    )
    # TODO: do more robust windows check
    if ":" in descriptor and not descriptor.startswith("file:") and not descriptor[1] == ":":
        scheme, path = descriptor.split(":", 1)
        if scheme not in ASSOCIATION_REGISTRY:
            raise ValueError(f"Unknown association scheme: {scheme}")
        entry = ASSOCIATION_REGISTRY[scheme]
        params, format, url_template, compressed = entry
        if params:
            param_vals = dict(zip(params, path.split("//"), strict=False))
        else:
            param_vals = {}
        url = url_template.format(**param_vals)
        # TODO: add option to cache using pystow
        if compressed:
            file = file_from_gzip_url(url)
        else:
            file = file_from_url(url)
        association_parser = get_association_parser(format)
        logging.info(f"Adding associations from {url}")
        if primary_knowledge_source is None:
            primary_knowledge_source = f"infores:{scheme}"
        if aggregator_knowledge_source is None:
            aggregator_knowledge_source = f"infores:{scheme}"
        assocs = list(association_parser.parse(file))
        association_parser.add_metadata(
            assocs,
            primary_knowledge_source=primary_knowledge_source,
            aggregator_knowledge_source=aggregator_knowledge_source,
        )
        adapter.add_associations(assocs, normalizers=normalizers)
        return
    if not format:
        toks = descriptor.split(".")
        while toks:
            format = toks[-1]
            if format not in ("csv", "tsv", "txt"):
                break
            toks = toks[:-1]
    if not format:
        raise ValueError(f"Could not determine format from descriptor {descriptor}")
    association_parser = get_association_parser(format)
    path = descriptor
    with open(path) as file:
        logging.info(f"Adding associations from {path} ({descriptor})")
        assocs = list(association_parser.parse(file))
        logging.info(f"Read {len(assocs)} associations from {path}")
        association_parser.add_metadata(assocs, primary_knowledge_source=primary_knowledge_source)
        adapter.add_associations(assocs, normalizers=normalizers)


def file_from_gzip_url(url, is_compressed=False):
    with requests.get(url, stream=True, timeout=TIMEOUT_SECONDS) as response:
        response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
        # Wrap the response's raw stream in a binary file-like object
        binary_file_like_object = io.BytesIO(response.raw.read())

        # Uncompress the gzipped binary file-like object using gzip
        return gzip.open(binary_file_like_object, "rt")


def file_from_url(url):
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code
    # Create a file-like object using the response content
    file_like_object = io.StringIO(response.text)
    return file_like_object


@deprecated("Use get_adapter instead")
def get_implementation_from_shorthand(
    descriptor: str, format: str = None
) -> BasicOntologyInterface:
    """
    Gets an adapter (implementation) for a given descriptor.

    .. warning ::

       this is an alias for `get_adapter` - use this instead,
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
    elif suffix == "json":
        impl_class = OboGraphImplementation
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

    if not descriptor:
        raise ValueError("No descriptor provided")
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
        elif impl_class == GildaImplementation:
            resource.slug = Path(rest).resolve().as_posix() if rest is not None else rest
        elif not impl_class:
            raise ValueError(f"Scheme {scheme} not known")
    else:
        logging.info(f"No schema: assuming file path {descriptor}")
        suffix = descriptor.split(".")[-1]
        impl_class, resource = get_resource_imp_class_from_suffix_descriptor(
            suffix, resource, descriptor
        )

    resource.implementation_class = impl_class
    return resource
