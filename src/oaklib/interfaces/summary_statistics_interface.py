from abc import ABC
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, RELATIONSHIP
#import oaklib.datamodels.summary_statistics_datamodel.slots as statdict_slots
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE


SUMMARY_STATISTICS_MAP = Dict[str, Any]


class SummaryStatisticsInterface(BasicOntologyInterface, ABC):
    """
    generates summary statistics

    Uses SummaryStatistics datamodel, see :ref:`datamodels`
    """

    def get_global_summary_statistics(self) -> SUMMARY_STATISTICS_MAP:
        """
        Gets summary statistics for all ontologies wrapped as a single dictionary

        :return:
        """
        raise NotImplementedError

    def get_partitioned_summary_statistics(self) -> Dict[CURIE, SUMMARY_STATISTICS_MAP]:
        """
        Gets summary statistics for all ontologies wrapped as multiple dictionaries keyed
        by ontology CURIE

        :return:
        """
        raise NotImplementedError

    def get_metric_description(self, metric: str) -> str:
        """
        Examines the data dictionary to retrieve the definition of a metric

        Any dictionary can be used, but summary_statistics_datamodel is favored

        :param metric:
        :return:
        """
        raise NotImplementedError

