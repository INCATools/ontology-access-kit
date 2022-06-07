"""
Command Line Interface to OAK
-----------------------------

Executed using "runoak" command
"""
# TODO: order commands. See https://stackoverflow.com/questions/47972638/how-can-i-define-the-order-of-click-sub-commands-in-help
import logging
import os
import subprocess
import sys
import re
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, unique
from pathlib import Path
from typing import Dict, List, Sequence, TextIO, Tuple, Any, Type, Iterator, Union, Iterable

import click
import rdflib
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.validation_datamodel import ValidationConfiguration
from oaklib.implementations import ProntoImplementation
from oaklib.implementations.aggregator.aggregator_implementation import AggregatorImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.interfaces import BasicOntologyInterface, OntologyInterface, ValidatorInterface, SubsetterInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_info_writer import StreamingInfoWriter
from oaklib.io.streaming_markdown_writer import StreamingMarkdownWriter
from oaklib.io.streaming_obo_writer import StreamingOboWriter
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.resource import OntologyResource
from oaklib.selector import get_resource_from_shorthand, get_implementation_from_shorthand
from oaklib.types import PRED_CURIE, CURIE
from oaklib.utilities.apikey_manager import set_apikey_value
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.lexical.lexical_indexer import create_lexical_index, save_lexical_index, lexical_index_to_sssom, \
    load_lexical_index, load_mapping_rules, add_labels_from_uris
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter
from oaklib.utilities.obograph_utils import draw_graph, graph_to_image, default_stylemap_path, graph_to_tree, \
    as_digraph, ancestors_with_stats
import sssom.writers as sssom_writers
from oaklib.datamodels.vocabulary import IS_A, PART_OF, EQUIVALENT_CLASS
from oaklib.utilities.subsets.slimmer_utils import roll_up_to_named_subset
from oaklib.utilities.taxon.taxon_constraint_utils import get_term_with_taxon_constraints, test_candidate_taxon_constraint, parse_gain_loss_file
import oaklib.datamodels.taxon_constraints as tcdm


@unique
class SetOperation(Enum):
    intersection = "intersection"
    union = "union"
    difference = "difference"
    symmetric_difference = "symmetric_difference"
    reverse_difference = "reverse_difference"


@dataclass
class Settings:
    impl: Any = None


settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="path to input implementation specification."
)
add_option = click.option(
    "-a",
    "--add",
    multiple=True,
    help="additional implementation specification."
)
set_operation_option = click.option(
    '--operation',
    type=click.Choice([x.value for x in SetOperation]),
    help="set operation, where left set is stdin list and right set is arguments."
)
input_type_option = click.option(
    "-I",
    "--input-type",
    help="Input type."
)
output_option = click.option(
    "-o",
    "--output",
    type=click.File(mode="w"),
    default=sys.stdout,
    help="Output file, e.g. obo file"
)
output_type_option = click.option(
    "-O",
    "--output-type",
    help=f'Desired output type',
)
predicates_option = click.option(
    "-p",
    "--predicates",
    help="A comma-separated list of predicates"
)
display_option = click.option(
    "-D",
    "--display",
    default='',
    help="A comma-separated list of display options"
)


def _process_predicates_arg(preds_str: str) -> List[PRED_CURIE]:
    if preds_str is None:
        return None
    inputs = preds_str.split(',')
    preds = [_shorthand_to_pred_curie(p) for p in inputs]
    return preds


# TODO: move to vocab
def _shorthand_to_pred_curie(shorthand: str) -> PRED_CURIE:
    if shorthand == 'i':
        return IS_A
    elif shorthand == 'p':
        return PART_OF
    elif shorthand == 'e':
        return EQUIVALENT_CLASS
    else:
        return shorthand


def query_terms_iterator(terms: List[str], impl: BasicOntologyInterface) -> Iterator[CURIE]:
    """
    Turn list of tokens that represent a term query into an iterator for curies

    For examples, see test_cli

    TODO: reimplement using an explicit query model

    :param terms:
    :param impl:
    :return:
    """
    iterators: List[Union[CURIE, Iterable[CURIE]]] = []
    predicates = None
    if isinstance(terms, tuple):
        terms = list(terms)

    def nxt(iterators) -> Iterator[CURIE]:
        for it in iterators:
            if isinstance(it, str):
                yield it
            else:
                for x in it:
                    yield x
    while len(terms) > 0:
        term = terms[0]
        terms = terms[1:]
        if term == '-':
            for line in sys.stdin.readlines():
                m = re.match(r'^(\S+)', line)
                iterators.append(m.group(1))
        elif re.match(r'^(\w+):(\S+)$', term):
            iterators.append(term)
        elif re.match(r'^\.predicates=(\S*)$', term):
            m = re.match(r'^\.predicates=(\S*)$', term)
            predicates = _process_predicates_arg(m.group(1))
        elif re.match(r'^http(\S+)$', term):
            iterators.append(term)
        elif term == '.and':
            rest = list(query_terms_iterator(terms, impl))
            for x in nxt(iterators):
                if x in rest:
                    yield x
            terms = []
        elif term == '.not':
            rest = list(query_terms_iterator(terms, impl))
            for x in nxt(iterators):
                if x not in rest:
                    yield x
            terms = []
        elif term == '.or':
            # or is implicit
            pass
        elif term.startswith('.in'):
            subset = terms[0]
            terms = terms[1:]
            iterators.append(impl.curies_by_subset(subset))
        elif term.startswith('.desc'):
            rest = list(query_terms_iterator([terms[0]], impl))
            terms = terms[1:]
            if isinstance(impl, OboGraphInterface):
                iterators.append(impl.descendants(rest, predicates=predicates))
            else:
                raise NotImplementedError
        elif term.startswith('.anc'):
            rest = list(query_terms_iterator([terms[0]], impl))
            terms = terms[1:]
            if isinstance(impl, OboGraphInterface):
                iterators.append(impl.ancestors(rest, predicates=predicates))
            else:
                raise NotImplementedError
        else:
            if isinstance(impl, SearchInterface):
                cfg = create_search_configuration(term)
                iterators.append(impl.basic_search(cfg.search_terms[0], config=cfg))
            else:
                raise NotImplementedError
    for x in nxt(iterators):
        yield x


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
@click.argument("terms", nargs=-1)
@output_option
def search(terms, output: str):
    """
    Searches ontology for entities that have a label, alias, or other property matching a search term.

    Example:

        runoak -i uberon.obo search limb

    This uses the Pronto implementation to load uberon from disk, and does a basic substring
    search over the labels and synonyms - results are not ranked

    Bioportal (all ontologies):

        runoak -i bioportal: search limb

    (You need to set your API key first)

    This uses the Bioportal API to search over a broad set of ontologies, returning a ranked list
    ranked by relevance. There may be many results, the results are streamed, do ctrl^C to stop

    Ubergraph (all ontologies):

        runoak -i ubergraph: search limb

    Ubergraph (one ontology):

        runoak -i ubergraph:uberon search limb

    For more on search, see https://incatools.github.io/ontology-access-kit/interfaces/search.html

    """
    impl = settings.impl
    if isinstance(impl, SearchInterface):
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            logging.info('** Next chunk:')
            for curie, label in impl.get_labels_for_curies(curie_it):
                print(f'{curie} ! {label}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def all_subsets(output: str):
    """
    Shows all subsets

    Example:
        runoak -i obolibrary:go.obo all-subsets

    Example:
        runoak -i cl.owl all-subsets

    For background on subsets, see https://incatools.github.io/ontology-access-kit/concepts.html#subsets
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for subset in impl.all_subset_curies():
            print(f'{subset} ! {impl.get_label_by_curie(subset)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def ontologies(output: str):
    """
    Shows ontologies

    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.all_ontology_curies():
            print(f'{curie}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@click.argument('ontologies', nargs=-1)
def ontology_versions(ontologies, output: str):
    """
    Shows ontology versions
    """
    impl = settings.impl
    writer = StreamingCsvWriter(output)
    if isinstance(impl, BasicOntologyInterface):
        for ont in list(ontologies):
            for v in impl.ontology_versions(ont):
                obj = dict(ontology=ont, version=v)
                writer.emit(obj)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@output_type_option
@click.argument('ontologies', nargs=-1)
def ontology_metadata(ontologies, output_type: str, output: str):
    """
    Shows ontology metadata
    """
    impl = settings.impl
    if output_type is None or output_type == 'yaml':
        writer = StreamingYamlWriter(output)
    elif output_type == 'csv':
        writer = StreamingCsvWriter(output)
    else:
        raise ValueError(f'No such format: {output_type}')
    if isinstance(impl, BasicOntologyInterface):
        for ont in list(ontologies):
            metadata = impl.ontology_metadata(ont)
            writer.emit(metadata)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@output_type_option
@click.option('--reification/--no-reification',
              default=False,
              show_default=True,
              help="if true then fetch axiom triples with annotations")
@click.argument('terms', nargs=-1)
def term_metadata(terms, reification: bool, output_type: str, output: str):
    """
    Shows term metadata
    """
    impl = settings.impl
    if output_type is None or output_type == 'yaml':
        writer = StreamingYamlWriter(output)
    elif output_type == 'csv':
        writer = StreamingCsvWriter(output)
    else:
        raise ValueError(f'No such format: {output_type}')
    if isinstance(impl, BasicOntologyInterface):
        for curie in query_terms_iterator(terms, impl):
            if reification:
                if isinstance(impl, MetadataInterface):
                    for ax in impl.statements_with_annotations(curie):
                        writer.emit(ax)
                else:
                    raise NotImplementedError
            else:
                metadata = impl.metadata_map_by_curie(curie)
                writer.emit(metadata)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("subset")
@output_option
def list_subset(subset, output: str):
    """
    Shows IDs in a given subset

    Example:
        runoak -i obolibrary:go.obo list-subset goslim_generic

    Example:
        oak -i sqlite:notebooks/input/go.db list-subset goslim_agr

    https://incatools.github.io/ontology-access-kit/concepts.html#subsets
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.curies_by_subset(subset):
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("words", nargs=-1)
@click.option('--text-file',
              type=click.File(mode="r"),
              help="Text file to annotate")
@output_option
@output_type_option
def annotate(words, output: str, text_file: TextIO, output_type: str):
    """
    Annotate a piece of text using a Named Entity Recognition annotation

    Example:
        runoak -i bioportal: annotate "enlarged nucleus in T-cells from peripheral blood"

    Currently BioPortal is the only implementation. Volunteers sought to implement for OLS.

    See the ontorunner framework for plugins for SciSpacy and OGER

    For more on text annotation, see https://incatools.github.io/ontology-access-kit/interfaces/text-annotator.html
    """
    impl = settings.impl
    if isinstance(impl, TextAnnotatorInterface):
        if output_type is None or output_type == 'yaml':
            writer = StreamingYamlWriter(output)
        elif output_type == 'csv':
            writer = StreamingCsvWriter(output)
        else:
            raise ValueError(f'unknown writer: {output_type}')
        if words and text_file:
            raise ValueError(f'Specify EITHER text-file OR a list of words as arguments')
        if text_file:
            for line in text_file.readlines():
                line = line.strip()
                for ann in impl.annotate_text(line):
                    # TODO: better way to represent this
                    ann.subject_source = line
                    writer.emit(ann)
        else:
            text = ' '.join(words)
            for ann in impl.annotate_text(text):
                writer.emit(ann)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option("--view/--no-view",
              default=True,
              show_default=True,
              help="if view is set then open the image after rendering")
@click.option("--down/--no-down",
              default=False,
              show_default=True,
              help="traverse down")
@click.option("--gap-fill/--no-gap-fill",
              default=False,
              show_default=True,
              help="If set then find the minimal graph that spans all input curies")
@click.option("--add-mrcas/--no-add-mrcas",
              default=False,
              show_default=True,
              help="If set then extend input seed list to include all pairwise MRCAs")
@click.option('-S', '--stylemap',
              help='a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/')
@click.option('-C', '--configure',
              help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `')
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
# TODO: the main output option uses a filelike object
@click.option('-o', '--output',
              help="Path to output file")
#@output_option
def viz(terms, predicates, down, gap_fill, add_mrcas, view, stylemap, configure, output_type: str, output: str):
    """
    Visualizing an ancestor graph using obographviz

    For general background on what is meant by a graph in OAK,
    see https://incatools.github.io/ontology-access-kit/interfaces/obograph.html

    :: note:
       This requires that `obographviz <https://github.com/INCATools/obographviz>`_ is installed.

    Example:

        runoak -i sqlite:cl.db viz CL:4023094

    Same query on ubergraph:

        runoak -i ubergraph: viz CL:4023094

    Example, showing only is-a:

        runoak -i sqlite:cl.db viz CL:4023094 -p i

    Example, showing only is-a and part-of, to include Uberon:

        runoak -i sqlite:cl.db viz CL:4023094 -p i,p

    As above, including develops-from:

        runoak -i sqlite:cl.db viz CL:4023094 -p i,p,RO:0002202
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        if stylemap is None:
            stylemap = default_stylemap_path()
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        if add_mrcas:
            if isinstance(impl, SemanticSimilarityInterface):
                curies_to_add = [lca for s, o, lca in impl.multiset_most_recent_common_ancestors(curies, predicates=actual_predicates)]
                curies = list(set(curies + curies_to_add))
                logging.info(f'Expanded CURIEs = {curies}')
            else:
                raise NotImplementedError(f'{impl} does not implement SemanticSimilarityInterface')
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        elif gap_fill:
            logging.info(f'Using gap-fill strategy')
            if isinstance(impl, SubsetterInterface):
                rels = impl.gap_fill_relationships(curies, predicates=actual_predicates)
                if isinstance(impl, OboGraphInterface):
                    graph = impl.relationships_to_graph(rels)
                else:
                    assert False
            else:
                raise NotImplementedError(f'{impl} needs to implement Subsetter for --gap-fill')
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        logging.info(f'Drawing graph seeded from {curies}')
        if output_type == 'json':
            if output:
                json_dumper.dump(graph, to_file=output, inject_type=False)
            else:
                print(json_dumper.dumps(graph))
        elif output_type == 'yaml':
            if output:
                yaml_dumper.dump(graph, to_file=output, inject_type=False)
            else:
                print(yaml_dumper.dumps(graph))
        elif output_type == 'obo':
            output_oi = ProntoImplementation()
            output_oi.load_graph(graph, replace=True)
            output_oi.store(OntologyResource(slug=output, local=True, format='obo'))
        else:
            imgfile = graph_to_image(graph, seeds=curies, stylemap=stylemap, configure=configure, imgfile=output)
            if view:
                subprocess.run(['open', imgfile])
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option("--view/--no-view",
              default=True,
              show_default=True,
              help="if view is set then open the image after rendering")
@click.option("--down/--no-down",
              default=False,
              show_default=True,
              help="traverse down")
@click.option("--gap-fill/--no-gap-fill",
              default=False,
              show_default=True,
              help="If set then find the minimal graph that spans all input curies")
@click.option('-S', '--stylemap',
              help='a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/')
@click.option('-C', '--configure',
              help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `')
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
@output_option
def tree(terms, predicates, down, gap_fill, view, stylemap, configure, output_type: str, output: TextIO):
    """
    Display an ancestor graph as an ascii/markdown tree

    For general instructions, see the viz command, which this is analogous too

    Example:

        runoak -i db/envo.db tree ENVO:00000372 -p i,p

    Note: for many ontologies the tree view will explode, especially if no predicates are specified.
    To avoid this,

    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        curies = list(query_terms_iterator(terms, impl))
        if stylemap is None:
            stylemap = default_stylemap_path()
        actual_predicates = _process_predicates_arg(predicates)
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        elif gap_fill:
            logging.info(f'Using gap-fill strategy')
            if isinstance(impl, SubsetterInterface):
                rels = impl.gap_fill_relationships(curies, predicates=actual_predicates)
                if isinstance(impl, OboGraphInterface):
                    graph = impl.relationships_to_graph(rels)
                else:
                    assert False
            else:
                raise NotImplementedError(f'{impl} needs to implement Subsetter for --gap-fill')
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        logging.info(f'Drawing graph with {len(graph.nodes)} nodes seeded from {curies} // {output_type}')
        graph_to_tree(graph, seeds=curies, predicates=actual_predicates,
                      format=output_type, stylemap=stylemap, output=output)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
@click.option('--statistics/--no-statistics',
              default=False,
              show_default=True,
              help="For each ancestor, show statistics."
              )
@output_option
def ancestors(terms, predicates, statistics: bool, output_type:str, output: str):
    """
    List all ancestors

    Example:

        runoak -i cl.owl ancestors CL:4023094

    Note that ancestors is by default over ALL relationship types

    Constrained to is-a and part-of:

        runoak -i cl.owl ancestors CL:4023094 -p i,BFO:0000050

    Same, on ubergraph:

        runoak -i ubergraph: ancestors CL:4023094 -p i,BFO:0000050

    Search terms can also be used:

        runoak -i cl.owl ancestors 'goblet cell'

    Multiple terms can be passed:

        runoak -i sqlite:go.db ancestors GO:0005773 GO:0005737 -p i,p

    More background:

        https://incatools.github.io/ontology-access-kit/interfaces/obograph.html
    """
    impl = settings.impl
    writer = StreamingCsvWriter(ontology_interface=impl)
    #writer.display_options = display.split(',')
    writer.file = output
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        logging.info(f'Ancestor seed: {curies}')
        graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        if statistics:
            logging.info(f'Calculating graph stats')
            ancs_stats = ancestors_with_stats(graph, curies)
        else:
            ancs_stats = None
        for n in graph.nodes:
            kwargs = {}
            if ancs_stats:
                for k, v in ancs_stats.get(n.id, {}).items():
                    kwargs[k] = v
            writer.emit(dict(id=n.id, label=n.lbl, **kwargs))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@display_option
@output_type_option
@output_option
def descendants(terms, predicates, display: str, output_type: str, output: TextIO):
    """
    List all descendants of a term

    See examples for 'ancestors' command

    More background:

        https://incatools.github.io/ontology-access-kit/interfaces/obograph.html
    """
    impl = settings.impl
    if output_type == 'obo':
        writer = StreamingOboWriter(ontology_interface=impl)
    else:
        writer = StreamingInfoWriter(ontology_interface=impl)
    writer.display_options = display.split(',')
    writer.file = output
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        result_it = impl.descendants(curies, predicates=actual_predicates)
        for curie_it in chunk(result_it):
            logging.info('** Next chunk:')
            for curie, label in impl.get_labels_for_curies(curie_it):
                writer.emit(curie, label)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')

@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
@output_type_option
def extract_triples(terms, predicates, output, output_type: str = 'ttl'):
    """
    Extracts a subontology as triples

    Currently the only endpoint to implement this is ubergraph. Ontobee seems
    to have performance issues with the query

    This will soon be supported in the SqlDatabase/Sqlite endpoint

    Example:

        runoak -v -i ubergraph: extract-triples GO:0005635 CL:0000099 -o test.ttl -O ttl

    """
    impl = settings.impl
    if isinstance(impl, RdfInterface):
        actual_predicates = _process_predicates_arg(predicates)
        g = rdflib.Graph()
        curies = list(query_terms_iterator(terms, impl))
        for t in impl.extract_triples(curies, predicates=actual_predicates, map_to_curies=False):
            logging.info(f'Triple: {t}')
            g.add(t)
        output.write(g.serialize())
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@predicates_option
@output_option
@click.argument("terms", nargs=-1)
def similarity(terms, predicates, output: TextIO):
    """
    Determine pairwise similarity between two terms using a variety of metrics

    Note: We recommend always specifying explicit predicate lists

    Example:

        runoak -i ubergraph: similarity -p i,p CL:0000540 CL:0000000

    You can omit predicates if you like but be warned this may yield
    hard to interpret results.

    E.g.

        runoak -i ubergraph: similarity CL:0000540 GO:0001750

    yields "fully formed stage" (i.e these are both found in the adult) as
    the MRCA

    Background: https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity.html
    """
    if len(terms) != 2:
        raise ValueError(f'Need exactly 2 terms: {terms}')
    subject = terms[0]
    object = terms[1]
    impl = settings.impl
    if isinstance(impl, SemanticSimilarityInterface):
        actual_predicates = _process_predicates_arg(predicates)
        sim = impl.pairwise_similarity(subject, object, predicates=actual_predicates)
        output.write(yaml_dumper.dumps(sim))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@predicates_option
@click.option('--set1',
              multiple=True,
              help="List of curies or curie queries for the first set. If empty uses all")
@click.option('--set2',
              multiple=True,
              help="List of curies or curie queries for the second set. If empty uses all")
@output_option
def all_similarity(predicates, set1, set2, output: TextIO):
    """
    All by all similarity
    """
    impl = settings.impl
    if isinstance(impl, SemanticSimilarityInterface):
        if len(set1) == 0:
            set1it = impl.all_entity_curies()
        else:
            set1it = query_terms_iterator(set1, impl)
        if len(set2) == 0:
            set2it = impl.all_entity_curies()
        else:
            set2it = query_terms_iterator(set2, impl)
        actual_predicates = _process_predicates_arg(predicates)
        for sim in impl.all_by_all_pairwise_similarity(set1it, set2it, predicates=actual_predicates):
            output.write(yaml_dumper.dumps(sim))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@output_type_option
def info(terms, output: TextIO, display: str, output_type: str):
    """
    Show info on terms

    Example:

        runoak -i cl.owl info CL:4023094

    In OBO format:

        runoak -i cl.owl info CL:4023094 -O obo

    With xrefs and definitions:

        runoak -i cl.owl info CL:4023094 -D x,d
    """
    impl = settings.impl
    if output_type == 'obo':
        writer = StreamingOboWriter(ontology_interface=impl)
    elif output_type == 'md':
        writer = StreamingMarkdownWriter(ontology_interface=impl)
    else:
        writer = StreamingInfoWriter(ontology_interface=impl)
    writer.display_options = display.split(',')
    writer.file = output
    logging.info(f'Input Terms={terms}; w={writer}')
    for curie in query_terms_iterator(terms, impl):
        writer.emit(curie)


@main.command()
@click.argument("terms", nargs=-1)
@click.option('--operation',
              type=click.Choice([x.value for x in SetOperation]),
              help="set operation, where left set is stdin list and right set is arguments")
@output_option
@display_option
@output_type_option
def combine(terms, operation: str, output: TextIO, display: str, output_type: str):
    """
    Perform set-wise combination operation on two sets of curies

    The first set is provided on standard input; the second set is provided on the command line

    For example, to intersect a term list with all PATO shapes:

        cat my_terms.txt | runoak -i ubergraph:pato combine --operation intersection t~shape

    This can be used to implement boolean logic in queries:

        alias uberon='runoak -d db/uberon.db'
        uberon search t~bone | uberon combine --operation union t~cartilage
    """
    impl = settings.impl
    if output_type == 'obo':
        writer = StreamingOboWriter(ontology_interface=impl)
    else:
        writer = StreamingInfoWriter(ontology_interface=impl)
    writer.display_options = display.split(',')
    writer.file = output
    set1 = set()
    for line in sys.stdin.readlines():
        m = re.match(r'^(\S+)', line)
        set1.add(m.group(1))
    set2 = set(query_terms_iterator(terms, impl))
    if operation == SetOperation.intersection.value:
        curies = set1.intersection(set2)
    elif operation == SetOperation.union.value:
        curies = set1.union(set2)
    elif operation == SetOperation.difference.value:
        curies = set1.difference(set2)
    elif operation == SetOperation.symmetric_difference.value:
        curies = set1.symmetric_difference(set2)
    elif operation == SetOperation.reverse_difference.value:
        curies = set2.difference(set1)
    else:
        raise NotImplementedError
    logging.info(f'Result Terms={curies}')
    for curie in curies:
        writer.emit(curie)


@main.command()
#@output_option
@click.option('-o', '--output',
              help="output file")
@output_type_option
def convert(output: str, output_type):
    """
    TODO
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        resource = get_resource_from_shorthand(output, format=output_type)
        curies = impl.store(resource)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("terms", nargs=-1)
@output_option
def relationships(terms, output: str):
    """
    Show all relationships for a term or terms

    Example:
        runoak -i cl.owl relationships CL:4023094

    Note: this subcommand will become redundant with other commands like info
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        curies = list(query_terms_iterator(terms, impl))
        for curie in curies:
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
            for pred, fillers in impl.get_outgoing_relationships_by_curie(curie).items():
                print(f'  PRED: {pred} ! {impl.get_label_by_curie(pred)}')
                for filler in fillers:
                    print(f'    * {filler} ! {impl.get_label_by_curie(filler)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_type_option
@output_option
def all_relationships(output: TextIO, output_type: str):
    """
    Show all relationships for all terms

    Example:
        runoak -i hp.db all-relationships

    """
    impl = settings.impl
    if output_type is None or output_type == 'yaml':
        writer = StreamingYamlWriter(output)
    elif output_type == 'csv':
        writer = StreamingCsvWriter(output)
    else:
        raise ValueError(f'No such format: {output_type}')
    if isinstance(impl, OboGraphInterface):
        for s, p, o in impl.all_relationships():
            writer.emit(dict(subject=s, predicate=p, object=o))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def terms(output: str):
    """
    List all terms in the ontology

    Example:

        runoak -i db/cob.db terms
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.all_entity_curies():
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@predicates_option
def roots(output: str, predicates: str):
    """
    List all root in the ontology

    Example:

        runoak -i db/cob.db terms

    Note that the default is to return the roots of the relation graph over *all* predicates

    TODO: filter obsoletes
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        for curie in impl.roots(actual_predicates):
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@predicates_option
def leafs(output: str, predicates: str):
    """
    List all leaf nodes in the ontology

    Example:

        runoak -i db/cob.db leafs

    Note that the default is to return the roots of the relation graph over *all* predicates

    TODO: filter obsoletes
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        for curie in impl.leafs(actual_predicates):
            print(f'{curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@output_type_option
def mappings(output, output_type):
    """
    List all SSSOM mappings in the ontology

    Example (YAML):

        runoak -i db/envo.db mappings

    TODO: TSV
    """
    impl = settings.impl
    if output_type is None or output_type == 'yaml':
        writer = StreamingYamlWriter(output)
    elif output_type == 'csv':
        writer = StreamingCsvWriter(output)
    elif output_type == 'sssom':
        writer = StreamingSssomWriter(output)
    else:
        raise ValueError(f'No such format: {output_type}')
    if isinstance(impl, MappingProviderInterface):
        for mapping in impl.all_sssom_mappings():
            writer.emit(mapping)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@output_type_option
@click.argument('terms', nargs=-1)
def term_mappings(terms, output, output_type):
    """
    List all SSSOM mappings for a term or terms

    Example:

        runoak -i bioportal: term-mappings  UBERON:0002101 -O sssom

    Example:

        runoak -i ols: term-mappings  UBERON:0002101 -O yaml

    Example:

        runoak -i db/uberon.db term-mappings  UBERON:0002101
    """
    impl = settings.impl
    if output_type is None or output_type == 'yaml':
        writer = StreamingYamlWriter(output)
    elif output_type == 'csv':
        writer = StreamingCsvWriter(output)
    elif output_type == 'sssom':
        writer = StreamingSssomWriter(output)
    else:
        raise ValueError(f'No such format: {output_type}')
    if isinstance(impl, MappingProviderInterface):
        for curie in query_terms_iterator(terms, impl):
            for mapping in impl.get_sssom_mappings_by_curie(curie):
                writer.emit(mapping)
        writer.close()
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def aliases(output):
    """
    List all aliases in the ontology

    Example:

        runoak -i db/envo.db aliases
    """
    impl = settings.impl
    writer = StreamingCsvWriter(output)
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.all_entity_curies():
            for pred, aliases in impl.alias_map_by_curie(curie).items():
                for alias in aliases:
                    writer.emit(dict(curie=curie, pred=pred, alias=alias))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
@click.argument('subsets', nargs=-1)
def subset_rollups(subsets: list, output):
    """
    For each subset provide a mapping of each term in the ontology to a subset

    Example:

        runoak -i db/pato.db subset-rollups attribute_slim value_slim
    """
    impl = settings.impl
    #writer = StreamingCsvWriter(output)
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        term_curies = list(impl.all_entity_curies())
        output.write("\t".join(['subset', 'term', 'subset_term']))
        if len(subsets) == 0:
            subsets = list(impl.all_subset_curies())
            logging.info(f'SUBSETS={subsets}')
        for subset in subsets:
            logging.info(f'Subset={subset}')
            m = roll_up_to_named_subset(impl, subset, term_curies, predicates=[IS_A, PART_OF])
            for term, mapped_to in m.items():
                for tgt in mapped_to:
                    output.write("\t".join([subset, term, tgt]))
                    output.write("\n")
                    #writer.emit(dict(subset=subset, term=term, subset_term=tgt))
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@output_option
def axioms(output: str):
    """
    List all axioms

    TODO: this is a placeholder -- will be added when we add funowl
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
@predicates_option
@click.option('-A/--no-A',
              '--all/--no-all',
              default=False,
              show_default=True,
              help="if specified then perform for all terms")
@click.option('--include-redundant/--no-include-redundant',
              default=False,
              show_default=True,
              help="if specified then include redundant taxon constraints from ancestral subjects")
@click.argument('terms', nargs=-1)
def taxon_constraints(terms: list, all: bool, include_redundant: bool, predicates: List, output):
    """
    List all taxon constraints for a term or terms

    Example:

        runoak -i db/go.db taxon-constraints GO:0034357 --include-redundant -p i,p

    Example:

        runoak -i db/uberon.db taxon-constraints UBERON:0003884 UBERON:0003941 -p i,p
    """
    impl = settings.impl
    writer = StreamingYamlWriter(output)
    if all:
        if curies:
            raise ValueError(f'Do not specify explicit curies with --all option')
        curies = [curie for curie in impl.all_entity_curies() if impl.get_label_by_curie(curie)]
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        actual_predicates = _process_predicates_arg(predicates)
        for curie in query_terms_iterator(terms, impl):
            st = get_term_with_taxon_constraints(impl, curie,
                                                 include_redundant=include_redundant, predicates=actual_predicates,
                                                 add_labels=True)
            writer.emit(st)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option('-E', '--evolution-file',
              help="path to file containing gains and losses")
@output_option
@predicates_option
@click.argument('constraints', nargs=-1)
def add_taxon_constraints(constraints, evolution_file, predicates: List, output):
    """
    Test candidate taxon constraints

    For the -E option, accepts the format used in https://arxiv.org/abs/1802.06004

    E.g.

        GO:0000229,Gain|NCBITaxon:1(root);>Loss|NCBITaxon:2759(Eukaryota);

    Example:

        runoak  -i db/go.db add-taxon-constraints -p i,p -E tests/input/go-evo-gains-losses.csv

    Example:

        runoak  -i db/go.db add-taxon-constraints -p i,p GO:0005743 only NCBITaxon:2759 never NCBITaxon:2 . GO:0005634 only NCBITaxon:2

    """
    actual_predicates = _process_predicates_arg(predicates)
    impl = settings.impl
    writer = StreamingYamlWriter(output)
    curr = None
    sts = []
    st = None
    while len(constraints) > 0:
        nxt = constraints[0]
        constraints = constraints[1:]
        if nxt == '.':
            st = None
            curr = None
            continue
        if st is None:
            st = tcdm.SubjectTerm(nxt, label=impl.get_label_by_curie(nxt))
            curr = st.only_in
            sts.append(st)
        else:
            if nxt.lower().startswith('only'):
                curr = st.only_in
            elif nxt.lower().startswith('never'):
                curr = st.never_in
            elif nxt.lower().startswith('present'):
                curr = st.present_in
            else:
                tc = tcdm.TaxonConstraint(taxon=tcdm.Taxon(nxt))
                curr.append(tc)
    if evolution_file is not None:
        with open(evolution_file) as file:
            sts += list(parse_gain_loss_file(file))
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        for st in sts:
            try:
                st = test_candidate_taxon_constraint(impl, st, predicates=actual_predicates)
                writer.emit(st)
            except ValueError as e:
                logging.error(f'Error with TC: {e}')
                st.description = 'PROBLEM'
                writer.emit(st)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option('--cutoff',
              default=50,
              show_default=True,
              help="maximum results to report for any (type, predicate) pair")
@output_option
def validate(output: str, cutoff: int):
    """
    Validate an ontology against ontology metadata

    Implementation notes: Currently only works on SQLite

    Example:

        runoak  -i db/ecto.db validate -o results.tsv
    """
    writer = StreamingCsvWriter(output)
    impl = settings.impl
    if isinstance(impl, ValidatorInterface):
        counts = defaultdict(int)
        for result in impl.validate():
            key = (result.type, result.predicate)
            n = counts[key]
            n += 1
            counts[key] = n
            if n % 1000 == 0:
                logging.info(f'Reached {n} results with {key}')
            if n == cutoff:
                print(f'**TRUNCATING RESULTS FOR {key} at {cutoff}')
            elif n < cutoff:
                writer.emit(result)
                print(yaml_dumper.dumps(result))
        for k, v in counts.items():
            print(f'{k}:: {v}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option('--cutoff',
              default=50,
              show_default=True,
              help="maximum results to report for any (type, predicate) pair")
@click.option('-s', '--schema',
              help="Path to schema (if you want to override the bundled OMO schema)")
@click.argument("dbs", nargs=-1)
@output_option
def validate_multiple(dbs, output, schema, cutoff: int):
    """
    Validate multiple ontologies against ontology metadata

    See the validate command - this is the same except you can pass a list of databases
    """
    writer = StreamingCsvWriter(output)
    config = ValidationConfiguration()
    if schema:
        config.schema_path = schema
    for db in dbs:
        try:
            path = Path(db).absolute()
            print(f'PATH={path}')
            resource = OntologyResource(slug=f'sqlite:///{str(path)}')
            impl = SqlImplementation(resource)
            counts = defaultdict(int)
            for result in impl.validate(configuration=config):
                result.source = f'sqlite:{db}'
                key = (result.type, result.predicate)
                n = counts[key]
                n += 1
                counts[key] = n
                if n % 1000 == 0:
                    logging.info(f'Reached {n} results with {key}')
                if n == cutoff:
                    print(f'**TRUNCATING RESULTS FOR {key} at {cutoff}')
                elif n < cutoff:
                    try:
                        print(yaml_dumper.dumps(result))
                        writer.emit(result)
                    except ValueError as e:
                        logging.error(e)
                        logging.error(f'Could not dump {result} -- bad identifier?')
        except Exception as e:
            logging.error(e)
            logging.error(f'Problem with db')
        for k, v in counts.items():
            print(f'{k}:: {v}')


@main.command()
@output_option
def check_definitions(output: str):
    """
    Check definitions

    REDUNDANT WITH VALIDATE - may be obsoleted
    """
    impl = settings.impl
    if isinstance(impl, ValidatorInterface):
        for curie in impl.term_curies_without_definitions():
            print(f'NO DEFINITION: {curie} ! {impl.get_label_by_curie(curie)}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("terms", nargs=-1)
@output_option
def extract_subset(terms, output: str):
    """
    Extracts a subset

    TODO: INCOMPLETE
    """
    impl = settings.impl
    if isinstance(impl, SubsetterInterface):
        curies = query_terms_iterator(terms, impl)
        subont = impl.extract_subset_ontology(curies)
        print(f'TODO: {subont}')
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.argument("curie_pairs", nargs=-1)
@click.option("--replace/--no-replace",
              default=False,
              show_default=True,
              help="If true, will update in place")
@output_type_option
@output_option
def migrate_curies(curie_pairs, replace: bool, output_type, output: str):
    """
    Rewires an ontology replacing all instances of an ID or IDs

    runoak -i db/uberon.db migrate-curies --replace SRC1=TGT1 SRC2=TGT2
    """
    impl = settings.impl
    curie_map = {}
    for p in curie_pairs:
        k, v = p.split("=")
        curie_map[k] = v
    if not replace:
        raise NotImplementedError(f'Must pass --replace as non-in-place updates not yet supported')
    if isinstance(impl, PatcherInterface):
        impl.migrate_curies(curie_map)
        if replace:
            impl.save()
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


@main.command()
@click.option('--endpoint',
              '-e',
              required=True,
              help="Name of endpoint, e.g. bioportal")
@click.argument("keyval")
def set_apikey(endpoint, keyval):
    """
    Sets an API key

    Example:
        oak set-apikey -e bioportal MY-KEY-VALUE

    This is stored in an OS-dependent path
    """
    set_apikey_value(endpoint, keyval)


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
def lexmatch(output, recreate, rules_file, lexical_index_file, add_labels):
    """
    Generates lexical index and mappings

    See :ref:`.lexical_index_to_sssom`

    Examples:

        runoak -i foo.obo lexmatch -o foo.sssom.tsv

    Outputting intermediate index:

        runoak -i foo.obo lexmatch -L foo.index.yaml -o foo.sssom.tsv

    Note: if you run the above command a second time it will be faster as the index
    will be reused

    Using custom rules:
    
        runoak  -i foo.obo lexmatch -R match_rules.yaml -L foo.index.yaml -o foo.sssom.tsv
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
            logging.info('Reusing previous index')
            ix = load_lexical_index(lexical_index_file)
        else:
            logging.info('Creating index')
            ix = create_lexical_index(impl)
        if lexical_index_file:
            if recreate:
                logging.info('Saving index')
                save_lexical_index(ix, lexical_index_file)
        logging.info(f'Generating mappings from {len(ix.groupings)} groupings')
        msdf = lexical_index_to_sssom(impl, ix, ruleset=ruleset)
        sssom_writers.write_table(msdf, output)
    else:
        raise NotImplementedError(f'Cannot execute this using {impl} of type {type(impl)}')


if __name__ == "__main__":
    main()
