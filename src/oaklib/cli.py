"""
Command Line Interface to OAK
-----------------------------

Executed using "runoak" command
"""
# TODO: order commands.
# See https://stackoverflow.com/questions/47972638/how-can-i-define-the-order-of-click-sub-commands-in-help
import itertools
import logging
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, unique
from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import (
    IO,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    TextIO,
    Tuple,
    Type,
    Union,
)

import click
import kgcl_schema.grammar.parser as kgcl_parser
import rdflib
import sssom.writers as sssom_writers
import yaml
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview
from sssom.parsers import parse_sssom_table, to_mapping_set_document

import oaklib.datamodels.taxon_constraints as tcdm
from oaklib import datamodels
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.datamodels.validation_datamodel import ValidationConfiguration
from oaklib.datamodels.vocabulary import (
    DEVELOPS_FROM,
    EQUIVALENT_CLASS,
    IS_A,
    PART_OF,
    RDF_TYPE,
)
from oaklib.implementations import ProntoImplementation
from oaklib.implementations.aggregator.aggregator_implementation import (
    AggregatorImplementation,
)
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.interfaces import (
    BasicOntologyInterface,
    OntologyInterface,
    SubsetterInterface,
    ValidatorInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import AxiomFilter, OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.io.streaming_axiom_writer import StreamingAxiomWriter
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_info_writer import StreamingInfoWriter
from oaklib.io.streaming_json_lines_writer import StreamingJsonLinesWriter
from oaklib.io.streaming_json_writer import StreamingJsonWriter
from oaklib.io.streaming_markdown_writer import StreamingMarkdownWriter
from oaklib.io.streaming_obo_json_writer import StreamingOboJsonWriter
from oaklib.io.streaming_obo_writer import StreamingOboWriter
from oaklib.io.streaming_owl_functional_writer import StreamingOwlFunctionalWriter
from oaklib.io.streaming_rdf_writer import StreamingRdfWriter
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.resource import OntologyResource
from oaklib.selector import (
    get_implementation_from_shorthand,
    get_resource_from_shorthand,
)
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities import table_filler
from oaklib.utilities.apikey_manager import set_apikey_value
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.kgcl_utilities import generate_change_id
from oaklib.utilities.lexical.lexical_indexer import (
    add_labels_from_uris,
    create_lexical_index,
    lexical_index_to_sssom,
    load_lexical_index,
    load_mapping_rules,
    save_lexical_index,
)
from oaklib.utilities.mapping.cross_ontology_diffs import (
    calculate_pairwise_relational_diff,
)
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter
from oaklib.utilities.obograph_utils import (
    ancestors_with_stats,
    default_stylemap_path,
    graph_to_image,
    graph_to_tree,
    shortest_paths,
    trim_graph,
)
from oaklib.utilities.subsets.slimmer_utils import roll_up_to_named_subset
from oaklib.utilities.table_filler import ColumnDependency, TableFiller, TableMetadata
from oaklib.utilities.taxon.taxon_constraint_utils import (
    get_term_with_taxon_constraints,
    parse_gain_loss_file,
    test_candidate_taxon_constraint,
)

OBO_FORMAT = "obo"
RDF_FORMAT = "rdf"
MD_FORMAT = "md"
OBOJSON_FORMAT = "obojson"
CSV_FORMAT = "csv"
JSON_FORMAT = "json"
JSONL_FORMAT = "jsonl"
YAML_FORMAT = "yaml"
INFO_FORMAT = "info"
SSSOM_FORMAT = "sssom"
OWLFUN_FORMAT = "ofn"

ONT_FORMATS = [
    OBO_FORMAT,
    OBOJSON_FORMAT,
    OWLFUN_FORMAT,
    RDF_FORMAT,
    JSON_FORMAT,
    YAML_FORMAT,
    CSV_FORMAT,
]

WRITERS = {
    OBO_FORMAT: StreamingOboWriter,
    RDF_FORMAT: StreamingRdfWriter,
    OWLFUN_FORMAT: StreamingOwlFunctionalWriter,
    MD_FORMAT: StreamingMarkdownWriter,
    OBOJSON_FORMAT: StreamingOboJsonWriter,
    CSV_FORMAT: StreamingCsvWriter,
    JSON_FORMAT: StreamingJsonWriter,
    JSONL_FORMAT: StreamingJsonWriter,
    YAML_FORMAT: StreamingYamlWriter,
    SSSOM_FORMAT: StreamingSssomWriter,
    INFO_FORMAT: StreamingInfoWriter,
}


@unique
class Direction(Enum):
    up = "up"
    down = "down"
    both = "both"


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
    autosave: bool = False


settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="input implementation specification. This is either a path to a file, or an ontology selector",
)
add_option = click.option(
    "-a", "--add", multiple=True, help="additional implementation specification."
)
set_operation_option = click.option(
    "--operation",
    type=click.Choice([x.value for x in SetOperation]),
    help="set operation, where left set is stdin list and right set is arguments.",
)
direction_option = click.option(
    "--direction",
    type=click.Choice([x.value for x in Direction]),
    help="direction of traversal over edges, which up is subject to object, down is object to subject.",
)
input_type_option = click.option("-I", "--input-type", help="Input type.")
autolabel_option = click.option(
    "--autolabel/--no-autolabel",
    default=True,
    show_default=True,
    help="If set, results will automatically have labels assigned",
)
filter_obsoletes_option = click.option(
    "--filter-obsoletes/--no-filter-obsoletes",
    default=True,
    show_default=True,
    help="If set, results will exclude obsoletes",
)
output_option = click.option(
    "-o",
    "--output",
    type=click.File(mode="w"),
    default=sys.stdout,
    help="Output file, e.g. obo file",
)
output_type_option = click.option(
    "-O",
    "--output-type",
    help="Desired output type",
)
ontological_output_type_option = click.option(
    "-O",
    "--output-type",
    type=click.Choice(ONT_FORMATS),
    help="Desired output type",
)
predicates_option = click.option("-p", "--predicates", help="A comma-separated list of predicates")
display_option = click.option(
    "-D",
    "--display",
    default="",
    help="A comma-separated list of display options. Use 'all' for all",
)


def _process_predicates_arg(
    preds_str: str, expected_number: Optional[int] = None
) -> Optional[List[PRED_CURIE]]:
    if preds_str is None:
        return None
    if "," in preds_str:
        inputs = preds_str.split(",")
    else:
        inputs = preds_str.split("+")
    preds = [_shorthand_to_pred_curie(p) for p in inputs]
    if expected_number and len(preds) != expected_number:
        raise ValueError(f"Expected {expected_number} parses of {preds_str}, got: {preds}")
    return preds


# TODO: move to vocab
def _shorthand_to_pred_curie(shorthand: str) -> PRED_CURIE:
    if shorthand == "i":
        return IS_A
    elif shorthand == "p":
        return PART_OF
    elif shorthand == "d":
        return DEVELOPS_FROM
    elif shorthand == "t":
        return RDF_TYPE
    elif shorthand == "e":
        return EQUIVALENT_CLASS
    else:
        return shorthand


def _get_writer(
    output_type: str,
    impl: OntologyInterface,
    default_type: Type[StreamingWriter] = StreamingInfoWriter,
    datamodel: ModuleType = None,
) -> StreamingWriter:
    if output_type is None:
        typ = default_type
    else:
        if output_type in WRITERS:
            typ = WRITERS[output_type]
        else:
            raise ValueError(f"Unrecognized output type: {output_type}")
    w = typ(ontology_interface=impl)
    if isinstance(w, StreamingRdfWriter) and datamodel is not None:
        w.schemaview = package_schemaview(datamodel.__name__)
    return w


# A list whose members are either strings (search terms, curies, or directives)
# or nested lists.
# TODO: Replace this with an explicit query model with boolean operations
NESTED_LIST = Union[List[str], List["NESTED_LIST"]]


def nest_list_of_terms(terms: List[str]) -> NESTED_LIST:
    """
    Gives a list of terms (typically passed on command line),
    replace blocks between '[', ..., ']' with nested lists of the contents

    :param terms:
    :return:
    """
    nested, rest = _nest_list_of_terms(terms)
    if rest:
        raise ValueError(f"Unparsed: {rest}")
    return nested


def _nest_list_of_terms(terms: List[str]) -> Tuple[NESTED_LIST, List[str]]:
    nested = []
    while len(terms) > 0:
        term = terms[0]
        terms = terms[1:]
        if term == "[":
            nxt, rest = _nest_list_of_terms(terms)
            terms = rest
            nested.append(nxt)
        elif term == "]":
            return nested, terms
        else:
            nested.append(term)
    return nested, []


def curies_from_file(file: IO) -> Iterator[CURIE]:
    """
    yield an iterator over CURIEs by parsing a file.

    The file can contain any content, so long as each line
    starts with a CURIE followed by whitespace -- the remainder of the line
    is ignored

    :param file:
    :return:
    """
    for line in file.readlines():
        m = re.match(r"^(\S+)", line)
        yield m.group(1)


def query_terms_iterator(terms: NESTED_LIST, impl: BasicOntologyInterface) -> Iterator[CURIE]:
    """
    Turn list of tokens that represent a term query into an iterator for curies

    For examples, see test_cli

    TODO: reimplement using an explicit query model

    :param terms:
    :param impl:
    :return:
    """
    curie_iterator: Iterable[CURIE] = iter([])
    predicates = None
    if isinstance(terms, tuple):
        terms = list(terms)

    def _parse_params(s: str) -> Dict:
        d = {}
        m = re.match(r"\.\w+//(.+)", s)
        if m:
            for p in m.group(1).split("//"):
                if "=" not in p:
                    raise ValueError(f"All arguments must be of param=val form, got {p} in {s}")
                [k, v] = p.split("=")
                if k == "p":
                    k = "predicates"
                if k == "predicates":
                    v = _process_predicates_arg(v)
                d[k] = v
        return d

    def chain_it(v):
        if isinstance(v, str):
            v = iter([v])
        nonlocal curie_iterator
        curie_iterator = itertools.chain(curie_iterator, v)

    terms = nest_list_of_terms(terms)

    while len(terms) > 0:
        term = terms[0]
        terms = terms[1:]
        if term == "-":
            chain_it(curies_from_file(sys.stdin))
        elif isinstance(term, list):
            chain_it(query_terms_iterator(term, impl))
        elif term.startswith(".load="):
            fn = term.replace(".load=", """""")
            with open(fn) as file:
                chain_it(curies_from_file(file))
        elif term.startswith(".idfile"):
            fn = terms.pop(0)
            with open(fn) as file:
                chain_it(curies_from_file(file))
        elif term.startswith(".termfile"):
            fn = terms.pop(0)
            with open(fn) as file:
                lines = [line.strip() for line in file.readlines()]
                terms = lines + terms
        elif re.match(r"^([\w\-\.]+):(\S+)$", term):
            chain_it(term)
        elif re.match(r"^\.predicates=(\S*)$", term):
            logging.warning("Deprecated: pass as parameter instead")
            m = re.match(r"^\.predicates=(\S*)$", term)
            predicates = _process_predicates_arg(m.group(1))
        elif re.match(r"^http(\S+)$", term):
            chain_it(term)
        elif term == ".and":
            rest = list(query_terms_iterator(terms, impl))
            for x in curie_iterator:
                if x in rest:
                    yield x
            terms = []
        elif term == ".xor":
            rest = list(query_terms_iterator(terms, impl))
            remaining = []
            for x in curie_iterator:
                if x not in rest:
                    yield x
                else:
                    remaining.append(x)
            for x in rest:
                if x not in remaining:
                    yield x
        elif term == ".not":
            rest = list(query_terms_iterator(terms, impl))
            for x in curie_iterator:
                if x not in rest:
                    yield x
            terms = []
        elif term == ".or":
            # or is implicit
            pass
        elif term.startswith(".all"):
            chain_it(impl.entities())
        elif term.startswith(".in"):
            subset = terms[0]
            terms = terms[1:]
            chain_it(impl.subset_members(subset))
        elif term.startswith(".filter"):
            expr = terms[0]
            terms = terms[1:]
            chain_it(eval(expr, {"impl": impl, "terms": curie_iterator}))
        elif term.startswith(".desc"):
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([terms[0]], impl))
            terms = terms[1:]
            if isinstance(impl, OboGraphInterface):
                chain_it(impl.descendants(rest, predicates=this_predicates))
            else:
                raise NotImplementedError
        elif term.startswith(".anc"):
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([terms[0]], impl))
            terms = terms[1:]
            if isinstance(impl, OboGraphInterface):
                chain_it(impl.ancestors(rest, predicates=this_predicates))
            else:
                raise NotImplementedError
        else:
            if isinstance(impl, SearchInterface):
                cfg = create_search_configuration(term)
                chain_it(impl.basic_search(cfg.search_terms[0], config=cfg))
            else:
                raise NotImplementedError
    for x in curie_iterator:
        yield x


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.option(
    "--save-to",
    help="For commands that mutate the ontology, this specifies where changes are saved to",
)
@click.option(
    "--autosave/--no-autosave",
    help="For commands that mutate the ontology, this determines if these are automatically saved in place",
)
@input_option
@input_type_option
@add_option
def main(
    verbose: int, quiet: bool, input: str, input_type: str, add: List, save_to: str, autosave: bool
):
    """Run the oaklib Command Line.

    A subcommand must be passed - for example: ancestors, terms, ...

    Most commands require an input ontology to be specified:

        runoak -i <INPUT SPECIFICATION> SUBCOMMAND <SUBCOMMAND OPTIONS AND ARGUMENTS>

    Get help on any command, e.g:

        runoak viz -h
    """
    logger = logging.getLogger()
    if verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    if quiet:
        logger.setLevel(logging.ERROR)
    resource = OntologyResource()
    resource.slug = input
    settings.autosave = autosave

    if input:
        impl_class: Type[OntologyInterface]
        resource = get_resource_from_shorthand(input, format=input_type)
        impl_class = resource.implementation_class
        logging.info(f"RESOURCE={resource}")
        settings.impl = impl_class(resource)
    if add:
        impls = [get_implementation_from_shorthand(d) for d in add]
        if settings.impl:
            impls = [settings.impl] + impls
        settings.impl = AggregatorImplementation(implementations=impls)
    if save_to:
        if autosave:
            raise ValueError("Cannot specify both --save-to and --autosave")
        settings.impl = settings.impl.clone(get_resource_from_shorthand(save_to))
        settings.autosave = True


@main.command()
@click.argument("terms", nargs=-1)
@ontological_output_type_option
@output_option
def search(terms, output_type: str, output: TextIO):
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
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.output = output
    if isinstance(impl, SearchInterface):
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            logging.info("** Next chunk:")
            # TODO: move chunking logic to writer
            for curie, label in impl.labels(curie_it):
                writer.emit(dict(id=curie, label=label))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
        for subset in impl.subsets():
            print(f"{subset} ! {impl.label(subset)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@ontological_output_type_option
@output_option
def obsoletes(output_type: str, output: str):
    """
    Shows all obsolete nodes

    Example:
        runoak -i obolibrary:go.obo obsoletes

    TODO: this command should be parameterizable
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.output = output
    if isinstance(impl, BasicOntologyInterface):
        for term in impl.obsoletes():
            writer.emit_curie(term, label=impl.label(term))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
def ontologies(output: str):
    """
    Shows ontologies

    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.ontologies():
            print(str(curie))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@click.argument("ontologies", nargs=-1)
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
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@click.option(
    "--all/--no-all",
    default=False,
    show_default=True,
    help="If true, show all ontologies. Use in place of passing an explicit list",
)
@click.argument("ontologies", nargs=-1)
def ontology_metadata(ontologies, output_type: str, output: str, all):
    """
    Shows ontology metadata

    Example:

        runoak -i bioportal: ontology-metadata obi uberon foodon

    Use the ``--all`` option to show all ontologies

    Example:

        runoak -i bioportal: ontology-metadata --all

    By default the output is YAML. You can get the results as TSV:

    Example:

        runoak -i bioportal: ontology-metadata --all -O csv

    .. warning::

        The output data model is not yet standardized -- this may change in future
    """
    impl = settings.impl
    if output_type is None or output_type == "yaml":
        writer = StreamingYamlWriter(output)
    elif output_type == "csv":
        writer = StreamingCsvWriter(output)
    else:
        raise ValueError(f"No such format: {output_type}")
    if isinstance(impl, BasicOntologyInterface):
        if len(ontologies) == 0:
            if all:
                ontologies = list(impl.ontologies())
            else:
                raise ValueError("Must pass one or more ontologies OR --all")
        else:
            if all:
                raise ValueError("--all should not be used in combination with an explicit lis")
        for ont in list(ontologies):
            metadata = impl.ontology_metadata(ont)
            writer.emit(metadata)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@click.option(
    "--reification/--no-reification",
    default=False,
    show_default=True,
    help="if true then fetch axiom triples with annotations",
)
@click.argument("terms", nargs=-1)
def term_metadata(terms, reification: bool, output_type: str, output: str):
    """
    Shows term metadata
    """
    impl = settings.impl
    if output_type is None or output_type == "yaml":
        writer = StreamingYamlWriter(output)
    elif output_type == "csv":
        writer = StreamingCsvWriter(output)
    else:
        raise ValueError(f"No such format: {output_type}")
    if isinstance(impl, BasicOntologyInterface):
        for curie in query_terms_iterator(terms, impl):
            if reification:
                if isinstance(impl, MetadataInterface):
                    for ax in impl.statements_with_annotations(curie):
                        writer.emit(ax)
                else:
                    raise NotImplementedError
            else:
                metadata = impl.entity_metadata_map(curie)
                writer.emit(metadata)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
        for curie in impl.subset_members(subset):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("words", nargs=-1)
@click.option(
    "-W/--no-W",
    "--matches-whole-text/--no-matches-whole-text",
    default=False,
    show_default=True,
    help="if true, then only show matches that span the entire input text",
)
@click.option(
    "--text-file",
    type=click.File(mode="r"),
    help="Text file to annotate. Each newline separated entry is a distinct text.",
)
@output_option
@output_type_option
def annotate(words, output: str, matches_whole_text: bool, text_file: TextIO, output_type: str):
    """
    Annotate a piece of text using a Named Entity Recognition annotation

    Example:
        runoak -i bioportal: annotate "enlarged nucleus in T-cells from peripheral blood"

    Currently BioPortal is the only implementation. Volunteers sought to implement for OLS.

    See the ontorunner framework for plugins for SciSpacy and OGER

    For more on text annotation, see:

     - <https://incatools.github.io/ontology-access-kit/interfaces/text-annotator.html>_
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.text_annotator)
    writer.output = output
    if isinstance(impl, TextAnnotatorInterface):
        configuration = TextAnnotationConfiguration(matches_whole_text=matches_whole_text)
        if words and text_file:
            raise ValueError("Specify EITHER text-file OR a list of words as arguments")
        if text_file:
            for line in text_file.readlines():
                line = line.strip()
                for ann in impl.annotate_text(line, configuration):
                    # TODO: better way to represent this
                    ann.subject_source = line
                    writer.emit(ann)
        else:
            text = " ".join(words)
            for ann in impl.annotate_text(text, configuration):
                writer.emit(ann)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option(
    "--view/--no-view",
    default=True,
    show_default=True,
    help="if view is set then open the image after rendering",
)
@click.option("--down/--no-down", default=False, show_default=True, help="traverse down")
@click.option(
    "--gap-fill/--no-gap-fill",
    default=False,
    show_default=True,
    help="If set then find the minimal graph that spans all input curies",
)
@click.option(
    "--add-mrcas/--no-add-mrcas",
    default=False,
    show_default=True,
    help="If set then extend input seed list to include all pairwise MRCAs",
)
@click.option(
    "-S",
    "--stylemap",
    help="a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/",
)
@click.option(
    "-C",
    "--configure",
    help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `',
)
@click.option(
    "--max-hops",
    type=int,
    help="Trim nodes that are equal to or greater than this distance from terms",
)
@click.option(
    "--meta/--no-meta",
    default=False,
    show_default=True,
    help="Add metadata object to graph nodes, including xrefs, definitions",
)
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
# TODO: the main output option uses a filelike object
@click.option("-o", "--output", help="Path to output file")
# @output_option
def viz(
    terms,
    predicates,
    down,
    gap_fill,
    max_hops: int,
    add_mrcas,
    view,
    stylemap,
    configure,
    meta,
    output_type: str,
    output: str,
):
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

    With abbreviation:

        runoak -i sqlite:cl.db viz CL:4023094 -p i,p,d

    We can also limit the number of "hops" from the seed terms; for
    example, all is-a and develops-from ancestors of T-cell, limiting
    to a distance of 2:

        runoak -i sqlite:cl.db viz 'T cell' -p i,d --max-hops 2
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        if stylemap is None:
            stylemap = default_stylemap_path()
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        if add_mrcas:
            if isinstance(impl, SemanticSimilarityInterface):
                curies_to_add = [
                    lca
                    for s, o, lca in impl.multiset_most_recent_common_ancestors(
                        curies, predicates=actual_predicates
                    )
                ]
                curies = list(set(curies + curies_to_add))
                logging.info(f"Expanded CURIEs = {curies}")
            else:
                raise NotImplementedError(f"{impl} does not implement SemanticSimilarityInterface")
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        elif gap_fill:
            logging.info("Using gap-fill strategy")
            if isinstance(impl, SubsetterInterface):
                rels = impl.gap_fill_relationships(curies, predicates=actual_predicates)
                if isinstance(impl, OboGraphInterface):
                    graph = impl.relationships_to_graph(rels)
                else:
                    raise AssertionError(f"{impl} needs to of type OboGraphInterface")
            else:
                raise NotImplementedError(f"{impl} needs to implement Subsetter for --gap-fill")
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        if max_hops is not None:
            logging.info(f"Trimming graph, max_hops={max_hops}")
            graph = trim_graph(graph, curies, distance=max_hops, include_intermediates=True)
        logging.info(f"Drawing graph seeded from {curies}")
        if meta:
            impl.add_metadata(graph)
        if output_type == "json":
            if output:
                json_dumper.dump(graph, to_file=output, inject_type=False)
            else:
                print(json_dumper.dumps(graph))
        elif output_type == "yaml":
            if output:
                yaml_dumper.dump(graph, to_file=output, inject_type=False)
            else:
                print(yaml_dumper.dumps(graph))
        elif output_type == "obo":
            output_oi = ProntoImplementation()
            output_oi.load_graph(graph, replace=True)
            output_oi.store(OntologyResource(slug=output, local=True, format="obo"))
        else:
            imgfile = graph_to_image(
                graph, seeds=curies, stylemap=stylemap, configure=configure, imgfile=output
            )
            if view:
                subprocess.run(["open", imgfile])
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("--down/--no-down", default=False, show_default=True, help="traverse down")
@click.option(
    "--gap-fill/--no-gap-fill",
    default=False,
    show_default=True,
    help="If set then find the minimal graph that spans all input curies",
)
@click.option(
    "--add-mrcas/--no-add-mrcas",
    default=False,
    show_default=True,
    help="If set then extend input seed list to include all pairwise MRCAs",
)
@click.option(
    "-S",
    "--stylemap",
    help="a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/",
)
@click.option(
    "-C",
    "--configure",
    help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `',
)
@click.option(
    "--max-hops",
    type=int,
    help="Trim nodes that are equal to or greater than this distance from terms",
)
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
@output_option
def tree(
    terms,
    predicates,
    down,
    gap_fill,
    max_hops,
    add_mrcas,
    stylemap,
    configure,
    output_type: str,
    output: TextIO,
):
    """
    Display an ancestor graph as an ascii/markdown tree

    For general instructions, see the viz command, which this is analogous too

    Example:

        runoak -i envo.db tree ENVO:00000372 -p i,p

    Note: for many ontologies the tree view will explode, especially if no predicates are specified.
    You may wish to start with the is-a tree.

    You can use the --gap-fill option to create a minimal tree:

    Example:

        runoak -i envo.db tree --gap-fill 'pyroclastic shield volcano' 'subglacial volcano' volcano -p i

    This will show the tree containing only these terms, and the most direct inferred relationships between them.

    You can also give a list of leaf terms and specify --add-mrcas alongside --gap-fill to fill in
    the most informative intermediate classes:

    Example:

        runoak -i envo.db tree --add-mrcas --gap-fill 'pyroclastic shield volcano'\
            'subglacial volcano' 'mud volcano' -p i

    This will fill in the term "volcano", as it is the most recent common ancestor of the specified terms

    The --max-hops option can control the distance

        runoak -i envo.db tree 'pyroclastic shield volcano' 'subglacial volcano' --max-hops 1 -p i

    This will generate:

        * [] ENVO:00000247 ! volcano
           * [i] ENVO:00000403 ! shield volcano
              * [i] **ENVO:00000372 ! pyroclastic shield volcano**
           * [i] **ENVO:00000407 ! subglacial volcano**

    Note that 'volcano' is the root, even though it is 2 hops from one of the terms, it can be connected
    to at least one of the seeds (highlighted with asterisks) by a path of length 1.

    """
    impl = settings.impl
    if configure:
        logging.warning("Configure is not yet supported")
    if isinstance(impl, OboGraphInterface):
        curies = list(query_terms_iterator(terms, impl))
        if stylemap is None:
            stylemap = default_stylemap_path()
        actual_predicates = _process_predicates_arg(predicates)
        if add_mrcas:
            if isinstance(impl, SemanticSimilarityInterface):
                curies_to_add = [
                    lca
                    for s, o, lca in impl.multiset_most_recent_common_ancestors(
                        curies, predicates=actual_predicates
                    )
                ]
                curies = list(set(curies + curies_to_add))
                logging.info(f"Expanded CURIEs = {curies}")
            else:
                raise NotImplementedError(f"{impl} does not implement SemanticSimilarityInterface")
        if down:
            graph = impl.subgraph(curies, predicates=actual_predicates)
        elif gap_fill:
            logging.info("Using gap-fill strategy")
            if isinstance(impl, SubsetterInterface):
                rels = impl.gap_fill_relationships(curies, predicates=actual_predicates)
                if isinstance(impl, OboGraphInterface):
                    graph = impl.relationships_to_graph(rels)
                else:
                    raise AssertionError(f"{impl} needs to of type OboGraphInterface")
            else:
                raise NotImplementedError(f"{impl} needs to implement Subsetter for --gap-fill")
        else:
            graph = impl.ancestor_graph(curies, predicates=actual_predicates)
        logging.info(
            f"Drawing graph with {len(graph.nodes)} nodes seeded from {curies} // {output_type}"
        )
        if max_hops is not None:
            graph = trim_graph(graph, curies, distance=max_hops)
        graph_to_tree(
            graph,
            seeds=curies,
            predicates=actual_predicates,
            format=output_type,
            stylemap=stylemap,
            output=output,
        )
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_type_option
@click.option(
    "--statistics/--no-statistics",
    default=False,
    show_default=True,
    help="For each ancestor, show statistics.",
)
@output_option
def ancestors(terms, predicates, statistics: bool, output_type: str, output: str):
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
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    # writer.display_options = display.split(',')
    writer.file = output
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        logging.info(f"Ancestor seed: {curies}")
        if statistics:
            if isinstance(impl, OboGraphInterface):
                graph = impl.ancestor_graph(curies, predicates=actual_predicates)
                logging.info("Calculating graph stats")
                ancs_stats = ancestors_with_stats(graph, curies)
                for n in graph.nodes:
                    kwargs = {}
                    for k, v in ancs_stats.get(n.id, {}).items():
                        kwargs[k] = v
                    writer.emit(dict(id=n.id, label=n.lbl, **kwargs))
            else:
                raise NotImplementedError
        else:
            if isinstance(impl, OboGraphInterface):
                logging.info(f"Getting ancestors of {curies} over {actual_predicates}")
                ancs = list(impl.ancestors(curies, actual_predicates))
                for a_curie, a_label in impl.labels(ancs):
                    writer.emit(dict(id=a_curie, label=a_label))
            else:
                raise NotImplementedError
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@click.option("--target", multiple=True)
@click.option(
    "--flat/--no-flat",
    default=False,
    show_default=True,
    help="If true then output path is written a list of terms",
)
@autolabel_option
@predicates_option
@output_type_option
@click.option(
    "--predicate-weights",
    help="key-value pairs specified in YAML where keys are predicates or shorthands and values are weights",
)
@output_option
def paths(
    terms,
    predicates,
    predicate_weights,
    autolabel: bool,
    flat: bool,
    target,
    output_type: str,
    output: str,
):
    """
    List all paths between one or more start curies

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane'

    This shows all shortest paths from nuclear membrane to all ancestors

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' --target cytoplasm

    This shows shortest paths between two nodes

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' 'thylakoid' --target cytoplasm 'thylakoid membrane'

    This shows all shortest paths between 4 combinations of starts and ends

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' --target cytoplasm \
                --predicate-weights "{i: 0.0001, p: 999}"

    This shows all shortest paths after weighting relations

    Example:

        alias go="runoak -i sqlite:obo:go"
        go paths  -p i,p 'nuclear membrane' --target cytoplasm --flat | go viz --fill-gaps -

    This visualizes the path by first exporting the path as a flat list, then passing the
    results to viz, using the fill-gaps option
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.file = output
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        actual_predicates = _process_predicates_arg(predicates)
        start_curies = list(query_terms_iterator(terms, impl))
        logging.info(f"Ancestor seed: {start_curies}")
        if isinstance(impl, OboGraphInterface):
            if target:
                end_curies = list(list(query_terms_iterator(list(target), impl)))
                all_curies = start_curies + end_curies
            else:
                end_curies = None
                all_curies = start_curies
                logging.info("Will search all ancestors")
            if predicate_weights:
                pw = {}
                for k, v in yaml.safe_load(predicate_weights).items():
                    [p] = _process_predicates_arg(k, expected_number=1)
                    pw[k] = v
            else:
                pw = None
            graph = impl.ancestor_graph(all_curies, predicates=actual_predicates)
            logging.info("Calculating graph stats")
            for s, o, path in shortest_paths(
                graph, start_curies, end_curies=end_curies, predicate_weights=pw
            ):
                if flat:
                    for path_node in path:
                        writer.emit_curie(path_node, impl.label(path_node))
                else:
                    writer.emit(
                        dict(subject=s, object=o, path=path),
                        label_fields=["subject", "object", "path"],
                    )
        else:
            raise NotImplementedError
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
@ontological_output_type_option
def siblings(terms, predicates, output_type: str, output: str):
    """
    List all siblings

    Example:

        runoak -i cl.owl siblings CL:4023094

    Note that ancestors is by default over ALL relationship types
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.file = output
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        logging.info(f"seed: {curies}")
        sibs = []
        for curie in curies:
            for _, parent in impl.outgoing_relationships(curie, actual_predicates):
                for _, child in impl.incoming_relationships(parent, actual_predicates):
                    if child not in sibs:
                        sibs.append(child)
        for sib in sibs:
            writer.emit(sib, impl.label(sib))

    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.display_options = display.split(",")
    writer.file = output
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        result_it = impl.descendants(curies, predicates=actual_predicates)
        for curie_it in chunk(result_it):
            logging.info("** Next chunk:")
            for curie, label in impl.labels(curie_it):
                writer.emit(curie, label)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@click.option("-o", "--output")
@output_type_option
def dump(terms, output, output_type: str):
    """
    Exports an ontology

    Example:

        runoak -i prontolib:pato.obo dump -o pato.json -O json

    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        impl.dump(output, output_type)
    else:
        raise NotImplementedError


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@output_option
@output_type_option
def extract_triples(terms, predicates, output, output_type: str = "ttl"):
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
            logging.info(f"Triple: {t}")
            g.add(t)
        output.write(g.serialize())
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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

    For phenotype ontologies, UPHENO relationship types connect phenotype terms to anatomy, etc:

       runoak -i ubergraph: similarity MP:0010922 HP:0010616  -p i,p,UPHENO:0000001

    Background: https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity.html
    """
    if len(terms) != 2:
        raise ValueError(f"Need exactly 2 terms: {terms}")
    subject = terms[0]
    object = terms[1]
    impl = settings.impl
    if isinstance(impl, SemanticSimilarityInterface):
        actual_predicates = _process_predicates_arg(predicates)
        sim = impl.pairwise_similarity(subject, object, predicates=actual_predicates)
        output.write(yaml_dumper.dumps(sim))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@predicates_option
@click.option(
    "--set1",
    multiple=True,
    help="List of curies or curie queries for the first set. If empty uses all",
)
@click.option(
    "--set2",
    multiple=True,
    help="List of curies or curie queries for the second set. If empty uses all",
)
@click.option(
    "--set1-file",
    help="ID file for set1",
)
@click.option(
    "--set2-file",
    help="ID file for set2",
)
@click.option(
    "--jaccard-minimum",
    type=float,
    help="Minimum value for jaccard score",
)
@click.option(
    "--ic-minimum",
    type=float,
    help="Minimum value for information content",
)
@output_option
@output_type_option
def all_similarity(
    predicates,
    set1,
    set2,
    set1_file,
    set2_file,
    jaccard_minimum,
    ic_minimum,
    output_type,
    output: TextIO,
):
    """
    All by all similarity

    This calculates a similarity matrix for two sets of terms.

    Example:

        runoak -i hp.db all-similarity -p i --set1-file HPO-TERMS1 --set2-file HPO-TERMS2 -O csv

    The .all term syntax can be used to select all terms in an ontology

    Example:

        runoak -i ma.db all-similarity -p i,p --set1 .all --set2 .all

    This can be mixed with other term selectors; for example to calculate the similarity of "neuron"
    vs all terms in CL:

        runoak -i cl.db all-similarity -p i,p --set1 .all --set2 neuron

    An example pipeline to do all by all over all phenotypes in HPO:

        runoak -i hp.db descendants -p i HP:0000118 > HPO
        runoak -i hp.db all-similarity -p i --set1-file HPO --set2-file HPO -O csv -o RESULTS.tsv


    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    if isinstance(impl, SemanticSimilarityInterface):
        if len(set1) == 0:
            if set1_file:
                logging.info(f"Getting set1 from {set1_file}")
                with open(set1_file) as file:
                    set1it = list(curies_from_file(file))
            else:
                set1it = impl.entities()
        else:
            set1it = query_terms_iterator(set1, impl)
        if len(set2) == 0:
            if set2_file:
                logging.info(f"Getting set2 from {set2_file}")
                with open(set2_file) as file:
                    set2it = list(curies_from_file(file))
            else:
                set2it = impl.entities()
        else:
            set2it = query_terms_iterator(set2, impl)
        actual_predicates = _process_predicates_arg(predicates)
        for sim in impl.all_by_all_pairwise_similarity(
            set1it, set2it, predicates=actual_predicates
        ):
            if jaccard_minimum is not None:
                if sim.jaccard_similarity < jaccard_minimum:
                    continue
            if ic_minimum is not None:
                if sim.ancestor_information_content < ic_minimum:
                    continue
            writer.emit(sim)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.display_options = display.split(",")
    writer.file = output
    logging.info(f"Input Terms={terms}; w={writer}")
    for curie in query_terms_iterator(terms, impl):
        writer.emit(curie)


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@ontological_output_type_option
def labels(terms, output: TextIO, display: str, output_type: str):
    """
    Show labels for terms

    Example:

        runoak -i cl.owl labels CL:4023094

    You can use the ".all" selector to show all labels:

    Example:

        runoak -i cl.owl labels .all

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    for curie_it in chunk(query_terms_iterator(terms, impl)):
        logging.info("** Next chunk:")
        for curie, label in impl.labels(curie_it):
            writer.emit(dict(id=curie, label=label))


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@ontological_output_type_option
def definitions(terms, output: TextIO, display: str, output_type: str):
    """
    Show definitions for terms

    Example:

        runoak -i sqlite:obo:envo definitions 'tropical biome' 'temperate biome'

    You can use the ".all" selector to show all definitions:

    Example:

        runoak -i sqlite:obo:envo definitions .all

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    for curie in query_terms_iterator(terms, impl):
        if isinstance(impl, BasicOntologyInterface):
            defn = impl.definition(curie)
            writer.emit(dict(id=curie, definition=defn))


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@direction_option
@autolabel_option
@output_type_option
@output_option
def relationships(
    terms, predicates: str, direction: str, autolabel: bool, output_type: str, output: str
):
    """
    Show all relationships for a term or terms

    Example:
        runoak -i cl.owl relationships CL:4023094

    Note: this subcommand will become redundant with other commands like info
    """
    impl = settings.impl
    if output_type == "obo":
        writer = StreamingOboWriter(ontology_interface=impl)
    elif output_type == "csv":
        writer = StreamingCsvWriter(ontology_interface=impl)
    else:
        writer = StreamingCsvWriter(ontology_interface=impl)
    writer.autolabel = autolabel
    actual_predicates = _process_predicates_arg(predicates)
    if isinstance(impl, BasicOntologyInterface):
        curies = list(query_terms_iterator(terms, impl))
        up_it = impl.relationships(curies, predicates=actual_predicates)
        down_it = impl.relationships(objects=curies, predicates=actual_predicates)
        if direction is None or direction == Direction.up.value:
            it = up_it
        elif direction == Direction.down.value:
            it = down_it
        else:
            it = chain(up_it, down_it)
        for rel in it:
            writer.emit(
                dict(subject=rel[0], predicate=rel[1], object=rel[2]),
                label_fields=["subject", "predicate", "object"],
            )
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@filter_obsoletes_option
@output_option
def terms(output: str, filter_obsoletes: bool):
    """
    List all terms in the ontology

    Example:

        runoak -i db/cob.db terms
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.entities(filter_obsoletes=filter_obsoletes):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@click.option("--maps-to-source")
@click.argument("terms", nargs=-1)
def mappings(terms, maps_to_source, output, output_type):
    """
    List all SSSOM mappings in the ontology

    Example (YAML):

        runoak -i db/envo.db mappings

    TODO: TSV
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    if isinstance(impl, MappingProviderInterface):
        if len(terms) == 0:
            for mapping in impl.sssom_mappings_by_source(subject_or_object_source=maps_to_source):
                writer.emit(mapping)
        else:
            for curie in query_terms_iterator(terms, impl):
                for mapping in impl.get_sssom_mappings_by_curie(curie):
                    writer.emit(mapping)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("--obo-model/--no-obo-model", help="If true, assume the OBO synonym datamodel")
@output_option
@click.argument("terms", nargs=-1)
def aliases(terms, output, obo_model):
    """
    List aliases for a term or set of terms

    Example:

        runoak -i ubergraph:uberon aliases UBERON:0001988

    Example:

        runoak -i db/envo.db aliases .all
    """
    impl = settings.impl
    writer = StreamingCsvWriter(output)
    if obo_model:
        if isinstance(impl, OboGraphInterface):
            curies = list(query_terms_iterator(terms, impl))
            syn_map = impl.synonym_map_for_curies(curies)
            for curie, spvs in syn_map.items():
                for spv in spvs:
                    writer.emit(
                        dict(
                            curie=curie,
                            pred=spv.pred,
                            value=spv.val,
                            type=spv.synonymType,
                            xrefs=spv.xrefs,
                        )
                    )
        else:
            raise NotImplementedError
    else:
        if isinstance(impl, BasicOntologyInterface):
            for curie in query_terms_iterator(terms, impl):
                for pred, aliases in impl.entity_alias_map(curie).items():
                    for alias in aliases:
                        writer.emit(dict(curie=curie, pred=pred, alias=alias))
        else:
            raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@click.argument("subsets", nargs=-1)
def subset_rollups(subsets: list, output):
    """
    For each subset provide a mapping of each term in the ontology to a subset

    Example:

        runoak -i db/pato.db subset-rollups attribute_slim value_slim
    """
    impl = settings.impl
    # writer = StreamingCsvWriter(output)
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        term_curies = list(impl.entities())
        output.write("\t".join(["subset", "term", "subset_term"]))
        if len(subsets) == 0:
            subsets = list(impl.subsets())
            logging.info(f"SUBSETS={subsets}")
        for subset in subsets:
            logging.info(f"Subset={subset}")
            m = roll_up_to_named_subset(impl, subset, term_curies, predicates=[IS_A, PART_OF])
            for term, mapped_to in m.items():
                for tgt in mapped_to:
                    output.write("\t".join([subset, term, tgt]))
                    output.write("\n")
                    # writer.emit(dict(subset=subset, term=term, subset_term=tgt))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
def all_axioms(output: str, output_type: str):
    """
    List all axioms

    TODO: this will be replaced by "axioms" command
    """
    impl = settings.impl
    if isinstance(impl, OwlInterface):
        writer = StreamingAxiomWriter(
            output, syntax=output_type, functional_writer=impl.functional_writer
        )
        for axiom in impl.axioms():
            writer.emit(axiom)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@click.option("--axiom-type", help="Type of axiom, e.g. SubClassOf")
@click.option("--about", help="CURIE that the axiom is about")
@click.option("--references", multiple=True, help="CURIEs that the axiom references")
@click.argument("terms", nargs=-1)
def axioms(terms, output: str, output_type: str, axiom_type: str, about: str, references: tuple):
    """
    Filters axioms

    """
    impl = settings.impl
    if terms:
        curies = [curie for curie in query_terms_iterator(terms, impl)]
    else:
        curies = None
    if isinstance(impl, OwlInterface):
        conditions = AxiomFilter(about=curies)
        if references:
            conditions.references = list(references)
        if axiom_type:
            conditions.set_type(axiom_type)
        for axiom in impl.filter_axioms(conditions=conditions):
            print(axiom)

    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@click.option(
    "-A/--no-A",
    "--all/--no-all",
    default=False,
    show_default=True,
    help="if specified then perform for all terms",
)
@click.option(
    "--include-redundant/--no-include-redundant",
    default=False,
    show_default=True,
    help="if specified then include redundant taxon constraints from ancestral subjects",
)
@click.argument("terms", nargs=-1)
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
        if terms:
            raise ValueError("Do not specify explicit terms with --all option")
        # curies = [curie for curie in impl.all_entity_curies() if impl.get_label_by_curie(curie)]
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        actual_predicates = _process_predicates_arg(predicates)
        for curie in query_terms_iterator(terms, impl):
            st = get_term_with_taxon_constraints(
                impl,
                curie,
                include_redundant=include_redundant,
                predicates=actual_predicates,
                add_labels=True,
            )
            writer.emit(st)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("-E", "--evolution-file", help="path to file containing gains and losses")
@output_option
@predicates_option
@click.argument("constraints", nargs=-1)
def add_taxon_constraints(constraints, evolution_file, predicates: List, output):
    """
    Test candidate taxon constraints

    For the -E option, accepts the format used in https://arxiv.org/abs/1802.06004

    E.g.

        GO:0000229,Gain|NCBITaxon:1(root);>Loss|NCBITaxon:2759(Eukaryota);

    Example:

        runoak  -i db/go.db add-taxon-constraints -p i,p -E tests/input/go-evo-gains-losses.csv

    Example:

        runoak  -i db/go.db add-taxon-constraints -p i,p GO:0005743 only NCBITaxon:2759
        never NCBITaxon:2 . GO:0005634 only NCBITaxon:2

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
        if nxt == ".":
            st = None
            curr = None
            continue
        if st is None:
            st = tcdm.SubjectTerm(nxt, label=impl.label(nxt))
            curr = st.only_in
            sts.append(st)
        else:
            if nxt.lower().startswith("only"):
                curr = st.only_in
            elif nxt.lower().startswith("never"):
                curr = st.never_in
            elif nxt.lower().startswith("present"):
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
                logging.error(f"Error with TC: {e}")
                st.description = "PROBLEM"
                writer.emit(st)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option(
    "--cutoff",
    default=50,
    show_default=True,
    help="maximum results to report for any (type, predicate) pair",
)
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
                logging.info(f"Reached {n} results with {key}")
            if n == cutoff:
                print(f"**TRUNCATING RESULTS FOR {key} at {cutoff}")
            elif n < cutoff:
                writer.emit(result)
                print(yaml_dumper.dumps(result))
        for k, v in counts.items():
            print(f"{k}:: {v}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option(
    "--cutoff",
    default=50,
    show_default=True,
    help="maximum results to report for any (type, predicate) pair",
)
@click.option(
    "-s", "--schema", help="Path to schema (if you want to override the bundled OMO schema)"
)
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
            print(f"PATH={path}")
            resource = OntologyResource(slug=f"sqlite:///{str(path)}")
            impl = SqlImplementation(resource)
            counts = defaultdict(int)
            for result in impl.validate(configuration=config):
                result.source = f"sqlite:{db}"
                key = (result.type, result.predicate)
                n = counts[key]
                n += 1
                counts[key] = n
                if n % 1000 == 0:
                    logging.info(f"Reached {n} results with {key}")
                if n == cutoff:
                    print(f"**TRUNCATING RESULTS FOR {key} at {cutoff}")
                elif n < cutoff:
                    try:
                        print(yaml_dumper.dumps(result))
                        writer.emit(result)
                    except ValueError as e:
                        logging.error(e)
                        logging.error(f"Could not dump {result} -- bad identifier?")
        except Exception as e:
            logging.error(e)
            logging.error("Problem with db")
        for k, v in counts.items():
            print(f"{k}:: {v}")


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
            print(f"NO DEFINITION: {curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


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
        print(f"TODO: {subont}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("curie_pairs", nargs=-1)
@click.option(
    "--replace/--no-replace", default=False, show_default=True, help="If true, will update in place"
)
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
        raise NotImplementedError("Must pass --replace as non-in-place updates not yet supported")
    if isinstance(impl, PatcherInterface):
        impl.migrate_curies(curie_map)
        if replace:
            impl.save()
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("--endpoint", "-e", required=True, help="Name of endpoint, e.g. bioportal")
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
@click.option(
    "--lexical-index-file",
    "-L",
    help="path to lexical index. This is recreated each time unless --no-recreate is passed",
)
@click.option("--rules-file", "-R", help="path to rules file. Conforms to rules_datamodel.")
@click.option(
    "--add-labels/--no-add-labels",
    default=False,
    show_default=True,
    help="Populate empty labels with URI fragments or CURIE local IDs, for ontologies that use semantic IDs",
)
@click.option(
    "--recreate/--no-recreate",
    default=True,
    show_default=True,
    help="if true and lexical index is specified, always recreate, otherwise load from index",
)
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
            logging.info("Reusing previous index")
            ix = load_lexical_index(lexical_index_file)
        else:
            logging.info("Creating index")
            ix = create_lexical_index(impl)
        if lexical_index_file:
            if recreate:
                logging.info("Saving index")
                save_lexical_index(ix, lexical_index_file)
        logging.info(f"Generating mappings from {len(ix.groupings)} groupings")
        msdf = lexical_index_to_sssom(impl, ix, ruleset=ruleset)
        sssom_writers.write_table(msdf, output)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("--other-ontology", help="other ontology")
@output_option
@click.argument("terms", nargs=-1)
def diff_terms(output, other_ontology, terms):
    """
    EXPERIMENTAL

    :param output:
    :param other_ontology:
    :param terms:
    :return:
    """
    impl = settings.impl
    other_impl = get_implementation_from_shorthand(other_ontology)
    terms = list(query_terms_iterator(terms, impl))
    if len(terms) == 2:
        [term, other_term] = terms
    elif len(terms) == 1:
        (term, other_term) = terms[0], None
    else:
        raise ValueError(f"Must pass one or two terms; got: {terms}")
    if isinstance(impl, DifferInterface):
        diff = impl.compare_term_in_two_ontologies(other_impl, term, other_curie=other_term)
        # THIS WILL CHANGE!!!
        left, right = diff
        print("LEFT")
        for x in left:
            print(f" * {x}")
        print("RIGHT")
        for x in right:
            print(f" * {x}")
    else:
        raise NotImplementedError


@main.command()
@click.option("-X", "--other-ontology", help="other ontology")
@click.option(
    "--simple/--no-simple",
    default=False,
    show_default=True,
    help="perform a quick difference showing only terms that differ",
)
@output_option
@output_type_option
def diff(simple: bool, output, output_type, other_ontology):
    """
    Diff between two ontologies

    The --simple option will compare the lists of terms in each ontology. This is currently
    implemented for most endpoints.

    If --simple is not set, then this will do a complete diff, and return the diff as KGCL
    change commands.

    Current limitations

    - complete diffs can only be done using local RDF files
    - Parsing using rdflib can be slow
    - Currently the return format is ONLY the KGCL change DSL. In future YAML, JSON, RDF will be an option
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingJsonLinesWriter)
    writer.output = output
    other_impl = get_implementation_from_shorthand(other_ontology)
    if isinstance(impl, DifferInterface):
        if simple:
            for change in impl.compare_ontology_term_lists(other_impl):
                writer.emit(change)
        else:
            for change in impl.diff(other_impl):
                print(change)
                # writer.emit(change)
    else:
        raise NotImplementedError


@main.command()
@click.option("--output", "-o")
@output_type_option
@click.argument("commands", nargs=-1)
def apply(commands, output, output_type):
    """
    Applies a patch to an ontology

    Example:

        runoak -i cl.owl.ttl apply "rename CL:0000561 to 'amacrine neuron'"  -o cl.owl.ttl -O ttl

    With URIs:

        runoak -i cl.owl.ttl apply \
          "rename <http://purl.obolibrary.org/obo/CL_0000561> from 'amacrine cell' to 'amacrine neuron'" \
           -o cl.owl.ttl -O ttl

    WARNING:

    This command is still experimental. Some things to bear in mind:

    - for some ontologies, CURIEs may not work, instead specify a full URI surrounded by <>s
    """
    impl = settings.impl
    if isinstance(impl, PatcherInterface):
        impl.autosave = settings.autosave
        for command in commands:
            change = kgcl_parser.parse_statement(command)
            logging.info(f"Change: {change}")
            impl.apply_patch(change)
        if not settings.autosave and not output:
            logging.warning("--autosave not passed, changes are NOT saved")
        if output:
            impl.dump(output, output_type)
    else:
        raise NotImplementedError


@main.command()
@click.option("--output", "-o")
@output_type_option
@click.argument("terms", nargs=-1)
def apply_obsolete(output, output_type, terms):
    """
    Sets an ontology element to be obsolete

    WARNING: this command may be replaced by a more general KGCL change command
    in future

    Example:

        runoak -i my.obo apply-obsolete MY:0002200 -o my-modified.obo

    This may be chained, for example to take all terms matching a search query and then
    obsolete them all:

        runoak -i my.db search 'l/^Foo/` | runoak -i my.db --autosave apply-obsolete -
    """
    impl = settings.impl
    if isinstance(impl, PatcherInterface):
        impl.autosave = settings.autosave
        for term in query_terms_iterator(terms, impl):
            impl.apply_patch(kgcl.NodeObsoletion(id=generate_change_id(), about_node=term))
        if not settings.autosave and not output:
            logging.warning("--autosave not passed, changes are NOT saved")
        if output:
            impl.dump(output, output_type)
        # impl.save()
    else:
        raise NotImplementedError


@main.command()
@click.option("-S", "--source", multiple=True, help="ontology prefixes  e.g. HP, MP")
@click.option(
    "--mapping-input",
    help="File of mappings in SSSOM format. If not provided then mappings in ontoogy are used",
)
@click.option("--other-input", help="Additional input file")
@click.option("--other-input-type", help="Type of additional input file")
@click.option(
    "--intra/--no-intra",
    default=False,
    show_default=True,
    help="If true, then all sources are in the main input ontology",
)
@click.option(
    "--add-labels/--no-add-labels",
    default=False,
    show_default=True,
    help="Populate empty labels with URI fragments or CURIE local IDs, for ontologies that use semantic IDs",
)
@predicates_option
@output_option
@output_type_option
def diff_via_mappings(
    source,
    mapping_input,
    intra,
    add_labels,
    other_input,
    other_input_type,
    predicates,
    output_type,
    output,
):
    """
    Calculates a relational diff between ontologies in two sources using the combined mappings
    from both

    E.g. use MP and HP mappings to give a report on how these ontologies are structurally different.
    """
    oi = settings.impl
    writer = _get_writer(
        output_type, oi, StreamingYamlWriter, datamodel=datamodels.cross_ontology_diff
    )
    writer.output = output
    if other_input:
        if intra:
            raise ValueError("No not specify --intra if --other-input is specified")
        else:
            other_oi = get_implementation_from_shorthand(other_input, format=other_input_type)
    else:
        if intra:
            other_oi = oi
        else:
            raise ValueError(
                "No --other-input specified - specify --intra if mappings are within the main input"
            )
    if mapping_input:
        mappings = to_mapping_set_document(parse_sssom_table(mapping_input)).mapping_set.mappings
        logging.info(f"Using {len(mappings)} from {mapping_input}")
    else:
        mappings = None
        logging.info("Mappings will be derived from ontologies")
    if source:
        sources = list(source)
        if len(sources) == 1:
            raise ValueError(
                f"If --source is specified, must pass more than one. You specified: {sources}"
            )
    else:
        sources = None
    actual_predicates = _process_predicates_arg(predicates)
    for r in calculate_pairwise_relational_diff(
        oi,
        other_oi,
        sources=sources,
        mappings=mappings,
        add_labels=add_labels,
        predicates=actual_predicates,
    ):
        writer.emit(r)


@main.command()
@click.option(
    "--allow-missing/--no-allow-missing",
    default=False,
    show_default=True,
    help="Allow some dependent values to be blank, post-processing",
)
@click.option("--missing-value-token", help="Populate all missing values with this token")
@click.option("--schema", help="Path to linkml schema")
@click.option(
    "--delimiter",
    default="\t",
    show_default=True,
    help="Delimiter between columns in input and output",
)
@click.option(
    "--relation",
    multiple=True,
    help="Serialized YAML string corresponding to a normalized relation between two columns",
)
@click.option(
    "--relation-file",
    type=click.File(mode="r"),
    help="Path to YAML file corresponding to a list of normalized relation between two columns",
)
@output_option
@click.argument("table_file")
def fill_table(
    table_file,
    output,
    delimiter,
    missing_value_token,
    allow_missing: bool,
    relation: tuple,
    relation_file: str,
    schema: str,
):
    """
    Fills missing values in a table of ontology elements

    Given a TSV with a populated ID column, and unpopulated columns for definition, label, mappings, ancestors,
    this will iterate through each row filling in each missing value by performing ontology lookups.

    In some cases, this can also perform reverse lookups; i.e given a table with labels populated and blank IDs,
    then fill in the IDs

    In the most basic scenario, you have a table with two columns 'id' and 'label'. These are the "conventional" column
    headers for a table of ontology elements (see later for configuration when you don't follow conventions)

    Example:

        runoak -i cl.owl.ttl fill-table my-table.tsv

    (any implementation can be used)

    The same command will work for the reverse scenario - when you have labels populated, but IDs are not populated

    By default this will throw an error if a lookup is not successful; this can be relaxed

    Relaxed:

        runoak -i cl.owl.ttl fill-table --allow-missing my-table.tsv

    In this case missing values that cannot be populated will remain empty

    To explicitly populate a value:

        runoak -i cl.owl.ttl fill-table --missing-value-token NO_DATA my-table.tsv

    Currently the following columns are recognized:

     - id -- the unique identifier of the element
     - label -- the rdfs:label of the element
     - definition -- the definition of the element
     - mappings -- mappings for the element
     - ancestors -- ancestors for the element (this can be parameterized)

    The metadata inference procedure will also work for when you have denormalized TSV files
    with columns such as "foo_id" and "foo_name". This will be recognized as an implicit normalized
    label relation between id and name of a foo element.

    You can be more explicit in one of two ways:

     1. Pass in a YAML structure (on command line or in a YAML file) listing relations
     2. Pass in a LinkML data definitions YAML file

    For the first method, you can pass in multiple relations using the --relation arg. For example,
    given a TSV with columns cl_identifier and cl_display_label you can say:

    Example:

        runoak -i cl.owl.ttl fill-table \
          --relation "{primary_key: cl_identifier, dependent_column: cl_display_label, relation: label}"

    You can also specify this in a YAML file

    For the 2nd method, you need to specify a LinkML schema with a class where (1) at least one field is annotated
    as being an identifier (2) one or more slots have slot_uri elements mapping them to standard metadata elements
    such as rdfs:label.

    For example, my-schema.yaml:

            classes:
              Person:
                attributes:
                  id:
                    identifier: true
                  name:
                    slot_uri: rdfs:label

    This is a powerful command with many ways of configuring it - we will add separate docs for this soon,
    for now please file an issue on github with any questions

    TODO: allow for an option that will perform fuzzy matches of labels
    TODO: reverse lookup is not provided for all fields, such as definitions
    TODO: add an option to detect inconsistencies
    TODO: add logical for obsoletion/replaced by
    TODO: use most optimized method for whichever backend
    """
    tf = TableFiller(settings.impl)
    with open(table_file) as input_file:
        input_table = table_filler.parse_table(input_file, delimiter=delimiter)
        if schema:
            metadata = tf.extract_metadata_from_linkml(schema)
        elif relation or relation_file:
            metadata = TableMetadata(dependencies=[])
            if relation_file:
                for d_args in yaml.safe_load(relation_file):
                    metadata.dependencies.append(ColumnDependency(**d_args))
            for d_str in list(relation):
                d_args = yaml.safe_load(d_str)
                metadata.dependencies.append(ColumnDependency(**d_args))
        else:
            metadata = tf.infer_metadata(input_table[0])
        metadata.set_allow_missing_values(allow_missing)
        metadata.set_missing_value_token(missing_value_token)
        tf.fill_table(input_table, table_metadata=metadata)
        table_filler.write_table(input_table, output, delimiter=delimiter)


if __name__ == "__main__":
    main()
