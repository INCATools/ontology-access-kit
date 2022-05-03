"""
Command Line Interface to OMK
-----------------------------

"""
import logging
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, TextIO, Tuple, Any, Type

import click
from linkml_runtime.dumpers import yaml_dumper
from oaklib.implementations.aggregator.aggregator_implementation import AggregatorImplementation
from oaklib.interfaces import BasicOntologyInterface, OntologyInterface, ValidatorInterface, SubsetterInterface
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.omk.omk_mapping_utils import caclulate_pairwise_relational_diff
from oaklib.resource import OntologyResource
from oaklib.selector import get_resource_from_shorthand, get_implementation_from_shorthand
from oaklib.cli import input_option, output_option, output_type_option, add_option, input_type_option, Settings
import oaklib.cli as oak_cli

settings = Settings()



@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@input_option
@input_type_option
@add_option
def main(verbose: int, quiet: bool, input: str, input_type: str, add: List):
    """Run the oaklib Command Line.

    A subcommand must be passed - for example: ancestors, terms, ...

    Most commands require an input ontology to be specified:

        runoak -i <INPUT SPECIFICATION> SUBCOMMAND <SUBCOMMAND OPTIONS AND ARGUMENTS>

    Get help on any command, e.g:

        runoak viz -h
    """
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

    # TODO: avoid repetition with main CLI
    if input:
        impl_class: Type[OntologyInterface]
        resource = get_resource_from_shorthand(input, format=input_type)
        impl_class = resource.implementation_class
        logging.info(f'RESOURCE={resource}')
        settings.impl = impl_class(resource)
    if add:
        impls = [get_implementation_from_shorthand(d) for d in add]
        if settings.impl:
            impls = [settings.impl] + impls
        settings.impl = AggregatorImplementation(implementations=impls)


@main.command()
@click.option('-S', '--source',
              multiple=True,
              help="ontology prefixes  e.g. HP, MP")
@click.option('--other-input',
              help="Additional input file")
@click.option('--other-input-type',
              help="Type of additional input file")
#@output_option
def mdiff(source, other_input, other_input_type):
    oi = settings.impl
    if other_input:
        other_oi = get_implementation_from_shorthand(other_input, format=other_input_type)
    else:
        other_oi = oi
    for r in caclulate_pairwise_relational_diff(oi, other_oi, sources=list(source)):
        print(r)


if __name__ == "__main__":
    main()
