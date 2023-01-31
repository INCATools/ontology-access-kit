import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, TextIO, Union, Optional, List

import click
import sssom_schema as sssom

from oaklib.datamodels.mapping_cluster_datamodel import (
    MappingCluster,
    MappingClusterReport,
)
from oaklib.parsers.boomer_parser import BoomerParser
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter
from sssom.constants import SEMAPV


logger = logging.getLogger(__name__)


@dataclass
class BoomerEngine:
    """
    Wrapper around boomer results.

    Currently this only allows conversion and filtering of SSSOM
    """

    report: Optional[MappingClusterReport] = None
    _mappings: Optional[List[sssom.Mapping]] = None

    def mappings(self, minimum_confidence: Optional[float] = None, maximum_confidence: Optional[float] = None, best_first: Optional[bool] = None) -> Iterator[sssom.Mapping]:
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

    def load(self, path: Union[TextIO, Path, str]) -> MappingClusterReport:
        if isinstance(path, Path):
            path = str(path)
        if isinstance(path, str):
            with open(path) as f:
                return self.load(f)
        bp = BoomerParser()
        clusters = list(bp.parse(path))
        self.report = MappingClusterReport(clusters=clusters)
        return self.report


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Run the ValueSet CLI."""
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
@click.option("--minimum-confidence",
              "-L",
              type=click.FLOAT,
              help="Do not show mappings with lower confidence")
@click.option("--maximum-confidence",
              "-H",
              type=click.FLOAT,
              help="Do not show mappings with higher confidence")
@click.argument("input_report")
def export(input_report, **kwargs):
    """
    Exports mappings from a boomer report.

    boomerang export tests/input/boomer-example.md
    """
    ben = BoomerEngine()
    ben.load(input_report)
    writer = StreamingSssomWriter()
    for m in ben.mappings(**kwargs):
        writer.emit(m)


if __name__ == "__main__":
    main()
