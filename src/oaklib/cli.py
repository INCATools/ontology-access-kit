"""
Command Line Interface to OAK
----------------------

Executed using "runoak" command
"""

# TODO: order commands.
# See https://stackoverflow.com/questions/47972638/how-can-i-define-the-order-of-click-sub-commands-in-help
import json
import logging
import statistics as stats
import sys
from collections import defaultdict
from enum import Enum, unique
from itertools import chain
from pathlib import Path
from types import ModuleType
from typing import (
    Any,
    List,
    Optional,
    TextIO,
    Type,
)

import click
import kgcl_schema.grammar.parser as kgcl_parser
import sssom.writers as sssom_writers
import sssom_schema
import yaml
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.introspection import package_schemaview
from prefixmaps.io.parser import load_multi_context
from pydantic import BaseModel
from sssom.parsers import parse_sssom_table, to_mapping_set_document

import oaklib.datamodels.taxon_constraints as tcdm
from oaklib import datamodels
from oaklib.constants import FILE_CACHE
from oaklib.converters.logical_definition_flattener import LogicalDefinitionFlattener
from oaklib.datamodels import synonymizer_datamodel
from oaklib.datamodels.association import RollupGroup
from oaklib.datamodels.cross_ontology_diff import DiffCategory
from oaklib.datamodels.obograph import (
    BasicPropertyValue,
    Edge,
    Graph,
    GraphDocument,
    LogicalDefinitionAxiom,
    Meta,
    Node,
    PrefixDeclaration,
)
from oaklib.datamodels.settings import Settings
from oaklib.datamodels.summary_statistics_datamodel import (
    GroupedStatistics,
    UngroupedStatistics,
)
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.datamodels.validation_datamodel import ValidationConfiguration
from oaklib.datamodels.vocabulary import (
    HAS_OBO_NAMESPACE,
    IS_A,
    IS_DEFINED_BY,
    OBSOLETION_RELATIONSHIP_PREDICATES,
    PART_OF,
    PREFIX_PREDICATE,
)
from oaklib.implementations.aggregator.aggregator_implementation import (
    AggregatorImplementation,
)
from oaklib.implementations.obograph.obograph_implementation import (
    OboGraphImplementation,
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
    SubjectOrObjectRole,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.differ_interface import (
    RESIDUAL_KEY,
    DiffConfiguration,
    DifferInterface,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.merge_interface import MergeInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import (
    EdgeTemplate,
    GraphTraversalMethod,
    OboGraphInterface,
)
from oaklib.interfaces.ontology_generator_interface import OntologyGenerationInterface
from oaklib.interfaces.owl_interface import AxiomFilter, OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.interfaces.usages_interface import UsagesInterface
from oaklib.io.heatmap_writer import HeatmapWriter
from oaklib.io.html_writer import HTMLWriter
from oaklib.io.obofoundry_markdown_writer import OboFoundryMarkdownWriter
from oaklib.io.obograph_writer import write_graph, write_graph_document
from oaklib.io.rollup_report_writer import write_report
from oaklib.io.streaming_axiom_writer import StreamingAxiomWriter
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_fhir_writer import StreamingFHIRWriter
from oaklib.io.streaming_info_writer import StreamingInfoWriter
from oaklib.io.streaming_json_lines_writer import StreamingJsonLinesWriter
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
from oaklib.query import curies_from_file, process_predicates_arg, query_terms_iterator
from oaklib.resource import OntologyResource
from oaklib.selector import get_adapter, get_resource_from_shorthand
from oaklib.transformers.transformers_factory import (
    apply_ontology_transformation,
    get_ontology_transformer,
)
from oaklib.types import CURIE
from oaklib.utilities import table_filler
from oaklib.utilities.apikey_manager import set_apikey_value
from oaklib.utilities.associations.association_differ import AssociationDiffer
from oaklib.utilities.associations.association_queries import get_association_iterator
from oaklib.utilities.axioms import (
    logical_definition_analyzer,
    logical_definition_summarizer,
)
from oaklib.utilities.axioms.disjointness_axiom_analyzer import (
    DisjointnessInducerConfig,
    generate_disjoint_class_expressions_axioms,
)
from oaklib.utilities.basic_utils import pairs_as_dict
from oaklib.utilities.caching import CachePolicy
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.kgcl_utilities import (
    generate_change_id,
    parse_kgcl_files,
    write_kgcl,
)
from oaklib.utilities.lexical import patternizer, synonymizer
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
from oaklib.utilities.mapping.mapping_crawler import MappingCrawler, MappingCrawlerConfig
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter
from oaklib.utilities.ner_utilities import get_exclusion_token_list
from oaklib.utilities.obograph_utils import (
    ancestors_with_stats,
    default_stylemap_path,
    graph_to_d3viz_objects,
    graph_to_image,
    graph_to_tree_display,
    remove_unlabeled_nodes,
    shortest_paths,
    trim_graph,
)
from oaklib.utilities.publication_utils.pubmed_wrapper import PubmedWrapper
from oaklib.utilities.subsets.slimmer_utils import (
    roll_up_to_named_subset,
)
from oaklib.utilities.subsets.subset_validator import SubsetValidationConfig
from oaklib.utilities.table_filler import ColumnDependency, TableFiller, TableMetadata
from oaklib.utilities.taxon.taxon_constraint_utils import parse_gain_loss_file
from oaklib.utilities.validation.lint_utils import lint_ontology
from oaklib.utilities.validation.rule_runner import RuleRunner

OBO_FORMAT = "obo"
RDF_FORMAT = "rdf"
MD_FORMAT = "md"
HTML_FORMAT = "html"
OBOJSON_FORMAT = "obojson"
CSV_FORMAT = "csv"
TSV_FORMAT = "tsv"
JSON_FORMAT = "json"
JSONL_FORMAT = "jsonl"
YAML_FORMAT = "yaml"
INFO_FORMAT = "info"
SSSOM_FORMAT = "sssom"
OWLFUN_FORMAT = "ofn"
NL_FORMAT = "nl"
KGCL_FORMAT = "kgcl"
FHIR_JSON_FORMAT = "fhirjson"
HEATMAP_FORMAT = "heatmap"

ONT_FORMATS = [
    OBO_FORMAT,
    OBOJSON_FORMAT,
    OWLFUN_FORMAT,
    RDF_FORMAT,
    JSON_FORMAT,
    YAML_FORMAT,
    FHIR_JSON_FORMAT,
    CSV_FORMAT,
    TSV_FORMAT,
    NL_FORMAT,
]

WRITERS = {
    OBO_FORMAT: StreamingOboWriter,
    RDF_FORMAT: StreamingRdfWriter,
    OWLFUN_FORMAT: StreamingOwlFunctionalWriter,
    MD_FORMAT: StreamingMarkdownWriter,
    HTML_FORMAT: HTMLWriter,
    OBOJSON_FORMAT: StreamingOboJsonWriter,
    CSV_FORMAT: StreamingCsvWriter,
    TSV_FORMAT: StreamingCsvWriter,
    JSON_FORMAT: StreamingJsonWriter,
    JSONL_FORMAT: StreamingJsonLinesWriter,
    YAML_FORMAT: StreamingYamlWriter,
    SSSOM_FORMAT: StreamingSssomWriter,
    FHIR_JSON_FORMAT: StreamingFHIRWriter,
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


# TODO: use contexts. See https://stackoverflow.com/questions/64381222/python-click-access-option-values-globally
settings = Settings()


def clear_cli_settings():
    for k in settings.__dict__:
        setattr(settings, k, None)


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
    default=True,
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
has_prefix_option = click.option(
    "--has-prefix", "-P", multiple=True, help="filter based on a prefix, e.g. OBI"
)
additional_metadata_option = click.option(
    "--additional-metadata/--no-additional-metadata",
    default=False,
    show_default=True,
    help="if true then fetch additional metadata about statements stored as OWL reification",
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
predicates_option = click.option(
    "-p",
    "--predicates",
    help="A comma-separated list of predicates. This may be a shorthand (i, p) or CURIE",
)
exclude_predicates_option = click.option(
    "--exclude-predicates", help="A comma-separated list of predicates to exclude"
)
graph_traversal_method_option = click.option(
    "-M",
    "--graph-traversal-method",
    type=click.Choice([v.value for v in GraphTraversalMethod]),
    help="Whether formal entailment or graph walking should be used.",
)
display_option = click.option(
    "-D",
    "--display",
    default="",
    help="A comma-separated list of display options. Use 'all' for all",
)
stylemap_option = click.option(
    "-S",
    "--stylemap",
    help="a json file to configure visualization. See https://berkeleybop.github.io/kgviz-model/",
)
stylemap_configure_option = click.option(
    "-C",
    "--configure",
    help='overrides for stylemap, specified as yaml. E.g. `-C "styles: [filled, rounded]" `',
)
configuration_file_option = click.option(
    "-C",
    "--configuration-file",
    help="Path to a configuration file. This is typically a YAML file, but may be a JSON file",
)
adapter_mapping_option = click.option(
    "--adapter-mapping",
    multiple=True,
    help="Multiple prefix=selector pairs, e.g. --adapter-mapping uberon=db/uberon.db",
)
pivot_languages = click.option(
    "--pivot-languages/--no-pivot-languages",
    help="include one column per language",
)
all_languages = click.option(
    "--all-languages/--no-all-languages",
    help="if source is multi-lingual, show all languages rather than just default",
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
    w.settings = settings
    return w


def _apply_changes(impl, changes: List[kgcl.Change]):
    if changes:
        logging.info(f"Applying {len(changes)} changes")
        if not isinstance(impl, PatcherInterface):
            raise NotImplementedError(f"Cannot apply {len(changes)} changes")
        for change in changes:
            impl.apply_patch(change)
        impl.save()


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet/--no-quiet")
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
    show_default=True,
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
@click.option(
    "--preferred-language", "-l", help="Preferred language for labels and lexical elements"
)
@click.option(
    "--other-languages", multiple=True, help="Additional languages for labels and lexical elements"
)
@click.option(
    "--requests-cache-db",
    help="If specified, all http requests will be cached to this sqlite file",
)
@click.option(
    "--wrap-adapter",
    "-W",
    help="Wrap the input adapter using another adapter (e.g. llm or semsimian).",
)
@input_option
@input_type_option
@add_option
@click.option(
    "--merge/--no-merge",
    default=False,
    show_default=True,
    help="Merge all inputs specified using --add",
)
@click.option(
    "--profile/--no-profile",
    default=False,
    show_default=True,
    help="If set, will profile the command",
)
@click.option(
    "--caching",
    type=CachePolicy.ClickType,
    help="Set the cache management policy",
)
def main(
    verbose: int,
    quiet: bool,
    stacktrace: bool,
    input: str,
    wrap_adapter: str,
    input_type: str,
    add: List,
    merge: bool,
    associations: List,
    associations_type: str,
    save_as: str,
    autosave: bool,
    named_prefix_map,
    metamodel_mappings,
    requests_cache_db,
    prefix,
    profile: bool,
    import_depth: Optional[int],
    caching: Optional[CachePolicy],
    **kwargs,
):
    """
    Run the oaklib Command Line.

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
    if profile:
        import atexit
        import cProfile
        import io
        import pstats

        print("Profiling...")
        pr = cProfile.Profile()
        pr.enable()

        def exit():
            pr.disable()
            print("Profiling completed")
            s = io.StringIO()
            pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats()
            print(s.getvalue())

        atexit.register(exit)
    if requests_cache_db:
        import requests_cache

        requests_cache.install_cache(requests_cache_db)
    FILE_CACHE.force_policy(caching)
    resource = OntologyResource()
    resource.slug = input
    settings.autosave = autosave
    for k, v in kwargs.items():
        if v is not None:
            logging.info(f"Setting {k}={v}")
            setattr(settings, k, v)
    logging.info(f"Settings = {settings}")
    if input:
        if wrap_adapter:
            input = wrap_adapter + ":" + input
        settings.impl = get_adapter(input)
        settings.impl.autosave = autosave
    if merge and not add:
        raise ValueError("Cannot use --merge without --add")
    if add:
        impls = [get_adapter(d) for d in add]
        if merge:
            if isinstance(settings.impl, MergeInterface):
                settings.impl.merge(impls)
            else:
                raise NotImplementedError(f"{type(settings.impl)} does not implement merging")
        else:
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
        logging.info(f"Using {len(msd.mapping_set.mappings)} metamodel mappings")
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
@autolabel_option
@output_option
def search(terms, output_type: str, autolabel, output: TextIO):
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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/search

    Data model:

       https://w3id.org/oak/search

    .. warning::

       The behavior of search is not yet fully unified across endpoints

    .. warning::

       The behavior of search is not yet fully unified across endpoints

    """
    impl = settings.impl
    if isinstance(impl, SearchInterface):
        writer = _get_writer(output_type, impl, StreamingInfoWriter)
        writer.output = output
        if autolabel:
            for curie_it in chunk(query_terms_iterator(terms, impl)):
                logging.info("** Next chunk:")
                # TODO: move chunking logic to writer
                for curie, label in impl.labels(curie_it):
                    writer.emit(dict(id=curie, label=label))
        else:
            for curie in query_terms_iterator(terms, impl):
                writer.emit(dict(id=curie), label_fields=[])
        writer.finish()
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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    See Also:
    -
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
@click.option(
    "--show-migration-relationships/--no-show-migration-relationships",
    default=False,
    show_default=True,
    help="Show migration relationships (e.g. replaced_by, consider)",
)
@ontological_output_type_option
@output_option
@click.argument("terms", nargs=-1)
def obsoletes(
    terms, include_merged: bool, show_migration_relationships: bool, output_type: str, output: str
):
    """
    Shows all obsolete entities.

    Example:

        runoak -i obolibrary:go.obo obsoletes

    To exclude *merged terms*, use the ``--no-include-merged`` flag

    Example:

        runoak -i obolibrary:go.obo obsoletes --no-include-merged

    To show migration relationships, use the ``--show-migration-relationships`` flag

    Example:

        runoak -i obolibrary:go.obo obsoletes --show-migration-relationships

    You can also specify terms to show obsoletes for:

    Example:

        runoak -i obolibrary:go.obo obsoletes --show-migration-relationships GO:0000187 GO:0000188

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Obsoletes.ipynb

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    if show_migration_relationships and isinstance(writer, StreamingInfoWriter):
        raise ValueError("Cannot show migration relationships with info output")
    writer.output = output
    if terms:
        term_iterator = query_terms_iterator(terms, impl)
    else:
        term_iterator = impl.obsoletes(include_merged=include_merged)
    if isinstance(impl, BasicOntologyInterface):
        for chunk_iterator in chunk(term_iterator):
            curies = list(chunk_iterator)
            logging.debug(f"Processing chunk of {len(curies)}")
            objs = {}
            for curie, label in impl.labels(curies):
                objs[curie] = dict(id=curie, label=label)
            if show_migration_relationships:
                for obj in objs.values():
                    for p in OBSOLETION_RELATIONSHIP_PREDICATES:
                        obj[p] = []
                for curie, rel, filler in impl.obsoletes_migration_relationships(curies):
                    objs[curie][rel].append(filler)
            for obj in objs.values():
                writer.emit(obj)
        writer.finish()
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
@click.option(
    "--compare-with",
    "-X",
    help="Compare with another ontology",
)
@has_prefix_option
@output_option
@click.argument("branches", nargs=-1)
def statistics(
    branches,
    group_by_property,
    group_by_obo_namespace: bool,
    group_by_defined_by: bool,
    group_by_prefix: bool,
    include_residuals: bool,
    has_prefix: str,
    compare_with: str,
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

    - by prefix (e.g. GO, PR, CL, OBI)

    Example:

        runoak -i sqlite:obo:pr statistics -p oio:hasOBONamespace

    Note: the oio:hasOBONamespace is *not* the same as the ID prefix, it is
    a field that is used by a subset of ontologies to partition classes into
    broad groupings, similar to subsets. Its use is non-standard, yet a lot
    of ontologies use this as the main partitioning mechanism.

    A note on bundled ontologies:

    The standard release many OBO ontologies "bundles" parts of other ontologies
    (formally, the release product includes a merged imports closure of import
    modules). This can complicate generation of statistics. A naive count of
    all classes in the main OBI release will include not only "native" OBI classes,
    but also classes from other ontologies that are bundled in the release.

    For bundled ontologies, we recommend some kind of partitioning, such as via
    defined roots, or via the CURIE prefix, using the ``--group-by-prefix`` option.

    Output formats:

    The recommended output types for this command are yaml, json, or csv.
    The default output type is yaml, following the SummaryStatistics data model.
    This is naturally nested, as the statistics includes faceted groupings
    (e.g. edge counts are broken down by predicate). When specifying a flat
    format like csv, this is flattened into a single table, with dynamic
    column names.

    Change statistics:

    You can optionally combine the ontology statistics with a change
    summary relative to another ontology, using the ``--compare-with``
    option.

    Example:

        runoak -i v2.obo statistics --group-by-obo-namespace --compare-with v1.obo

    This will also include change stats broken down by KGCL change types. If
    a group-by option is specified, these will be grouped accordingly.

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/summary-statistics

    Data model:

       https://w3id.org/oak/summary-statistics

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.heterogeneous_keys = True
    diff_config = DiffConfiguration(simple=False)
    if not isinstance(impl, SummaryStatisticsInterface):
        raise NotImplementedError(f"Cannot execute this using {type(impl)}")
    impl.include_residuals = include_residuals
    prefixes = list(has_prefix) if has_prefix else None
    if group_by_obo_namespace:
        group_by_property = HAS_OBO_NAMESPACE
        diff_config.group_by_property = HAS_OBO_NAMESPACE
    if group_by_defined_by:
        group_by_property = IS_DEFINED_BY
        diff_config.group_by_property = IS_DEFINED_BY
    if group_by_prefix:
        group_by_property = PREFIX_PREDICATE
        diff_config.group_by_property = PREFIX_PREDICATE
    diff_stats = None
    if compare_with:
        if branches:
            raise click.UsageError("Cannot specify both branches and compare_with")
        if not isinstance(impl, DifferInterface):
            raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
        other = get_adapter(compare_with)
        logging.info(f"Comparing {impl} with {other} using {diff_config}")
        diff_stats = impl.diff_summary(other, configuration=diff_config)
    if not branches and not group_by_property:
        ssc = impl.branch_summary_statistics(prefixes=prefixes)
    else:
        if branches and group_by_property:
            raise click.UsageError("Cannot specify both branches and predicates")
        if branches:
            branches = list(query_terms_iterator(branches, impl))
            ssc = impl.global_summary_statistics(
                branches={impl.label(b): [b] for b in branches}, prefixes=prefixes
            )
        else:
            ssc = impl.global_summary_statistics(group_by=group_by_property, prefixes=prefixes)
    if diff_stats:
        logging.info("Integrating diff stats")
        for k, v in diff_stats.items():
            if isinstance(ssc, GroupedStatistics):
                if k not in ssc.partitions:
                    if k != RESIDUAL_KEY:
                        raise RuntimeError(f"Unexpected grouping {k}")
                    continue
                ssc.partitions[k].change_summary = v
            else:
                if not isinstance(ssc, UngroupedStatistics):
                    raise RuntimeError(f"Unexpected type {type(ssc)}")
                if k != RESIDUAL_KEY:
                    raise RuntimeError(f"Unexpected key {k}")
                ssc.change_summary = v
    if isinstance(writer, StreamingCsvWriter) and isinstance(ssc, GroupedStatistics):
        # special purpose behavior for global stats and TSV writing;
        # write one block per partition
        for p in ssc.partitions.values():
            writer.emit(p)
    else:
        writer.emit(ssc)
    writer.finish()


@main.command()
@output_option
def ontologies(output: str):
    """
    Shows all ontologies

    If the input is a pre-merged ontology, then the output of this command is trivially
    a single line, with the name of the input ontology

    This command is more meaningful when the input is a multi-ontology endpoint, e.g

        runoak -i ubergraph: ontologies

    Or

        runoak -i bioportal: ontologies

    In future this command will be expanded to allow showing more metadata about each ontology

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic
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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    impl = settings.impl
    if output_type is None or output_type == "yaml":
        writer = StreamingYamlWriter(output)
    elif output_type == "csv":
        writer = StreamingCsvWriter(output)
    elif output_type == "md":
        writer = OboFoundryMarkdownWriter(output)
    else:
        raise ValueError(f"No such format: {output_type}")
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if len(ontologies) == 0:
        if all:
            ontologies = list(impl.ontologies())
        else:
            raise ValueError("Must pass one or more ontologies OR --all")
    else:
        if all:
            raise ValueError("--all should not be used in combination with an explicit list")
    for ont in list(ontologies):
        logging.info(f"Looking up {ont}")
        metadata = impl.ontology_metadata_map(ont)
        writer.emit(metadata)


@main.command()
@output_option
@output_type_option
@predicates_option
@additional_metadata_option
@click.argument("terms", nargs=-1)
def term_metadata(terms, predicates, additional_metadata: bool, output_type: str, output: str):
    """
    Shows term metadata.

    Example:

        runoak -i sqlite:obo:uberon term-metadata lung heart

    You can filter the results for only selected predicates:

        runoak -i sqlite:obo:uberon term-metadata lung heart -p id,oio:hasDbXref

    The default output is YAML documents, where each YAML document is a term, with
    keys representing selected predicates. Values are always lists of atoms, even
    when there is typically one value (e.g. rdfs:label)

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    Data model:

       https://w3id.org/oak/ontology-metadata

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    if isinstance(impl, BasicOntologyInterface):
        for curie in query_terms_iterator(terms, impl):
            if additional_metadata:
                if isinstance(impl, MetadataInterface):
                    for ax in impl.statements_with_annotations(curie):
                        writer.emit(ax)
                else:
                    raise NotImplementedError
            else:
                metadata = impl.entity_metadata_map(curie)
                if predicates:
                    metadata = {
                        p: metadata.get(p, None) for p in process_predicates_arg(predicates)
                    }
                writer.emit(metadata)
        writer.finish()
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
    "--include-aliases/--no-include-aliases",
    default=False,
    show_default=True,
    help="Include alias maps in output.",
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
    "--match-column",
    "-A",
    help="name of column to match on (if the input is tsv/csv)",
)
@click.option(
    "--model",
    "-m",
    required=False,
    help="Name of trained model to use for annotation, e.g. 'en_ner_craft_md'.",
)
@click.option(
    "--exclude-tokens",
    "-x",
    multiple=True,
    help="Text file or list of tokens to filter from input prior to annotation.\
        If passed as text file, each newline separated entry is a distinct text.",
)
@click.option(
    "--rules-file",
    "-R",
    help="path to rules file. Conforms to https://w3id.org/oak/mapping-rules",
)
@click.option(
    "--configuration-file",
    "-C",
    help="path to config file. Conforms to https://w3id.org/oak/text-annotator",
)
@click.option(
    "--category",
    multiple=True,
    help="Categories of entities to annotate. If not specified, all categories are annotated.",
)
@output_option
@output_type_option
def annotate(
    words,
    output: str,
    lexical_index_file: str,
    matches_whole_text: bool,
    include_aliases: bool,
    exclude_tokens: str,
    rules_file: str,
    configuration_file: str,
    category: str,
    text_file: TextIO,
    match_column: str,
    model: str,
    output_type: str,
):
    """
    Annotate a piece of text using a Named Entity Recognition annotation.

    Some endpoints such as BioPortal have built-in support for annotation;
    in these cases the endpoint functionality is used:

    Example:

        runoak -i bioportal: annotate "enlarged nucleus in T-cells from peripheral blood"

    For other endpoints, the built-in OAK annotator is used. This currently uses a basic
    algorithm based on lexical matching.

    Example:

        runoak -i sqlite:obo:cl annotate "enlarged nucleus in T-cells from peripheral blood"

    Using the builtin annotator can be slow, as the lexical index is re-built every time.
    To preserve this, use the ``--lexical-index-file`` (``-L``) option to specify a file to save.
    On subsequent iterations the file is reused.

    You can also use ``--text-file`` to pass in a text file to be parsed one line at a time

    If gilda is installed as an extra, it can be used,
    but ``--matches-whole-text`` (``-W``) must be specified,
    as gilda only performs grounding.

    Example:

        runoak -i gilda: annotate -W BRCA2

    Aliases can be listed in the output by setting the flag
    --include-aliases to `true` (default: false).

    Example (using the plugin oakx-spacy):

        runoak -i spacy:sqlite:obo:bero annotate Myeloid derived suppressor cells. --include-aliases

    will yield:

        confidence: 0.8
        object_aliases:
        - Myeloid-Derived Suppressor Cells
        - MDSCs
        - mdscs
        - myeloid-derived suppressor cells
        object_id: obo:MESH_D000072737
        object_label: Myeloid-Derived Suppressor Cells
        subject_end: 30
        subject_start: 0

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/text-annotator

    Data model:

       https://w3id.org/oak/text-annotator

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.text_annotator)
    writer.output = output
    if not isinstance(impl, TextAnnotatorInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if rules_file:
        impl.rule_collection = load_mapping_rules(rules_file)
    if lexical_index_file:
        if not Path(lexical_index_file).exists():
            logging.info(f"Creating new index: {lexical_index_file}")
            impl.lexical_index = create_lexical_index(impl)
            save_lexical_index(impl.lexical_index, lexical_index_file)
        else:
            impl.lexical_index = load_lexical_index(lexical_index_file)
    if configuration_file:
        configuration = yaml_loader.load(configuration_file, TextAnnotationConfiguration)
    else:
        configuration = TextAnnotationConfiguration(matches_whole_text=matches_whole_text)
    if exclude_tokens:
        token_exclusion_list = get_exclusion_token_list(exclude_tokens)
        configuration.token_exclusion_list = token_exclusion_list
    if model:
        configuration.model = model
    configuration.include_aliases = include_aliases
    if category:
        configuration.categories = list(category)
    # if plugin_config:
    #     with open(plugin_config, "r") as p:
    #         configuration.plugin_configuration = yaml.safe_load(p)
    if words and text_file:
        raise ValueError("Specify EITHER text-file OR a list of words as arguments")
    if text_file:
        if match_column:
            writer = _get_writer(output_type, impl, StreamingCsvWriter)
            writer.output = output
            for row in impl.annotate_tabular_file(
                text_file, configuration=configuration, match_column=match_column
            ):
                writer.emit(row)
        else:
            for ann in impl.annotate_file(text_file, configuration):
                writer.emit(ann)
    else:
        logging.info(f"Annotating: {words}")
        for ann in impl.annotate_text(" ".join(list(words)), configuration):
            writer.emit(ann)
    writer.finish()


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
@stylemap_option
@stylemap_configure_option
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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/obograph

    Data model:

       https://w3id.org/oak/obograph

    """
    impl = settings.impl
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    impl.precompute_lookups()
    if stylemap is None:
        stylemap = default_stylemap_path()
    actual_predicates = process_predicates_arg(predicates)
    curies_highlight = None
    if "@" in terms:
        ix = terms.index("@")
        terms_highlight = terms[0:ix]
        terms = terms[ix + 1 :]
        curies_highlight = list(query_terms_iterator(terms_highlight, impl))
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
        graph = impl.subgraph_from_traversal(curies, predicates=actual_predicates)
    elif gap_fill:
        logging.info("Using gap-fill strategy")
        if isinstance(impl, SubsetterInterface):
            graph = impl.extract_gap_filled_graph(curies, predicates=actual_predicates)
        else:
            raise NotImplementedError(f"{impl} needs to implement Subsetter for --gap-fill")
    else:
        graph = impl.ancestor_graph(curies, predicates=actual_predicates)
    if max_hops is not None:
        logging.info(f"Trimming graph, max_hops={max_hops}")
        graph = trim_graph(graph, curies, distance=max_hops, include_intermediates=True)
    logging.info(f"Drawing graph seeded from {len(curies)} curies: {curies}")
    if meta:
        impl.add_metadata(graph)
    if not graph.nodes:
        raise ValueError(f"No nodes in graph for {curies}")
    if curies_highlight is None:
        curies_highlight = curies
    # TODO: abstract this out
    if not output_type or output_type in ["png", "svg", "dot"]:
        graph_to_image(
            graph,
            seeds=curies_highlight,
            stylemap=stylemap,
            configure=configure,
            imgfile=output,
            view=view,
            format=output_type,
        )
    else:
        # non-visual format
        write_graph(graph, format=output_type, output=output)


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
@display_option
@predicates_option
@output_type_option
@output_option
@click.argument("terms", nargs=-1)
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
    display,
    output_type: str,
    output: TextIO,
):
    """
    Display an ancestor graph as an ascii/markdown tree.

    For general instructions, see the viz command, which this is analogous too.

    Example:

        runoak -i envo.db tree ENVO:00000372 -p i,p

    This produces output like:

    .packages::

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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/obograph

    Data model:

       https://w3id.org/oak/obograph

    """
    impl = settings.impl
    if configure:
        logging.warning("Configure is not yet supported")
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    curies = list(query_terms_iterator(terms, impl))
    if stylemap is None:
        stylemap = default_stylemap_path()
    actual_predicates = process_predicates_arg(predicates)
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
        graph = impl.subgraph_from_traversal(curies, predicates=actual_predicates)
    elif gap_fill:
        logging.info("Using gap-fill strategy")
        if isinstance(impl, SubsetterInterface):
            rels = impl.gap_fill_relationships(curies, predicates=actual_predicates)
            if isinstance(impl, OboGraphInterface):
                graph = impl.relationships_to_graph(rels)
            else:
                raise AssertionError(f"{impl} needs to be of type OboGraphInterface")
        else:
            raise NotImplementedError(f"{impl} needs to implement Subsetter for --gap-fill")
    else:
        graph = impl.ancestor_graph(curies, predicates=actual_predicates)
    logging.info(
        f"Drawing graph with {len(graph.nodes)} nodes seeded from {curies} // {output_type}"
    )
    if max_hops is not None:
        graph = trim_graph(graph, curies, distance=max_hops)
    if output_type in ["d3viz", "d3viz_relational"]:
        trees = graph_to_d3viz_objects(
            graph,
            predicates=actual_predicates,
            start_curies=list(root) if root else None,
            relations_as_nodes=output_type == "d3viz_relational",
            max_paths=None,
        )
        json_dump = json.dumps(trees, indent=2)
        output.write(json_dump)
    else:
        graph_to_tree_display(
            graph,
            seeds=curies,
            predicates=actual_predicates,
            start_curies=list(root) if root else None,
            skip=list(skip) if skip else None,
            format=output_type,
            stylemap=stylemap,
            display_options=display.split(","),
            output=output,
        )


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@graph_traversal_method_option
@output_type_option
@click.option(
    "--statistics/--no-statistics",
    default=False,
    show_default=True,
    help="For each ancestor, show statistics.",
)
@output_option
def ancestors(
    terms, predicates, statistics: bool, graph_traversal_method: str, output_type: str, output: str
):
    """
    List all ancestors of a given term or terms.

    Here ancestor means the transitive closure of the parent relationship, where
    a parent includes all relationship types, not just is-a.

    Example:

        runoak -i cl.owl ancestors CL:4023094

    This will show ancestry over the full relationship graph. Like any relational
    OAK command, this can be filtered by relationship type (predicate), using --predicate (-p).
    For example, constrained to is-a and part-of:

        runoak -i cl.owl ancestors CL:4023094 -p i,BFO:0000050

    Multiple backends can be used, including ubergraph:

        runoak -i ubergraph: ancestors CL:4023094 -p i,BFO:0000050

    Search terms can also be used:

        runoak -i cl.owl ancestors 'goblet cell'

    Multiple terms can be passed:

        runoak -i sqlite:go.db ancestors GO:0005773 GO:0005737 -p i,p

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/obograph

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    # writer.display_options = display.split(',')
    writer.file = output
    if isinstance(impl, OboGraphInterface) and isinstance(impl, SearchInterface):
        if graph_traversal_method:
            graph_traversal_method = GraphTraversalMethod[graph_traversal_method]
            if graph_traversal_method == GraphTraversalMethod.HOP:
                impl.precompute_lookups()
        actual_predicates = process_predicates_arg(predicates)
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
                ancs = list(
                    impl.ancestors(curies, actual_predicates, method=graph_traversal_method)
                )
                for a_curie, a_label in impl.labels(ancs):
                    writer.emit(dict(id=a_curie, label=a_label))
            else:
                raise NotImplementedError
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    writer.finish()


@main.command()
@click.argument("terms", nargs=-1)
@click.option("--target", multiple=True, help="end point of path")
@click.option(
    "--narrow/--no-narrow",
    default=False,
    show_default=True,
    help="If true then output path is written a list of terms",
)
@click.option(
    "--viz/--no-viz",
    default=False,
    show_default=True,
    help="If true then generate a path graph from output",
)
@autolabel_option
@predicates_option
@exclude_predicates_option
@output_type_option
@click.option(
    "--directed/--no-directed", default=False, show_default=True, help="only show directed paths"
)
@click.option(
    "--include-predicates/--no-include-predicates",
    default=False,
    show_default=True,
    help="show predicates between nodes",
)
@click.option(
    "--predicate-weights",
    help="key-value pairs specified in YAML where keys are predicates or shorthands and values are weights",
)
@stylemap_option
@stylemap_configure_option
@click.option("-o", "--output", help="Path to output file")
def paths(
    terms,
    predicates,
    predicate_weights,
    autolabel: bool,
    narrow: bool,
    viz: bool,
    directed: bool,
    include_predicates: bool,
    exclude_predicates: str,
    target,
    stylemap,
    configure,
    output_type: str,
    output: str,
):
    """
    List all paths between one or more start curies.

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane'

    This shows all shortest paths from nuclear membrane to all ancestors

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' --target cytoplasm

    This shows shortest paths between two nodes

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' 'thylakoid' --target cytoplasm 'thylakoid membrane'

    This shows all shortest paths between 4 combinations of starts and ends

    You can also use "@" to separate start node list and end node list. Like most OAK commands,
    you can pass either explicit terms, or term queries. For example, if you have two files of IDs,
    then you can do this:

        runoak -i sqlite:obo:go paths  -p i,p .idfile START_NODES.txt @ .idfile END_NODES.txt

    You can also pass in weights for each predicate, used when calculating shortest paths.

    Example:

        runoak -i sqlite:obo:go paths  -p i,p 'nuclear membrane' --target cytoplasm \
                --predicate-weights "{i: 0.0001, p: 999}"

    This shows all shortest paths after weighting relations

    (Note: you can use the same shorthands as in the `--predicates` option)

    This command can be combined with others to visualize the paths.

    Example:

        alias go="runoak -i sqlite:obo:go"
        go paths  -p i,p 'nuclear membrane' --target cytoplasm --narrow | go viz --fill-gaps -

    This visualizes the path by first exporting the path as a flat list, then passing the
    results to viz, using the fill-gaps option.

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Paths.ipynb

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    if output:
        writer.file = output
    else:
        writer.file = sys.stdout
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(
        predicates, exclude_predicates_str=exclude_predicates, impl=impl
    )
    logging.info(f"Using predicates {actual_predicates}")
    if predicate_weights:
        pw = {}
        for k, v in yaml.safe_load(predicate_weights).items():
            [p] = process_predicates_arg(k, expected_number=1)
            pw[k] = v
    else:
        pw = None
    if "@" in terms:
        if target:
            raise ValueError("Cannot use @ and --target together")
        ix = terms.index("@")
        logging.info(f"Splitting terms {terms} on {ix}")
        start_curies = list(query_terms_iterator(terms[0:ix], impl))
        end_curies = list(query_terms_iterator(terms[ix + 1 :], impl))
        all_curies = start_curies + end_curies
    else:
        start_curies = list(query_terms_iterator(terms, impl))
        if target:
            logging.info(f"Using explicit target list: {target}")
            end_curies = list(list(query_terms_iterator(list(target), impl)))
            all_curies = start_curies + end_curies
        else:
            end_curies = None
            all_curies = start_curies
            logging.info("Will search all ancestors")
    logging.info(f"Start curies: {start_curies}")
    logging.info(f"End curies: {end_curies}")
    # TODO: move the logic from CLI to OboGraphInterface
    impl.precompute_lookups()
    graph = impl.ancestor_graph(all_curies, predicates=actual_predicates)
    logging.info("Calculating graph stats")
    path_graph = Graph(id="paths")
    node_ids = set()
    path_id = 0
    for s, o, path in shortest_paths(
        graph,
        start_curies,
        end_curies=end_curies,
        predicate_weights=pw,
        directed=directed,
    ):
        path_id += 1
        if include_predicates:
            new_path = []
            last_n = None
            for n in path:
                node_ids.add(n)
                if last_n is not None:
                    path_graph.edges.append(
                        Edge(
                            sub=last_n,
                            pred=f"{path_id}",
                            obj=n,
                            meta=Meta(
                                subsets=["path"],
                                basicPropertyValues=[
                                    BasicPropertyValue(
                                        pred="https://w3id.org/kgviz/color", val="grey"
                                    ),
                                    BasicPropertyValue(
                                        pred="https://w3id.org/kgviz/fontcolor", val="grey"
                                    ),
                                ],
                            ),
                        )
                    )
                    rels = [p for _s, p, _o in impl.relationships(subjects=[last_n], objects=[n])]
                    for rel in rels:
                        path_graph.edges.append(Edge(sub=last_n, pred=rel, obj=n))
                    if not rels and not directed:
                        rels = [
                            p for _s, p, _o in impl.relationships(subjects=[n], objects=[last_n])
                        ]
                        for rel in rels:
                            path_graph.edges.append(Edge(sub=n, pred=rel, obj=last_n))
                        rels = [f"^{rel}" for rel in rels]
                    new_path.append(rels[0] if rels else "?")
                last_n = n
                new_path.append(n)
            path = new_path
        if narrow:
            for path_node in path:
                writer.emit(
                    dict(subject=s, object=o, path_node=path_node),
                    label_fields=["subject", "object", "path_node"],
                )
        elif not viz:
            writer.emit(
                dict(subject=s, object=o, path=path),
                label_fields=["subject", "object", "path"],
            )
        writer.finish()
    if not node_ids:
        logging.warning("No paths found")
    if viz:
        for node_id in node_ids.union({e.pred for e in graph.edges}):
            [n] = [n for n in graph.nodes if n.id == node_id]
            path_graph.nodes.append(n)
        # TODO: abstract this out
        if output_type:
            write_graph(path_graph, format=output_type, output=output)
        else:
            if stylemap is None:
                stylemap = default_stylemap_path()
            graph_to_image(
                path_graph,
                seeds=all_curies,
                imgfile=output,
                stylemap=stylemap,
                configure=configure,
                view=viz,
            )


@main.command()
@click.argument("terms", nargs=-1)
@autolabel_option
@output_type_option
@click.option("-o", "--output", help="Path to output file")
def chains(
    terms,
    autolabel: bool,
    output_type: str,
    output: str,
):
    """
    List all paths following a query template.

    (Experimental)

    Assume we have aliased `cl` to `runoak -i sqlite:obo:cl`:

    All chains of is-a followed by develops from:

        cl chains /rdfs:subClassOf /RO:0002202

    Or using predicate shorthand:

        cl chains /i /d

    As above, but ending with "stem cell"

        cl chains /i /d "stem cell"

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    if output:
        writer.file = output
    else:
        writer.file = sys.stdout
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    # list(query_terms_iterator(terms[0:ix], impl))
    blocks = [[]]
    for t in terms:
        if t.startswith("/"):
            preds = t[1:]
            if t.endswith("/"):
                preds = t[0:-1]
            actual_preds = process_predicates_arg(preds, impl=impl) if preds else None
            blocks.append(set(actual_preds or []))
            blocks.append([])
        else:
            blocks[-1].append(t)
    logging.info(f"Blocks: {blocks}")
    query = []
    et = EdgeTemplate()
    for block in blocks:
        if isinstance(block, set):
            if et.predicates is not None:
                query.append(et)
                et = EdgeTemplate()
            if "{inverted}" in block:
                et.inverted = True
                block.remove("{inverted}")
            if "{entailed}" in block:
                et.entailed = True
                block.remove("{entailed}")
            if any([x.startswith("{") for x in block]):
                raise ValueError(f"Unrecognized directive: {block}")
            et.predicates = block
        else:
            terms = list(query_terms_iterator(list(block), impl))
            if et.predicates is None:
                et.subject_nodes = terms
            else:
                et.object_nodes = terms
    if et.predicates is not None:
        query.append(et)
    for this_chain in impl.chains(query):
        obj = {}
        for i, e in enumerate(this_chain):
            for k in ["sub", "pred", "obj"]:
                unrolled_k = f"{k}_{i+1}"
                obj[unrolled_k] = getattr(e, k)
                if autolabel:
                    label_k = f"{k}_label_{i+1}"
                    obj[label_k] = impl.label(getattr(e, k)) or ""
        writer.emit(obj)


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
        actual_predicates = process_predicates_arg(predicates)
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
        writer.finish()
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@graph_traversal_method_option
@display_option
@output_type_option
@output_option
def descendants(
    terms, predicates, graph_traversal_method, display: str, output_type: str, output: TextIO
):
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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/obograph

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingInfoWriter)
    writer.display_options = display.split(",")
    writer.file = output
    if graph_traversal_method:
        graph_traversal_method = GraphTraversalMethod[graph_traversal_method]
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(predicates)
    curies = list(query_terms_iterator(terms, impl))
    result_it = impl.descendants(
        curies, predicates=actual_predicates, method=graph_traversal_method
    )
    writer.emit_multiple(result_it)
    writer.finish()


@main.command()
@click.argument("terms", nargs=-1)
@click.option("-o", "--output", help="Path to output file")
@output_type_option
@click.option(
    "-c",
    "--config-file",
    help="""Config file for additional params. Presently used by  `fhirjson` only.""",
)
@click.option(
    "--enforce-canonical-ordering/--no-enforce-canonical-ordering",
    default=False,
    show_default=True,
    help="Forces the serialization to be in canonical order, which is useful for diffing",
)
def dump(terms, output, output_type: str, config_file: str = None, **kwargs):
    """
    Exports (dumps) the entire contents of an ontology.

    Example:

        runoak -i pato.obo dump -o pato.json -O json

    Example:

        runoak -i pato.owl dump -o pato.ttl -O turtle

    You can also pass in a JSON configuration file to parameterize the dump process.

    Currently this is only used for fhirjson dumps, the configuration options are specified here:

    https://incatools.github.io/ontology-access-kit/converters/obo-graph-to-fhir.html

    Example:

        runoak -i pato.owl dump -o pato.ttl -O fhirjson -c fhir_config.json -o pato.fhir.json

    Currently each implementation only supports a subset of formats.

    The dump command is also blocked for remote endpoints such as Ubergraph,
    to avoid killer queries.

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    if terms:
        raise NotImplementedError("Currently dump for a subset of terms is not supported")
    impl = settings.impl
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError
    logging.info(f"Out={output} syntax={output_type}")
    if config_file:
        with open(config_file) as file:
            kwargs |= json.load(file)
    impl.dump(output, syntax=output_type, **kwargs)


@main.command()
@click.argument("terms", nargs=-1)
@click.option("-o", "--output", help="Path to output file")
@output_type_option
@click.option(
    "-c",
    "--config-file",
    help="""Config file for additional transform params.""",
)
@click.option(
    "-t",
    "--transform",
    required=True,
    help="""Name of transformation to apply.""",
)
def transform(terms, transform, output, output_type: str, config_file: str = None, **kwargs):
    """
    Applies a defined transformation to an ontology (EXPERIMENTAL).

    Transformations include:

    - SEPTransform: implements Structured-Entities-Parts (SEP) design pattern
    - EdgeFilterTransformer: filters edges based on a predicate

    Note that for most transformation operations, we recommend using ROBOT
    and commands such as remove, filter, query.

    Example:

        runoak -i xao.obo transform -t SEPTransform -o xao.sep.obo

    Removes all P part-of Ws from XAO and replaces occurrences with triads of the form:

    - W subClassOf W-structure
    - W subClassOf W-structure
    - W-Part subClassOf W-structure
    - P subClassOf W-Part

    """
    if terms:
        raise NotImplementedError("Currently transform for a subset of terms is not supported")
    impl = settings.impl
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError
    logging.info(f"Out={output} syntax={output_type}")
    if config_file:
        with open(config_file) as file:
            kwargs |= yaml.safe_load(file)
    transformer = get_ontology_transformer(transform, **kwargs)
    new_impl = apply_ontology_transformation(impl, transformer)
    new_impl.dump(output, syntax=output_type)


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
@click.option("-o", "--output", help="Path to output file")
@click.option(
    "--dangling/--no-dangling",
    default=False,
    show_default=True,
    help="If True, allow dangling edges in the output",
)
@click.option(
    "--include-metadata/--no-include-metadata",
    default=False,
    show_default=True,
    help="If True, include term metadata such as definitions, synonyms",
)
@output_type_option
def extract(terms, predicates, dangling: bool, output, output_type, **kwargs):
    """
    Extracts a sub-ontology.

    Simple example:

        runoak -i cl.db extract neuron

    This will extract a single node for "neuron". No relationships will be included,
    as --no-dangling is the default

    To include edges even if dangling:

        runoak -i cl.db extract neuron --dangling

    A subset of relationship types (predicates):

        runoak -i cl.db extract neuron --dangling -p i

    If you wish to get a fully connected is-a graph for all is-a ancestors:

        runoak -i cl.db extract .anc//p=i neuron --dangling -p i

    If you prefer, you can split this into 2 commands:

        runoak -i cl.db ancestors -p i neuron > seed.txt

    Then:

        runoak -i cl.db extract .idfile seed.txt --dangling -p i

    You can specify different output types and output paths:

        runoak -i cl.db extract .idfile seed.txt -O owl -o neuron.owl.ttl

    Allowed formats include: obo, obographs, owl/ttl, fhirjson

    """
    impl = settings.impl
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(predicates)
    curies = list(set(query_terms_iterator(terms, impl)))
    graph = impl.extract_graph(curies, predicates=actual_predicates, dangling=dangling, **kwargs)
    graph_impl = OboGraphImplementation(obograph_document=GraphDocument(graphs=[graph]))
    if output_type is None:
        output_type = "obo"
    graph_impl.dump(output, output_type)


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

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity

    Data model:

       https://w3id.org/oak/similarity

    """
    if len(terms) != 2:
        raise ValueError(f"Need exactly 2 terms: {terms}")
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    writer.output = output
    subject = list(query_terms_iterator([terms[0]], impl))[0]
    object = list(query_terms_iterator([terms[1]], impl))[0]
    if not isinstance(impl, SemanticSimilarityInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(predicates)
    sim = impl.pairwise_similarity(subject, object, predicates=actual_predicates)
    if autolabel:
        if not sim.subject_label:
            sim.subject_label = impl.label(sim.subject_id)
        if not sim.object_label:
            sim.object_label = impl.label(sim.object_id)
        if not sim.ancestor_label:
            sim.ancestor_label = impl.label(sim.ancestor_id)
    writer.emit(sim)
    writer.finish()


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
    "--min-jaccard-similarity",
    type=float,
    help="Minimum value for jaccard score",
)
@click.option(
    "--min-ancestor-information-content",
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
@click.option(
    "--information-content-file",
    help="File containing information content for each term",
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
    min_jaccard_similarity: Optional[float],
    min_ancestor_information_content: Optional[float],
    main_score_field,
    information_content_file,
    output_type,
    output,
):
    """
    All by all similarity.

    This calculates a similarity matrix for two sets of terms.

    Input sets of a terms can be specified in different ways:

    - via a file
    - via explicit lists of terms or queries

    Example:

        runoak -i hp.db similarity -p i --set1-file HPO-TERMS1 --set2-file HPO-TERMS2 -O csv

    This will compare every term in TERMS1 vs TERMS2

    Alternatively standard OAK term queries can be used, with "@" separating the two lists

    Example:

        runoak -i hp.db similarity -p i TERM_1 TERM_2 ... TERM_N @ TERM_N+1 ... TERM_M

    The .all term syntax can be used to select all terms in an ontology

    Example:

        runoak -i ma.db similarity -p i,p .all @ .all

    This can be mixed with other term selectors; for example to calculate the similarity of "neuron"
    vs all terms in CL:

        runoak -i cl.db similarity -p i,p .all @ neuron

    An example pipeline to do all by all over all phenotypes in HPO:

    Explicit:

        runoak -i hp.db descendants -p i HP:0000118 > HPO

        runoak -i hp.db similarity -p i --set1-file HPO --set2-file HPO -O csv -o RESULTS.tsv

    The same thing can be done more compactly with term queries:

        runoak -i hp.db similarity -p i .desc//p=i HP:0000118 @ .desc//p=i HP:0000118

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity

    Data model:

       https://w3id.org/oak/similarity

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    logging.info(f"out={output} {type(output)}")
    writer.output = output
    logging.info(f"file={writer.file} {type(writer.output)}")
    if main_score_field and isinstance(writer, HeatmapWriter):
        writer.value_field = main_score_field
    if not isinstance(impl, SemanticSimilarityInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if information_content_file:
        impl.load_information_content_scores(information_content_file)
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
    actual_predicates = process_predicates_arg(predicates)
    for sim in impl.all_by_all_pairwise_similarity(
        set1it,
        set2it,
        predicates=actual_predicates,
        min_jaccard_similarity=min_jaccard_similarity,
        min_ancestor_information_content=min_ancestor_information_content,
    ):
        if autolabel:
            # TODO: this can be made more efficient
            sim.subject_label = impl.label(sim.subject_id)
            sim.object_label = impl.label(sim.object_id)
            sim.ancestor_label = impl.label(sim.ancestor_id)
        writer.emit(sim)
    writer.finish()
    writer.file.close()


@main.command()
@predicates_option
@output_option
@output_type_option
@autolabel_option
@click.option(
    "--information-content-file",
    help="File containing information content for each term",
)
@click.argument("terms", nargs=-1)
def termset_similarity(
    terms,
    predicates,
    autolabel,
    output_type,
    information_content_file,
    output: TextIO,
):
    """
    Termset similarity.

    This calculates a similarity matrix for two sets of terms.

    Example:

        runoak -i go.db termset-similarity -p i,p nucleus membrane @ "nuclear membrane" vacuole -p i,p

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/semantic-similarity

    Data model:

       https://w3id.org/oak/similarity

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodels.similarity)
    writer.output = output
    if not isinstance(impl, SemanticSimilarityInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")

    if information_content_file:
        impl.load_information_content_scores(information_content_file)
    terms = list(terms)
    ix = terms.index("@")
    set1 = list(query_terms_iterator(terms[0:ix], impl))
    set2 = list(query_terms_iterator(terms[ix + 1 :], impl))
    logging.info(f"Set1={set1}")
    logging.info(f"Set2={set2}")
    actual_predicates = process_predicates_arg(predicates)
    sim = impl.termset_pairwise_similarity(
        set1, set2, predicates=actual_predicates, labels=autolabel
    )
    writer.emit(sim)
    writer.finish()


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@output_type_option
@predicates_option
@click.option(
    "--use-associations/--no-use-associations",
    default=False,
    show_default=True,
    help="Use associations to calculate IC",
)
def information_content(
    terms,
    predicates,
    output: TextIO,
    output_type: str,
    use_associations: bool,
):
    """
    Show information content for term or list of terms

    Example:

        runoak -i cl.db information-content -p i .all

    Like all OAK commands that operate over graphs, the graph traversal is controlled
    by the `--predicates` option. In the above case, the frequency of each term is equal to
    the number of reflexive is-a descendants of the term divided by total number of terms

    By default, the ontology is used as the corpus for computing term frequency.

    You can use an association file as the corpus:

        runoak -g hpoa.tsv -G hpoa -i hp.db information-content -p i --use-associations .all

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.file = output
    if not isinstance(impl, SemanticSimilarityInterface):
        raise NotImplementedError(f"Cannot execute this with {type(impl)}")
    actual_predicates = process_predicates_arg(predicates)
    n = 0
    logging.info("Fetching ICs...")
    if terms:
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            logging.info("** Next chunk:")
            for curie, ic in impl.information_content_scores(
                curie_it,
                object_closure_predicates=actual_predicates,
                use_associations=use_associations,
            ):
                obj = dict(id=curie, information_content=ic)
                writer.emit(obj)
                n += 1
    else:
        for curie, ic in impl.information_content_scores(
            object_closure_predicates=actual_predicates,
            use_associations=use_associations,
        ):
            obj = dict(id=curie, information_content=ic)
            writer.emit(obj)
            n += 1
    if n == 0:
        raise ValueError(f"No results for input: {terms}")
    writer.finish()


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
    writer.finish()


@main.command()
def languages():
    """
    Show available languages

    Example:

        runoak languages

    """
    impl = settings.impl
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    for lang in impl.languages():
        print(lang + ("*" if lang == settings.preferred_language else ""))


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@ontological_output_type_option
@pivot_languages
@all_languages
@if_absent_option
@set_value_option
def labels(
    terms,
    output: TextIO,
    display: str,
    output_type: str,
    if_absent,
    set_value,
    pivot_languages: bool,
    all_languages: bool,
):
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

    Multilingual support: if the adapter supports multilingual querying
    (currently only SQL) *and* the ontology has multilingual support, you can restrict results to
    a particular language.

    Example:

        runoak --preferred-language fr -i sqlite:obo:hpinternational labels .ancestors HP:0020110

    You can also query for all languages, and see these pivoted:

    Example:

        runoak  -i sqlite:obo:hpinternational labels .ancestors HP:0020110 --pivot-languages

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/labels

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    if len(terms) == 0:
        raise ValueError("You must specify a list of terms. Use '.all' for all terms")
    n = 0
    logging.info(f"Fetching labels; lang={settings.preferred_language}")
    changes = []
    if pivot_languages:
        all_languages = True
        writer.pivot_fields = ["language"]
    for curie_it in chunk(query_terms_iterator(terms, impl)):
        logging.info("** Next chunk:")
        n += 1
        if all_languages:
            for curie, label, lang in impl.multilingual_labels(curie_it):
                obj = dict(id=curie, label=label, language=lang)
                if set_value is not None:
                    raise NotImplementedError("Cannot set value for multilingual labels yet")
                if _skip_if_absent(if_absent, label):
                    continue
                writer.emit(obj)
        else:
            for curie, label in impl.labels(curie_it, lang=settings.preferred_language):
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
    writer.finish()


@main.command()
@click.argument("terms", nargs=-1)
@output_option
@display_option
@ontological_output_type_option
@if_absent_option
@additional_metadata_option
@set_value_option
@click.option(
    "--lookup-references/--no-lookup-references",
    "-P",
    default=False,
    show_default=True,
    help="Lookup references for each term, e.g. PMIDs",
)
@autolabel_option
def definitions(
    terms,
    output: TextIO,
    additional_metadata: bool,
    display: str,
    output_type: str,
    if_absent: bool,
    autolabel: bool,
    lookup_references: bool,
    set_value,
):
    """
    Show textual definitions for term or set of terms

    Example:


        runoak -i sqlite:obo:envo definitions 'tropical biome' 'temperate biome'

    You can use the ".all" selector to show all definitions for all terms in the ontology:

    Example:


        runoak -i sqlite:obo:envo definitions .all

    You can also include definition metadata, such as provenance and source:

        runoak -i sqlite:obo:cl definitions --additional-metadata neuron

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.display_options = display.split(",")
    writer.file = output
    if lookup_references and not additional_metadata:
        logging.warning("Setting lookup_references to True implies additional_metadata=True")
        additional_metadata = True
    if additional_metadata:
        writer.heterogeneous_keys = True
    changes = []
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    all_curies = []
    for curie_it in chunk(query_terms_iterator(terms, impl)):
        curies = list(curie_it)
        all_curies.extend(curies)
        labels = {}
        if autolabel:
            labels = {curie: label for curie, label in impl.labels(curies)}
        for curie, defn, metadata in impl.definitions(
            curies, include_metadata=additional_metadata, include_missing=True
        ):
            if metadata is None:
                metadata = {}
            obj = dict(id=curie, label=labels.get(curie, None), definition=defn, **metadata)
            if lookup_references:
                refs = []
                obj["references"] = refs
                pubmed_wrapper = PubmedWrapper()
                for _k, vs in metadata.items():
                    pmids = [v for v in vs if v.startswith("PMID:")]
                    if pmids:
                        objs = pubmed_wrapper.objects_by_ids(pmids)
                        refs.extend(objs)

            if set_value is not None:
                # set the value by creating a KGCL change object for applying later
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
    writer.finish()
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
    "--non-redundant-entailed/--no-non-redundant-entailed",
    default=False,
    show_default=True,
    help="Include entailed but exclude entailed redundant relationships",
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
@click.option(
    "--include-metadata/--no-include-metadata",
    default=False,
    show_default=True,
    help="Include metadata (axiom annotations)",
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
    non_redundant_entailed: bool,
    include_metadata: bool,
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

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Relationships.ipynb

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    if not (include_tbox or include_abox):
        raise ValueError("Cannot exclude both tbox AND abox")
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
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
    if non_redundant_entailed:
        if not isinstance(impl, OboGraphInterface):
            raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
        up_it = impl.non_redundant_entailed_relationships(
            subjects=curies,
            predicates=actual_predicates,
            include_abox=include_abox,
            include_tbox=include_tbox,
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
        label_fields = ["subject", "predicate", "object"]
        obj = {k: rel[i] for i, k in enumerate(label_fields)}
        if include_metadata:
            metadata_tuples = list(impl.relationships_metadata([rel]))[0][1]
            obj["metadata"] = dict(pairs_as_dict(metadata_tuples))
        writer.emit(
            obj,
            label_fields=label_fields,
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
    writer.finish()


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--unmelt/--no-unmelt", default=False, show_default=True, help="Flatten to a wide table"
)
@click.option(
    "--matrix-axes",
    help="If specified, transform results to matrix using these row and column axes. Examples: d,p; f,g",
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
    matrix_axes: str,
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

    You can optionally choose to "--matrix-axes" to transform the output to a matrix form.
    This is a comma-separated pair of axes, where each element is a logical definition element
    type: "f" for filler, "p" for predicate, "g" for genus, "d" for defined class.

    Example:

    - Each property/predicate is a column
    - For repeated properties, columns of the form prop_1, prop_2, ... are generated

    Example:

        pato logical-definitions .all  --matrix-axes d,p --output-type csv

    This will generate a row for each defined class with a logical definition, with columns
    for each predicate ("genus" is treated as a predicate here).

    Limitations:

    Currently this only works for definitions that follow a basic genus-differentia pattern,
    which is what is currently represented in the OboGraph datamodel.

    Consider using the "axioms" command for inspection of complex nested OWL axioms.

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/LogicalDefinitions.ipynb

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/obograph

    Data model:

       https://w3id.org/oak/obograph

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.autolabel = autolabel
    actual_predicates = process_predicates_arg(predicates, impl=impl)

    def _exclude_ldef(ldef: LogicalDefinitionAxiom) -> bool:
        if actual_predicates:
            if not any(r for r in ldef.restrictions if r.propertyId in actual_predicates):
                return True
        return False

    if set_value:
        raise NotImplementedError
    label_fields = [
        "definedClassId",
        "genusIds",
        "restrictionFillerIds",
        "restrictionsPropertyIds",
        "restrictionsFillerIds",
    ]
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {type(impl)}")
    # curies = list(query_terms_iterator(terms, impl))
    has_relationships = defaultdict(bool)
    curies = []
    if matrix_axes:
        config = logical_definition_summarizer.parse_axes_to_config(matrix_axes)
        ldefs = []
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            ldefs.extend(list(impl.logical_definitions(curie_it)))
        ldefs = [ldef for ldef in ldefs if not _exclude_ldef(ldef)]
        objs = logical_definition_summarizer.logical_definitions_to_matrix(impl, ldefs, config)
        writer.heterogeneous_keys = True
        label_fields = None
        for obj in objs:
            if label_fields is None:
                label_fields = list(obj.keys())
            writer.emit(obj, label_fields=label_fields)
        writer.finish()
        writer.file.close()
        return
    if unmelt:
        logging.warning("Deprecated: use --matrix-type d,p instead")
        ldef_flattener = LogicalDefinitionFlattener(
            labeler=lambda x: impl.label(x), curie_converter=impl.converter
        )
        writer.heterogeneous_keys = True
    for curie_it in chunk(query_terms_iterator(terms, impl)):
        curie_chunk = list(curie_it)
        curies += curie_chunk
        for ldef in impl.logical_definitions(curie_chunk):
            if _exclude_ldef(ldef):
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
    elif not if_absent:
        for curie in curies:
            if not has_relationships.get(curie, False):
                writer.emit({"defined_class": curie}, label_fields=["defined_class"])
    writer.finish()
    writer.file.close()


@main.command()
@click.argument("terms", nargs=-1)
@predicates_option
@autolabel_option
@output_type_option
@click.option(
    "--named-classes-only/--no-named-classes-only",
    default=False,
    show_default=True,
    help="Only show disjointness axioms between two named classes.",
)
@output_option
def disjoints(
    terms,
    predicates: str,
    autolabel: bool,
    output_type: str,
    named_classes_only: bool,
    output: str,
):
    """
    Show all disjoints for a set of terms, or whole ontology.

    Leave off all arguments for defaults - all terms, YAML OboGraph model
    serialization:

    Example:

        runoak -i sqlite:obo:uberon disjoints

    Note that this will include pairwise disjoints, setwise disjoints,
    disjoint unions, and disjoints involving simple class expressions.

    A tabular format can be easier to browse, and includes labels by default:

    Example:

        runoak -i sqlite:obo:uberon disjoints --autolabel -O csv

    To perform this on a subset:

    Example:

        runoak -i sqlite:obo:cl disjoints --autolabel -O csv  .desc//p=i "immune cell"

    Data model:

       https://w3id.org/oak/obograph

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.autolabel = autolabel
    actual_predicates = process_predicates_arg(predicates, impl=impl)

    label_fields = [
        "classIds",
        "classExpressionPropertyIds",
        "classExpressionFillerIds",
        "unionEquivalentToFillerId",
        "unionEquivalentToPropertyId",
    ]
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {type(impl)}")
    if terms == ".all":
        terms = None
    term_it = query_terms_iterator(terms, impl) if terms else None
    dxas = impl.disjoint_class_expressions_axioms(term_it, predicates=actual_predicates)
    for dxa in dxas:
        if named_classes_only and dxa.classExpressions:
            continue
        writer.emit(dxa, label_fields=label_fields)
    writer.finish()
    writer.file.close()


@main.command()
@output_option
@output_type_option
@autolabel_option
@click.option(
    "--query", "-q", help="Main query, specified in adapter-specific language (SQL, SPARQL)"
)
@click.option("--label-fields", "-L", help="Comma-separated list of fields to use as labels")
@click.option("--prefixes", "-P", help="Comma-separated list of prefixes to expand")
def query(query, autolabel: bool, output: str, output_type: str, prefixes: str, label_fields: str):
    """
    Execute an arbitrary query.

    The syntax of the query is backend-dependent.
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    writer.autolabel = autolabel
    label_fields = label_fields.split(",") if label_fields else []
    prefixes = prefixes.split(",") if prefixes else None

    def _is_uri_or_curie(v):
        return v is not None and isinstance(v, str) and ":" in v and " " not in v

    # batch query results: this allows us to produce buffered output
    # for a long-running query
    for row_it in chunk(impl.query(query, prefixes=prefixes)):
        rows = []
        # collect rows in batch, and set label_fields if not already set
        for r in row_it:
            if not label_fields and autolabel:
                # use heuristic to determine if is a curie
                # label_fields = list([k for k, v in r.items() if _is_uri_or_curie(v)])
                label_fields = list([k for k, v in r.items()])
            rows.append(r)
        idmap = {}
        for f in label_fields:
            # collect labels for designated fields in chunks; this is typically
            # more efficient than querying one at a time when the backend is
            # remote or is a database engine like sqlite
            ids = [r[f] for r in rows if _is_uri_or_curie(r[f])]
            id_labels = impl.labels(ids)
            idmap[f] = {id: label for id, label in id_labels if ":" in id}
        for r in rows:
            if label_fields:
                # inject labels immediately after id columns
                new_r = {}
                for k in r:
                    new_r[k] = r[k]
                    if k in label_fields:
                        new_r[f"{k}_label"] = idmap[k].get(r[k], r[k])
            else:
                new_r = r
            writer.emit(new_r)
    writer.finish()


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
@has_prefix_option
@output_type_option
@click.option(
    "--annotated-roots/--no-annotated-roots",
    "-A/--no-A",
    default=False,
    show_default=True,
    help="If true, use annotated roots, if present",
)
def roots(output: str, output_type: str, predicates: str, has_prefix: str, annotated_roots: bool):
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
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    prefixes = list(has_prefix) if has_prefix else None
    for curie in impl.roots(
        actual_predicates, annotated_roots=annotated_roots, id_prefixes=prefixes
    ):
        writer.emit(dict(id=curie, label=impl.label(curie)))
    writer.finish()


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
        actual_predicates = process_predicates_arg(predicates, impl=impl)
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
        actual_predicates = process_predicates_arg(predicates, impl=impl)
        for curie in impl.singletons(actual_predicates, filter_obsoletes=filter_obsoletes):
            print(f"{curie} ! {impl.label(curie)}")
    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@click.option("-o", "--output", help="Path to output file")
@output_type_option
@autolabel_option
@click.option(
    "--maps-to-source",
    "-M",
    help="Return only mappings with subject or object source equal to this",
)
@click.option(
    "--mapper",
    help="A selector for an adapter that is to be used for the main lookup operation",
)
@click.option(
    "--unmelt/--no-unmelt",
    default=False,
    show_default=True,
    help="Use a wide table for display.",
)
@click.option(
    "--adapters",
    help="A comma-separated list of adapters",
)
@click.option(
    "--allowed-prefixes",
    help="A comma-separated list of prefixes to traverse over",
)
@click.option(
    "--mapping-predicates",
    help="A comma-separated list of mapping predicates to traverse over",
)
@click.option(
    "--viz/--no-viz",
    default=False,
    show_default=True,
    help="If true then draw a graph",
)
@stylemap_option
@stylemap_configure_option
@click.option("-d", "--directory", help="Directory to write output files")
@click.option(
    "--whole-ontology/--no-whole-ontology",
    default=False,
    show_default=True,
    help="Run over whole ontology",
)
@click.option("-C", "--config-yaml")
@click.argument("terms", nargs=-1)
def crawl(
    terms,
    maps_to_source,
    adapters,
    autolabel: bool,
    output,
    output_type,
    allowed_prefixes,
    mapping_predicates,
    viz,
    stylemap,
    configure,
    config_yaml,
    whole_ontology,
    directory,
    mapper,
    unmelt,
):
    """
    Crawl one or more ontologies, hopping over edges and mappings

    Crawl is a powerful command that allows for multi-ontology traversal, particularly
    on mapping paths. Multiple ontologies and ontology sources (e.g. BioPortal, OLS)
    provide mappings between terms. No single ontology is likely to have a complete source.
    Using crawl, you can walk across the union of mappings in all ontologies, with custom rules
    for each ontology (e.g. normalizing prefixes).

    Documentation for this command will be provided in a separate notebook.
    """
    # TODO: normalize this option; avoid confusing with 'config'
    stylemap_configure = configure
    impl = settings.impl
    if viz:
        writer = None
    else:
        writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodel=sssom_schema)
        if unmelt:
            writer.heterogeneous_keys = True
        if isinstance(writer, StreamingSssomWriter) and unmelt:
            raise ValueError("Cannot use --unmelt with SSSOM output")
        writer.output = output
        writer.autolabel = autolabel
    if config_yaml:
        with open(config_yaml) as f:
            config = MappingCrawlerConfig(**yaml.safe_load(f))
    else:
        config = MappingCrawlerConfig()
    if adapters:
        config.adapter_configs = {k: None for k in adapters.split(",")}
    if allowed_prefixes:
        config.allowed_prefixes = allowed_prefixes.split(",")
    if directory:
        config.clique_directory = directory
    if mapping_predicates:
        config.mapping_predicates = mapping_predicates.split(",")
    crawler = MappingCrawler(config)
    if impl:
        terms = list(query_terms_iterator(terms, impl))
    if whole_ontology:
        for clique in crawler.crawl_ontology_iter(terms):
            logging.info(f"Got clique: {clique}")
        return
    mappings = []
    for mapping in crawler.crawl_iter(terms):
        if writer:
            writer.emit(mapping)
        mappings.append(mapping)
    if viz:
        from oaklib.utilities.mapping.mapping_obograph_utils import mappings_to_obograph

        graph = mappings_to_obograph(mappings)
        if output_type and output_type not in ["png", "svg", "dot", "jpeg"]:
            write_graph(graph, format=output_type, output=output)
        else:
            if stylemap is None:
                stylemap = default_stylemap_path()
            if config.stylemap_overrides:
                stylemap_configure = config.stylemap_overrides
            if stylemap_configure:
                # TODO: this is a bit backwards
                stylemap_configure = yaml.dump(stylemap_configure)
            graph_to_image(
                graph,
                seeds=terms,
                imgfile=output,
                stylemap=stylemap,
                configure=stylemap_configure,
                format=output_type,
                view=True,
            )
    if writer:
        writer.finish()


@main.command()
@output_option
@output_type_option
@autolabel_option
@click.option(
    "--maps-to-source",
    "-M",
    help="Return only mappings with subject or object source equal to this",
)
@click.option(
    "--mapper",
    help="A selector for an adapter that is to be used for the main lookup operation",
)
@click.option(
    "--unmelt/--no-unmelt",
    default=False,
    show_default=True,
    help="Use a wide table for display.",
)
@click.argument("terms", nargs=-1)
def mappings(terms, maps_to_source, autolabel: bool, output, output_type, mapper, unmelt):
    """
    List all mappings encoded in the ontology

    Example:

        runoak -i sqlite:obo:envo mappings

    The default output is SSSOM YAML. To use the (canonical) csv format:

        runoak -i sqlite:obo:envo mappings -O sssom

    By default, labels are not included. Use --autolabel to include labels (but note
    that if the label is not in the source ontology, then no label will be retrieved)

        runoak -i sqlite:obo:envo mappings -O sssom

    You can also "unmelt" (pivot) tabular output, such that each column/field
    is a mapping object source.

        runoak -i sqlite:obo:go mappings -O csv --unmelt

    (this format is lossy as it doesn't include the predicate or provenance of the
    mapping, but it can be useful for high level breakdowns)

    To constrain the mapped object source:

        runoak -i sqlite:obo:foodon mappings -O sssom --maps-to-source SUBSET_SIREN

    Like most OAK commands, you can pass in lists of individidual IDs, term labels,
    or OAK query expressions.

    For example, to find all mappings for the MF branch of GO:

        runoak -i sqlite:obo:go mappings .sub molecular_function

    All parts of the brain in Uberon:

        runoak -i sqlite:obo:uberon mappings .desc//p=i,p "brain"

    To get all GO mappings for terms that are mapped to EC:

        runoak -i sqlite:obo:go mappings x^EC

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/mapping-provider

    Data model:

       https://w3id.org/oak/mapping-provider

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Mappings.ipynb

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, datamodel=sssom_schema)
    if unmelt:
        writer.heterogeneous_keys = True
    if isinstance(writer, StreamingSssomWriter) and unmelt:
        raise ValueError("Cannot use --unmelt with SSSOM output")
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, MappingProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    mapper_impl = impl
    if mapper:
        mapper_impl = get_adapter(mapper)

    by_term = defaultdict(dict)
    subject_labels = {}

    def _emit(mapping):
        if autolabel:
            impl.inject_mapping_labels([mapping])
        if unmelt:
            if mapping.subject_label:
                subject_labels[mapping.subject_id] = mapping.subject_label
            k = mapping.object_source
            if k not in by_term[mapping.subject_id]:
                by_term[mapping.subject_id][k] = []
            v = str(mapping.object_id)
            if mapping.object_label:
                v = f"{v} {mapping.object_label}"
            by_term[mapping.subject_id][k].append(v)
            return
        writer.emit(mapping)

    if len(terms) == 0:
        logging.info(f"No terms provided: fetching all mappings for {maps_to_source}")
        for mapping in mapper_impl.sssom_mappings_by_source(
            subject_or_object_source=maps_to_source
        ):
            _emit(mapping)
    else:
        logging.info(f"Fetching mappings for {terms}")
        for curie_it in chunk(query_terms_iterator(terms, impl)):
            for mapping in list(mapper_impl.sssom_mappings(curie_it)):
                if maps_to_source and not mapping.object_id.lower().startswith(
                    f"{maps_to_source.lower()}:"
                ):
                    continue
                _emit(mapping)
    if unmelt:
        for subject_id, mappings in by_term.items():
            writer.emit(
                dict(id=str(subject_id), label=subject_labels.get(subject_id, None), **mappings)
            )
    writer.finish()


@main.command()
@output_option
@output_type_option
@autolabel_option
@click.option(
    "--maps-to-source",
    "-M",
    required=True,
    help="Return only mappings with subject or object source equal to this",
)
@click.argument("terms", nargs=-1)
def normalize(terms, maps_to_source, autolabel: bool, output, output_type):
    """
    Normalize all input identifiers.

    Example:

        runoak -i translator: normalize HGNC:1 HGNC:2 -M NCBIGene

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/mapping-provider

    Data model:

       https://w3id.org/oak/mapping-provider

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, MappingProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if len(terms) == 0:
        raise ValueError("Must provide at least one term")
    curies = query_terms_iterator(terms, impl)
    logging.info(f"Normalizing: {curies}")
    for mapping in impl.sssom_mappings(curies, source=maps_to_source):
        if mapping.object_id.startswith(f"{maps_to_source}:"):
            writer.emit_curie(mapping.object_id, mapping.object_label)
        if mapping.subject_id.startswith(f"{maps_to_source}:"):
            writer.emit_curie(mapping.subject_id, mapping.subject_label)
    writer.finish()


@main.command()
@click.option(
    "--obo-model/--no-obo-model",
    help="If true, assume the OBO synonym datamodel, including provenancem synonym types",
)
@output_type_option
@output_option
@click.argument("terms", nargs=-1)
def aliases(terms, output, output_type, obo_model):
    """
    List aliases for a term or set of terms.

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
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    if obo_model:
        if isinstance(impl, OboGraphInterface):
            curies = list(query_terms_iterator(terms, impl))
            for curie, spv in impl.synonym_property_values(curies):
                writer.emit(
                    dict(
                        curie=curie,
                        pred=str(spv.pred),
                        value=spv.val,
                        type=str(spv.synonymType),
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
    writer.finish()


@main.command()
@output_option
@output_type_option
@click.argument("terms", nargs=-1)
def term_subsets(terms, output, output_type):
    """
    List subsets for a term or set of terms.

    Example:

        runoak -i sqlite:obo:uberon term-subsets heart lung

    Python API:

       https://incatools.github.io/ontology-access-kit/interfaces/basic

    """
    impl = settings.impl
    if isinstance(impl, BasicOntologyInterface):
        writer = _get_writer(output_type, impl, StreamingCsvWriter)
        curies_it = query_terms_iterator(terms, impl)
        for curie, subset in impl.terms_subsets(curies_it):
            writer.emit(dict(curie=curie, subset=subset))
        writer.finish()
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
        actual_predicates = process_predicates_arg(predicates, impl=impl)
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
def term_categories(terms, category_system, output, output_type):
    """
    List categories for a term or set of terms.
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    curies_it = query_terms_iterator(terms, impl)
    for curie, subset in impl.terms_categories(curies_it):
        writer.emit(dict(curie=curie, subset=subset))
    writer.finish()


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
@output_type_option
@predicates_option
@graph_traversal_method_option
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
@click.option(
    "--direct/--no-direct",
    default=False,
    show_default=True,
    help="only include directly asserted taxon constraints",
)
@click.argument("terms", nargs=-1)
def taxon_constraints(
    terms: list,
    all: bool,
    include_redundant: bool,
    direct: bool,
    predicates: List,
    graph_traversal_method,
    output,
    output_type,
):
    """
    Compute all taxon constraints for a term or terms.

    This will apply rules using the inferred ancestors of subject terms, as well as inferred
    ancestors/descendants of taxon terms.

    The input ontology MUST include both the taxon constraint relationships AND the relevant portion
    of NCBI Taxonomy

    Example:

        runoak -i db/go.db taxon-constraints GO:0034357 --include-redundant -p i,p

    Example:

        runoak -i sqlite:obo:uberon taxon-constraints UBERON:0003884 UBERON:0003941 -p i,p

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/TaxonConstraints.ipynb

    This command is a wrapper onto taxon_constraints_utils:

    - https://incatools.github.io/ontology-access-kit/src/oaklib.utilities.taxon.taxon_constraints_utils

    """
    impl = settings.impl
    writer = _get_writer(
        output_type, impl, StreamingYamlWriter, datamodel=datamodels.taxon_constraints
    )
    writer.output = output
    if all:
        if terms:
            raise ValueError("Do not specify explicit terms with --all option")
        # curies = [curie for curie in impl.all_entity_curies() if impl.get_label_by_curie(curie)]
    if isinstance(impl, OboGraphInterface):
        impl.enable_transitive_query_cache()
        impl.cache_lookups = True
        if graph_traversal_method:
            impl.subject_graph_traversal_method = GraphTraversalMethod[graph_traversal_method]
    if not isinstance(impl, TaxonConstraintInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    impl.precompute_lookups()
    impl.precompute_direct_constraint_cache()
    for curie in query_terms_iterator(terms, impl):
        st = impl.get_term_with_taxon_constraints(
            curie,
            include_redundant=include_redundant,
            direct=direct,
            predicates=actual_predicates,
            add_labels=True,
        )
        if direct and not st.only_in and not st.never_in and not st.present_in:
            logging.debug(f"{st.id} has no direct constraints - skipping")
            continue
        writer.emit(st)
    writer.finish()


@main.command()
@click.option("-E", "--evolution-file", help="path to file containing gains and losses")
@output_option
@predicates_option
@graph_traversal_method_option
@click.argument("constraints", nargs=-1)
def apply_taxon_constraints(
    constraints, evolution_file, predicates: List, graph_traversal_method, output
):
    """
    Test candidate taxon constraints

    Multiple candidate constraints can be passed as arguments. these are in the form of triples
    separated by periods.

    Example:

        runoak  -i db/go.db apply-taxon-constraints -p i,p GO:0005743 only NCBITaxon:2759
        never NCBITaxon:2 . GO:0005634 only NCBITaxon:2

    The --evolution-file (-E) option can be used to pass in a file of candidates.
    This should follow the format used in https://arxiv.org/abs/1802.06004

    E.g.

        GO:0000229,Gain|NCBITaxon:1(root);>Loss|NCBITaxon:2759(Eukaryota);

    Example:

        runoak  -i db/go.db eval-taxon-constraints -p i,p -E tests/input/go-evo-gains-losses.csv

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Apply.ipynb

    """
    impl = settings.impl
    actual_predicates = process_predicates_arg(predicates, impl=impl)
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
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    impl.enable_transitive_query_cache()
    impl.precompute_lookups()
    impl.cache_lookups = True
    if graph_traversal_method:
        impl.subject_graph_traversal_method = GraphTraversalMethod[graph_traversal_method]
    if not isinstance(impl, TaxonConstraintInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    for st in sts:
        try:
            st = impl.eval_candidate_taxon_constraint(st, predicates=actual_predicates)
            writer.emit(st)
        except ValueError as e:
            logging.error(f"Error with TC: {e}")
            st.description = "PROBLEM"
            writer.emit(st)


@main.command()
@output_option
@autolabel_option
@output_type_option
@output_option
@click.option(
    "--used-by-prefix",
    "-P",
    multiple=True,
)
@click.option(
    "--include-unused/--no-include-unused",
    default=True,
    show_default=True,
)
@click.argument("terms", nargs=-1)
def usages(
    terms,
    autolabel: bool,
    output_type: str,
    output: str,
    used_by_prefix: List,
    **kwargs,
):
    """
    List usages of a term or set of terms.

    Usages of neuron in GO:

        runoak -i sqlite:obo:go usages CL:0000540

    Association/annotations sources can also be used:

        runoak -i quickgo: usages GO:0031969

    Note this query may be slow - you can restrict to a species:

        runoak -i quickgo:NCBITaxon:9606 usages GO:0031969

    (this should return no results, as there should be no human proteins annotated
    to chloroplast membrane)

    Using amigo:

        runoak -i amigo: usages GO:0031969

    Using ubergraph:

        runoak -i ubergraph: usages CL:0000540

    This will include usages over multiple ontologies

    Using ontobee:

        runoak -i ubergraph: usages CL:0000540

    You can multiple queries over multiple sources (an AggregatorImplementation):

        runoak -i sqlite:obo:go -a ubergraph: -a amigo: -a quickgo: usages GO:0031969

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    if not isinstance(impl, UsagesInterface):
        raise NotImplementedError(
            f"Cannot execute this using {settings.impl} of type {type(settings.impl)}"
        )
    used_by = None
    if "@" in terms:
        ix = terms.index("@")
        curies = list(query_terms_iterator(terms[:ix], impl))
        used_by = terms[ix + 1 :]
    else:
        curies = list(query_terms_iterator(terms, impl))
    for usage in impl.usages(curies, used_by=used_by, used_by_prefixes=used_by_prefix, **kwargs):
        writer.emit(usage)


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@if_absent_option
@set_value_option
@click.option(
    "--add-closure-fields/--no-add-closure-fields",
    default=False,
    show_default=True,
    help="Add closure fields to the output",
)
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.option(
    "--terms-role",
    "-Q",
    type=click.Choice([x.value for x in SubjectOrObjectRole]),
    default=SubjectOrObjectRole.OBJECT.value,
    show_default=True,
    help="How to interpret query terms.",
)
@click.option(
    "--expand/--no-expand",
    default=False,
    show_default=True,
    help="Expand by feeding results into subsequent query",
)
@click.option(
    "--header/--no-header",
    "-H/--no-H",
    default=False,
    show_default=True,
    help="Show a header",
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
    expand: bool,
    header: bool,
    **kwargs,
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
    to is-a descendants.

    Using input specifications:

    It can be awkward to specify both input ontology and association path and format. You
    can use input specifications to bundle common combinations of inputs together.

    For example, the go-dictybase-input-spec combines go plus dictybase associations.

    Example:

        runoak --i src/oaklib/conf/go-dictybase-input-spec.yaml associations -p i,p GO:0008104

    More examples:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Associations.ipynb

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    actual_association_predicates = process_predicates_arg(association_predicates)
    if not isinstance(impl, AssociationProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    curies = list(query_terms_iterator(terms, impl))
    if header:
        writer.emit_header(
            f"Query IDs: {', '.join(curies)}",
            f"Ontology closure predicates: {', '.join(actual_predicates or [])}",
        )
        if expand:
            writer.emit_header("The results include a round of expansion")
    qs_it = impl.associations(
        curies,
        predicates=actual_association_predicates,
        subject_closure_predicates=actual_predicates,
        **kwargs,
    )
    qo_it = impl.associations(
        objects=curies,
        predicates=actual_association_predicates,
        object_closure_predicates=actual_predicates,
        **kwargs,
    )
    if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
        it = qs_it
    elif terms_role == SubjectOrObjectRole.OBJECT.value:
        it = qo_it
    else:
        logging.info("Using query terms to query both subject and object")
        it = chain(qs_it, qo_it)
    # track which nodes have relationships (used for if_absent)
    has_relationships = defaultdict(bool)
    entities_to_expand = set()
    for assoc in it:
        if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
            has_relationships[assoc.subject] = True
            entities_to_expand.add(assoc.object)
        elif terms_role == SubjectOrObjectRole.OBJECT.value:
            has_relationships[assoc.object] = True
            entities_to_expand.add(assoc.subject)
        else:
            has_relationships[assoc.subject] = True
            has_relationships[assoc.object] = True
            entities_to_expand.add(assoc.subject)
            entities_to_expand.add(assoc.object)
        if if_absent and if_absent == IfAbsent.absent_only.value:
            continue
        writer.emit(
            assoc,
            label_fields=["subject", "predicate", "object"],
        )
    if expand:
        logging.info(f"Expanding using {len(entities_to_expand)} nodes")
        exp_it = get_association_iterator(
            impl,
            list(entities_to_expand),
            terms_role=(
                SubjectOrObjectRole.SUBJECT.value
                if terms_role == SubjectOrObjectRole.OBJECT.value
                else SubjectOrObjectRole.OBJECT.value
            ),
            association_predicates=actual_association_predicates,
            ontology_predicates=actual_predicates,
            **kwargs,
        )
        for assoc in exp_it:
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


@main.command()
@predicates_option
@output_type_option
@click.option(
    "-o",
    "--output",
    help="Output file",
)
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.option(
    "-A",
    "--ontology-adapter",
    help="Adapter to use for traversing ontology graph",
)
@click.option(
    "--gap-fill/--no-gap-fill",
    default=False,
    show_default=True,
    help="Fill in missing nodes",
)
@click.option(
    "--terms-role",
    "-Q",
    type=click.Choice([x.value for x in SubjectOrObjectRole]),
    default=SubjectOrObjectRole.OBJECT.value,
    show_default=True,
    help="How to interpret query terms.",
)
@click.option(
    "--view/--no-view",
    default=True,
    show_default=True,
    help="if view is set then open the image after rendering",
)
@stylemap_option
@stylemap_configure_option
@click.argument("terms", nargs=-1)
def associations_graph(
    terms,
    predicates: str,
    association_predicates: str,
    terms_role: str,
    gap_fill: bool,
    output_type: str,
    output: str,
    view: bool,
    stylemap: str,
    ontology_adapter,
    **kwargs,
):
    """
    Query associations and fill out ontology graph.

    Example:

        runoak -i amigo: associations-graph -p i,p -A sqlite:obo:go -Q subject WB:WBGene00001187 -o gene.json

    This queries for associations whose subject is the gene WBGene00001187 in AmiGO, and uses
    the GO ontology to fill out the graph, following is-a and part-of relationships.

    To immediately visualize, add --view to the end:

        runoak -i amigo: associations-graph -p i,p -A sqlite:obo:go -Q subject WB:WBGene00001187 --view

    You can use --gap-fill to trim the graph to only pairwise MRCAs and span the gaps:

        runoak -i amigo: associations-graph -p i,p -A sqlite:obo:go -Q subject WB:WBGene00001187 --gap-fill --view
    """
    impl = settings.impl
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    actual_association_predicates = process_predicates_arg(association_predicates)
    if not isinstance(impl, AssociationProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    curies = list(query_terms_iterator(terms, impl))
    # TODO: consider abstracting this into a method
    qs_it = impl.associations(
        curies,
        predicates=actual_association_predicates,
        subject_closure_predicates=actual_predicates,
        **kwargs,
    )
    qo_it = impl.associations(
        objects=curies,
        predicates=actual_association_predicates,
        object_closure_predicates=actual_predicates,
        **kwargs,
    )
    if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
        it = qs_it
    elif terms_role == SubjectOrObjectRole.OBJECT.value:
        it = qo_it
    else:
        logging.info("Using query terms to query both subject and object")
        it = chain(qs_it, qo_it)
    node_map = {}
    edges = []
    for assoc in it:
        node_map[assoc.subject] = Node(id=assoc.subject, lbl=assoc.subject_label)
        node_map[assoc.object] = Node(id=assoc.object, lbl=assoc.object_label)
        edges.append(Edge(sub=assoc.subject, obj=assoc.object, pred=assoc.predicate))
    logging.info(f"Initial AG, num_nodes={len(node_map)}, num_edges={len(edges)}")
    curies = list(node_map.keys())
    if ontology_adapter:
        oa = get_adapter(ontology_adapter)
    else:
        oa = impl
    if gap_fill:
        if not isinstance(oa, SemanticSimilarityInterface):
            raise NotImplementedError(f"{oa} does not implement SemanticSimilarityInterface")
        curies_to_add = [
            lca
            for s, o, lca in oa.multiset_most_recent_common_ancestors(
                curies, predicates=actual_predicates
            )
        ]
        curies = list(set(curies + curies_to_add))
        logging.info(f"Expanded CURIEs = {curies}")
        if not isinstance(oa, SubsetterInterface):
            raise NotImplementedError(f"{oa} does not implement SubsetterInterface")
        graph = oa.extract_gap_filled_graph(curies, predicates=actual_predicates)
    else:
        # walk up
        if not isinstance(oa, OboGraphInterface):
            raise NotImplementedError(f"Cannot execute this using {oa} of type {type(oa)}")

        graph = oa.ancestor_graph(
            curies, predicates=actual_predicates, method=GraphTraversalMethod.ENTAILMENT
        )
    graph.edges.extend(edges)
    existing_nodes = set([node.id for node in graph.nodes])
    for node in node_map.values():
        if node.id not in existing_nodes:
            graph.nodes.append(node)
    logging.info(f"Final AG, num_nodes={len(graph.nodes)}, num_edges={len(graph.edges)}")
    remove_unlabeled_nodes(graph)
    gd = GraphDocument(graphs=[graph])
    if stylemap is None:
        stylemap = default_stylemap_path()
    write_graph_document(
        gd, output, format=output_type, view=view, stylemap=stylemap, seeds=curies, **kwargs
    )


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@click.option(
    "--add-closure-fields/--no-add-closure-fields",
    default=False,
    show_default=True,
    help="Add closure fields to the output",
)
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.option(
    "--terms-role",
    "-Q",
    type=click.Choice([x.value for x in SubjectOrObjectRole]),
    default=SubjectOrObjectRole.OBJECT.value,
    show_default=True,
    help="How to interpret query terms.",
)
@click.option(
    "--limit",
    "-L",
    default=10,
    show_default=True,
    help="Limit the number of results",
)
@click.option(
    "--filter",
    "-F",
    multiple=True,
    help="Additional filters in K=V format",
)
@click.option(
    "--min-facet-count",
    default=1,
    show_default=True,
    help="Minimum count for a facet to be included",
)
@click.option(
    "--group-by",
    default="object",
    show_default=True,
    help="Group by subject or object",
)
@click.argument("terms", nargs=-1)
def associations_counts(
    terms,
    predicates: str,
    association_predicates: str,
    terms_role: str,
    autolabel: bool,
    output_type: str,
    output: str,
    filter,
    **kwargs,
):
    """
    Count associations, grouped by subject or object

    Example:

        runoak -i sqlite:obo:hp -g test.hpoa -G hpoa associations-counts

    This will default to summarzing by objects (HPO term), showing the number
    of associations for each term.

    This will be direct counts only. To include is-a closure, specify
    the closure predicate(s), e.g.

    Example:

        runoak -i sqlite:obo:hp -g test.hpoa -G hpoa associations -p i

    You can also group by other fields

    Example:

        runoak -i sqlite:obo:hp -g test.hpoa -G hpoa associations-counts --group-by subject

    This will show the number of associations for each disease.

    OAK also includes a number of specialized adapters that implement this method
    for particular databases.

    For example, to get the number of IEA associations for each GO term:

        runoak -i amigo: associations-counts  --limit -1 -F evidence_type=IEA --no-autolabel

    This can be constrained by species:

        runoak -i amigo:NCBITaxon:9606 associations-counts  --limit -1 -F evidence_type=IEA --no-autolabel

    Other options:

    This command accepts many of the same options as the associations command, see
    the docs for this command for details.

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    actual_association_predicates = process_predicates_arg(association_predicates)
    if not isinstance(impl, AssociationProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    curies = list(query_terms_iterator(terms, impl))
    filter_dict = {k: v for k, v in (x.split("=") for x in filter)}
    kwargs["property_filter"] = filter_dict
    qs_it = impl.association_counts(
        curies,
        predicates=actual_association_predicates,
        subject_closure_predicates=actual_predicates,
        **kwargs,
    )
    qo_it = impl.association_counts(
        objects=curies,
        predicates=actual_association_predicates,
        object_closure_predicates=actual_predicates,
        **kwargs,
    )
    if terms_role is None or terms_role == SubjectOrObjectRole.SUBJECT.value:
        it = qs_it
    elif terms_role == SubjectOrObjectRole.OBJECT.value:
        it = qo_it
    else:
        logging.info("Using query terms to query both subject and object")
        it = chain(qs_it, qo_it)
    for term, count in it:
        writer.emit(
            {"term": term, "count": count},
            label_fields=["term"],
        )


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@click.option(
    "--association-predicates",
    help="A comma-separated list of predicates for the association relation",
)
@click.option(
    "--terms-role",
    "-Q",
    type=click.Choice([x.value for x in SubjectOrObjectRole]),
    default=SubjectOrObjectRole.OBJECT.value,
    show_default=True,
    help="How to interpret query terms.",
)
@click.option(
    "--include-entities/--no-include-entities",
    default=True,
    show_default=True,
    help="Include entities (e.g. genes) in the output, otherwise just the counts",
)
@click.option(
    "--main-score-field",
    "-S",
    default="proportion_subjects_in_common",
    show_default=True,
    help="Score used for summarization",
)
@click.argument("terms", nargs=-1)
def associations_matrix(
    terms,
    predicates: str,
    association_predicates: str,
    terms_role: str,
    autolabel: bool,
    output_type: str,
    output: str,
    main_score_field: str,
    **kwargs,
):
    """
    Co-annotation matrix query.

    This queries for co-annotations between pairs of terms.

    See: Wood V., Carbon S., et al, https://royalsocietypublishing.org/doi/10.1098/rsob.200149

    Example:

        runoak  -i amigo:NCBITaxon:9606 associations-matrix -p i,p GO:0042416 GO:0014046

    This results in a 2x2 matrix (shown as a long table)

    As a heatmap:

        runoak  -i amigo:NCBITaxon:9606 associations-matrix -p i,p GO:0042416 GO:0014046 -O heatmap > /tmp/heatmap.png

    By default the heatmap will show the percentage of overlap between the two terms. To change this
    to be either the percentage of the first term in the second, or the percentage of the second term in the first,
    use the --main-score-field (-S) option, with "1" or "2".

    You can plug in as many terms as you like, it will perform an all-by-all

    To compare one set with another, use the "@" separator.

    You can also substitute OAK expression language query terms

        runoak --stacktrace  -i amigo:NCBITaxon:9606 associations-matrix -p i,p .idfile cp.txt @ .idfile ct.txt
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.autolabel = autolabel
    writer.output = output
    if main_score_field and isinstance(writer, HeatmapWriter):
        if main_score_field == "1":
            main_score_field = "proportion_entity1_subjects_in_entity2"
        if main_score_field == "2":
            main_score_field = "proportion_entity2_subjects_in_entity1"
        writer.value_field = main_score_field
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    actual_association_predicates = process_predicates_arg(association_predicates)
    if not isinstance(impl, AssociationProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if "@" in terms:
        ix = terms.index("@")
        logging.info(f"Splitting terms into two, position = {ix}")
        curies1 = list(query_terms_iterator(terms[0:ix], impl))
        curies2 = list(query_terms_iterator(terms[ix + 1 :], impl))
    else:
        curies1 = list(query_terms_iterator(terms, impl))
        curies2 = list(curies1)
    if terms_role != SubjectOrObjectRole.OBJECT.value:
        raise NotImplementedError("terms-role not yet supported")
    pairs_it = impl.association_pairwise_coassociations(
        curies1=curies1,
        curies2=curies2,
        predicates=actual_association_predicates,
        subject_closure_predicates=actual_predicates,
        **kwargs,
    )
    jaccards = []
    n = 0
    for pair in pairs_it:
        # TODO: more elegant way to handle this
        pair.associations_for_subjects_in_common = None
        jaccards.append(pair.proportion_subjects_in_common)
        writer.emit(
            pair,
            label_fields=["object1", "object2"],
        )
        n += 1
    logging.info(f"Emitted {n} pairs")
    writer.finish()
    logging.info(f"Average Jaccard index: {stats.mean([j for j in jaccards if j is not None])}")


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@click.option(
    "--object-group",
    help="An object ID to group by. If a comma separated list of IDs is provided, the first one is interpreted as a "
    + "top-level grouping and the remaining IDs are interpreted as sub-groups within.",
    multiple=True,
)
@click.argument("terms", nargs=-1)
def rollup(
    terms, output, predicates: str, autolabel: bool, output_type: str, object_group: List[str]
):
    """
    Produce an association rollup report.

    The report will list associations where the subject is one of the terms provided. The
    associations will be grouped by any provided --object-group options. This option can be
    provided multiple times. If the value is a comma separated list of object IDs, the first
    will be used as a primary grouping dimension and the remainder will be used to create
    sub-groups.

    Example:

        runoak -i sqlite:go.db -g wb.gaf -G gaf rollup \
            --object-group GO:0032502,GO:0007568,GO:0048869,GO:0098727 \
            --object-group GO:0008152,GO:0009056,GO:0044238,GO:1901275 \
            --object-group GO:0050896,GO:0051716,GO:0051606,GO:0051606,GO:0014823 \
            --object-group=GO:0023052 \
            --output rollup.html \
            WB:WBGene00000417 WB:WBGene00000912 WB:WBGene00000898 WB:WBGene00006752

    By default, is-a relationships between association objects are used to perform the rollup.
    Use the -p/--predicates option to change this behavior.

    """
    impl = settings.impl

    if not output_type:
        output_type = "html"

    if not predicates:
        predicates = "i"

    if isinstance(impl, AssociationProviderInterface) and isinstance(impl, OboGraphInterface):
        split_ids = [o.split(",", 1) for o in object_group]
        primary_ids = (s[0] for s in split_ids)
        secondary_ids = (s[1].split(",") if len(s) > 1 else [] for s in split_ids)
        objects_dict = dict(zip(primary_ids, secondary_ids, strict=False))

        object_closure_predicates = process_predicates_arg(predicates, impl=impl)

        groups: List[RollupGroup] = []
        for primary, secondaries in objects_dict.items():
            group = RollupGroup(group_object=primary)
            for secondary in secondaries:
                associations = list(
                    impl.associations(
                        subjects=terms,
                        objects=[secondary],
                        object_closure_predicates=object_closure_predicates,
                    )
                )
                group.sub_groups.append(
                    RollupGroup(group_object=secondary, associations=associations)
                )

            sub_group_objects = [
                association.object
                for sub_group in group.sub_groups
                for association in sub_group.associations
            ]
            associations = list(
                impl.associations(
                    subjects=terms,
                    objects=[primary],
                    object_closure_predicates=object_closure_predicates,
                )
            )
            group.associations = [
                association
                for association in associations
                if association.object not in sub_group_objects
            ]
            groups.append(group)

        group_dicts = [json_dumper.to_dict(g) for g in groups]
        if autolabel:

            def apply_labels(group):
                group["group_object_label"] = impl.label(group.get("group_object"))
                for association in group.get("associations", []):
                    association["object_label"] = impl.label(association.get("object"))
                for sub_group in group.get("sub_groups", []):
                    apply_labels(sub_group)

            for group in group_dicts:
                apply_labels(group)

        write_report(terms, group_dicts, output, output_type)

    else:
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@click.option(
    "--ontology-only/--no-ontology-only",
    "-T",
    default=False,
    show_default=True,
    help="If true, perform a pseudo-enrichment analysis treating each term as an association to itself.",
)
@click.option(
    "--cutoff",
    type=click.FLOAT,
    default=0.05,
    show_default=True,
    help="The cutoff for the p-value; any p-values greater than this are not reported.",
)
@click.option(
    "--sample-file",
    "-U",
    required=False,
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
@click.option(
    "--filter-redundant/--no-filter-redundant",
    default=False,
    help="If true, filter out redundant terms",
)
@click.option(
    "--allow-labels/--no-allow-labels",
    default=False,
    help="If true, allow labels as well as CURIEs in the input files",
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
    ontology_only: bool,
    allow_labels: bool,
    **kwargs,
):
    """
    Run class enrichment analysis.

    Given a sample file of identifiers (e.g. gene IDs), plus a set of associations (e.g. gene to term
    associations, return the terms that are over-represented in the sample set.

    Example:

        runoak -i sqlite:obo:uberon -g gene2anat.txt -G g2t enrichment -U my-genes.txt -O csv

    This runs an enrichment using Uberon on my-genes.txt, using the gene2anat.txt file as the
    association file (assuming simple gene-to-term format). The output is in CSV format.

    It is recommended you always provide a background set, including all the entity identifiers
    considered in the experiment.

    You can specify --filter-redundant to filter out redundant terms. This will block reporting
    of any terms that are either subsumed by or subsume a lower p-value term that is already
    reported.

    For a full example, see:

       https://github.com/INCATools/ontology-access-kit/blob/main/notebooks/Commands/Enrichment.ipynb

    Note that it is possible to run "pseudo-enrichments" on term lists only by passing
    no associations and using --ontology-only. This creates a fake association set that is simply
    reflexive relations between each term and itself. This can be useful for summarizing term lists,
    but note that P-values may not be meaningful.

    """
    impl = settings.impl
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    actual_association_predicates = process_predicates_arg(association_predicates)
    if sample_file:
        subjects = list(curies_from_file(sample_file, adapter=impl, allow_labels=allow_labels))
        curies = list(query_terms_iterator(terms, impl))
    else:
        if "@" in terms:
            if not ontology_only:
                raise ValueError("Cannot use @ with --no-ontology-only")
            ix = terms.index("@")
            logging.info(f"Splitting terms into two, position = {ix}")
            subjects = list(query_terms_iterator(terms[0:ix], impl))
            curies = list(query_terms_iterator(terms[ix + 1 :], impl))
            logging.info(f"Num Subjects={len(subjects)} (using {len(curies)} terms)")
        else:
            subjects = list(query_terms_iterator(terms, impl))
            curies = None
            logging.info(f"Num Subjects={len(subjects)} (using all terms)")
    if not subjects:
        raise ValueError("No terms or upload provided")
    background = (
        list(curies_from_file(background_file, adapter=impl, allow_labels=allow_labels))
        if background_file
        else None
    )
    if not isinstance(impl, ClassEnrichmentCalculationInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if (
        impl.requires_associations
        and not ontology_only
        and not any(True for _ in impl.associations())
    ):
        raise click.UsageError("no associations -- specify --ontology-only or load associations")
    if ontology_only:
        impl.create_self_associations()
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.autolabel = autolabel
    writer.output = output
    results = impl.enriched_classes(
        subjects,
        predicates=actual_association_predicates,
        object_closure_predicates=actual_predicates,
        hypotheses=curies if curies else None,
        background=background,
        cutoff=cutoff,
        autolabel=autolabel,
        **kwargs,
    )
    for result in results:
        writer.emit(result)
    writer.finish()


@main.command()
@output_option
@predicates_option
@autolabel_option
@output_type_option
@output_option
@click.option("--old-date", help="Old date, in YYYY-MM-DD format")
@click.option("--new-date", help="Old date, in YYYY-MM-DD format")
@click.option("-g", "--associations", help="associations")
@click.option("-X", "--other-associations", help="other associations")
@click.option(
    "--group-by",
    help="One of: publications; primary_knowledge_source",
)
def diff_associations(
    predicates: str,
    autolabel: bool,
    output_type: str,
    output: str,
    group_by: str,
    associations: str,
    other_associations: str,
    **kwargs,
):
    """
    Diffs two association sources.

    Example:

        runoak -i sqlite:obo:go  -G gaf  diff-associations \
           --old-date ${date1} --new-date ${date2} \
           -g  "${download_dir}/${group}-${date1}.gaf" \
           -X "${download_dir}/${group}-${date2}.gaf" \
           --group-by publications -p i,p \
           -o "${group}-diff-${date1}-to-${date2}.tsv

    See https://w3id.org/oak/association for the diff data model.

    NOTE: This functionality may move out of core

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.heterogeneous_keys = True
    writer.autolabel = autolabel
    writer.output = output
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    logging.info(f"Fetching parser for {settings.associations_type}")
    association_parser = get_association_parser(settings.associations_type)
    if not isinstance(impl, AssociationProviderInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
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
        if not isinstance(impl, OboGraphInterface):
            raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
        differ = AssociationDiffer(impl)
        impl.enable_transitive_query_cache()
        if group_by == "publications":
            changes = differ.changes_by_publication(assocs1, assocs2, actual_predicates)
        elif group_by == "primary_knowledge_source":
            changes = differ.changes_by_primary_knowledge_source(
                assocs1, assocs2, actual_predicates
            )
        elif group_by:
            raise ValueError(f"Unknown group-by: {group_by}")
        else:
            changes = differ.calculate_change_objects(assocs1, assocs2, actual_predicates)
        for change in changes:
            if kwargs:
                for k, v in kwargs.items():
                    setattr(change, k, v)
            writer.emit(change, label_fields=["old_object", "new_object"])
    writer.finish()


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
@click.argument("terms", nargs=-1)
def validate(
    terms: List[str],
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
    if not isinstance(impl, ValidatorInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if terms:
        # note: currently the validate interface doesn't supported filtered lists,
        # so we post-hoc filter. This is potentially inefficient.
        entities = list(query_terms_iterator(terms, impl))
    else:
        entities = None
    if not skip_structural_validation:
        counts = defaultdict(int)
        for result in impl.validate():
            if entities and result.subject not in entities:
                continue
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
            if entities and result.subject not in entities:
                continue
            writer.emit(result)
    writer.finish()


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
@configuration_file_option
@adapter_mapping_option
@output_type_option
@output_option
@click.argument("terms", nargs=-1)
def validate_definitions(
    terms,
    skip_text_annotation,
    output: str,
    output_type: str,
    configuration_file: str,
    adapter_mapping: List[str],
):
    """
    Checks presence and structure of text definitions.

    To run:

        runoak validate-definitions -i db/uberon.db -o results.tsv

    By default this will apply basic text mining of text definitions to check
    against machine actionable OBO text definition guideline rules.
    This can result in an initial lag - to skip this, and ONLY perform
    checks for *presence* of definitions, use --skip-text-annotation:

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
    -----

    This command is largely redundant with the validate command, but is useful for
    targeted validation focused solely on definitions

    """
    impl = settings.impl
    writer = _get_writer(
        output_type, impl, StreamingCsvWriter, datamodel=datamodels.validation_datamodel
    )
    writer.autolabel = True
    writer.output = output
    if not isinstance(impl, ValidatorInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if configuration_file:
        config = yaml_loader.load(configuration_file, target_class=ValidationConfiguration)
    else:
        config = None
    adapters = {}
    for am in adapter_mapping:
        prefix, selector = am.split("=")
        adapters[prefix] = get_adapter(selector)
        logging.info(f"Loaded adapter for {prefix} => {selector}")
    if terms:
        entities = query_terms_iterator(terms, impl)
    else:
        entities = None
    for vr in impl.validate_definitions(
        entities, adapters=adapters, configuration=config, skip_text_annotation=skip_text_annotation
    ):
        writer.emit(vr, label_fields=["subject"])
    writer.finish()


@main.command()
@autolabel_option
@output_type_option
@adapter_mapping_option
@output_option
@configuration_file_option
@click.argument("terms", nargs=-1)
def validate_mappings(
    terms, autolabel, adapter_mapping, output: str, output_type: str, configuration_file: str
):
    """
    Validates mappings in ontology using additional ontologies.

    To run:

        runoak validate-mappings -i db/uberon.db

    For sssom:

        runoak validate-mappings -i db/uberon.db -o bad-mappings.sssom.tsv

    By default this will attempt to download and connect to
    sqlite versions of different ontologies, when attempting to resolve a foreign
    subject or object id.

    You can customize this mapping:

        runoak validate-mappings -i db/uberon.db --adapter-mapping uberon=db/uberon.db \
            --adapter-mapping zfa=db/zfa.db

    This will use a local sqlite file for ZFA:nnnnnnn IDs.

    You can use "*" as a wildcard, in the case where you have an application ontology
    with many mapped entities merged in:

        runoak validate-mappings -i db/uberon.db --adapter-mapping "*"=db/merged.db"

    The default behavior for this command is to perform deterministic rule-based
    checks; for example, the mapped IDs should not be obsolete, and if the mapping
    is skos:exactMatch, then the cardinality is expected to be 1:1.

    Other adapters may choose to implement bespoke behaviors. In future there
    might be a boomer adapter that will perform probabilistic reasoning on the
    mappings. The experimental LLM backend will use an LLM to qualitatively
    validate mappings (see the LLM how-to guide for more details).
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, ValidatorInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if terms:
        entities = query_terms_iterator(terms, impl)
    else:
        entities = None
    if configuration_file:
        config = yaml_loader.load(configuration_file, target_class=ValidationConfiguration)
    else:
        config = None

    adapters = {}
    for am in adapter_mapping:
        prefix, selector = am.split("=")
        adapters[prefix] = get_adapter(selector)
        logging.info(f"Loaded adapter for {prefix} => {selector}")
    for result in impl.validate_mappings(entities, adapters=adapters, configuration=config):
        writer.emit_obj(result)
    writer.finish()


@main.command()
@autolabel_option
@output_type_option
@adapter_mapping_option
@output_option
@configuration_file_option
@click.option(
    "--rules-file",
    "-R",
    help="path to rules file. Conforms to rules_datamodel.\
        e.g. https://github.com/INCATools/ontology-access-kit/blob/main/tests/input/matcher_rules.yaml",
)
@click.argument("terms", nargs=-1)
def validate_synonyms(
    terms,
    autolabel,
    adapter_mapping,
    output: str,
    output_type: str,
    rules_file: str,
    configuration_file: str,
):
    """
    Validates synonyms in ontology using additional ontologies.

    To run:

        runoak validate-synonyms -i db/uberon.db

    You can customize this mapping:

        runoak validate-synonyms -i db/uberon.db --adapter-mapping uberon=db/uberon.db \
            --adapter-mapping zfa=sqlite:obo:zfa

    This will use a remote sqlite file for ZFA:nnnnnnn IDs.

    You can use "*" as a wildcard, in the case where you have an application ontology
    with many mapped entities merged in:

        runoak validate-synonyms -i db/uberon.db --adapter-mapping "*"=db/merged.db"

    You can also pass synonymizer rules. For example:

        runoak -i sqlite:obo:go  validate-synonyms \
           -R go-strip-activity.synonymizer.yaml GO:0000010 \
            --adapter-mapping ec=sqlite:obo:eccode

    In this case if the synonymizer rule file contains:

        \b
        rules:
          - match: " activity"
            replacement: ""
        \b

    Then the GO synonyms will have the word "activity" stripped from them, prior to attempting
    to match with EC.

    The default behavior for this command is to perform deterministic rule-based
    checks; for example, the mapped IDs should not be obsolete, and if the mapping
    is skos:exactMatch, then the cardinality is expected to be 1:1.

    Other adapters may choose to implement bespoke behaviors. In future there
    might be a boomer adapter that will perform probabilistic reasoning on the
    mappings. The experimental LLM backend will use an LLM to qualitatively
    validate mappings (see the LLM how-to guide for more details).
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingCsvWriter)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, ValidatorInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if terms:
        entities = query_terms_iterator(terms, impl)
    else:
        entities = None
    if configuration_file:
        config = yaml_loader.load(configuration_file, target_class=ValidationConfiguration)
    else:
        config = None
    if rules_file:
        ruleset = synonymizer_datamodel.RuleSet(**yaml.safe_load(open(rules_file)))
    else:
        ruleset = None

    adapters = {}
    for am in adapter_mapping:
        prefix, selector = am.split("=")
        adapters[prefix] = get_adapter(selector)
        logging.info(f"Loaded adapter for {prefix} => {selector}")
    for result in impl.validate_synonyms(
        entities, adapters=adapters, configuration=config, synonymizer_rules=ruleset
    ):
        writer.emit_obj(result)
    writer.finish()


@main.command()
@autolabel_option
@output_type_option
@adapter_mapping_option
@predicates_option
@click.option(
    "--exclude-query",
    "-X",
    help="A query to exclude certain terms",
)
@click.option(
    "--information-content-file",
    help="File containing information content for each term",
)
@click.option(
    "--information-content-adapter",
    help="Adapter to use for information content scores",
)
@click.option("--config-yaml")
@output_option
@configuration_file_option
@click.argument("terms", nargs=-1)
def validate_subset(
    terms,
    autolabel,
    predicates,
    adapter_mapping,
    information_content_file,
    information_content_adapter,
    exclude_query,
    config_yaml,
    output: str,
    output_type: str,
    configuration_file: str,
):
    """
     Validates term subsets.

     The default metrics used for evaluation involve calculating the degree of overlap between members of the
     subset. Subsets in general should partition the ontology into sets that overlap as little as possible.

     Different overlap metrics can be plugged in, see the information-content methods for more details.

     The simplest way to run this is to pass in a list of terms via a subset query

         runoak -i po.db validate-subset p i,p  .in Tomato

     You can also calculate IC scores for each term and pass them in via a file:

         runoak -i amigo:NCBITaxon:9606 information-content -o human-ic.tsv

    Then

         runoak -i go.db validate-subset p i,p  .in goslim_generic --information-content-file human-ic.tsv

    This command also understand the GO subset metadata format. You can use this as configuration for
    validating multiple subsets:

        runoak -i go.db validate-subset --config-yaml go_subsets_metadata.yaml -X "i^BFO:" -O yaml

    The taxon field is used to validate each subset according to its appropriate context
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, SemanticSimilarityInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
    if information_content_file:
        impl.load_information_content_scores(information_content_file)
    configs = []
    if config_yaml:
        main_config = yaml.safe_load(open(config_yaml))
        # assume GO schema for now
        subsets_objs = main_config.get("subsets")
        for subset in subsets_objs:
            if subset.get("status") == "obsolete":
                continue
            if "ExclusionList" in subset.get("role", []):
                continue
            taxa = subset.get("taxa")
            if taxa:
                taxa_ids = [x["id"] for x in taxa]
            else:
                taxa_ids = ["NCBITaxon:1"]
            for taxa_id in taxa_ids:
                config = SubsetValidationConfig(
                    subset_name=subset["id"], ic_score_adapter_name=f"amigo:{taxa_id}"
                )
                configs.append(config)
                logging.info(f"Loaded config for {subset['id']} with {taxa_id}")
    else:
        if terms:
            entities = list(query_terms_iterator(terms, impl))
        else:
            raise ValueError("No terms provided")

        config = SubsetValidationConfig(
            subset_terms=entities,
        )
        configs = [config]
    for config in configs:
        if information_content_adapter:
            config.ic_score_adapter_name = information_content_adapter
        actual_predicates = process_predicates_arg(predicates, impl=impl)
        if actual_predicates:
            config.predicates = actual_predicates
        if exclude_query:
            config.exclude_terms = list(query_terms_iterator(exclude_query.split(" "), impl))
        import oaklib.utilities.subsets.subset_validator as subset_validator

        try:
            result = subset_validator.validate_subset(impl, config)
        except Exception as e:
            logging.error(e)
            continue
        if isinstance(writer, StreamingCsvWriter):
            # denormalize
            obj = result.model_dump()
            for k in ["overall", "sibling_pairs", "ancestor_pairs", "leaf_pairs"]:
                v = obj.get(k)
                del obj[k]
                for k2, v2 in v.items():
                    obj[f"{k}_{k2}"] = v2
            writer.emit_obj(obj)
        else:
            writer.emit_obj(result)
    writer.finish()


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
def cache_ls():
    """
    List the contents of the pystow oaklib cache.

    """
    units = ["B", "KB", "MB", "GB", "TB"]
    for path, size, mtime in FILE_CACHE.get_contents(subdirs=True):
        i = 0
        while size > 1024 and i < len(units) - 1:
            size /= 1024
            i += 1
        click.echo(f"{path} ({size:.2f} {units[i]}, {mtime:%Y-%m-%d})")


@main.command()
@click.option(
    "--days-old",
    default=100,
    show_default=True,
    type=click.INT,
    help="Clear anything more than this number of days old",
)
def cache_clear(days_old: int):
    """
    Clear the contents of the pystow oaklib cache.

    """

    for name, _, age in FILE_CACHE.clear(subdirs=False, older_than=days_old, pattern="*.db*"):
        click.echo(f"Deleted {name} which was {age.days} days old")


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
@click.option(
    "--ensure-strict-prefixes/--no-ensure-strict-prefixes",
    default=False,
    show_default=True,
    help="Clean prefix map and mappings before generating an output.",
)
@click.option(
    "--exclude-mapped/--no-exclude-mapped",
    default=False,
    show_default=True,
    help="Return only mappings for subjects that have not been mapped",
)
@click.option(
    "--add-pipeline-step",
    multiple=True,
    help="E.g. WordOrderNormalization",
)
@output_option
@click.argument("terms", nargs=-1)
def lexmatch(
    output,
    recreate,
    ensure_strict_prefixes,
    rules_file,
    lexical_index_file,
    add_labels,
    add_pipeline_step,
    terms,
    exclude_mapped,
):
    """
    Performs lexical matching between pairs of terms in one more more ontologies.

    Examples
    -
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

    - https://incatools.github.io/ontology-access-kit/packages/src/oaklib.utilities.lexical.lexical_indexer.html#
    module-oaklib.utilities.lexical.lexical_indexer

    """
    impl = settings.impl
    if rules_file:
        ruleset = load_mapping_rules(rules_file)
    else:
        ruleset = None
    prefix_map = impl.prefix_map()

    # if exclude_tokens:
    #     token_exclusion_list = get_exclusion_token_list(exclude_tokens)

    if not isinstance(impl, BasicOntologyInterface):
        raise NotImplementedError(f"Cannot execute this using {impl} of type {type(impl)}")
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
        logging.info(f"Synonymizer rules: {syn_rules}")
        ix = create_lexical_index(
            impl,
            synonym_rules=syn_rules,
            add_steps=list(add_pipeline_step) if add_pipeline_step else None,
        )
    if lexical_index_file:
        if recreate:
            logging.info("Saving index")
            save_lexical_index(ix, lexical_index_file)
    logging.info(f"Generating mappings from {len(ix.groupings)} groupings")
    # TODO: abstract this way from serialization format
    msdf = lexical_index_to_sssom(
        impl,
        ix,
        ruleset=ruleset,
        subjects=subjects,
        objects=objects,
        prefix_map=prefix_map,
        ensure_strict_prefixes=ensure_strict_prefixes,
    )
    # TODO: coordinate with sssom-py to have simpler ways of filtering, no reliance on pandas
    if exclude_mapped and not msdf.df.empty:
        if not isinstance(impl, MappingProviderInterface):
            raise ValueError(f"{type(impl)} does not implement MappingProviderInterface")
        df = msdf.df
        subjects = set(df["subject_id"])
        existing_mappings = list(impl.sssom_mappings(subjects))
        pairs = [(m.subject_id, m.object_source) for m in existing_mappings]
        pairs += [(m.object_id, m.subject_source) for m in existing_mappings]
        # filter df by pairs
        df = df[
            df.apply(lambda x: (x["subject_id"], x["object_id"].split(":")[0]) not in pairs, axis=1)
        ]
        df = df[
            df.apply(lambda x: (x["object_id"], x["subject_id"].split(":")[0]) not in pairs, axis=1)
        ]
        msdf.df = df
    sssom_writers.write_table(msdf, output)


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
        other_impl = get_adapter(other_ontology)
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
@click.option(
    "--change-type",
    multiple=True,
    help="filter by KGCL change type (e.g. 'ClassCreation', 'EdgeDeletion')",
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
    change_type,
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
    other_impl = get_adapter(other_ontology)
    config = DiffConfiguration(simple=simple)
    if group_by_obo_namespace:
        config.group_by_property = HAS_OBO_NAMESPACE
    if group_by_defined_by:
        config.group_by_property = IS_DEFINED_BY
    if group_by_prefix:
        config.group_by_property = PREFIX_PREDICATE
    if group_by_property:
        if config.group_by_property:
            logging.warning(
                f"Duplicative setting of property {group_by_property} and {config.group_by_property}"
            )
            if config.group_by_property != group_by_property:
                raise ValueError(
                    f"Cannot set both {config.group_by_property} and {group_by_property}"
                )
        config.group_by_property = group_by_property
    if not isinstance(impl, DifferInterface):
        raise NotImplementedError
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
        if isinstance(writer, StreamingMarkdownWriter):
            for change_type, changes in impl.grouped_diff(other_impl, configuration=config):
                writer.emit({change_type: changes}, other_impl=other_impl)
        else:
            for change in impl.diff(other_impl, configuration=config):
                writer.emit(change)
    writer.finish()


@main.command()
@click.option("--output", "-o")
@click.option("--changes-output", help="output file for KGCL changes")
@click.option("--changes-input", type=click.File(mode="r"), help="Path to an input changes file")
@click.option("--changes-format", help="Format of the changes file (json or kgcl)")
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    show_default=True,
    help="if true, only perform the parse of KCGL and do not apply",
)
@click.option(
    "--expand/--no-expand",
    default=True,
    show_default=True,
    help="if true, expand complex changes to atomic changes",
)
@click.option(
    "--ignore-invalid-changes/--no-ignore-invalid-changes",
    default=False,
    show_default=True,
    help="if true, ignore invalid changes, e.g. obsoletions of dependent entities",
)
@click.option("--contributor", help="CURIE for the person contributing the patch")
@output_type_option
@overwrite_option
@click.argument("commands", nargs=-1)
def apply(
    commands,
    output,
    output_type,
    changes_input: TextIO,
    changes_format,
    changes_output,
    contributor: str,
    ignore_invalid_changes: bool,
    dry_run: bool,
    expand: bool,
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

    Warning:

    This command is still experimental. Some things to bear in mind:

    - for some ontologies, CURIEs may not work, instead specify a full URI surrounded by <>s
    - only a subset of KGCL commands are supported by each backend

    """
    impl = settings.impl
    configuration = kgcl.Configuration()
    if isinstance(impl, PatcherInterface):
        impl.autosave = settings.autosave
        impl.ignore_invalid_changes = ignore_invalid_changes
        changes = []
        files = []
        if changes_input:
            files.append(changes_input)
        for command in commands:
            if command == "-":
                files.append(sys.stdin)
            else:
                logging.info(f"Parsing: {command}")
                change = kgcl_parser.parse_statement(command)
                logging.info(f"parsed {command} == {change}")
                changes.append(change)
        changes += list(parse_kgcl_files(files, changes_format))
        applied_changes = []
        for change in changes:
            if expand:
                expanded_changes = impl.expand_changes([change], configuration=configuration)
            else:
                expanded_changes = [change]
            for expanded_change in expanded_changes:
                if contributor:
                    if expanded_change.contributor and expanded_change.contributor != contributor:
                        raise ValueError(
                            f"Cannot set contributor to {contributor} existing value = {expanded_change.contributor}"
                        )
                    expanded_change.contributor = contributor
                logging.info(f"Change: {expanded_change}")
                if dry_run:
                    logging.info(f"Skipping application of change: {change}")
                else:
                    impl.apply_patch(expanded_change)
            applied_changes.append(expanded_change)
        if dry_run or changes_output:
            write_kgcl(changes, changes_output, changes_format)
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
@click.option(
    "--expand/--no-expand",
    default=True,
    show_default=True,
    help="if true, expand complex changes to atomic changes",
)
@click.option(
    "--ignore-invalid-changes/--no-ignore-invalid-changes",
    default=False,
    show_default=True,
    help="if true, ignore invalid changes, e.g. obsoletions of dependent entities",
)
@output_type_option
@click.argument("terms", nargs=-1)
def apply_obsolete(output, output_type, expand: bool, terms, **kwargs):
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
    if not isinstance(impl, PatcherInterface):
        raise NotImplementedError
    impl.autosave = settings.autosave
    for k, v in kwargs.items():
        setattr(impl, k, v)
    for term in query_terms_iterator(terms, impl):
        change = kgcl.NodeObsoletion(id=generate_change_id(), about_node=term)
        if expand:
            changes = impl.expand_change(change)
        else:
            changes = [change]
        for change in changes:
            impl.apply_patch(change)
    if not settings.autosave and not output:
        logging.warning("--autosave not passed, changes are NOT saved")
    if output:
        if output == "-":
            output = sys.stdout
        impl.dump(output, output_type)


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
@click.option(
    "--bidirectional/--no-bidirectional",
    default=True,
    show_default=True,
    help="Show diff from both left and right perspectives",
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
    bidirectional: bool,
    output_type,
    output,
    terms,
):
    """
    Calculates cross-ontology diff using mappings

    Given a pair of ontologies, and mappings that connect terms in both ontologies, this
    command will perform a structural comparison of all mapped pairs of terms

    Example:

        runoak -i sqlite:obo:uberon diff-via-mappings --other-input sqlite:obo:zfa  --source UBERON --source ZFA -O csv

    Note the above command does not have any mapping file specified; the mappings that are distributed within
    each ontology is used (in this case, Uberon contains mappings to ZFA)

    If the mappings are provided externally:

        runoak -i ont1.obo diff-via-mappings --other-input ont2.obo --mapping-input mappings.sssom.tsv

    (in the above example, --source is not passed, so all mappings are tested)

    If there are no existing mappings, you can use the lexmatch command to generate them:

        runoak -i ont1.obo diff-via-mappings -a ont2.obo lexmatch -o mappings.sssom.tsv

        runoak -i ont1.obo diff-via-mappings --other-input ont2.obo --mapping-input mappings.sssom.tsv

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
            other_oi = get_adapter(other_input, format=other_input_type)
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
    actual_predicates = process_predicates_arg(predicates, impl=oi)
    n = 0
    for r in calculate_pairwise_relational_diff(
        oi,
        other_oi,
        sources=sources,
        entities=entities,
        mappings=mappings,
        add_labels=autolabel,
        include_identity_mappings=include_identity_mappings,
        predicates=actual_predicates,
        bidirectional=bidirectional,
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
@click.option(
    "--schema",
    help=(
        "Path to linkml schema. "
        "This is used to infer which fields are identifiers and which are dependent columns, e.g labels"
    ),
)
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
@click.option(
    "--fields-to-label",
    help="Comma-separated list of field names for identifiers which should be labeled.",
)
@click.option(
    "--autolabel/--no-autolabel",
    default=False,
    show_default=True,
    help="Autolabel columns",
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
    fields_to_label: str,
    autolabel: bool,
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
        if autolabel:
            hdr = input_table[0]
            for col in list(hdr.keys()):
                if col.endswith("_id"):
                    hdr[col.replace("_id", "_label")] = None
        if schema:
            metadata = tf.extract_metadata_from_linkml(schema)
        elif relation or relation_file or fields_to_label:
            metadata = TableMetadata(dependencies=[])
            if relation_file:
                for d_args in yaml.safe_load(relation_file):
                    metadata.dependencies.append(ColumnDependency(**d_args))
            for d_str in list(relation):
                d_args = yaml.safe_load(d_str)
                if "relation" not in d_args:
                    d_args["relation"] = "label"
                if "dependent_column" not in d_args:
                    d_args["dependent_column"] = d_args["primary_key"] + "_label"
                metadata.dependencies.append(ColumnDependency(**d_args))
            if fields_to_label:
                for field in fields_to_label.split(","):
                    metadata.dependencies.append(
                        ColumnDependency(
                            primary_key=field, dependent_column=field + "_label", relation="label"
                        )
                    )
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
@click.pass_context
def synonymize(ctxt, **kwargs):
    """Deprecated: use generate-synonyms"""
    logging.warning("This command has been renamed to generate-synonyms")
    ctxt.forward(generate_synonyms)


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--rules-file",
    "-R",
    required=True,
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
    help="Path to where patch file will be written.",
)
@click.option(
    "--patch-format",
    help="Output syntax for patches.",
)
@output_option
@output_type_option
def generate_synonyms(terms, rules_file, apply_patch, patch, patch_format, output, output_type):
    """
    Generate synonyms based on a set of synonymizer rules.

    If the `--apply-patch` flag is set, the output will be an ontology file with the changes
    applied. Pass the `--patch` argument to lso get the patch file in KGCL format.

    Example:

        runoak -i foo.obo generate-synonyms -R foo_rules.yaml --patch patch.kgcl --apply-patch -o foo_syn.obo

    If the `apply-patch` flag is NOT set then the main input will be KGCL commands

    Example:

        runoak -i foo.obo generate-synonyms -R foo_rules.yaml -o changes.kgcl

    see https://github.com/INCATools/kgcl.

    """
    impl = settings.impl
    if apply_patch:
        writer = _get_writer(patch_format, impl, StreamingKGCLWriter, kgcl)
        writer.output = patch
    else:
        writer = _get_writer(output_type, impl, StreamingKGCLWriter, kgcl)
        writer.output = output
    ruleset = synonymizer_datamodel.RuleSet(**yaml.safe_load(open(rules_file)))
    change_list = []
    curie_iter = query_terms_iterator(terms, impl)
    for change in synonymizer.apply_synonymizer_to_terms(impl, curie_iter, ruleset):
        change_list.append(change)
        writer.emit(change)

    writer.finish()
    if apply_patch and len(change_list) > 0:
        if output:
            impl.resource.slug = output
        _apply_changes(impl, change_list)


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--rules-file",
    "-R",
    help="path to rules file. Conforms to rules_datamodel.\
        e.g. https://github.com/INCATools/ontology-access-kit/blob/main/tests/input/matcher_rules.yaml",
)
@click.option(
    "--rules-expression",
    "-Y",
    multiple=True,
    help="YAML encoding of a rules expression",
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
    help="Path to where patch file will be written.",
)
@click.option(
    "--patch-format",
    help="Output syntax for patches.",
)
@output_option
@output_type_option
def generate_lexical_replacements(
    terms, rules_file, rules_expression, apply_patch, patch, patch_format, output, output_type
):
    """
    Generate lexical replacements based on a set of synonymizer rules.


    If the `--apply-patch` flag is set, the output will be an ontology file with the changes
    applied. Pass the `--patch` argument to lso get the patch file in KGCL format.

    Example:


        runoak -i foo.obo generate-lexical-replacements -R foo_rules.yaml\
           --patch patch.kgcl --apply-patch -o foo_syn.obo

    If the `apply-patch` flag is NOT set then the main input will be KGCL commands

    Example:


        runoak -i foo.obo generate-lexical-replacements -R foo_rules.yaml -o changes.kgcl


    You can also pass the expressions directly as YAML

    Example:


        runoak -i foo.obo generate-lexical-replacements \
          -Y '{match: "nuclear (\\w+)", replacement: "\\1 nucleus"}' .all

    see https://github.com/INCATools/kgcl.

    Note: this command is very similar to generate-synonyms, but the main use case here
    is replacing terms, and applying rules to other elements such as definitions

    """
    impl = settings.impl
    if apply_patch:
        writer = _get_writer(patch_format, impl, StreamingKGCLWriter, kgcl)
        writer.output = patch
    else:
        writer = _get_writer(output_type, impl, StreamingKGCLWriter, kgcl)
        writer.output = output
    if rules_file:
        ruleset = synonymizer_datamodel.RuleSet(**yaml.safe_load(open(rules_file)))
    elif rules_expression:
        ruleset = synonymizer_datamodel.RuleSet()
        for rule_expression in rules_expression:
            rule = synonymizer_datamodel.Synonymizer(**yaml.safe_load(rule_expression))
            ruleset.rules.append(rule)
    else:
        raise ValueError("Must specify either --rules-file or --rules-expression")
    change_list = []
    curie_iter = query_terms_iterator(terms, impl)
    for change in synonymizer.apply_synonymizer_to_terms(
        impl, curie_iter, ruleset, include_all=True
    ):
        change_list.append(change)
        writer.emit(change)

    writer.finish()
    if apply_patch and len(change_list) > 0:
        if output:
            impl.resource.slug = output
        _apply_changes(impl, change_list)


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--style-hints",
    help="Description of style for definitions",
)
@click.option(
    "--apply-patch/--no-apply-patch",
    default=False,
    show_default=True,
    help="Apply KGCL syntax.",
)
@click.option(
    "--patch",
    type=click.File(mode="w"),
    default=sys.stdout,
    help="Path to where patch file will be written.",
)
@click.option(
    "--patch-format",
    help="Output syntax for patches.",
)
@click.option(
    "--exclude-defined/--no-exclude-defined",
    default=False,
    show_default=True,
    help="Exclude terms that already have definitions",
)
@output_option
@output_type_option
def generate_definitions(
    terms, apply_patch, patch, patch_format, output, output_type, exclude_defined, **kwargs
):
    """
    Generate definitions for a term or terms.

    Currently this only works with the llm extension.

    Example:

        runoak -i llm:sqlite:obo:foodon generate-definitions FOODON:03315258

    The --style-hints option can be used to provide hints to the definition generator.

    Example:

        runoak -i llm:sqlite:obo:foodon generate-definitions FOODON:03315258 \
          --style-hints "Write the definition in the style of a pretentious food critic"

    Generates:

        "The pancake, a humble delight in the realm of breakfast fare,
        presents itself as a delectable disc of gastronomic delight..."

    """
    impl = settings.impl
    if apply_patch:
        writer = _get_writer(patch_format, impl, StreamingKGCLWriter, kgcl)
        writer.output = patch
    else:
        writer = _get_writer(output_type, impl, StreamingKGCLWriter, kgcl)
        writer.output = output
    if not isinstance(impl, OntologyGenerationInterface):
        raise NotImplementedError
    all_terms = list(query_terms_iterator(terms, impl))
    logging.info(f"Generating definitions for {len(all_terms)} terms")
    if exclude_defined:
        exclusion_list = [x[0] for x in impl.definitions(all_terms)]
        logging.info(f"Excluding {len(exclusion_list)} terms that already have definitions")
        all_terms = list(set(all_terms) - set(exclusion_list))
    logging.info(f"Generating definitions for final list of {len(all_terms)} terms")
    curie_defns = impl.generate_definitions(all_terms, **kwargs)
    change_list = []
    for curie, defn in curie_defns:
        change = kgcl.NewTextDefinition(
            id="kgcl_change_id_" + str(curie),
            about_node=curie,
            new_value=defn.val,
        )
        change_list.append(change)
        writer.emit(change)
    writer.finish()
    if apply_patch and len(change_list) > 0:
        if output:
            impl.resource.slug = output
        _apply_changes(impl, change_list)


@main.command()
@click.argument("terms", nargs=-1)
@click.option(
    "--patterns-file",
    "-P",
    multiple=True,
    help="path to patterns file",
)
@click.option(
    "--show-extract/--no-show-extract",
    default=False,
    show_default=True,
    help="Show the original extracted object.",
)
@click.option(
    "--parse/--no-parse",
    default=True,
    show_default=True,
    help="Parse the input terms according to the patterns.",
)
@click.option(
    "--fill/--no-fill",
    default=False,
    show_default=True,
    help="If true, fill in descendant logical definitions.",
)
@click.option(
    "--analyze/--no-analyze",
    default=False,
    show_default=True,
    help="Analyze consistency of logical definitions (in progress).",
)
@click.option(
    "--unmelt/--no-unmelt",
    default=False,
    show_default=True,
    help="Use a wide table for display.",
)
@autolabel_option
@output_option
@output_type_option
def generate_logical_definitions(
    terms, patterns_file, show_extract, unmelt, autolabel, parse, fill, analyze, output, output_type
):
    """
    Generate logical definitions based on patterns file.
    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, kgcl)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError
    curies = list(query_terms_iterator(terms, impl))
    pattern_collection = None
    for pf in patterns_file:
        if pattern_collection is None:
            pattern_collection = patternizer.load_pattern_collection(pf)
        else:
            pattern_collection.patterns.extend(patternizer.load_pattern_collection(pf).patterns)
    if show_extract:
        results = patternizer.lexical_pattern_instances(impl, pattern_collection.patterns, curies)
        # label_fields = []
        if unmelt:
            results = patternizer.as_matrix(results, pattern_collection)
            # label_fields = [p.name for p in pattern_collection.patterns]
        for result in results:
            if isinstance(result, BaseModel):
                result = result.dict()
            writer.emit(result)
    else:
        label_fields = [
            "definedClassId",
            "genusIds",
            "restrictionFillerIds",
            "restrictionsPropertyIds",
            "restrictionsFillerIds",
        ]
        if parse:
            if not pattern_collection:
                raise ValueError("Must specify -P if --parse is set")
            results = patternizer.lexical_pattern_instances(
                impl, pattern_collection.patterns, curies
            )
            ldefs = list(patternizer.as_logical_definitions(results))
        else:
            ldefs = list(impl.logical_definitions(curies))
        if fill:
            for ldef in ldefs:
                for (
                    filled_ldef
                ) in logical_definition_analyzer.generate_descendant_logical_definitions(
                    impl, ldef
                ):
                    writer.emit(filled_ldef, label_fields=label_fields)
        if analyze:
            logging.warning("Analyzing logical definitions is incomplete")
            reports = logical_definition_analyzer.analyze_logical_definitions(impl, ldefs)
            for report in reports:
                print(report)
        if unmelt:
            ldef_flattener = LogicalDefinitionFlattener(
                labeler=lambda x: impl.label(x), curie_converter=impl.converter
            )
            writer.heterogeneous_keys = True
            for ldef in ldefs:
                flat_obj = ldef_flattener.convert(ldef)
                writer.emit(flat_obj, label_fields=list(flat_obj.keys()))
        else:
            for ldef in ldefs:
                writer.emit(ldef, label_fields=label_fields)
    writer.finish()
    writer.file.close()


@main.command()
@click.argument("terms", nargs=-1)
@autolabel_option
@output_option
@predicates_option
@output_type_option
@click.option(
    "--min-descendants",
    "-M",
    default=3,
    show_default=True,
    help="Minimum number of descendants for a class to have to be considered a candidate.",
)
@click.option(
    "--exclude-existing/--no-exclude-existing",
    default=True,
    show_default=True,
    help="Do not report duplicates with existing disjointness axioms.",
)
def generate_disjoints(
    terms,
    predicates,
    autolabel,
    output,
    output_type,
    exclude_existing,
    min_descendants,
):
    """
    Generate candidate disjointness axioms.

    Example:

        runoak -i sqlite:obo:iao generate-disjoints -O obo

    To generate spatial disjointness axioms:

        runoak -i sqlite:obo:zfa generate-disjoints -O obo p i,p

    """
    impl = settings.impl
    writer = _get_writer(output_type, impl, StreamingYamlWriter, kgcl)
    writer.output = output
    writer.autolabel = autolabel
    if not isinstance(impl, OboGraphInterface):
        raise NotImplementedError
    curies = list(query_terms_iterator(terms, impl))
    actual_predicates = process_predicates_arg(predicates, impl=impl)
    if not actual_predicates:
        actual_predicates = [IS_A]
    config = DisjointnessInducerConfig(
        min_descendants=min_descendants, exclude_existing=exclude_existing
    )
    dxas = generate_disjoint_class_expressions_axioms(
        impl, curies, [actual_predicates], config=config
    )
    label_fields = [
        "classIds",
        "classExpressionPropertyIds",
        "classExpressionFillerIds",
        "unionEquivalentToFillerId",
        "unionEquivalentToPropertyId",
    ]
    for dxa in dxas:
        writer.emit(dxa, label_fields=label_fields)
    writer.finish()
    writer.file.close()


if __name__ == "__main__":
    main()
