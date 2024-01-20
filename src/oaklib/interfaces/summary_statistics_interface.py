import getpass
import logging
from abc import ABC
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Iterator, List

from linkml_runtime.utils.metamodelcore import XSDDateTime

from oaklib.datamodels.summary_statistics_datamodel import (
    FacetedCount,
    GroupedStatistics,
    Ontology,
    SummaryStatisticsCalculationActivity,
    SummaryStatisticsReport,
    UngroupedStatistics,
)
from oaklib.datamodels.vocabulary import IS_A, OWL_CLASS
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE

SUMMARY_STATISTICS_MAP = Dict[str, Any]


class SummaryStatisticsInterface(BasicOntologyInterface, ABC):
    """
    generates summary statistics

    Uses SummaryStatistics datamodel, see :ref:`datamodels`
    """

    include_residuals = False
    _metadata_property_summary_statistics: Dict[PRED_CURIE, Dict[Any, int]] = None

    def global_summary_statistics(
        self,
        branches: Dict[str, List[CURIE]] = None,
        group_by: PRED_CURIE = None,
        values: List[Any] = None,
        include_entailed: bool = False,
        prefixes: List[CURIE] = None,
    ) -> GroupedStatistics:
        """
        Gets summary statistics for all ontologies treated as a single ontology.

        :param branches: if provided, only statistics for the given branch roots will be returned
        :param group_by: if provided, statistics will be grouped by the values of this property
        :param values: if provided, only statistics where the group_by property value matches this will be considered
        :param include_entailed: include inference
        :param prefixes: if provided, only statistics for entities with these prefixes will be considered
        :return:
        """
        onts = list(self._ontologies())
        stats = GroupedStatistics(id=f"{onts[0].version}-statistics")
        self._add_statistics_metadata(stats)
        if group_by is not None and branches is not None:
            raise ValueError("Cannot specify both metadata_property and branches")
        if branches is not None:
            for branch_name, branch_roots in branches.items():
                logging.info(f"Getting summary statistics for branch {branch_name}")
                branch_statistics = self.branch_summary_statistics(
                    branch_name=branch_name,
                    branch_roots=branch_roots,
                    include_entailed=include_entailed,
                    parent=stats,
                    prefixes=prefixes,
                )
                stats.partitions[branch_name] = branch_statistics
        if group_by is not None:
            logging.info(f"Getting summary statistics for metadata property {group_by}")
            if values is None:
                values = list(self.metadata_property_summary_statistics(group_by).keys())
                logging.info(f"Found {len(values)} values for metadata property {group_by}")
                if self.include_residuals:
                    values += [None]
            for v in values:
                logging.info(
                    f"Getting summary statistics for metadata property {group_by} value {v}"
                )
                branch_statistics = self.branch_summary_statistics(
                    v,
                    property_values={group_by: v},
                    include_entailed=include_entailed,
                    parent=stats,
                    prefixes=prefixes,
                )
                if v is None:
                    v = "__RESIDUAL__"
                stats.partitions[v] = branch_statistics
        if group_by is None and branches is None:
            branch_statistics = self.branch_summary_statistics(
                include_entailed=include_entailed,
                parent=stats,
                prefixes=prefixes,
            )
            stats.partitions[branch_statistics.id] = branch_statistics
        return stats

    def branch_summary_statistics(
        self,
        branch_name: str = None,
        branch_roots: List[CURIE] = None,
        property_values: Dict[CURIE, Any] = None,
        include_entailed=False,
        parent: GroupedStatistics = None,
        prefixes: List[CURIE] = None,
    ) -> UngroupedStatistics:
        """
        Gets summary statistics for all ontologies treated as a single ontology.

        Note that different implementations may implement subsets of the full stats datamodel.

        :param branch_name:
        :param branch_roots: if provided, only statistics for the given branch roots will be returned
        :param property_values: if provided, only statistics for entities that match these will be considered
        :param include_entailed: if True, include statistics for entailed edges
        :param parent: set if this is a partition of a larger group
        :param prefixes: if provided, only statistics for entities with these prefixes will be considered
        :return:
        """
        if branch_name is None:
            branch_name = "AllBranches"
        if branch_roots is not None:
            if not isinstance(self, OboGraphInterface):
                raise NotImplementedError(f"branch_roots not implemented for {type(self)}")
            filtered_entities = self.descendants(branch_roots, predicates=[IS_A])
        elif property_values is not None:

            def _match(e: CURIE):
                for p, v in property_values.items():
                    if v not in self.entity_metadata_map(e).get(p, []):
                        return False
                return True

            filtered_entities = [e for e in self.entities(filter_obsoletes=False) if _match(e)]
        else:
            filtered_entities = list(self.entities(filter_obsoletes=False))
        filtered_entities = set(filtered_entities)
        logging.info(f"Getting summary statistics for branch {branch_name}")
        ssc = UngroupedStatistics(branch_name)
        if not parent:
            self._add_statistics_metadata(ssc)
        class_entities = filtered_entities.intersection(
            list(self.entities(owl_type=OWL_CLASS, filter_obsoletes=False))
        )
        obsoletes = filtered_entities.intersection(list(self.obsoletes()))
        ssc.class_count = len(class_entities)
        ssc.class_count_with_text_definitions = len(
            [c for c in class_entities if self.definition(c)]
        )
        ssc.deprecated_class_count = len(set(class_entities).intersection(obsoletes))
        rel_counts = defaultdict(int)
        if isinstance(self, OboGraphInterface):
            for r in self.relationships():
                if r[0] in filtered_entities:
                    rel_counts[r[1]] += 1
        for k, v in rel_counts.items():
            ssc.edge_count_by_predicate[k] = FacetedCount(k, filtered_count=v)
        ssc.edge_count = sum(rel_counts.values())
        synonyms = [
            s for e in filtered_entities for s in self.alias_relationships(e, exclude_labels=True)
        ]
        ssc.synonym_statement_count = len(synonyms)
        ssc.distinct_synonym_count = len(set([s[1] for s in synonyms]))
        self._add_derived_statistics(ssc)
        return ssc

    def _add_statistics_metadata(self, report: SummaryStatisticsReport):
        """
        Adds metadata to a report

        :param report:
        :return:
        """
        onts = list(self._ontologies())
        report.ontologies = onts
        report.was_generated_by = SummaryStatisticsCalculationActivity(
            was_associated_with="OAK",
            acted_on_behalf_of=getpass.getuser(),
            started_at_time=XSDDateTime(datetime.now()),
        )

    def _ontologies(self) -> Iterator[Ontology]:
        """
        Maps ontology metadata to Ontology object in stats datamodel.

        :return:
        """
        property_map = {
            "version_info": "owl:versionInfo",
            "version": "owl:versionIRI",
            "title": "dcterms:title",
            "description": "dcterms:description",
        }
        for ontology in self.ontologies():
            metadata = self.ontology_metadata_map(ontology)
            params = {}
            for slot, pred in property_map.items():
                if pred in metadata:
                    params[slot] = metadata[pred][0]
            yield Ontology(id=ontology, **params)

    def metadata_property_summary_statistics(self, metadata_property: PRED_CURIE) -> Dict[Any, int]:
        """
        Gets summary statistics for all ontologies wrapped as multiple dictionaries keyed
        by ontology CURIE

        :return:
        """
        if not self._metadata_property_summary_statistics:
            self._metadata_property_summary_statistics = defaultdict(dict)
            for e in self.entities(filter_obsoletes=False):
                for p, vs in self.entity_metadata_map(e).items():
                    for v in vs:
                        if v not in self._metadata_property_summary_statistics[p]:
                            self._metadata_property_summary_statistics[p][v] = 0
                        self._metadata_property_summary_statistics[p][v] += 1
        return self._metadata_property_summary_statistics[metadata_property]

    def _add_derived_statistics(self, ssc: UngroupedStatistics) -> None:
        """
        Adds derived statistics to the summary statistics collection

        :param ssc:
        :return:
        """
        logging.debug("Adding derived statistics")
        ssc.non_deprecated_class_count = ssc.class_count - ssc.deprecated_class_count
        ssc.class_count_without_text_definitions = (
            ssc.class_count - ssc.class_count_with_text_definitions
        )

    def summary_statistic_description(self, metric: str) -> str:
        """
        Examines the data dictionary to retrieve the definition of a metric

        Any dictionary can be used, but summary_statistics_datamodel is favored

        :param metric:
        :return:
        """
        raise NotImplementedError
