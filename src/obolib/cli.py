import logging
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, TextIO, Tuple, Any, Type

import click
from obolib.implementations.pronto.pronto_implementation import ProntoImplementation
from obolib.implementations.sqldb.sql_implementation import SqlImplementation
from obolib.interfaces import BasicOntologyInterface, OntologyInterface, ValidatorInterface, SubsetterInterface
from obolib.interfaces.obograph_interface import OboGraphInterface
from obolib.resource import OntologyResource
from obolib.types import PRED_CURIE
from obolib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    load_lexical_index, load_mapping_rules, add_labels_from_uris
from obolib.utilities.obograph_utils import draw_graph, graph_to_image
import sssom.writers as sssom_writers
from obolib.vocabulary.vocabulary import IS_A, PART_OF

# https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
from obolib import conf as conf_package

DEFAULT_STYLEMAP = 'obograph-style.json'


@dataclass
class Settings:
    impl: Any = None


settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="path to file or URI for resource."
)
input_type_option = click.option(
    "-I",
    "--input-type",
    help="Input type."
)
output_option = click.option(
    "-o",
    "--output",
    help="Output file, e.g. obo file"
)
output_type_option = click.option(
    "-O",
    "--output-type",
    help=f'Desired output type, e.g. {",".join([])}',
)
predicates_option = click.option(
    "-p",
    "--predicates",
    help="A comma-separated list of predicates"
)

def _process_predicates_arg(preds_str: str) -> List[PRED_CURIE]:
    if preds_str is None:
        return None
    inputs = preds_str.split(',')
    preds = [_shorthand_to_pred_curie(p) for p in inputs]
    return preds

def _shorthand_to_pred_curie(shorthand: str) -> PRED_CURIE:
    if shorthand == 'i':
        return IS_A
    elif shorthand == 'p':
        return PART_OF
    else:
        return shorthand


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
    if input:
        if ':' in input:
            toks = input.split(':')
            scheme = toks[0]
            rest = ':'.join(toks[1:])
            if scheme == 'sqlite':
                impl_class = SqlImplementation
                resource.slug = f'sqlite:///{Path(rest).absolute()}'
            elif scheme == 'obolibrary':
                impl_class = ProntoImplementation
                if resource.slug.endswith('.obo'):
                    resource.format = 'obo'
                resource.local = False
                resource.slug = resource.slug.replace('obolibrary:', '')
            else:
                raise ValueError(f'Scheme {scheme} not known')
        else:
            resource.local = True
            impl_class = ProntoImplementation
        logging.info(f'RESOURCE={resource}')
        settings.impl = impl_class(resource)


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


@main.command()
@click.argument("subset")
@output_option
def list_subset(subset, output: str):
    """
    Shows IDs in subset
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.curies_by_subset(subset):
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option("--view/--no-view",
              default=True,
              show_default=True,
              help="if view is set then open the image after rendering")
@click.option("--down/--no-down",
              default=True,
              show_default=True,
              help="traverse down")
@click.option('-S', '--stylemap',
              help='a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/')
@click.option('-C', '--configure',
              help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `')
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
def viz(terms, predicates, down, view, stylemap, configure, output: str):
    """
    Visualizing an ancestor graph using obographviz
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        if stylemap is None:
            conf_path = os.path.dirname(conf_package.__file__)
            stylemap = str(Path(conf_path) / DEFAULT_STYLEMAP)
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(impl.multiterm_search(terms))
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        logging.info(f'Drawing graph seeded from {curies}')
        imgfile = graph_to_image(graph, seeds=curies, stylemap=stylemap, configure=configure, imgfile=output)
        if view:
            subprocess.run(['open', imgfile])
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
def ancestors(terms, predicates, output: str):
    """
    List all ancestors
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        graph = impl.ancestor_graph(list(impl.multiterm_search(terms)), predicates=actual_predicates)
        for n in graph.nodes:
            print(f'{n.id} ! {n.label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
def descendants(terms, predicates, output: str):
    """
    List all descendants
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        graph = impl.descendant_graph(list(impl.multiterm_search(terms)), predicates=actual_predicates)
        for n in graph.nodes:
            print(f'{n.id} ! {n.label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@output_option
def info(terms, output: str):
    """
    Show info on terms
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        curies = list(impl.multiterm_search(terms))
        for curie in curies:
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@output_option
def terms(output: str):
    """
    List all terms
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.all_entity_curies():
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def axioms(output: str):
    """
    List all axioms

    TODO: as soon as funowl does not pin rdf version
    """
    impl = settings.impl
    #if isinstance(impl, OwlInterface):
    #    for axiom in impl.axioms():
    #        print(f'{axiom}')
    #else:
    #    raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')
    raise NotImplementedError


@main.command()
@output_option
def validate(output: str):
    """
    Validate an ontology

    INCOMPLETE
    """
    impl = settings.impl
    if isinstance(impl, ValidatorInterface):
        for curie in impl.term_curies_without_definitions():
            print(f'NO DEFINITION: {curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("curies", nargs=-1)
@output_option
def subset(curies, output: str):
    """
    Extracts a subset

    INCOMPLETE
    """
    impl = settings.impl
    if isinstance(impl, SubsetterInterface):
        subont = impl.extract_subset_ontology(curies)
        print(f'TODO: {subont}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option("--lexical-index-file", "-L",
              help="path to lexical index. This is recreated each time unless --no-recreate is passed")
@click.option("--rules-file", "-R",
              help="path to rules file. Conforms to rules_datamodel.")
@click.option("--add-labels/--no-add-labels",
              default=False,
              show_default=True,
              help="Populate empty labels with URI fragments or CURIE local IDs, for ontologies that use semantic IDs")
@click.option("--recreate/--no-recreate",
              default=True,
              show_default=True,
              help="if true and lexical index is specified, always recreate, otherwise load from index")
@output_option
def lexmatch(output: str, recreate, rules_file, lexical_index_file, add_labels):
    """
    Generates lexical index and mappings

    Examples:
        lexmatch -i foo.obo -o foo.sssom.tsv

    Outputting intermediate index:
        lexmatch -i foo.obo -L foo.index.yaml -o foo.sssom.tsv

    Using custom rules:
        lexmatch -i foo.obo -R match_rules.yaml -L foo.index.yaml -o foo.sssom.tsv
    """
    impl = settings.impl
    if rules_file:
        ruleset = load_mapping_rules(rules_file)
    else:
        ruleset = None
    if isinstance(impl, BasicOntologyInterface):
        if add_labels:
            add_labels_from_uris(impl)
        if not recreate and Path(lexical_index_file).exists():
            ix = load_lexical_index(lexical_index_file)
        else:
            ix = create_lexical_index(impl)
        if lexical_index_file:
            if recreate:
                save_lexical_index(ix, lexical_index_file)
        msdf = lexical_index_to_sssom(impl, ix, ruleset=ruleset)
        with open(output, 'w', encoding='utf-8') as file:
            sssom_writers.write_table(msdf, file)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


if __name__ == "__main__":
    main()
