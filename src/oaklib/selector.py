import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Union

from oaklib.implementations.bioportal.bioportal_implementation import BioportalImplementation
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph import UbergraphImplementation
from oaklib.interfaces import OntologyInterface
from oaklib.resource import OntologyResource


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
            elif scheme == 'bioportal':
                impl_class = BioportalImplementation
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
            if descriptor.endswith('.db') or (format and format == 'sqlite'):
                impl_class = SqlImplementation
                resource.slug = f'sqlite:///{Path(descriptor).absolute()}'
            else:
                resource.local = True
                impl_class = ProntoImplementation
    else:
        raise ValueError(f'No descriptor')
    resource.implementation_class = impl_class
    return resource
