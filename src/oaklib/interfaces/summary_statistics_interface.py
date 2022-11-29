import logging
from abc import ABC
from collections import defaultdict
from typing import Any, Dict, List

from oaklib.datamodels.summary_statistics_datamodel import (
    FacetedCount,
    GlobalStatistics,
    SummaryStatisticCollection,
)
from oaklib.datamodels.vocabulary import OWL_CLASS
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
        include_entailed=False,
    ) -> GlobalStatistics:
        """
        Gets summary statistics for all ontologies treated as a single ontology.

        :param branches:
        :param group_by:
        :param values:
        :param include_entailed:
        :return:
        """
        stats = GlobalStatistics()
        if group_by is not None and branches is not None:
            raise ValueError("Cannot specify both metadata_property and branches")
        if branches is not None:
            for branch_name, branch_roots in branches.items():
                logging.info(f"Getting summary statistics for branch {branch_name}")
                branch_statistics = self.branch_summary_statistics(
                    branch_name=branch_name,
                    branch_roots=branch_roots,
                    include_entailed=include_entailed,
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
                    v, property_values={group_by: v}, include_entailed=include_entailed
                )
                if v is None:
                    v = "__OTHER__"
                stats.partitions[v] = branch_statistics
        if group_by is None and branches is None:
            branch_statistics = self.branch_summary_statistics(include_entailed=include_entailed)
            stats.partitions[branch_statistics.id] = branch_statistics
        return stats

    def branch_summary_statistics(
        self,
        branch_name: str = None,
        branch_roots: List[CURIE] = None,
        property_values: Dict[CURIE, Any] = None,
        include_entailed=False,
    ) -> SummaryStatisticCollection:
        """
        Gets summary statistics for all ontologies treated as a single ontology.

        Note that different implementations may implement subsets of the full stats datamodel.

        :param branch_name:
        :param branch_roots: if provided, only statistics for the given branch roots will be returned
        :param property_values: if provided, only statistics for entities that match these will be considered
        :param include_entailed: if True, include statistics for entailed edges
        :return:
        """
        if branch_name is None:
            branch_name = "AllBranches"
        if branch_roots is not None:
            raise NotImplementedError(f"branch_roots not implemented for {type(self)}")
        if property_values is not None:

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
        ssc = SummaryStatisticCollection(branch_name)
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
        self._add_derived_statistics(ssc)
        return ssc

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

    def _add_derived_statistics(self, ssc: SummaryStatisticCollection) -> None:
        """
        Adds derived statistics to the summary statistics collection

        :param ssc:
        :return:
        """
        ssc.non_deprecated_class_count = ssc.class_count - ssc.deprecated_class_count
        ssc.class_count_without_text_definitions = (
            ssc.class_count - ssc.class_count_with_text_definitions
        )

    def partitioned_summary_statistics(self) -> Dict[CURIE, SUMMARY_STATISTICS_MAP]:
        """
        Gets summary statistics for all ontologies wrapped as multiple dictionaries keyed
        by ontology CURIE

        :return:
        """
        raise NotImplementedError

    def summary_statistic_description(self, metric: str) -> str:
        """
        Examines the data dictionary to retrieve the definition of a metric

        Any dictionary can be used, but summary_statistics_datamodel is favored

        :param metric:
        :return:
        """
        raise NotImplementedError
