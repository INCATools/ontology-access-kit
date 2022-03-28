import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, TextIO, Tuple, Any, Type

import click
from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.implementations.sqldb.sql_implementation import SqlImplementation
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.interfaces.ontology_interface import OntologyInterface
from obolib.resource import OntologyResource


@dataclass
class Settings:
    impl: Any = None

settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="path to file or URI for resource."
)
output_option = click.option(
    "-o",
    "--output",
    help="Output file, e.g. obo file"
)
output_format_option = click.option(
    "-O",
    "--output-format",
    help=f'Desired output format, e.g. {",".join([])}',
)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@input_option
def main(verbose: int, quiet: bool, input: str):
    """Run the obolib CLI."""
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)
    resource = OntologyResource()
    resource.slug = input
    impl_class: Type[OntologyInterface]
    if ':' in input:
        toks = input.split(':')
        scheme = toks[0]
        rest = ':'.join(toks[1:])
        if scheme == 'sqlite':
            impl_class = SqlImplementation
        if scheme == 'obolibrary':
            impl_class = ProntoImplementation
            if resource.slug.endswith('.obo'):
                resource.format = 'obo'
            resource.local = False
            resource.slug = resource.slug.replace('obolibrary:', '')
        else:
            raise ValueError(f'Scheme {scheme} not known')
    else:
        impl_class = ProntoImplementation
    logging.info(f'RESOURCE={resource}')
    settings.impl = impl_class.create(resource)

@main.command()
@click.argument("terms", nargs=-1)
@output_option
def search(terms, output: str):
    """
    Searches ontology for entities that have a label, alias, or other property matching a search term
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for t in terms:
            for curie in impl.basic_search(t):
                print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')




if __name__ == "__main__":
    main()