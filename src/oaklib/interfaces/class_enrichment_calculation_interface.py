import logging
from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional

from oaklib.datamodels.class_enrichment import ClassEnrichmentResult
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.stats.hypergeometric import hypergeometric_p_value


@dataclass
class ClassEnrichmentCalculationInterface(AssociationProviderInterface, ABC):
    """
    An interface that provides services to test for over representation of class membership in a set of entities.

    This interface is intended to be used to test for over representation of a class in a set of entities,

    for example: to
    test for over representation of a disease in a set of genes.
    """

    def enriched_classes(
        self,
        subjects: Iterable[CURIE],
        predicates: Iterable[CURIE] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        background: Iterable[CURIE] = None,
        hypotheses: Iterable[CURIE] = None,
        cutoff=0.05,
        autolabel=False,
        sort_by: str = None,
        direction="greater",
    ) -> Iterator[ClassEnrichmentResult]:
        """
        Test for overrepresentation of classes in a set of entities.

        :param subjects: The set of entities to test for overrepresentation of classes
        :param background: The set of entities to use as a background for the test
        :param hypotheses: The set of classes to test for overrepresentation
        :param cutoff: The threshold to use for significance
        :param labels: Whether to include labels for the classes
        :param direction: The direction of the test. One of 'greater', 'less', 'two-sided'
        :return: An iterator over ClassEnrichmentResult objects
        """
        subjects = list(subjects)
        sample_size = len(subjects)
        logging.info(f"Calculating sample_counts for {sample_size} subjects")
        sample_count = {
            k: v
            for k, v in self.association_subject_counts(
                subjects, predicates=predicates, object_closure_predicates=object_closure_predicates
            )
        }
        potential_hypotheses = set(sample_count.keys())
        if hypotheses is None:
            hypotheses = potential_hypotheses
        else:
            hypotheses = potential_hypotheses.intersection(hypotheses)
        logging.debug("Hypotheses: {}".format(hypotheses))

        # get background counts
        if background is None:
            logging.info(
                f"Calculating backgrounds for all associations using {object_closure_predicates}"
            )
            background = set()
            for a in self.associations(
                predicates=predicates, object_closure_predicates=object_closure_predicates
            ):
                background.add(a.subject)
        else:
            background = set(background)
        # ensure background includes all subjects
        background.update(subjects)

        bg_size = len(background)

        logging.info(f"Calculating background_counts for {bg_size} background entities")
        bg_count = {
            k: v
            for k, v in self.association_subject_counts(
                background,
                predicates=predicates,
                object_closure_predicates=object_closure_predicates,
            )
        }

        hypotheses = [x for x in hypotheses if bg_count[x] > 1]
        logging.info("Filtered hypotheses: {}".format(hypotheses))
        num_hypotheses = len(hypotheses)

        results = []
        for cls in hypotheses:
            logging.debug(f"Calculating enrichment for {cls}")
            p_val_raw, _dn = hypergeometric_p_value(
                sample_count[cls], sample_size, bg_count[cls], bg_size
            )
            p_val_adj = p_val_raw * num_hypotheses
            if p_val_adj > 1.0:
                p_val_adj = 1.0
            if p_val_adj <= cutoff:
                r = ClassEnrichmentResult(
                    cls,
                    p_value=p_val_raw,
                    p_value_adjusted=p_val_adj,
                    sample_count=sample_count[cls],
                    sample_total=sample_size,
                    background_count=bg_count[cls],
                    background_total=bg_size,
                )
                if autolabel:
                    r.label = self.label(cls)
                results.append(r)
        if isinstance(self, OboGraphInterface):
            anc_counts = {
                x.class_id: len(
                    list(self.ancestors([x.class_id], predicates=object_closure_predicates))
                )
                for x in results
            }
        else:
            anc_counts = {}
        results.sort(key=lambda x: x.p_value - anc_counts.get(x.class_id, 0) / 1e12)
        for r in results:
            yield r
