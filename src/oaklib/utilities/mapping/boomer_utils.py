import logging
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, Iterator, List, Optional, TextIO, Tuple, Union

import click
import sssom_schema as sssom
import yaml
from linkml_renderer.style.model import RenderRule
from sssom.constants import SEMAPV, SKOS_EXACT_MATCH

from oaklib import get_implementation_from_shorthand
from oaklib.cli import _get_writer, output_option, output_type_option
from oaklib.datamodels import mapping_cluster_datamodel
from oaklib.datamodels.mapping_cluster_datamodel import (
    MappingCluster,
    MappingClusterReport,
)
from oaklib.datamodels.vocabulary import HAS_DBXREF, SKOS_CLOSE_MATCH
from oaklib.interfaces import MappingProviderInterface
from oaklib.io.html_writer import HTMLWriter
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.io.streaming_yaml_writer import StreamingYamlWriter
from oaklib.parsers.boomer_parser import BoomerParser
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter

logger = logging.getLogger(__name__)

PAIR = Tuple[CURIE, CURIE]
MAPPING_SP_INDEX = Dict[PAIR, List[sssom.Mapping]]


class DiffType(Enum):
    OK = "OK"
    AMBIGUOUS = "AMBIGUOUS"
    NEW = "NEW"
    CONFLICT = "CONFLICT"
    REJECT = "REJECT"


MAPPING_DIFF = Tuple[DiffType, PRED_CURIE, sssom.Mapping, Optional[float]]


def _predicate_ids(mappings: List[sssom.Mapping]) -> List[CURIE]:
    return list(set([m.predicate_id for m in mappings]))


def _satisfies(c, minimum_confidence: Optional[float], maximum_confidence: Optional[float]) -> bool:
    conf = c.confidence
    if minimum_confidence is not None and conf < minimum_confidence:
        return False
    if maximum_confidence is not None and conf > maximum_confidence:
        return False
    return True


@dataclass
class BoomerEngine:
    """
    Wrapper around boomer results.

    Currently this only allows conversion and filtering of SSSOM
    """

    report: Optional[MappingClusterReport] = None
    _mappings: Optional[List[sssom.Mapping]] = None
    _mappings_by_sp: Optional[MAPPING_SP_INDEX] = None
    _parsed_curie_label_map: Optional[Dict[str, str]] = None

    def mappings(
        self,
        minimum_confidence: Optional[float] = None,
        maximum_confidence: Optional[float] = None,
        best_first: Optional[bool] = None,
    ) -> Iterator[sssom.Mapping]:
        """
        Yield all mappings that match the confidence threshold criteria.

        :param minimum_confidence: set this to only retrieve mappings with high confidence
        :param maximum_confidence: set this to retrieve low confidence mappings, for QC purposes
        :return:
        """
        if self._mappings is None:
            self._mappings = []
            for cluster in self.report.clusters:
                self._mappings.extend(list(self.cluster_to_mappings(cluster)))
        mappings = self._mappings
        if best_first is not None:
            mappings = list(self._mappings)
            if best_first:
                sorted(mappings, key=lambda m: -m.confidence)
            else:
                sorted(mappings, key=lambda m: m.confidence)
        for m in mappings:
            conf = m.confidence
            if minimum_confidence is not None and conf < minimum_confidence:
                continue
            if maximum_confidence is not None and conf > maximum_confidence:
                continue
            yield m

    def cluster_to_mappings(self, cluster: MappingCluster):
        justification = sssom.EntityReference(SEMAPV.CompositeMatching.value)
        for sm in cluster.resolved_mappings:
            m = sssom.Mapping(
                subject_id=sm.subject_id,
                subject_label=sm.subject_label,
                predicate_id=sm.predicate_id,
                object_id=sm.object_id,
                object_label=sm.object_label,
                confidence=sm.confidence,
                mapping_justification=justification,
            )
            yield m

    def filter(
        self,
        minimum_confidence: Optional[float] = None,
        maximum_confidence: Optional[float] = None,
        best_first: Optional[bool] = None,
    ) -> MappingClusterReport:
        report = copy(self.report)
        clusters = report.clusters
        if best_first is not None:
            if best_first:
                clusters = sorted(clusters, key=lambda m: -m.confidence)
            else:
                clusters = sorted(clusters, key=lambda m: m.confidence)
        report.clusters = [
            c for c in clusters if _satisfies(c, minimum_confidence, maximum_confidence)
        ]
        return report

    def load(
        self, path: Union[TextIO, Path, str], prefix_map: Dict[str, str] = None
    ) -> MappingClusterReport:
        if isinstance(path, Path):
            path = str(path)
        if isinstance(path, str):
            with open(path) as f:
                return self.load(f, prefix_map=prefix_map)
        bp = BoomerParser(prefix_map=prefix_map)
        clusters = list(bp.parse(path))
        self._parsed_curie_label_map = bp._curie_label_map
        self.report = MappingClusterReport(clusters=clusters)
        return self.report

    def index_mappings(
        self, mappings: List[sssom.Mapping], max_per_pair: Optional[int] = None
    ) -> MAPPING_SP_INDEX:
        mix: MAPPING_SP_INDEX = defaultdict(list)
        for m in mappings:
            pair = (m.subject_id, m.object_id)
            mix[pair].append(m)
            if max_per_pair is not None and len(mix[pair]) > max_per_pair:
                raise ValueError(f"Too many for {pair} => {mix[pair]}")
        return mix

    def compare(
        self,
        current_mappings: List[sssom.Mapping],
        minimum_confidence: Optional[float] = 0.95,
        reject_non_exact=False,
        promote_xref_to_exact=False,
        discard_new_close_matches=True,
    ) -> Iterator[MAPPING_DIFF]:
        """
        Compares a set of pre-existing mappings with boomer resolved mappings.

        :param current_mappings: source mappings to evaluate
        :param minimum_confidence: any boomer resolved mapping that has confidence beneath this is ignored
        :param reject_non_exact: if True, then any mapping that matches a confident resolved mapping is typed REJECT
        :param promote_xref_to_exact: if True, then any xref in the source is treated as skos:exactMatch
        :param discard_new_close_matches: if True, then do not suggest NEW lines for high confidence closeMatch
        :return:
        """
        boomer_mapping_ix = self.index_mappings(
            list(self.mappings(minimum_confidence=minimum_confidence)), max_per_pair=1
        )
        current_mapping_ix = self.index_mappings(current_mappings)
        for pair, mappings in boomer_mapping_ix.items():
            [bm] = mappings
            boomer_pred_id = bm.predicate_id
            if pair in current_mapping_ix:
                current_mappings_for_pair = current_mapping_ix[pair]
                if len(current_mappings_for_pair) > 1:
                    for m in current_mappings_for_pair:
                        m.subject_label = self._parsed_curie_label_map[m.subject_id]
                        m.object_label = self._parsed_curie_label_map[m.object_id]
                        yield DiffType.AMBIGUOUS, None, m, None
                for m in current_mappings_for_pair:
                    m.subject_label = self._parsed_curie_label_map[m.subject_id]
                    m.object_label = self._parsed_curie_label_map[m.object_id]
                    if promote_xref_to_exact and m.predicate_id == HAS_DBXREF:
                        m = copy(m)
                        m.predicate_id = SKOS_EXACT_MATCH
                    if m.predicate_id == boomer_pred_id:
                        yield DiffType.OK, None, m, bm.confidence
                    else:
                        if reject_non_exact and bm.predicate_id != SKOS_EXACT_MATCH:
                            yield DiffType.REJECT, bm.predicate_id, m, bm.confidence
                        else:
                            yield DiffType.CONFLICT, bm.predicate_id, m, bm.confidence
            else:
                if reject_non_exact and bm.predicate_id != SKOS_EXACT_MATCH:
                    continue
                if discard_new_close_matches and bm.predicate_id == SKOS_CLOSE_MATCH:
                    continue
                yield DiffType.NEW, None, bm, bm.confidence


min_confidence_option = click.option(
    "--minimum-confidence",
    "-L",
    type=click.FLOAT,
    help="Do not show mappings with lower confidence",
)
max_confidence_option = click.option(
    "--maximum-confidence",
    "-H",
    type=click.FLOAT,
    help="Do not show mappings with higher confidence",
)
best_first_option = click.option(
    "--best-first/--no-best-first",
    default=True,
    show_default=True,
    help="Sort by highest confidence first",
)

global_prefix_map = {}


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.option(
    "--prefix-map",
    help="curie prefix map",
)
def main(verbose: int, quiet: bool, prefix_map):
    """Run the ValueSet CLI."""
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)
    if prefix_map:
        with open(prefix_map) as f:
            global global_prefix_map
            global_prefix_map = yaml.safe_load(f)


@main.command()
@min_confidence_option
@max_confidence_option
@click.argument("input_report")
def mappings(input_report, **kwargs):
    """
    Exports mappings from a boomer report.

    Example:
    -------
        boomerang mappings tests/input/boomer-example.md

    To filter by confidence:

        boomerang mappings tests/input/boomer-example.md -L 0.8

    """
    ben = BoomerEngine()
    ben.load(input_report, prefix_map=global_prefix_map)
    writer = StreamingSssomWriter()
    for m in ben.mappings(**kwargs):
        writer.emit(m)
    writer.finish()


@main.command()
@min_confidence_option
@max_confidence_option
@best_first_option
@output_option
@output_type_option
@click.argument("input_report")
def report(input_report, output, output_type, **kwargs):
    """
    Renders a report performing optional filtering and sorting

    Passing no options will just generate the input report in the desired format.

    Example:
    -------
        boomerang report tests/input/boomer-example.md  report.yaml

    The generic LinkML rendered can be used:

    Example:
    -------
        boomerang report tests/input/boomer-example.md -O html -o report.html

    To show the lowest confidence first:

        boomerang report tests/input/boomer-example.md --no-best-first

    """
    ben = BoomerEngine()
    ben.load(input_report, prefix_map=global_prefix_map)
    writer = _get_writer(
        output_type, None, StreamingYamlWriter, datamodel=mapping_cluster_datamodel
    )
    writer.output = output
    if isinstance(writer, HTMLWriter):
        writer.render_rules = [
            RenderRule(applies_to_slots=["clusters"], render_as="description_list")
        ]
    report = ben.filter(**kwargs)
    writer.emit(report)
    writer.finish()


@main.command()
@click.option("--input-ontology", "-i", help="ontology from which to retrieve mappings")
@click.option(
    "--reject-non-exact/--no-reject-non-exact",
    help="if set then any match to a high confidence boomer interpretation that is a reject.",
)
@click.option(
    "--promote-xref-to-exact/--no-promote-xref-to-exact",
    help="if set then any xref in the source is promoted to an EXACT.",
)
@min_confidence_option
@click.argument("input_report")
def compare(input_report, input_ontology: str, **kwargs):
    """
    Compares boomer results with existing mappings.

    This assumes boomer has been executed in advance, and a markdown report generated.
    Pass in as an argument the same ontology used in the boomer run.

    Example:
    -------
        boomerang compare foo-boomer.md -i foo.db

    For any mapping marked NEW, this can be incorporated into the ontology.

    For any mapping marked CONFLICT, there is some action that needs to be taken

    By default any boomer resolved mapping beneath the default minimum confidence is ignored.
    To customize, e.g. stringent:

    Example:
    -------
        boomerang compare foo-boomer.md -i foo.db -L 0.999

    For each high confidence boomer mapping, this is compared against current mappings and
    a suggestion made.

    SPECIFIC SUGGESTIONS FOR OBO ONTOLOGIES:

    In many ontologies it is conventional to (a) model all mappings as xrefs (b) assume
    a default interpretation of exactMatch.

    In these cases, we want to REJECT any existing xref IF there is a high confidence
    boomer mapping FOR ANYTHING OTHER THAN exactMatch (including SiblingOf)

    Example:
    -------
        boomerang compare foo-boomer.md -i foo.db -L 0.999 --reject-non-exact --promote-xref-to-exact

    The results here are straightforward, either REJECT, NEW, or OK

    If this is NOT your workflow, then the results may include CONFLICT lines where
    the interpretation you state is different from the interpretation in

    See https://github.com/INCATools/boomer/issues/334

    """
    writer = StreamingCsvWriter()
    adapter = get_implementation_from_shorthand(input_ontology)
    if not isinstance(adapter, MappingProviderInterface):
        raise NotImplementedError(f"{input_ontology} can't supply mappings")
    current_mappings = list(adapter.all_sssom_mappings())
    ben = BoomerEngine()
    ben.load(input_report, prefix_map=global_prefix_map)
    for md in ben.compare(current_mappings, **kwargs):
        t, info, m, conf = md
        writer.emit(
            dict(
                type=t.value,
                info=info,
                confidence=conf,
                predicate_id=m.predicate_id,
                subject_id=m.subject_id,
                subject_label=m.subject_label,
                object_id=m.object_id,
                object_label=m.object_label,
            )
        )


if __name__ == "__main__":
    main()
