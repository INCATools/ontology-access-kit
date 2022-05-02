import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Union

from oaklib.implementations.bioportal.bioportal_implementation import BioportalImplementation
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph import UbergraphImplementation
from oaklib.implementations.wikidata.wikidata_implementation import WikidataImplementation
from oaklib.interfaces import OntologyInterface
from oaklib.resource import OntologyResource


RDF_SUFFIX_TO_FORMAT = {
    'ttl': 'turtle',
    'rdf': 'turtle',
    'jsonld': 'json-ld',
    'json-ld': 'json-ld',
}

def get_implementation_from_shorthand(descriptor: str, format: str = None) -> OntologyResource:
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

def get_resource_from_shorthand(descriptor: str, format: str = None) -> OntologyResource:
    """
    Maps from a shorthand descriptor to an OntologyResource.




    :param descriptor:
    :param format:
    :return:
    """
    resource = OntologyResource(format=format)
    resource.slug = descriptor
    impl_class: Type[OntologyInterface]
    if descriptor:
        if ':' in descriptor:
            toks = descriptor.split(':')
            scheme = toks[0]
            rest = ':'.join(toks[1:])
            if not rest:
                rest= None
            resource.slug = rest
            if scheme == 'sqlite':
                impl_class = SqlImplementation
                resource.slug = f'sqlite:///{Path(rest).absolute()}'
            elif scheme == 'ubergraph':
                impl_class = UbergraphImplementation
            elif scheme == 'ontobee':
                impl_class = OntobeeImplementation
            elif scheme == 'sparql':
                impl_class = SparqlImplementation
            elif scheme == 'bioportal':
                impl_class = BioportalImplementation
            elif scheme == 'wikidata':
                impl_class = WikidataImplementation
            elif scheme == 'ols':
                impl_class = OlsImplementation
            elif scheme == 'pronto':
                impl_class = ProntoImplementation
                if resource.slug.endswith('.obo'):
                    resource.format = 'obo'
                resource.local = True
                resource.slug = rest
            elif scheme == 'obolibrary' or scheme == 'prontolib':
                impl_class = ProntoImplementation
                if resource.slug.endswith('.obo'):
                    resource.format = 'obo'
                resource.local = False
                resource.slug = rest
            elif scheme == 'http' or scheme == 'https':
                raise NotImplementedError(f'Web requests not implemented yet')
            else:
                raise ValueError(f'Scheme {scheme} not known')
        else:
            logging.info(f'No schema: assuming file path {descriptor}')
            suffix = descriptor.split('.')[-1]
            if suffix == 'db' or (format and format == 'sqlite'):
                impl_class = SqlImplementation
                resource.slug = f'sqlite:///{Path(descriptor).absolute()}'
            elif format and format in RDF_SUFFIX_TO_FORMAT.values():
                impl_class = SparqlImplementation
            elif suffix in RDF_SUFFIX_TO_FORMAT:
                impl_class = SparqlImplementation
                resource.format = RDF_SUFFIX_TO_FORMAT[suffix]
            elif suffix == 'owl':
                impl_class = SparqlImplementation
                resource.format = 'xml'
                logging.warning(f'Using rdflib rdf/xml parser; this behavior may change in future')
            else:
                resource.local = True
                impl_class = ProntoImplementation
    else:
        raise ValueError(f'No descriptor')
    resource.implementation_class = impl_class
    return resource
