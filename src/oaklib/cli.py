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
import secrets
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
import sssom_schema
import yaml
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview
from prefixmaps.io.parser import load_multi_context
from sssom.parsers import parse_sssom_table, to_mapping_set_document

import oaklib.datamodels.taxon_constraints as tcdm
from oaklib import datamodels
from oaklib.converters.logical_definition_flattener import LogicalDefinitionFlattener
from oaklib.datamodels.cross_ontology_diff import DiffCategory
from oaklib.datamodels.lexical_index import LexicalTransformation, TransformationType
from oaklib.datamodels.obograph import PrefixDeclaration
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.summary_statistics_datamodel import GlobalStatistics
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.datamodels.validation_datamodel import ValidationConfiguration
from oaklib.datamodels.vocabulary import (
    DEVELOPS_FROM,
    EQUIVALENT_CLASS,
    HAS_OBO_NAMESPACE,
    IS_A,
    IS_DEFINED_BY,
    PART_OF,
    PREFIX_PREDICATE,
    RDF_TYPE,
)
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
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.differ_interface import DiffConfiguration, DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import AxiomFilter, OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.io.heatmap_writer import HeatmapWriter
from oaklib.io.obograph_writer import write_graph
from oaklib.io.streaming_axiom_writer import StreamingAxiomWriter
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_info_writer import StreamingInfoWriter
from oaklib.io.streaming_json_writer import StreamingJsonWriter
from oaklib.io.streaming_kgcl_writer import StreamingKGCLWriter
from oaklib.io.streaming_markdown_writer import StreamingMarkdownWriter
from oaklib.io.streaming_nl_writer import StreamingNaturalLanguageWriter
from oaklib.io.streaming_obo_json_writer import StreamingOboJsonWriter
from oaklib.io.streaming_obo_writer import StreamingOboWriter
from oaklib.io.streaming_owl_functional_writer import StreamingOwlFunctionalWriter
from oaklib.io.streaming_rdf_writer import StreamingRdfWriter
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.mappers.ontology_metadata_mapper import OntologyMetadataMapper
from oaklib.parsers.association_parser_factory import get_association_parser
from oaklib.resource import OntologyResource
from oaklib.selector import (
    get_implementation_from_shorthand,
    get_resource_from_shorthand,
)
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities import table_filler
from oaklib.utilities.apikey_manager import set_apikey_value
from oaklib.utilities.associations.association_differ import AssociationDiffer
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.kgcl_utilities import generate_change_id, parse_kgcl_files
from oaklib.utilities.lexical.lexical_indexer import (
    DEFAULT_QUALIFIER,
    add_labels_from_uris,
    apply_transformation,
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
from oaklib.utilities.ner_utilities import get_exclusion_token_list
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
    eval_candidate_taxon_constraint,
    get_term_with_taxon_constraints,
    parse_gain_loss_file,
)
from oaklib.utilities.validation.definition_ontology_rule import (
    TextAndLogicalDefinitionMatchOntologyRule,
)
from oaklib.utilities.validation.lint_utils import lint_ontology
from oaklib.utilities.validation.rule_runner import RuleRunner

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
NL_FORMAT = "nl"
KGCL_FORMAT = "kgcl"
HEATMAP_FORMAT = "heatmap"

ONT_FORMATS = [
    OBO_FORMAT,
    OBOJSON_FORMAT,
    OWLFUN_FORMAT,
    RDF_FORMAT,
    JSON_FORMAT,
    YAML_FORMAT,
    CSV_FORMAT,
    NL_FORMAT,
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
    NL_FORMAT: StreamingNaturalLanguageWriter,
    KGCL_FORMAT: StreamingKGCLWriter,
    HEATMAP_FORMAT: HeatmapWriter,
}


@unique
class Direction(Enum):
    """
    Permissible directions for graph traversal.
    """

    up = "up"
    down = "down"
    both = "both"


@unique
class SubjectOrObjectRole(Enum):
    """
    Role of terms in the term list
    """

    SUBJECT = "subject"
    OBJECT = "object"
    BOTH = "both"


@unique
class IfAbsent(Enum):
    """
    Permissible values for --if-absent

    This indicates the policy when a specific value is not present
    """

    absent_only = "absent-only"
    present_only = "present-only"


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
    associations_type: str = None


settings = Settings()

input_option = click.option(
    "-i",
    "--input",
    help="input implementation specification. This is either a path to a file, or an ontology selector",
)
add_option = click.option(
    "-a", "--add", multiple=True, help="additional implementation specification."
)
all_ontologies_option = click.option(
    "--all/--no-all",
    default=False,
    show_default=True,
    help="If true, show all ontologies. Use in place of passing an explicit list",
)
set_operation_option = click.option(
    "--operation",
    type=click.Choice([x.value for x in SetOperation]),
    help="set operation, where left set is stdin list and right set is arguments.",
)
set_value_option = click.option(
    "-S",
    "--set-value",
    help="the value to set for all terms for the given property.",
)
direction_option = click.option(
    "--direction",
    type=click.Choice([x.value for x in Direction]),
    help="direction of traversal over edges, which up is subject to object, down is object to subject.",
)
if_absent_option = click.option(
    "--if-absent",
    type=click.Choice([x.value for x in IfAbsent]),
    help="determines behavior when the value is not present or is empty.",
)
owl_type_option = click.option(
    "--owl-type", help="only include entities of this type, e.g. owl:Class, rdf:Property"
)
input_type_option = click.option(
    "-I", "--input-type", help="Input format. Permissible values vary depending on the context"
)
dry_run_option = click.option(
    "--dry-run/--no-dry-run",
    default=False,
    show_default=False,
    help="If true, nothing will be modified by executing command",
)
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
overwrite_option = click.option(
    "--overwrite/--no-overwrite",
    default=False,
    show_default=False,
    help="If set, any changes applied will be saved back to the input file/source",
)
output_option = click.option(
    "-o",
    "--output",
    type=click.File(mode="w"),
    default="-",
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
group_by_property_option = click.option(
    "--group-by-property",
    help="group summaries by a metadata property, e.g. rdfs:isDefinedBy",
)
group_by_obo_namespace_option = click.option(
    "--group-by-obo-namespace/--no-group-by-obo-namespace",
    default=False,
    show_default=True,
    help="shortcut for --group-by-property oio:hasOBONamespace (note this is distinct from the ID namespace)",
)
group_by_defined_by_option = click.option(
    "--group-by-defined-by/--no-group-by-defined-by",
    default=False,
    show_default=True,
    help="shortcut for --group-by-property rdfs:isDefinedBy. This may be inferred from prefix if not set explicitly",
)
group_by_prefix_option = click.option(
    "--group-by-prefix/--no-group-by-prefix",
    default=False,
    show_default=True,
    help="shortcut for --group-by-property sh:prefix. Groups by the prefix of the CURIE",
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


def _skip_if_absent(if_absent: bool, v: Any):
    if if_absent:
        if if_absent == IfAbsent.absent_only.value and v:
            return True
        elif if_absent == IfAbsent.present_only.value and not v:
            return True
    return False


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
    if w.uses_schemaview and datamodel is not None:
        w.schemaview = package_schemaview(datamodel.__name__)
    return w


def _apply_changes(impl, changes):
    if changes:
        logging.info(f"Applying {len(changes)} changes")
        if isinstance(impl, PatcherInterface):
            for change in changes:
                impl.apply_patch(change)
            impl.save()
        else:
            raise NotImplementedError(f"Cannot apply {len(changes)} changes")


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
            logging.info(f"Reading ids from {fn}")
            file = open(fn)
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
        elif term.startswith(".rand"):
            for x in impl.entities():
                if secrets.randbelow(100) == 0:
                    yield x
        elif term.startswith(".in"):
            subset = terms[0]
            terms = terms[1:]
            chain_it(impl.subset_members(subset))
        elif term.startswith(".is_obsolete"):
            chain_it(impl.obsoletes())
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
                logging.info(f"Search config: {term} => {cfg}")
                chain_it(impl.basic_search(cfg.search_terms[0], config=cfg))
            else:
                raise NotImplementedError
    for x in curie_iterator:
        yield x


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.option(
    "--stacktrace/--no-stacktrace",
    default=False,
    show_default=True,
    help="If set then show full stacktrace on error",
)
@click.option(
    "--save-as",
    help="For commands that mutate the ontology, this specifies where changes are saved to",
)
# @click.option(
#    "--save-as-syntax",
#    help="For commands that mutate the ontology, this specifies the syntax for saving",
# )
@click.option(
    "--autosave/--no-autosave",
    help="For commands that mutate the ontology, this determines if these are automatically saved in place",
)
@click.option(
    "--named-prefix-map",
    multiple=True,
    help="the name of a prefix map, e.g. obo, prefixcc",
)
@click.option(
    "--prefix",
    multiple=True,
    help="prefix=expansion pair",
)
@click.option(
    "--metamodel-mappings",
    help="overrides for metamodel properties such as rdfs:label",
)
@click.option(
    "--import-depth",
    type=click.INT,
    help="Maximum depth in the import tree to traverse. Currently this is only used by the pronto adapter",
)
@click.option("--associations", "-g", multiple=True, help="Location of ontology associations")
@click.option("--associations-type", "-G", help="Syntax of associations input")
@input_option
@input_type_option
@add_option
def main(
    verbose: int,
    quiet: bool,
    stacktrace: bool,
    input: str,
    input_type: str,
    add: List,
    associations: List,
    associations_type: str,
    save_as: str,
    autosave: bool,
    named_prefix_map,
    metamodel_mappings,
    prefix,
    import_depth: Optional[int],
):
    """Run the oaklib Command Line.

    A subcommand must be passed - for example: ancestors, terms, ...

    Most commands require an input ontology to be specified:

        runoak -i <INPUT SPECIFICATION> SUBCOMMAND <SUBCOMMAND OPTIONS AND ARGUMENTS>

    Get help on any command, e.g:

        runoak viz -h
    """
    if not stacktrace:
        sys.tracebacklimit = 0
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
    logging.info(f"Settings = {settings}")
    if input:
        impl_class: Type[OntologyInterface]
        resource = get_resource_from_shorthand(input, format=input_type, import_depth=import_depth)
        impl_class = resource.implementation_class
        logging.info(f"RESOURCE={resource}")
        settings.impl = impl_class(resource)
        settings.impl.autosave = autosave
    if add:
        impls = [get_implementation_from_shorthand(d) for d in add]
        if settings.impl:
            impls = [settings.impl] + impls
        settings.impl = AggregatorImplementation(implementations=impls)
    settings.associations_type = associations_type
    if associations:
        if isinstance(settings.impl, AssociationProviderInterface):
            association_parser = get_association_parser(associations_type)
            for af in associations:
                with open(af) as file:
                    assocs = association_parser.parse(file)
                    settings.impl.add_associations(assocs)
        else:
            raise NotImplementedError(f"{type(settings.impl)} does not implement associations")
    if metamodel_mappings:
        msdf = parse_sssom_table(metamodel_mappings)
        msd = to_mapping_set_document(msdf)
        settings.impl.ontology_metamodel_mapper = OntologyMetadataMapper(
            msd.mapping_set.mappings, curie_converter=settings.impl.converter
        )
    if save_as:
        if autosave:
            raise ValueError("Cannot specify both --save-as and --autosave")
        settings.impl = settings.impl.clone(get_resource_from_shorthand(save_as))
        settings.autosave = True
    if prefix:
        for p in prefix:
            [pfx, ns] = p.split("=", 1)
            if isinstance(settings.impl, BasicOntologyInterface):
                settings.impl.prefix_map()[pfx] = ns
    if named_prefix_map:
        pm = load_multi_context(list(named_prefix_map))
        for pfx, ns in pm.as_dict().items():
            if settings.impl is None:
                logging.info("Creating dummy BasicOntologyInterface to hold prefixes")
                settings.impl = BasicOntologyInterface()
            settings.impl.prefix_map()[pfx] = ns


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

    .. warning::

       The behavior of search is not yet fully unified across endpoints

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
def subsets(output: str):
    """
    Shows information on subsets

    Example:

        runoak -i obolibrary:go.obo subsets

    Example:

        runoak -i cl.owl subsets

    For background on subsets, see https://incatools.github.io/ontology-access-kit/concepts.html#subsets

    Note you can use subsets in selector queries for other commands; e.g. to fetch all
    terms (directly) in goslim_generic in GO:

    Example:

        runoak -i sqlite:obo:go info .in goslim_generic

    See also:

        term-subsets command, which shows relationships of terms to subsets
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for subset in impl.subsets():
            print(f"{subset} ! {impl.label(subset)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option(
    "--include-merged/--no-include-merged",
    default=True,
    show_default=True,
    help="Include merged terms in output",
)
@ontological_output_type_option
@output_option
def obsoletes(include_merged: bool, output_type: str, output: str):
    """
    Shows all obsolete entities

    Example:

        runoak -i obolibrary:go.obo obsoletes

    To exclude *merged terms*, use the ``--no-include-merged`` flag

    Example:

        runoak -i obolibrary:go.obo obsoletes --no-include-merged

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.output = output
    if isinstance(impl, BasicOntologyInterface):
        for term in impl.obsoletes(include_merged=include_merged):
            writer.emit_curie(term, label=impl.label(term))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@ontological_output_type_option
@group_by_property_option
@group_by_obo_namespace_option
@group_by_prefix_option
@group_by_defined_by_option
@click.option(
    "--include-residuals/--no-include-residuals",
    help="If true include an OTHER category for terms that do not have the property",
)
@output_option
@click.argument("branches", nargs=-1)
def statistics(
    branches,
    group_by_property,
    group_by_obo_namespace: bool,
    group_by_defined_by: bool,
    group_by_prefix: bool,
    include_residuals: bool,
    output_type: str,
    output: str,
):
    """
    Shows all descriptive/summary statistics

    Example:

        runoak -i sqlite:obo:pr statistics

    By default, this will show combined summary statistics for all terms

    You can also break down the statistics in two ways:

    - by a collection of branch roots
    - by a metadata property (e.g. oio:hasOBONamespace, rdfs:isDefinedBy)

    Example:

        runoak -i sqlite:obo:pr statistics -p oio:hasOBONamespace

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    if isinstance(impl, SummaryStatisticsInterface):
        impl.include_residuals = include_residuals
        if group_by_obo_namespace:
            group_by_property = HAS_OBO_NAMESPACE
        if group_by_defined_by:
            group_by_property = IS_DEFINED_BY
        if group_by_prefix:
            group_by_property = PREFIX_PREDICATE
        if not branches and not group_by_property:
            ssc = impl.branch_summary_statistics()
        else:
            if branches and group_by_property:
                raise ValueError("Cannot specify both branches and predicates")
            if branches:
                branches = list(query_terms_iterator(branches, impl))
                ssc = impl.global_summary_statistics(
                    branches={impl.label(b): [b] for b in branches}
                )
            else:
                ssc = impl.global_summary_statistics(group_by=group_by_property)
        if isinstance(writer, StreamingCsvWriter):
            if isinstance(ssc, GlobalStatistics):
                for p in ssc.partitions.values():
                    writer.emit(p)
            else:
                writer.emit(ssc)
        else:
            writer.emit(ssc)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
def ontologies(output: str):
    """
    Shows all ontologies

    If the input is a pre-merged ontology, then the output of this command is trivially
    a single line, with the name of the input ontology

    This command is more meaningful when the input is a multi-ontology endpoint, e.g

        runoak -i ubergraph ontologies

    In future this command will be expanded to allow showing more metadata about each ontology
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.ontologies():
            print(str(curie))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@all_ontologies_option
@click.argument("ontologies", nargs=-1)
def ontology_versions(ontologies, output: str, all: bool):
    """
    Shows ontology versions

    Currently only implemented for BioPortal

    Example:

        runoak -i bioportal: ontology-versions mp

    All ontologies:

        runoak -i bioportal ontology-versions --all
    """
    impl = settings.impl
    writer = StreamingCsvWriter(output)
    if isinstance(impl, BasicOntologyInterface):
        if len(ontologies) == 0:
            if all:
                ontologies = list(impl.ontologies())
            else:
                raise ValueError("Must pass one or more ontologies OR --all")
        for ont in list(ontologies):
            for v in impl.ontology_versions(ont):
                obj = dict(ontology=ont, version=v)
                writer.emit(obj)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@all_ontologies_option
@click.argument("ontologies", nargs=-1)
def ontology_metadata(ontologies, output_type: str, output: str, all: bool):
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
            metadata = impl.ontology_metadata_map(ont)
            writer.emit(metadata)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@predicates_option
@click.option(
    "--reification/--no-reification",
    default=False,
    show_default=True,
    help="if true then fetch axiom triples with annotations",
)
@click.argument("terms", nargs=-1)
def term_metadata(terms, predicates, reification: bool, output_type: str, output: str):
    """
    Shows term metadata.

    Example:

        runoak -i sqlite:obo:uberon term-metadata lung heart
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
@click.option(
    "--lexical-index-file",
    "-L",
    help="path to lexical index. This is recreated each time unless --no-recreate is passed",
)
@click.option(
    "--exclude-tokens",
    "-x",
    multiple=True,
    help="Text file or list of tokens to filter from input prior to annotation.\
        If passed as text file, each newline separated entry is a distinct text.",
)
@output_option
@output_type_option
def annotate(
    words,
    output: str,
    lexical_index_file: str,
    matches_whole_text: bool,
    exclude_tokens: str,
    text_file: TextIO,
    output_type: str,
):
    """
    Annotate a piece of text using a Named Entity Recognition annotation

    Example:

        runoak -i bioportal: annotate "enlarged nucleus in T-cells from peripheral blood"

    Currently most implementations do not yet support annotation.

    See the ontorunner framework for plugins for SciSpacy and OGER - these will
    later become plugins.

    If gilda is installed as an extra, it can be used,
    but ``--matches-whole-text`` (``-W``) must be specified,
    as gilda only performs grounding.

    Example:

        runoak -i gilda: annotate -W BRCA2

    Programmatic usage:

        This command is a wrapper onto the annotate_text method,
        this is provided as part of the *TextAnnotator* interface:

        https://incatools.github.io/ontology-access-kit/interfaces/text-annotator
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.text_annotator)
    writer.output = output

    if isinstance(impl, TextAnnotatorInterface):
        if lexical_index_file:
            if not Path(lexical_index_file).exists():
                logging.info(f"Creating new index: {lexical_index_file}")
                impl.lexical_index = create_lexical_index(impl)
                save_lexical_index(impl.lexical_index, lexical_index_file)
            else:
                impl.lexical_index = load_lexical_index(lexical_index_file)
        configuration = TextAnnotationConfiguration(matches_whole_text=matches_whole_text)
        if exclude_tokens:
            token_exclusion_list = get_exclusion_token_list(exclude_tokens)
            configuration.token_exclusion_list = token_exclusion_list
        if words and text_file:
            raise ValueError("Specify EITHER text-file OR a list of words as arguments")
        if text_file:
            for ann in impl.annotate_file(text_file, configuration):
                writer.emit(ann)
            # for line in text_file.readlines():
            #     line = line.strip()
            #     for ann in impl.annotate_text(line, configuration):
            #         # TODO: better way to represent this
            #         ann.subject_source = line
            #         writer.emit(ann)
        else:
            for ann in impl.annotate_text(words, configuration):
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
    Visualize an ancestor graph using **obographviz**

    For general background on what is meant by a graph in OAK,
    see https://incatools.github.io/ontology-access-kit/interfaces/obograph

    .. note::

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
        # TODO: abstract this out
        if output_type:
            write_graph(graph, format=output_type, output=output)
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
@click.option("--skip", multiple=True, help="Exclude paths that contain this node")
@click.option("--root", multiple=True, help="Use this node or nodes as roots")
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
    skip,
    root,
    output_type: str,
    output: TextIO,
):
    """
    Display an ancestor graph as an ascii/markdown tree

    For general instructions, see the viz command, which this is analogous too

    Example:

        runoak -i envo.db tree ENVO:00000372 -p i,p

    This produces output like:

    .code::

                        * [i] ENVO:00000094 ! volcanic feature
                            * [i] ENVO:00000247 ! volcano
                                * [i] ENVO:00000403 ! shield volcano
                                    * [i] **ENVO:00000372 ! pyroclastic shield volcano**


    Note: for many ontologies the tree view will explode, especially if no predicates are specified.
    You may wish to start with the is-a tree (-p i).

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
            start_curies=list(root) if root else None,
            skip=list(skip) if skip else None,
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
    List all ancestors of a given term or terms.

    Here ancestor means the transitive closure of the parent relationship, where
    a parent includes all relationship types, not just is-a.

    Example:

        runoak -i cl.owl ancestors CL:4023094

    This will show ancestry over the full relationship graph. Like any relational
    OAK command, this can be filtered by relationship type (predicate), using --predicate (-p).
    For exampple, constrained to is-a and part-of:

        runoak -i cl.owl ancestors CL:4023094 -p i,BFO:0000050

    Multiple backends can be used, including ubergraph:

        runoak -i ubergraph: ancestors CL:4023094 -p i,BFO:0000050

    Search terms can also be used:

        runoak -i cl.owl ancestors 'goblet cell'

    Multiple terms can be passed:

        runoak -i sqlite:go.db ancestors GO:0005773 GO:0005737 -p i,p

    More background:

        https://incatools.github.io/ontology-access-kit/interfaces/obograph.html
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    # writer.display_options = display.split(',')
    writer.file = output
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        actual_predicates = _process_predicates_arg(predicates)
        curies = list(query_terms_iterator(terms, impl))
        logging.info(f"Ancestor seed: {curies}")
        if statistics:
            if isinstance(writer, StreamingInfoWriter):
                raise ValueError(
                    "StreamingInfoWriter (`-O info`) does not support --statistics output"
                )
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
@click.option("--target", multiple=True, help="end point of path")
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
    List all siblings of a specified term or terms

    Example:

        runoak -i cl.owl siblings CL:4023094

    Note that siblings is by default over ALL relationship types, so we recommend
    always being explicit and passing a predicate using -p (--predicates)
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

    Example:

        runoak -i sqlite:obo:obi descendants assay -p i

    Example:

        runoak -i sqlite:obo:uberon descendants heart -p i,p

    This is the inverse of the 'ancestors' command; see the documentation for
    that command. But note that 'descendants' commands have the potential to be more
    "explosive" than ancestors commands, especially for high level terms, and for when
    predicates are not specified

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
    Exports (dumps) the entire contents of an ontology.

    Example:

        runoak -i pato.obo dump -o pato.json -O json

    Example:

        runoak -i pato.owl dump -o pato.ttl -O turtle

    Currently each implementation only supports a subset of formats.

    The dump command is also blocked for remote endpoints such as Ubergraph,
    to avoid killer queries.
    """
    if terms:
        raise NotImplementedError("Currently dump for a subset of terms is not supported")
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        logging.info(f"Out={output} syntax={output_type}")
        impl.dump(output, syntax=output_type)
    else:
        raise NotImplementedError


@main.command()
@click.argument("terms", nargs=-1)
@click.option("-o", "--output")
@click.option(
    "--used-only/--no-used-only",
    default=False,
    show_default=True,
    help="If True, show only prefixes used in ontology",
)
@output_type_option
def prefixes(terms, used_only: bool, output, output_type: str):
    """
    Shows prefix declarations.

    All standard prefixes:

        runoak prefixes

    Specific prefixes:

        runoak prefixes GO CL oio skos

    By default, prefix maps are exported as simple pairwise TSVs.

    Prefixes can also be exported in different formats, such as YAML and JSON, where they are
    simple dictionaries:

    In yaml:

        runoak prefixes --O yaml

    In turtle:

        runoak prefixes --O rdf

    For RDF exports, the prefix declaration should appear in BOTH prefix declarations, AND also as
    instances of SHACL PrefixDeclarations, e.g.

        @prefix CL: <http://purl.obolibrary.org/obo/CL_> .
        ...
        [] a sh:PrefixDeclaration ;
            sh:namespace CL: ;
            sh:prefix "CL" .

    The default prefixmap is always used, unless options are passed specifying additional
    prefix maps.

    Example:

        runoak --named-prefix-map prefixcc prefixes

    If an ontology is loaded, then --used-only can be used to restrict to
    prefixes for entities in that ontology

        runoak -i sqlite:obo:cl prefixes --used-only

    """
    if settings.impl is None:
        settings.impl = BasicOntologyInterface()
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    if isinstance(impl, BasicOntologyInterface):
        pm = impl.prefix_map()
        if not terms and used_only:

            def entity_prefix(curie: CURIE):
                if ":" in curie:
                    return curie.split(":")[0]

            terms = list(set([entity_prefix(e) for e in impl.entities() if e]))
        if terms:
            pm = {k: v for k, v in pm.items() if k in terms or v in terms}
        writer.emit_dict(pm, object_type=PrefixDeclaration)


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
@output_type_option
@autolabel_option
@click.argument("terms", nargs=-1)
def similarity_pair(terms, predicates, autolabel: bool, output: TextIO, output_type):
    """
    Determine pairwise similarity between two terms using a variety of metrics

    NOTE: this command may be deprecated, consider using similarity

    Note: We recommend always specifying explicit predicate lists

    Example:

        runoak -i ubergraph: similarity-pair -p i,p CL:0000540 CL:0000000

    You can omit predicates if you like but be warned this may yield
    hard to interpret results.

    E.g.

        runoak -i ubergraph: similarity-pair CL:0000540 GO:0001750

    yields "fully formed stage" (i.e these are both found in the adult) as
    the MRCA

    For phenotype ontologies, UPHENO relationship types connect phenotype terms to anatomy, etc:

       runoak -i ubergraph: similarity-pair MP:0010922 HP:0010616  -p i,p,UPHENO:0000001

    Background: https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity.html
    """
    if len(terms) != 2:
        raise ValueError(f"Need exactly 2 terms: {terms}")
    subject = terms[0]
    object = terms[1]
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    writer.output = output
    if isinstance(impl, SemanticSimilarityInterface):
        actual_predicates = _process_predicates_arg(predicates)
        sim = impl.pairwise_similarity(subject, object, predicates=actual_predicates)
        if autolabel:
            sim.subject_label = impl.label(sim.subject_id)
            sim.object_label = impl.label(sim.object_id)
            sim.ancestor_label = impl.label(sim.ancestor_id)
        writer.emit(sim)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@predicates_option
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
@click.option("-o", "--output", help="path to output")
@click.option(
    "--main-score-field",
    default="phenodigm_score",
    show_default=True,
    help="Score used for summarization",
)
@autolabel_option
@output_type_option
@click.argument("terms", nargs=-1)
def similarity(
    terms,
    predicates,
    set1_file,
    set2_file,
    autolabel: bool,
    jaccard_minimum,
    ic_minimum,
    main_score_field,
    output_type,
    output,
):
    """
    All by all similarity

    This calculates a similarity matrix for two sets of terms.

    Input sets of a terms can be specified in different ways:

    - via a file
    - via explicit lists of terms or queries

    Example:

        runoak -i hp.db all-similarity -p i --set1-file HPO-TERMS1 --set2-file HPO-TERMS2 -O csv

    This will compare every term in TERMS1 vs TERMS2

    Alternatively standard OAK term queries can be used, with "@" separating the two lists

    Example:

        runoak -i hp.db all-similarity -p i TERM_1 TERM_2 ... TERM_N @ TERM_N+1 ... TERM_M

    The .all term syntax can be used to select all terms in an ontology

    Example:

        runoak -i ma.db all-similarity -p i,p .all @ .all

    This can be mixed with other term selectors; for example to calculate the similarity of "neuron"
    vs all terms in CL:

        runoak -i cl.db all-similarity -p i,p .all @ neuron

    An example pipeline to do all by all over all phenotypes in HPO:

    Explicit:

        runoak -i hp.db descendants -p i HP:0000118 > HPO
        runoak -i hp.db all-similarity -p i --set1-file HPO --set2-file HPO -O csv -o RESULTS.tsv

    The same thing can be done more compactly with term queries:

        runoak -i hp.db all-similarity -p i .desc//p=i HP:0000118 @ .desc//p=i HP:0000118

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    logging.info(f"out={output} {type(output)}")
    writer.output = output
    logging.info(f"file={writer.file} {type(writer.output)}")
    if main_score_field and isinstance(writer, HeatmapWriter):
        writer.value_field = main_score_field
    if isinstance(impl, SemanticSimilarityInterface):
        set1it = None
        set2it = None
        if not (set1_file or set2_file):
            terms = list(terms)
            ix = terms.index("@")
            logging.info(f"Splitting terms {terms} on {ix}")
            set1it = query_terms_iterator(terms[0:ix], impl)
            set2it = query_terms_iterator(terms[ix + 1 :], impl)
        else:
            if set1_file:
                logging.info(f"Getting set1 from {set1_file}")
                with open(set1_file) as file:
                    set1it = list(curies_from_file(file))
            else:
                set1it = query_terms_iterator(terms, impl)
            if set2_file:
                logging.info(f"Getting set2 from {set2_file}")
                with open(set2_file) as file:
                    set2it = list(curies_from_file(file))
            else:
                set2it = query_terms_iterator(terms, impl)
        actual_predicates = _process_predicates_arg(predicates)
        for sim in impl.all_by_all_pairwise_similarity(
            set1it, set2it, predicates=actual_predicates
        ):
            if autolabel:
                # TODO: this can be made more efficient
                sim.subject_label = impl.label(sim.subject_id)
                sim.object_label = impl.label(sim.object_id)
                sim.ancestor_label = impl.label(sim.ancestor_id)
            if jaccard_minimum is not None:
                if sim.jaccard_similarity < jaccard_minimum:
                    continue
            if ic_minimum is not None:
                if sim.ancestor_information_content < ic_minimum:
                    continue
            writer.emit(sim)
        writer.finish()
        writer.file.close()
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@predicates_option
@output_option
@output_type_option
@autolabel_option
@click.argument("terms", nargs=-1)
def termset_similarity(
    terms,
    predicates,
    autolabel,
    output_type,
    output: TextIO,
):
    """
    Termset similarity

    This calculates a similarity matrix for two sets of terms.

    Example:

        runoak -i go.db termset-similarity -p i,p nucleus membrane @ "nuclear membrane" vacuole -p i,p

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    writer.output = output
    if isinstance(impl, SemanticSimilarityInterface):
        terms = list(terms)
        ix = terms.index("@")
        set1 = list(query_terms_iterator(terms[0:ix], impl))
        set2 = list(query_terms_iterator(terms[ix + 1 :], impl))
        logging.info(f"Set1={set1}")
        logging.info(f"Set2={set2}")
        actual_predicates = _process_predicates_arg(predicates)
        sim = impl.termset_pairwise_similarity(
            set1, set2, predicates=actual_predicates, labels=autolabel
        )
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
    Show information on term or set of terms

    Example:

        runoak -i sqlite:obo:cl info CL:4023094

    The default output is minimal, showing only ID and label

    The --output-type (-O) option can be used to specify other formats for the output.

    Currently there are only a few output types are supported. More will be provided in future.

    In OBO format:

        runoak -i cl.owl info CL:4023094 -O obo

    As CSV:

        runoak -i cl.obo info CL:4023094 -O csv

    The info output format can be parameterized with --display (-D)

    With xrefs and definitions:

        runoak -i cl.owl info CL:4023094 -D x,d

    With all information:

        runoak -i cl.owl info CL:4023094 -D all

    Like all OAK commands, input term lists can be multivalued, a mixture of IDs and labels, as well
    as queries that can be combined using boolean logic

    Info on two STATO terms:

        runoak -i ontobee:stato info STATO:0000286 STATO:0000287 -O obo

    All terms in ENVO with the string "forest" in them:

        runoak -i sqlite:obo:envo info l~forest

    Info on all subtypes of "statistical hypothesis test" in STATO:

        runoak -i sqlite:obo:stato info .desc//p=i 'statistical hypothesis test'
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
@if_absent_option
@set_value_option
def labels(terms, output: TextIO, display: str, output_type: str, if_absent: bool, set_value):
    """
    Show labels for term or list of terms

    Example:

        runoak -i cl.owl labels CL:4023093 CL:4023094

    You can use the ".all" selector to show all labels:

    Example:

        runoak -i cl.owl labels .all

    (this may be blocked for remote endpoints)

    You can query for terms that have either no label, or to include only ones with labels:

    Nodes with no labels:

        runoak -i cl.owl labels .all --if-absent exclude
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    if len(terms) == 0:
        raise ValueError("You must specify a list of terms. Use '.all' for all terms")
    n = 0
    changes = []
    for curie_it in chunk(query_terms_iterator(terms, impl)):
        logging.info("** Next chunk:")
        n += 1
        for curie, label in impl.labels(curie_it):
            obj = dict(id=curie, label=label)
            if set_value is not None:
                obj["new_value"] = set_value
                if set_value != label:
                    changes.append(
                        kgcl.NodeRename(
                            id="x", about_node=curie, old_value=label, new_value=set_value
                        )
                    )
                else:
                    logging.info(f"No change for {curie}")
            if _skip_if_absent(if_absent, label):
                continue
            writer.emit(obj)
    if n == 0:
        raise ValueError(f"No results for input: {terms}")
    _apply_changes(impl, changes)


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@ontological_output_type_option
@if_absent_option
@set_value_option
def definitions(terms, output: TextIO, display: str, output_type: str, if_absent: bool, set_value):
    """
    Show textual definitions for term or set of terms

    Example:

        runoak -i sqlite:obo:envo definitions 'tropical biome' 'temperate biome'

    You can use the ".all" selector to show all definitions for all terms in the ontology:

    Example:

        runoak -i sqlite:obo:envo definitions .all

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    changes = []
    for curie in query_terms_iterator(terms, impl):
        if isinstance(impl, BasicOntologyInterface):
            defn = impl.definition(curie)
            obj = dict(id=curie, definition=defn)
            if set_value is not None:
                obj["new_value"] = set_value
                if set_value != defn:
                    changes.append(
                        kgcl.NodeTextDefinitionChange(
                            id="x", about_node=curie, old_value=defn, new_value=set_value
                        )
                    )
                else:
                    logging.info(f"No change for {curie}")
            if _skip_if_absent(if_absent, defn):
                continue
            writer.emit(obj)
    _apply_changes(impl, changes)


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@direction_option
@autolabel_option
@output_type_option
@output_option
@if_absent_option
@set_value_option
@click.option(
    "--include-entailed/--no-include-entailed",
    default=False,
    show_default=True,
    help="Include entailed indirect relationships",
)
@click.option(
    "--include-tbox/--no-include-tbox",
    default=True,
    show_default=True,
    help="Include class-class relationships (subclass and existentials)",
)
@click.option(
    "--include-abox/--no-include-abox",
    default=True,
    show_default=True,
    help="Include instance relationships (class and object property assertions)",
)
def relationships(
    terms,
    predicates: str,
    direction: str,
    autolabel: bool,
    output_type: str,
    output: str,
    if_absent: bool,
    set_value: str,
    include_entailed: bool,
    include_tbox: bool,
    include_abox: bool,
):
    """
    Show all relationships for a term or terms

    By default, this shows all relationships where the input term(s) are the *subjects*

    Example:

        runoak -i cl.db relationships CL:4023094

    Like all OAK commands, a label can be passed instead of a CURIE

    Example:

        runoak -i cl.db relationships neuron

    To reverse the direction, and query where the search term(s) are *objects*, use the --direction flag:

    Example:

        runoak -i cl.db relationships --direction down neuron

    Multiple terms can be passed

    Example:

        runoak -i uberon.db relationships heart liver lung

    And like all OAK commands, a query can be passed rather than an explicit term list

    The following query lists all arteries in the limb together which what structures they supply

    Query:

        runoak -i uberon.db relationships -p RO:0002178 .desc//p=i "artery" .and .desc//p=i,p "limb"

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = _process_predicates_arg(predicates)
    if not (include_tbox or include_abox):
        raise ValueError("Cannot exclude both tbox AND abox")
    if isinstance(impl, BasicOntologyInterface):
        curies = list(query_terms_iterator(terms, impl))
        up_it = impl.relationships(
            curies,
            predicates=actual_predicates,
            include_abox=include_abox,
            include_tbox=include_tbox,
            include_entailed=include_entailed,
        )
        down_it = impl.relationships(
            objects=curies,
            predicates=actual_predicates,
            include_abox=include_abox,
            include_tbox=include_tbox,
            include_entailed=include_entailed,
        )
        if direction is None or direction == Direction.up.value:
            it = up_it
        elif direction == Direction.down.value:
            it = down_it
        else:
            it = chain(up_it, down_it)
        has_relationships = defaultdict(bool)
        for rel in it:
            if direction is None or direction == Direction.up.value:
                has_relationships[rel[0]] = True
            elif direction == Direction.down.value:
                has_relationships[rel[2]] = True
            else:
                has_relationships[rel[0]] = True
                has_relationships[rel[2]] = True
            if if_absent and if_absent == IfAbsent.absent_only.value:
                continue
            writer.emit(
                dict(subject=rel[0], predicate=rel[1], object=rel[2]),
                label_fields=["subject", "predicate", "object"],
            )
        if if_absent and if_absent == IfAbsent.absent_only.value:
            for curie in curies:
                if not has_relationships[curie]:
                    writer.emit(
                        dict(subject=curie, predicate=None, object=None),
                        label_fields=["subject", "predicate", "object"],
                    )
        if set_value:
            if len(actual_predicates) != 1:
                raise ValueError(f"predicates={actual_predicates}, expected exactly one")
            pred = actual_predicates[0]
            changes = []
            for curie in curies:
                changes.append(
                    kgcl.EdgeCreation(id="x", subject=curie, predicate=pred, object=set_value)
                )
            _apply_changes(impl, changes)

    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--unmelt/--no-unmelt", default=False, show_default=True, help="Flatten to a wide table"
)
@predicates_option
@autolabel_option
@output_type_option
@output_option
@if_absent_option
@set_value_option
def logical_definitions(
    terms,
    predicates: str,
    autolabel: bool,
    output_type: str,
    output: str,
    if_absent: bool,
    unmelt: bool,
    set_value: str,
):
    """
    Show all logical definitions for a term or terms.

    To show all logical definitions in an ontology, pass the ".all" query term

    Example; first create an alias:

        alias pato="runoak -i obo:sqlite:pato"

    Then run the query:

        pato logical-definitions .all

    By default, ".all" will query all axioms for all terms including merged terms;
    to restrict to only the current terms, use an ID query:

        pato logical-definitions i^PATO

    You can also restrict to branches:

        pato logical-definitions .desc//p=i "physical object quality"

    By default, the output is a subset of OboGraph datamodel rendered as YAML, e.g.

      definedClassId: PATO:0045071
        genusIds:
        - PATO:0001439
        restrictions:
        - fillerId: PATO:0000461
          propertyId: RO:0015010

    You can also specify CSV to generate a flattened form of this.

    Example:

        pato logical-definitions .all --output-type csv

    You can optionally choose to "unmelt" or flatten this, such that:

    - Each property/predicate is a column
    - For repeated properties, columns of the form prop_1, prop_2, ... are generated

    Example:

        pato logical-definitions .all  --unmelt --output-type csv

    Limitations:

    Currently this only works for definitions that follow a basic genus-differentia pattern,
    which is what is currently represented in the OboGraph datamodel.

    Consider using the "axioms" command for inspection of complex nested OWL axioms.
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.autolabel = autolabel
    actual_predicates = _process_predicates_arg(predicates)
    if set_value:
        raise NotImplementedError
    label_fields = [
        "definedClassId",
        "genusIds",
        "restrictionFillerIds",
        "restrictionsPropertyIds",
        "restrictionsFillerIds",
    ]
    if isinstance(impl, OboGraphInterface):
        # curies = list(query_terms_iterator(terms, impl))
        has_relationships = defaultdict(bool)
        curies = []
        if unmelt:
            ldef_flattener = LogicalDefinitionFlattener(
                labeler=lambda x: impl.label(x), curie_converter=impl.converter
            )
            writer.heterogeneous_keys = True
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            curie_chunk = list(curie_it)
            curies += curie_chunk
            for ldef in impl.logical_definitions(curie_chunk):
                if actual_predicates:
                    if not any(r for r in ldef.restrictions if r.propertyId in actual_predicates):
                        continue
                if ldef.definedClassId:
                    has_relationships[ldef.definedClassId] = True
                    if if_absent and if_absent == IfAbsent.absent_only.value:
                        continue
                    if unmelt:
                        flat_obj = ldef_flattener.convert(ldef)
                        writer.emit(flat_obj, label_fields=list(flat_obj.keys()))
                    else:
                        writer.emit(ldef, label_fields=label_fields)
        if if_absent and if_absent == IfAbsent.absent_only.value:
            for curie in curies:
                if not has_relationships.get(curie, False):
                    writer.emit({"noLogicalDefinition": curie})
        writer.finish()
        writer.file.close()
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@filter_obsoletes_option
@output_option
@owl_type_option
def terms(output: str, owl_type, filter_obsoletes: bool):
    """
    List all terms in the ontology

    Example:

        runoak -i db/cob.db terms

    All terms without obsoletes:

        runoak -i prontolib:cl.obo  terms --filter-obsoletes

    By default "terms" is considered to be any entity type in the ontology. Use --owl-type to constrain this:

    Classes:

        runoak -i sqlite:obo:ro terms --owl-type owl:Class

    Relationship types (Object properties):

        runoak -i sqlite:obo:ro terms --owl-type owl:ObjectProperty

    Annotation properties:

        runoak -i sqlite:obo:omo terms --owl-type owl:AnnotationProperty
    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        for curie in impl.entities(filter_obsoletes=filter_obsoletes, owl_type=owl_type):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@click.option(
    "--annotated-roots/--no-annotated-roots",
    "-A/--no-A",
    default=False,
    show_default=True,
    help="If true, use annotated roots, if present",
)
def roots(output: str, predicates: str, annotated_roots: bool):
    """
    List all root nodes in the ontology

    Like all OAK relational commands, this is parameterized by --predicates (-p).
    Note that the default is to return the roots of the relation graph over *all* predicates.
    This can sometimes give unintuitive results, so we recommend always being explicit
    and parameterizing

    Example:

        runoak -i db/cob.db roots

    This command is a wrapper onto the "roots" command in the BasicOntologyInterface.

    - https://incatools.github.io/ontology-access-kit/interfaces/basic.html#
      oaklib.interfaces.basic_ontology_interface.BasicOntologyInterface.roots

    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        for curie in impl.roots(actual_predicates, annotated_roots=annotated_roots):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@filter_obsoletes_option
def leafs(output: str, predicates: str, filter_obsoletes: bool):
    """
    List all leaf nodes in the ontology

    Like all OAK relational commands, this is parameterized by --predicates (-p).
    Note that the default is to return the roots of the relation graph over *all* predicates

    Example:

        runoak -i db/cob.db leafs

    This command is a wrapper onto the "leafs" command in the BasicOntologyInterface.

    - https://incatools.github.io/ontology-access-kit/interfaces/basic.html#
      oaklib.interfaces.basic_ontology_interface.BasicOntologyInterface.leafs
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        for curie in impl.leafs(actual_predicates, filter_obsoletes=filter_obsoletes):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@filter_obsoletes_option
def singletons(output: str, predicates: str, filter_obsoletes: bool):
    """
    List all singleton nodes in the ontology

    Like all OAK relational commands, this is parameterized by --predicates (-p).
    Note that the default is to return the singletons of the relation graph over *all* predicates

    Obsoletes are filtered by default

    Example:

        runoak -i db/cob.db singletons

    This command is a wrapper onto the "singletons" command in the BasicOntologyInterface.

    - https://incatools.github.io/ontology-access-kit/interfaces/basic.html#
      oaklib.interfaces.basic_ontology_interface.BasicOntologyInterface.singletons
    """
    impl = settings.impl
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        for curie in impl.singletons(actual_predicates, filter_obsoletes=filter_obsoletes):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@output_type_option
@autolabel_option
@click.option(
    "--maps-to-source", help="Return only mappings with subject or object source equal to this"
)
@click.argument("terms", nargs=-1)
def mappings(terms, maps_to_source, autolabel: bool, output, output_type):
    """
    List all mappings encoded in the ontology

    Example:

        runoak -i sqlite:obo:envo mappings

    The default output is SSSOM YAML. To use the (canonical) csv format:

        runoak -i sqlite:obo:envo mappings -O sssom

    By default, labels are not included. Use --autolabel to include labels (but note
    that if the label is not in the source ontology, then no label will be retrieved)

        runoak -i sqlite:obo:envo mappings -O sssom

    To constrain the mapped object source:

        runoak -i sqlite:obo:foodon mappings -O sssom --maps-to-source SUBSET_SIREN
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodel=sssom_schema)
    writer.output = output
    writer.autolabel = autolabel
    if isinstance(impl, MappingProviderInterface):
        if len(terms) == 0:
            for mapping in impl.sssom_mappings_by_source(subject_or_object_source=maps_to_source):
                if autolabel:
                    impl.inject_mapping_labels([mapping])
                writer.emit(mapping)
        else:
            for curie in query_terms_iterator(terms, impl):
                for mapping in impl.get_sssom_mappings_by_curie(curie):
                    if autolabel:
                        impl.inject_mapping_labels([mapping])
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

    TERMS should be either an explicit list of terms or queries, or can be a selector query,
    such as '.all' to fetch all terms in the ontology

    Show all aliases:

        runoak -i db/envo.db aliases .all

    Currently the core behavior of this command assumes a simple datamodel for aliases, where an aliases
    is a simple property-value tuples, with the property being from some standard vocabulary (e.g. skos:altLabel,
    oboInOwl, etc)

    If you know the synonyms follow the OBO/oboInOwl datamodel you can pass --obo-model, this will give back
    richer data if present in the ontology, including synonym categories/types, synonym provenance

    In future, this may become the default
    """
    impl = settings.impl
    writer = StreamingCsvWriter(output)
    if obo_model:
        if isinstance(impl, OboGraphInterface):
            curies = list(query_terms_iterator(terms, impl))
            for curie, spv in impl.synonym_property_values(curies):
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
@output_type_option
@click.argument("terms", nargs=-1)
def term_subsets(terms, output, output_type):
    """
    List subsets for a term or set of terms
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    if isinstance(impl, BasicOntologyInterface):
        curies_it = query_terms_iterator(terms, impl)
        for curie, subset in impl.terms_subsets(curies_it):
            writer.emit(dict(curie=curie, subset=subset))
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@click.argument("subsets", nargs=-1)
def expand_subsets(subsets: list, output, predicates):
    """
    For each subset provide a mapping of each term in the ontology to a subset

    Example:

        runoak -i db/pato.db expand-subsets attribute_slim value_slim
    """
    impl = settings.impl
    # writer = StreamingCsvWriter(output)
    if isinstance(impl, OboGraphInterface):
        actual_predicates = _process_predicates_arg(predicates)
        if not actual_predicates:
            actual_predicates = [IS_A, PART_OF]
        impl.enable_transitive_query_cache()
        term_curies = list(impl.entities())
        output.write("\t".join(["subset", "term", "subset_term"]))
        if len(subsets) == 0:
            subsets = list(impl.subsets())
            logging.info(f"SUBSETS={subsets}")
        for subset in subsets:
            logging.info(f"Subset={subset}")
            m = roll_up_to_named_subset(impl, subset, term_curies, predicates=actual_predicates)
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
@click.option("--category-system", help="Example: biolink, cob, bfo, dbpedia, ...")
@click.argument("terms", nargs=-1)
def term_categories(terms, output, output_type):
    """
    List categories for a term or set of terms

    TODO
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    if isinstance(impl, BasicOntologyInterface):
        curies_it = query_terms_iterator(terms, impl)
        for curie, subset in impl.terms_categories(curies_it):
            writer.emit(dict(curie=curie, subset=subset))
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

    Example:

        runoak -i cl.ofn axiom

    The above will write all axioms.

    You can filter by axiom type:

    Example:

        runoak -i cl.ofn axiom --axiom-type SubClassOf

    Note this currently only works with the funowl adapter, on functional syntax files
    """
    impl = settings.impl
    writer = StreamingAxiomWriter(syntax=output_type, functional_writer=impl.functional_writer)
    writer.output = output
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
            writer.emit(axiom)

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
    Compute all taxon constraints for a term or terms

    Note that this *computes* the taxon constraints rather than doing a lookup

    Example:

        runoak -i db/go.db taxon-constraints GO:0034357 --include-redundant -p i,p

    Example:

        runoak -i sqlite:obo:uberon taxon-constraints UBERON:0003884 UBERON:0003941 -p i,p

    This command is a wrapper onto taxon_constraints_utils:

    - https://incatools.github.io/ontology-access-kit/src/oaklib.utilities.taxon.taxon_constraints_utils
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
def eval_taxon_constraints(constraints, evolution_file, predicates: List, output):
    """
    Test candidate taxon constraints

    Multiple candidate constraints can be passed as arguments. these are in the form of triples
    separated by periods.

    Example:

        runoak  -i db/go.db eval-taxon-constraints -p i,p GO:0005743 only NCBITaxon:2759
        never NCBITaxon:2 . GO:0005634 only NCBITaxon:2

    The --evolution-file (-E) option can be used to pass in a file of candidates.
    This should follow the format used in https://arxiv.org/abs/1802.06004

    E.g.

        GO:0000229,Gain|NCBITaxon:1(root);>Loss|NCBITaxon:2759(Eukaryota);

    Example:

        runoak  -i db/go.db eval-taxon-constraints -p i,p -E tests/input/go-evo-gains-losses.csv

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
                st = eval_candidate_taxon_constraint(impl, st, predicates=actual_predicates)
                writer.emit(st)
            except ValueError as e:
                logging.error(f"Error with TC: {e}")
                st.description = "PROBLEM"
                writer.emit(st)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@if_absent_option
@set_value_option
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.option(
    "--terms-role",
    type=click.Choice([x.value for x in SubjectOrObjectRole]),
    default=SubjectOrObjectRole.OBJECT.value,
    show_default=True,
    help="How to interpret query terms.",
)
@click.argument("terms", nargs=-1)
def associations(
    terms,
    predicates: str,
    association_predicates: str,
    terms_role: str,
    autolabel: bool,
    output_type: str,
    output: str,
    if_absent: bool,
    set_value: str,
):
    """
    Lookup associations from or to entities.

    Example:

        runoak -i sqlite:obo:hp -g test.hpoa -G hpoa associations

    The above will show all associations

    To query using an ontology term, including is-a closure, specify one or more
    terms or term queries, plus the closure predicate(s), e.g.

    Example:

        runoak -i sqlite:obo:hp -g test.hpoa -G hpoa associations -p i HP:0001392

    This shows all annotations either to "Abnormality of the liver" (HP:0001392), or
    to is-a descendants

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = _process_predicates_arg(predicates)
    actual_association_predicates = _process_predicates_arg(association_predicates)
    if isinstance(impl, AssociationProviderInterface):
        curies = list(query_terms_iterator(terms, impl))
        qs_it = impl.associations(
            curies,
            predicates=actual_association_predicates,
            subject_closure_predicates=actual_predicates,
        )
        qo_it = impl.associations(
            objects=curies,
            predicates=actual_association_predicates,
            object_closure_predicates=actual_predicates,
        )
        if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
            it = qs_it
        elif terms_role == SubjectOrObjectRole.OBJECT.value:
            it = qo_it
        else:
            logging.info("Using query terms to query both subject and object")
            it = chain(qs_it, qo_it)
        has_relationships = defaultdict(bool)
        for assoc in it:
            if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
                has_relationships[assoc.subject] = True
            elif terms_role == SubjectOrObjectRole.OBJECT.value:
                has_relationships[assoc.object] = True
            else:
                has_relationships[assoc.subject] = True
                has_relationships[assoc.object] = True
            if if_absent and if_absent == IfAbsent.absent_only.value:
                continue
            writer.emit(
                assoc,
                label_fields=["subject", "predicate", "object"],
            )
        if if_absent and if_absent == IfAbsent.absent_only.value:
            for curie in curies:
                if not has_relationships[curie]:
                    writer.emit(
                        dict(subject=curie, predicate=None, object=None),
                        label_fields=["subject", "predicate", "object"],
                    )
        if set_value:
            if len(actual_predicates) != 1:
                raise ValueError(f"predicates={actual_predicates}, expected exactly one")
            pred = actual_predicates[0]
            changes = []
            for curie in curies:
                changes.append(
                    kgcl.EdgeCreation(id="x", subject=curie, predicate=pred, object=set_value)
                )
            _apply_changes(impl, changes)

    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@if_absent_option
@set_value_option
@click.option(
    "--cutoff", type=click.FLOAT, default=0.05, show_default=True, help="The cutoff for the p-value"
)
@click.option(
    "--sample-file",
    "-S",
    type=click.File(mode="r"),
    help="file containing input list of entity IDs (e.g. gene IDs)",
)
@click.option(
    "--background-file",
    "-B",
    type=click.File(mode="r"),
    help="file containing background list of entity IDs (e.g. gene IDs)",
)
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.argument("terms", nargs=-1)
def enrichment(
    terms,
    predicates: str,
    association_predicates: str,
    cutoff: float,
    autolabel: bool,
    output_type: str,
    output: str,
    sample_file: TextIO,
    background_file: TextIO,
    if_absent: bool,
    set_value: str,
):
    """
    Run class enrichment analysis.

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = _process_predicates_arg(predicates)
    actual_association_predicates = _process_predicates_arg(association_predicates)
    subjects = list(curies_from_file(sample_file))
    background = list(curies_from_file(background_file)) if background_file else None
    if isinstance(impl, ClassEnrichmentCalculationInterface):
        curies = list(query_terms_iterator(terms, impl))
        results = impl.enriched_classes(
            subjects,
            predicates=actual_association_predicates,
            object_closure_predicates=actual_predicates,
            hypotheses=curies if curies else None,
            background=background,
            cutoff=cutoff,
            autolabel=autolabel,
        )
        for result in results:
            writer.emit(result)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@click.option("-g", "--associations", help="associations")
@click.option("-X", "--other-associations", help="other associations")
def diff_associations(
    predicates: str,
    autolabel: bool,
    output_type: str,
    output: str,
    associations: str,
    other_associations: str,
):
    """
    Diffs two association sources. EXPERIMENTAL.

    This functionality may move out of core
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = _process_predicates_arg(predicates)
    logging.info(f"Fetching parser for {settings.associations_type}")
    association_parser = get_association_parser(settings.associations_type)
    if isinstance(impl, AssociationProviderInterface):
        if associations:
            logging.info(f"Loading main associations from {associations}")
            with open(associations) as file:
                assocs1 = list(association_parser.parse(file))
        else:
            assocs1 = list(impl.associations(predicates=actual_predicates))
        if len(assocs1) == 0:
            raise ValueError("No associations to compare")
        logging.info(f"Loading other associations from {other_associations}")
        with open(other_associations) as file:
            assocs2 = list(association_parser.parse(file))
            if isinstance(impl, OboGraphInterface):
                differ = AssociationDiffer(impl)
                impl.enable_transitive_query_cache()
                for change in differ.changes(assocs1, assocs2, actual_predicates):
                    writer.emit(
                        {"entity": change[0], "set": change[1], "term": change[2]},
                        label_fields=["term"],
                    )


@main.command()
@click.option(
    "--cutoff",
    default=50,
    show_default=True,
    help="maximum results to report for any (type, predicate) pair",
)
@click.option(
    "--skip-structural-validation/--no-skip-structural-validation",
    default=False,
    show_default=True,
    help="If true, main structural validation checks are skipped",
)
@click.option(
    "--skip-ontology-rules/--no-skip-ontology-rules",
    default=True,
    show_default=True,
    help="If true, ontology rules are skipped",
)
@click.option(
    "--rule",
    "-R",
    multiple=True,
    help="A rule to run. Can be specified multiple times. If not specified, all rules are run.",
)
@output_option
@output_type_option
def validate(
    output: str,
    cutoff: int,
    skip_structural_validation: bool,
    skip_ontology_rules: bool,
    rule,
    output_type,
):
    """
    Validate an ontology against ontology metadata

    Implementation notes: Currently only works on SQLite

    Example:

        runoak  -i db/ecto.db validate -o results.tsv

    The default validation performed is structural (conformance to the ontology_metadata schema)

    There is experimental support for additional ontology rules, which includes heuristic methods
    such as aligning text and logical definitions. These are off by default.

    To run these, pass --no-skip-ontology-rules

    Example:

        runoak -i db/uberon.db validate --skip-structural-validation --no-skip-ontology-rules

    For more information, see the OAK how-to guide:

    - https://incatools.github.io/ontology-access-kit/howtos/validate-an-obo-ontology.html
    """
    impl = settings.impl
    writer = _get_writer(
        output_type, impl, StreamingCsvWriter, datamodel=datamodels.validation_datamodel
    )
    writer.output = output
    if rule:
        skip_ontology_rules = False
    if isinstance(impl, ValidatorInterface):
        if not skip_structural_validation:
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
                    # print(yaml_dumper.dumps(result))
            for k, v in counts.items():
                print(f"{k}:: {v}")
        if not skip_ontology_rules:
            rr = RuleRunner()
            if rule:
                rr.set_rules(rule)
            for result in rr.run(impl):
                writer.emit(result)
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

    For more information, see the OAK how-to guide:

    - https://incatools.github.io/ontology-access-kit/howtos/validate-an-obo-ontology.html
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
@click.option(
    "--skip-text-annotation/--no-skip-text-annotation",
    default=False,
    show_default=True,
    help="If true, do not parse text annotations",
)
@output_type_option
@output_option
@click.argument("terms", nargs=-1)
def validate_definitions(terms, skip_text_annotation, output: str, output_type: str):
    """
    Checks presence and structure of text definitions.

    To run:

        runoak validate-definitions -i db/uberon.db -o results.tsv

    By default this will apply basic text mining of text definitions to check
    against machine actionable OBO text definition guideline rules.
    This can result in an initial lag - to skip this, and ONLY perform
    checks for presence of definitions, use --skip-text-annotation:

    Example:

        runoak validate-definitions -i db/uberon.db --skip-text-annotation

    Like most OAK commands, this accepts lists of terms or term queries
    as arguments. You can pass in a CURIE list to selectively validate
    individual classes

    Example:

         runoak validate-definitions -i db/cl.db CL:0002053

    Only on CL identifiers:

        runoak validate-definitions -i db/cl.db i^CL:

    Only on neuron hierarchy:

        runoak validate-definitions -i db/cl.db .desc//p=i neuron

    Output format:

    This command emits objects conforming to the OAK validation datamodel.
    See https://incatools.github.io/ontology-access-kit/datamodels for more
    on OAK datamodels.

    The default serialization of the datamodel is CSV.

    Notes:

    This command is largely redundant with the validate command, but is useful for
    targeted validation focused solely on definitions
    """
    impl = settings.impl
    writer = _get_writer(
        output_type, impl, StreamingCsvWriter, datamodel=datamodels.validation_datamodel
    )
    writer.output = output
    if isinstance(impl, ValidatorInterface):
        if terms:
            entities = query_terms_iterator(terms, impl)
        else:
            entities = None
        definition_rule = TextAndLogicalDefinitionMatchOntologyRule(
            skip_text_annotation=skip_text_annotation
        )
        for vr in definition_rule.evaluate(impl, entities=entities):
            writer.emit(vr)
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

    Note: the specified ontology is modified in place

    The input for this command is a list equals-separated pairs, specifying the
    source and the target

    Example:

        runoak -i db/uberon.db migrate-curies --replace SRC1=TGT1 SRC2=TGT2

    This command is a wrapper onto the "migrate_curies" command in the PatcherInterface

    - https://incatools.github.io/ontology-access-kit/interfaces/patcher.html#
    oaklib.interfaces.patcher_interface.PatcherInterface.migrate_curies
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
    "--rules-file",
    "-R",
    help="path to rules file. Conforms to rules_datamodel.\
        e.g. https://github.com/INCATools/ontology-access-kit/blob/main/tests/input/matcher_rules.yaml",
)
@click.option(
    "--add-labels/--no-add-labels",
    default=False,
    show_default=True,
    help="Populate empty labels with URI fragments or CURIE local IDs, for ontologies that use semantic IDs",
)
@click.option(
    "--lexical-index-file",
    "-L",
    help="path to lexical index. This is recreated each time unless --no-recreate is passed",
)
# @click.option(
#     "--exclude-tokens",
#     "-x",
#     help="Text file or list of terms to exclude from annotation. Each newline separated entry is a distinct text.",
# )
@click.option(
    "--recreate/--no-recreate",
    default=True,
    show_default=True,
    help="if true and lexical index is specified, always recreate, otherwise load from index",
)
@output_option
@click.argument("terms", nargs=-1)
def lexmatch(output, recreate, rules_file, lexical_index_file, add_labels, terms):
    """
    Performs lexical matching between pairs of terms in one more more ontologies.

    Examples:

        runoak -i foo.obo lexmatch -o foo.sssom.tsv

    In this example, the input ontology file is assumed to contain all pairs of terms to be mapped.

    It is more common to map between all pairs of terms in two ontology files. In this case,
    you can merge the ontologies using a tool like ROBOT; or,  to avoid a merge
    preprocessing step, use the --addl (-a) option to specify a second ontology file.

        runoak -i foo.obo --add bar.obo lexmatch -o foo.sssom.tsv

    By default, this command will compare all terms in all ontologies. You can use the OAK
    term query syntax to pass in the set of all terms to be compared.

    For example, to compare all terms in union of FOO and BAR namespaces:

        runoak -i foo.obo --add bar.obo lexmatch -o foo.sssom.tsv i^FOO: i^BAR:

    All members of the set are compared (including FOO to FOO matches and BAR to BAR
    matches), omitting trivial reciprocal matches.

    Use an "@" separator between two queries to feed in two explicit sets:

        runoak -i foo.obo --add bar.obo lexmatch -o foo.sssom.tsv i^FOO: @ i^BAR:

    ALGORITHM: lexmatch implements a simple algorithm:

    - create a lexical index, keyed by normalized strings of labels, synonyms
    - report all pairs of entities that have the same key

    The lexical index can be exported (in native YAML) using -L:

        runoak -i foo.obo lexmatch -L foo.index.yaml -o foo.sssom.tsv

    Note: if you run the above command a second time it will be faster as the index
    will be reused.

    RULES: Using custom rules:

        runoak  -i foo.obo lexmatch -R match_rules.yaml -L foo.index.yaml -o foo.sssom.tsv

    Full documentation:

    - https://incatools.github.io/ontology-access-kit/src/oaklib.utilities.lexical.lexical_indexer.html#
    module-oaklib.utilities.lexical.lexical_indexer
    """
    impl = settings.impl
    if rules_file:
        ruleset = load_mapping_rules(rules_file)
    else:
        ruleset = None

    # if exclude_tokens:
    #     token_exclusion_list = get_exclusion_token_list(exclude_tokens)

    if isinstance(impl, BasicOntologyInterface):
        if terms:
            if "@" in terms:
                ix = terms.index("@")
                logging.info(f"Splitting terms into two, position = {ix}")
                subjects = list(query_terms_iterator(terms[0:ix], impl))
                objects = list(query_terms_iterator(terms[ix + 1 :], impl))
            else:
                subjects = list(query_terms_iterator(terms, impl))
                objects = subjects
        else:
            subjects = None
            objects = None
        if add_labels:
            add_labels_from_uris(impl)
        if not recreate and Path(lexical_index_file).exists():
            logging.info("Reusing previous index")
            ix = load_lexical_index(lexical_index_file)
        else:
            logging.info("Creating index")
            if ruleset:
                syn_rules = [x.synonymizer for x in ruleset.rules if x.synonymizer]
            else:
                syn_rules = []
            ix = create_lexical_index(impl, synonym_rules=syn_rules)
        if lexical_index_file:
            if recreate:
                logging.info("Saving index")
                save_lexical_index(ix, lexical_index_file)
        logging.info(f"Generating mappings from {len(ix.groupings)} groupings")
        msdf = lexical_index_to_sssom(impl, ix, ruleset=ruleset, subjects=subjects, objects=objects)
        sssom_writers.write_table(msdf, output)
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("--other-ontology", help="other ontology")
@output_option
@click.argument("terms", nargs=-1)
def diff_terms(output, other_ontology, terms):
    """
    Compares a pair of terms in two ontologies

    EXPERIMENTAL
    """
    impl = settings.impl
    if other_ontology is None:
        other_impl = impl
    else:
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
@click.option(
    "--statistics/--no-statistics",
    default=False,
    show_default=True,
    help="show summary statistics only",
)
@group_by_property_option
@group_by_obo_namespace_option
@group_by_defined_by_option
@group_by_prefix_option
@output_option
@output_type_option
def diff(
    simple: bool,
    statistics: bool,
    output,
    group_by_property,
    group_by_obo_namespace: bool,
    group_by_prefix: bool,
    group_by_defined_by: bool,
    output_type,
    other_ontology,
):
    """
    Compute difference between two ontologies.

    Example:

        runoak -i foo.obo diff -X bar.obo -o diff.yaml

    This will produce a list of Changes that are required to go from the main input ontology (--input)
    to the other ontology (--other-ontology, or -X).

    The output follows the KGCL data model.
    See https://incatools.github.io/ontology-access-kit/datamodels/kgcl/index.html

    You can use --output-type to control the output format.

    KGCL controlled natural language:

        runoak -i foo.obo diff -X bar.obo -o diff.txt --output-type kgcl

    KGCL JSON:

        runoak -i foo.obo diff -X bar.obo -o diff.json --output-type json

    YAML (default):

        runoak -i foo.obo diff -X bar.obo -o diff.yaml --output-type yaml

    The --statistics option can be used to generate summary statistics for the changes.
    These are grouped according to the --group-by-property option. For example,
    the GO uses the oio:hasOBONamespace property to partition classes into 3 categories.

    Example:

        runoak -i go.obo diff -X go-new.obo -o diff.yaml --statistics --group-by-property oio:hasOBONamespace

    This will produce a YAML dictionary, with outer keys being the values of the oio:hasOBONamespace property,
    and inner keys being the change types.

    If --group-by-property is not specified, or there is no value for this property, then the outer key
    will be "__RESIDUAL__"

    For summary statistics, you can also specify --output-type csv, to get a tabular out

    Limitations:

    This does not do a diff over every axiom in each ontology. For a complete OWL diff, you should
    use ROBOT.

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.heterogeneous_keys = True
    other_impl = get_implementation_from_shorthand(other_ontology)
    config = DiffConfiguration(simple=simple)
    if group_by_obo_namespace:
        config.summary_partition_property = HAS_OBO_NAMESPACE
    if group_by_defined_by:
        config.summary_partition_property = IS_DEFINED_BY
    if group_by_prefix:
        config.summary_partition_property = PREFIX_PREDICATE
    if group_by_property:
        if config.summary_partition_property:
            logging.warning(
                f"Duplicative setting of property {group_by_property} and {config.summary_partition_property}"
            )
            if config.summary_partition_property != group_by_property:
                raise ValueError(
                    f"Cannot set both {config.summary_partition_property} and {group_by_property}"
                )
        config.summary_partition_property = group_by_property
    if isinstance(impl, DifferInterface):
        if statistics:
            summary = impl.diff_summary(other_impl, configuration=config)
            if isinstance(writer, StreamingCsvWriter):
                # inject the key into object, ensuring it is the first column
                for k, v in summary.items():
                    v = {**{"group": k}, **v}
                    writer.emit(v)
            else:
                writer.emit(summary)
        else:
            for change in impl.diff(other_impl, configuration=config):
                if isinstance(writer, StreamingYamlWriter):
                    # TODO: when a complete type designator is added to KGCL
                    # we can remove this
                    change.type = change.__class__.__name__
                writer.emit(change)
        writer.finish()
    else:
        raise NotImplementedError


@main.command()
@click.option("--output", "-o")
@click.option("--changes-input", type=click.File(mode="r"), help="Path to an input changes file")
@click.option("--changes-format", help="Format of the changes file (json or kgcl)")
@click.option(
    "--parse-only/--no-parse-only",
    default=False,
    show_default=True,
    help="if true, only perform the parse of KCGL and do not apply",
)
@output_type_option
@overwrite_option
@click.argument("commands", nargs=-1)
def apply(
    commands,
    output,
    output_type,
    changes_input: TextIO,
    changes_format,
    parse_only: bool,
    overwrite: bool,
):
    """
    Applies a patch to an ontology. The patch should be specified using KGCL syntax, see
    https://github.com/INCATools/kgcl

    Example:

        runoak -i cl.owl.ttl apply "rename CL:0000561 to 'amacrine neuron'"  -o cl.owl.ttl -O ttl

    On an obo format file:

        runoak -i simpleobo:go-edit.obo apply "rename GO:0005634 from 'nucleus' to 'foo'" -o go-edit-new.obo

    With URIs:

        runoak -i cl.owl.ttl apply \
          "rename <http://purl.obolibrary.org/obo/CL_0000561> from 'amacrine cell' to 'amacrine neuron'" \
           -o cl.owl.ttl -O ttl

    WARNING:

    This command is still experimental. Some things to bear in mind:

    - for some ontologies, CURIEs may not work, instead specify a full URI surrounded by <>s
    - only a subset of KGCL commands are supported by each backend
    """
    impl = settings.impl
    if isinstance(impl, PatcherInterface):
        impl.autosave = settings.autosave
        changes = []
        files = []
        if changes_input:
            files.append(changes_input)
        for command in commands:
            if command == "-":
                files.append(sys.stdin)
            else:
                change = kgcl_parser.parse_statement(command)
                logging.info(f"parsed {command} == {change}")
                changes.append(change)
        changes += list(parse_kgcl_files(files, changes_format))
        for change in changes:
            logging.info(f"Change: {change}")
            if parse_only:
                print(json_dumper.dumps(change))
            else:
                impl.apply_patch(change)
        if not settings.autosave and not overwrite and not output:
            logging.warning("--autosave not passed, changes are NOT saved")
        if output:
            if output == "-":
                output = sys.stdout
            impl.dump(output, output_type)
        elif overwrite:
            logging.info("Over-writing")
            impl.dump(impl.resource.local_path)
    else:
        raise NotImplementedError


@main.command()
@click.option("--output", "-o")
@output_type_option
@click.argument("terms", nargs=-1)
def apply_obsolete(output, output_type, terms):
    """
    Sets an ontology element to be obsolete

    Example:

        runoak -i my.obo apply-obsolete MY:0002200 -o my-modified.obo

    Multiple terms can be passed, as labels, IDs, or using OAK queries:

        runoak -i my.obo apply-obsolete MY:1 MY:2 MY:3 ... -o my-modified.obo

    This may be chained, for example to take all terms matching a search query and then
    obsolete them all:

        runoak -i my.db search 'l/^Foo/` | runoak -i my.db --autosave apply-obsolete -

    This command is partially redundant with the more general "apply" command
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
@click.option("--output", "-o")
@click.option("--report-format", help="Output format for reporting proposed/applied changes")
@dry_run_option
@output_type_option
def lint(output, output_type, report_format, dry_run: bool):
    """
    Lints an ontology, applying changes in place.

    The current implementation is highly incomplete, and only handles
    linting of syntactic patterns (chains of whitespace, trailing whitespace)
    in labels and definitions.

    The output is a list of changes, in a KCGL-compliant syntax.

    By default, changes will be applied

    Example:

        runoak -i my.obo lint

    This can be executed in dry-run mode, in which case changes are not applied:

        runoak -i my.obo lint --dry-run

    One common workflow is to emit the changes to a KCGL file which is manually checked,
    then applied as a separate step.

    Example workflow:

        runoak -i my.obo lint --dry-run -o changes.kgcl
        # examine and edit changes.kgcl
        runoak -i my.obo apply --changes-input changes.kgcl

    """
    impl = settings.impl
    writer = _get_writer(report_format, impl, StreamingJsonWriter)
    writer.output = output
    if isinstance(impl, PatcherInterface):
        impl.autosave = settings.autosave
        changes = lint_ontology(impl, dry_run=dry_run)
        for _, change in changes:
            writer.emit(change)
        writer.finish()
    else:
        raise NotImplementedError


@main.command()
@click.option("-S", "--source", multiple=True, help="ontology prefixes  e.g. HP, MP")
@click.option(
    "--mapping-input",
    help="File of mappings in SSSOM format. If not provided then mappings in ontology(ies) are used",
)
@click.option("--other-input", "-X", help="Additional input file")
@click.option("--other-input-type", help="Type of additional input file")
@click.option(
    "--intra/--no-intra",
    default=False,
    show_default=True,
    help="If true, then all sources are in the main input ontology",
)
@autolabel_option
@click.option(
    "--include-identity-mappings/--no-include-identity-mappings",
    default=False,
    show_default=True,
    help="Use identity relation as mapping; use this for two versions of the same ontology",
)
@click.option(
    "--filter-category-identical/--no-filter-category-identical",
    default=False,
    show_default=True,
    help="Do not report cases where a relationship has not changed",
)
@predicates_option
@output_option
@output_type_option
@click.argument("terms", nargs=-1)
def diff_via_mappings(
    source,
    mapping_input,
    intra,
    autolabel,
    include_identity_mappings: bool,
    filter_category_identical: bool,
    other_input,
    other_input_type,
    predicates,
    output_type,
    output,
    terms,
):
    """
    Calculates cross-ontology diff using mappings

    Given a pair of ontologies, and mappings that connect terms in both ontologies, this
    command will perform a structural comparison of all mapped pairs of terms

    Example:

        runoak -i sqlite:obo:uberon --other-input sqlite:obo:zfa  --source UBERON --source ZFA -O csv

    Note the above command does not have any mapping file specified; the mappings that are distributed within
    each ontology is used (in this case, Uberon contains mappings to ZFA)

    If the mappings are provided externally:

        runoak -i ont1.obo --other-input ont2.obo --mapping-input mappings.sssom.tsv

    (in the above example, --source is not passed, so all mappings are tested)

    If there are no existing mappings, you can use the lexmatch command to generate them:

        runoak -i ont1.obo -a ont2.obo lexmatch -o mappings.sssom.stv
        runoak -i ont1.obo --other-input ont2.obo --mapping-input mappings.sssom.tsv

    The output from this command follows the cross-ontology-diff data model
    (https://incatools.github.io/ontology-access-kit/datamodels/cross-ontology-diff/index.html)

    This can be serialized in YAML or TSV form
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
    if terms:
        entities = list(query_terms_iterator(terms, oi))
    else:
        logging.info("No term list provided, will compare all mapped terms")
        entities = None
    actual_predicates = _process_predicates_arg(predicates)
    n = 0
    for r in calculate_pairwise_relational_diff(
        oi,
        other_oi,
        sources=sources,
        entities=entities,
        mappings=mappings,
        add_labels=autolabel,
        include_identity=include_identity_mappings,
        predicates=actual_predicates,
    ):
        if filter_category_identical and r.category == DiffCategory(DiffCategory.Identical):
            continue
        writer.emit(r)
        n += 1
    if n == 0:
        raise ValueError("No mappings extracted")


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
    "--comment",
    default="#",
    show_default=True,
    help="Comment indicator at the beginning of a row.",
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
    comment,
    missing_value_token,
    allow_missing: bool,
    relation: tuple,
    relation_file: str,
    schema: str,
):
    """
    Fills missing values in a table of ontology elements

    See https://incatools.github.io/ontology-access-kit/src/oaklib.utilities.table_filler

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

    - TODO: allow for an option that will perform fuzzy matches of labels
    - TODO: reverse lookup is not provided for all fields, such as definitions
    - TODO: add an option to detect inconsistencies
    - TODO: add logical for obsoletion/replaced by
    - TODO: use most optimized method for whichever backend
    """
    tf = TableFiller(settings.impl)
    with open(table_file) as input_file:
        comment_lines = [x for x in input_file.readlines() if x.startswith(comment)]

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
        table_filler.write_table(input_table, output, delimiter=delimiter, comments=comment_lines)


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--rules-file",
    "-R",
    help="path to rules file. Conforms to rules_datamodel.\
        e.g. https://github.com/INCATools/ontology-access-kit/blob/main/tests/input/matcher_rules.yaml",
)
@click.option(
    "--apply-patch/--no-apply-patch",
    default=False,
    show_default=True,
    help="Apply KGCL syntax generated based on the synonymizer rules file.",
)
@click.option(
    "--patch",
    type=click.File(mode="w"),
    default=sys.stdout,
    help="Output patch file containing KGCL commands.",
)
@output_option
def synonymize(terms, rules_file, apply_patch, patch, output):
    """
    Apply synonymizer rule from the rules file to generate KGCL syntax
    see https://github.com/INCATools/kgcl.

    Example:
        runoak -i foo.obo synonymize -R foo_rules.yaml --patch patch.kgcl --apply-patch
    """
    impl = settings.impl
    # TODO: Eventually get this from settings as above

    if rules_file:
        ruleset = load_mapping_rules(rules_file)
    else:
        ruleset = None

    if isinstance(impl, OboGraphInterface):
        syn_rules = [x.synonymizer for x in ruleset.rules if x.synonymizer]

        terms_to_synonymize = {}
        change_list = []

        for curie in query_terms_iterator(terms, impl):
            # for rule in syn_rules:
            for _, aliases in impl.entity_alias_map(curie).items():
                matches = []
                if aliases is not None:
                    # matches.extend([x for x in aliases if re.search(eval(rule.match), x) is not None])
                    for alias in aliases:
                        if alias:
                            synonymized, new_alias, qualifier = apply_transformation(
                                alias,
                                LexicalTransformation(
                                    TransformationType.Synonymization, params=syn_rules
                                ),
                            )
                            if synonymized:
                                matches.append(new_alias)

                if len(matches) > 0:
                    if qualifier is None or qualifier == "":
                        qualifier = DEFAULT_QUALIFIER
                    terms_to_synonymize[curie] = matches
                    change = kgcl.NewSynonym(
                        id="kgcl_change_id_" + str(len(terms_to_synonymize)),
                        about_node=curie,
                        old_value=alias,
                        new_value=new_alias,
                        qualifier=qualifier,
                    )
                    change_list.append(change)
                    if patch:
                        patch.write(str(change))
                        patch.write("\n")

        if apply_patch and len(change_list) > 0:
            if output:
                impl.resource.slug = output
            _apply_changes(impl, change_list)


# runoak -i tests/input/synonym-test.obo synonymize -R
# tests/input/matcher_rules.yaml  .all --patch test.kgcl --apply-patch


if __name__ == "__main__":
    main()
