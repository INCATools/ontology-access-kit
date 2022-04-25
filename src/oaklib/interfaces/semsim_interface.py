from abc import ABC
from typing import Dict, List, Iterable

from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE


class SemanticSimilarityInterface(BasicOntologyInterface, ABC):
    """
    TODO: consider direct use of nxontology
    """

    def most_recent_common_ancestors(self, subject: CURIE, object: CURIE,
                                     predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        if isinstance(self, OboGraphInterface):
            s_ancs = set(self.ancestors([subject], predicates))
            o_ancs = set(self.ancestors([object], predicates))
            common = s_ancs.intersection(o_ancs)
            ancs_of_common = []
            for ca in common:
                for caa in self.ancestors(ca, predicates):
                    if caa != ca:
                        ancs_of_common.append(caa)
            for a in common:
                if a not in ancs_of_common:
                    yield a
        else:
            raise NotImplementedError

    def common_ancestors(self, subject: CURIE, object: CURIE, predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        if isinstance(self, OboGraphInterface):
            s_ancs = set(self.ancestors(subject, predicates))
            o_ancs = set(self.ancestors(object, predicates))
            for a in s_ancs.intersection(o_ancs):
                yield a
        else:
            raise NotImplementedError


    def get_information_content(self, curie: CURIE, background: CURIE = None,
                                predicates: List[PRED_CURIE] = None) -> float:
        raise NotImplementedError

    def pairwise_similarity(self, subject: CURIE, object: CURIE = None,
                            predicates: List[PRED_CURIE] = None) -> TermPairwiseSimilarity:
        cas = list(self.most_recent_common_ancestors(subject, object, predicates))
        ics = {a: self.get_information_content(a, predicates) for a in cas}
        max_ic = max(ics.values())
        best_mrcas = [a for a in cas if ics[a] == max_ic]
        sim = TermPairwiseSimilarity(subject_id=subject, object_id=object, ancestor_id=best_mrcas[0])
        sim.ancestor_information_content = max_ic
        return sim

