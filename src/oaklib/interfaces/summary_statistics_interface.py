from abc import ABC
from collections import defaultdict
from typing import Any, Dict

from oaklib.datamodels.summary_statistics_datamodel import (
    FacetedCount,
    SummaryStatisticCollection,
)
from oaklib.datamodels.vocabulary import OWL_CLASS
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface

# import oaklib.datamodels.summary_statistics_datamodel.slots as statdict_slots
from oaklib.types import CURIE

SUMMARY_STATISTICS_MAP = Dict[str, Any]


class SummaryStatisticsInterface(BasicOntologyInterface, ABC):
    """
    generates summary statistics

    Uses SummaryStatistics datamodel, see :ref:`datamodels`
    """

    def global_summary_statistics(self) -> SummaryStatisticCollection:
        """
        Gets summary statistics for all ontologies treated as a single ontology.

        Note that different implementations may implement subsets of the full stats datamodel.

        :return:
        """
        ssc = SummaryStatisticCollection()
        class_entities = list(self.entities(owl_type=OWL_CLASS, filter_obsoletes=False))
        obsoletes = list(self.obsoletes())
        ssc.class_count = len(class_entities)
        ssc.deprecated_class_count = len(set(class_entities).intersection(obsoletes))
        rel_counts = defaultdict(int)
        if isinstance(self, OboGraphInterface):
            for r in self.relationships():
                rel_counts[r[1]] += 1
        for k, v in rel_counts.items():
            ssc.edge_count_by_predicate[k] = FacetedCount(k, filtered_count=v)
        ssc.edge_count = sum(rel_counts.values())
        self._add_derived_statistics(ssc)
        return ssc

    def _add_derived_statistics(self, ssc: SummaryStatisticCollection) -> None:
        """
        Adds derived statistics to the summary statistics collection

        :param ssc:
        :return:
        """
        ssc.non_deprecated_class_count = ssc.class_count - ssc.deprecated_class_count

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
