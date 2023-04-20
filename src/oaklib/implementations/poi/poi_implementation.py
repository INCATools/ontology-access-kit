import inspect
import logging
import math
import pickle
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union

from oaklib.datamodels.association import Association
from oaklib.datamodels.similarity import (
    BestMatch,
    TermInfo,
    TermPairwiseSimilarity,
    TermSetPairwiseSimilarity,
)
from oaklib.datamodels.vocabulary import IS_A, PART_OF
from oaklib.interfaces import SubsetterInterface, TextAnnotatorInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import (
    PRED_CURIE,
    BasicOntologyInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE
from oaklib.utilities.indexes.intset_ontology_index import POS, IntSetOntologyIndex


@dataclass
class PoiImplementation(
    RelationGraphInterface,
    OboGraphInterface,
    ValidatorInterface,
    SearchInterface,
    SubsetterInterface,
    MappingProviderInterface,
    PatcherInterface,
    SemanticSimilarityInterface,
    MetadataInterface,
    DifferInterface,
    AssociationProviderInterface,
    TextAnnotatorInterface,
):
    """
    Python Ontology Index.

    A pure-python implementation of an integer-indexed ontology.

    Command line:

    .. code-block:: bash

        runoak -v -i poi:$db/cl.db similarity l~neuron @ l~neuron
    """

    wrapped_adapter: BasicOntologyInterface = None
    """A POI delegates most of its methods to the wrapped adapter"""

    closure_predicates: List[PRED_CURIE] = field(default_factory=lambda: [IS_A, PART_OF])
    """Predicates to use for traversal. These must be fixed at time of indexing."""

    jaccard_threshold: float = field(default=0.5)
    """Threshold below which pairwise matches are discarded."""

    ontology_index: IntSetOntologyIndex = None
    """In-memory index of ontology entities plus closures."""

    cache_pairwise_information_content: bool = True

    delegated_methods: ClassVar[List[str]] = [
        BasicOntologyInterface.entities,
        BasicOntologyInterface.label,
        BasicOntologyInterface.labels,
        BasicOntologyInterface.curies_by_label,
        BasicOntologyInterface.curie_to_uri,
        BasicOntologyInterface.uri_to_curie,
        BasicOntologyInterface.ontologies,
        BasicOntologyInterface.obsoletes,
        SearchInterface.basic_search,
        OboGraphInterface.node,
    ]
    """all methods that should be delegated to wrapped_adapter"""

    def __post_init__(self):
        source = None
        if self.wrapped_adapter is None:
            from oaklib.selector import get_implementation_from_shorthand

            if self.resource:
                slug = self.resource.slug
                logging.info(f"Wrapping an existing OAK implementation to fetch {slug}")
                inner_oi = get_implementation_from_shorthand(slug)
                if isinstance(inner_oi, OboGraphInterface):
                    self.wrapped_adapter = inner_oi
                else:
                    raise NotImplementedError
                source = str(self.resource.slug)
        else:
            source = str(self.wrapped_adapter.resource.slug)
        # delegation magic
        methods = dict(inspect.getmembers(self.wrapped_adapter))
        for m in self.delegated_methods:
            mn = m if isinstance(m, str) else m.__name__
            setattr(PoiImplementation, mn, methods[mn])
        if source:
            self.build_index(source)

    def build_index(self, source: str = None):
        """
        Build the POI index.

        - build_curie_index: curies <-> ints
        - build_ancestor_index
        - build_association_index
        - build_information_content_index
        - build_term_pair_index

        :return:
        """
        self.ontology_index = IntSetOntologyIndex(source=source)
        self.build_curie_index()
        self.build_ancestor_index()
        self.build_information_content_index()
        # self.build_term_pair_index()

    def add_associations(self, associations: Iterable[Association]) -> bool:
        super().add_associations(associations)
        self.build_association_index()

    def build_curie_index(self):
        logging.info("Building curie index")
        oix = self.ontology_index
        n = 0
        _curie_to_int = {}
        _int_to_curie = {}
        for e in self.wrapped_adapter.entities(filter_obsoletes=False):
            _curie_to_int[e] = n
            _int_to_curie[n] = e
            n += 1
        oix.curie_to_int = _curie_to_int
        oix.int_to_curie = _int_to_curie

    def build_ancestor_index(self):
        logging.info("Building ancestor index")
        oix = self.ontology_index
        oix.ancestor_map = {}
        inner_oi = self.wrapped_adapter
        if not isinstance(inner_oi, OboGraphInterface):
            raise NotImplementedError
        for i, e in oix.int_to_curie.items():
            ancs = inner_oi.ancestors(e, predicates=self.closure_predicates, reflexive=True)
            oix.ancestor_map[i] = set(self._map_curies_to_ints(ancs))

    def build_association_index(self):
        logging.info("Building association index")
        oix = self.ontology_index
        _curie_to_int = oix.curie_to_int
        obj_closure_by_subj: Dict[POS, List[POS]] = defaultdict(set)
        for a in self.associations():
            s_ix = _curie_to_int[a.subject]
            obj_closure_ixs = oix.ancestor_map[_curie_to_int[a.object]]
            obj_closure_by_subj[s_ix] = obj_closure_by_subj[s_ix].union(obj_closure_ixs)

    def build_information_content_index(self):
        logging.info("Building information content index")
        oix = self.ontology_index
        oix.information_content_map = {}
        counts = defaultdict(int)
        if self._association_index:
            raise NotImplementedError
        else:
            for i in oix.int_to_curie.keys():
                ancs = self.ontology_index.ancestor_map[i]
                for a in ancs:
                    counts[a] += 1
            oix.reflexive_descendant_count_map = counts
            for i, count in counts.items():
                oix.information_content_map[i] = -math.log(
                    count / len(oix.int_to_curie)
                ) / math.log(2)

    def build_term_pair_index(self):
        logging.info("Building term pair index")
        oix = self.ontology_index
        oix.term_pair_jaccard_index = {}
        oix.term_pair_max_information_content = {}
        oix.term_pair_best_ancestor = {}
        entities = self.filtered_entities()
        entity_ixs = [oix.curie_to_int[e] for e in entities]
        for e1_ix in entity_ixs:
            logging.info(f"Indexing {e1_ix}")
            e1_ix_ancs = oix.ancestor_map[e1_ix]
            for e2_ix in entity_ixs:
                e2_ix_ancs = oix.ancestor_map[e2_ix]
                if e1_ix <= e2_ix:
                    anc_intersection = e1_ix_ancs.intersection(e2_ix_ancs)
                    anc_union = e1_ix_ancs.union(e2_ix_ancs)
                    if not anc_union:
                        # TODO
                        continue
                    jaccard = len(anc_intersection) / len(anc_union)
                    if jaccard > self.jaccard_threshold:
                        oix.term_pair_jaccard_index[(e1_ix, e2_ix)] = jaccard
                        if self.cache_pairwise_information_content:
                            ics = [oix.information_content_map[i] for i in anc_intersection]
                            max_ics = max(ics)
                            oix.term_pair_max_information_content[(e1_ix, e2_ix)] = max_ics
                            best_ancs = [
                                i
                                for i in anc_intersection
                                if math.isclose(
                                    oix.information_content_map[i], max_ics, rel_tol=1e-5
                                )
                            ]
                            oix.term_pair_best_ancestor[(e1_ix, e2_ix)] = best_ancs

    def _jaccard_using_ints(self, e1_ix: POS, e2_ix: POS, e1_ancs: Set[POS] = None) -> float:
        oix = self.ontology_index
        if e1_ancs is None:
            e1_ancs = oix.ancestor_map[e1_ix]
        e2_ancs = oix.ancestor_map[e2_ix]
        anc_intersection = e1_ancs.intersection(e2_ancs)
        anc_union = e1_ancs.union(e2_ancs)
        return len(anc_intersection) / len(anc_union)

    def _maxic_using_ints(self, e1_ix: POS, e2_ix: POS, e1_ancs: Set[POS] = None) -> float:
        oix = self.ontology_index
        if e1_ancs is None:
            e1_ancs = oix.ancestor_map[e1_ix]
        e2_ancs = oix.ancestor_map[e2_ix]
        anc_intersection = e1_ancs.intersection(e2_ancs)
        ics = [oix.information_content_map[i] for i in anc_intersection]
        return max(ics + [0.0])

    def filtered_entities(self) -> List[CURIE]:
        return list(self.entities())

    def dump(self, path: str = None, syntax: str = None):
        protocol = 0
        if syntax is not None:
            if "." in syntax:
                protocol = int(syntax.split(".")[-1])
        logging.info("Dumping index")
        with open(path, "wb") as file:
            pickle.dump(self.ontology_index, file, protocol=protocol)

    def load(self, path: str = None, syntax: str = None):
        logging.info(f"Loading index from {path}")
        with open(path, "rb") as file:
            self.ontology_index = pickle.load(file)

    def _map_curies_to_ints(self, curies: Iterable[CURIE]) -> Iterator[POS]:
        oix = self.ontology_index
        return [oix.curie_to_int[c] for c in curies]

    def _map_ints_to_curies(self, ints: Iterable[POS]) -> Iterator[CURIE]:
        oix = self.ontology_index
        return [oix.int_to_curie[i] for i in ints]

    def _check_predicates(self, predicates: Optional[List[PRED_CURIE]]):
        if predicates is not None and set(predicates) != set(self.closure_predicates):
            raise ValueError(f"Only a single index is supported: {self.closure_predicates}")

    def ancestors(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
    ) -> Iterable[CURIE]:
        self._check_predicates(predicates)
        if isinstance(start_curies, str):
            start_curies = [start_curies]
        oix = self.ontology_index
        bm = set()
        for e in start_curies:
            bm = bm.union(oix.ancestor_map[oix.curie_to_int[e]])
        for i in bm:
            yield oix.int_to_curie[i]

    def information_content_scores(
        self,
        curies: Iterable[CURIE],
        predicates: List[PRED_CURIE] = None,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
    ) -> Iterator[Tuple[CURIE, float]]:
        self._check_predicates(predicates)
        oix = self.ontology_index
        for c in curies:
            if c in oix.curie_to_int:
                c_ix = oix.curie_to_int[c]
                if c_ix in oix.information_content_map:
                    yield c, oix.information_content_map[c_ix]
                else:
                    # TODO
                    yield c, 0.0
            else:
                yield c, 0.0

    def pairwise_similarity(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
    ) -> TermPairwiseSimilarity:
        self._check_predicates(predicates)
        oix = self.ontology_index
        if subject not in oix.curie_to_int or object not in oix.curie_to_int:
            return TermPairwiseSimilarity(
                subject,
                object,
                jaccard_similarity=0.0,
                ancestor_information_content=0.0,
                phenodigm_score=0.0,
            )
        s_ix = oix.curie_to_int[subject]
        o_ix = oix.curie_to_int[object]
        k = (s_ix, o_ix)
        if oix.term_pair_jaccard_index is None:
            self.build_term_pair_index()
        if k not in oix.term_pair_jaccard_index:
            k = (o_ix, s_ix)
        if k in oix.term_pair_jaccard_index:
            jaccard = oix.term_pair_jaccard_index[k]
            ts = TermPairwiseSimilarity(
                subject_id=subject,
                object_id=object,
                jaccard_similarity=jaccard,
                ancestor_information_content=oix.term_pair_max_information_content[k],
                ancestor_id=list(self._map_ints_to_curies(oix.term_pair_best_ancestor[k]))[0],
            )
            ts.phenodigm_score = math.sqrt(ts.jaccard_similarity * ts.ancestor_information_content)
            return ts
        else:
            return TermPairwiseSimilarity(
                subject_id=subject,
                object_id=object,
                jaccard_similarity=0,
                ancestor_information_content=0.0,
                phenodigm_score=0.0,
            )

    def _all_by_all_pairwise_similarity_on_indexes(
        self,
        subjects: Iterable[POS],
        objects: Iterable[POS],
    ) -> Iterator[Tuple]:
        objects = list(objects)
        for s in subjects:
            s_ancs = self.ontology_index.ancestor_map[s]
            for o in objects:
                yield s, o, self._maxic_using_ints(s, o, s_ancs)

    def termset_pairwise_similarity(
        self,
        subjects: List[CURIE],
        objects: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        labels=False,
    ) -> TermSetPairwiseSimilarity:
        self._check_predicates(predicates)
        oix = self.ontology_index
        subject_ixs = self._map_curies_to_ints(subjects)
        object_ixs = self._map_curies_to_ints(objects)
        pairs = list(self._all_by_all_pairwise_similarity_on_indexes(subject_ixs, object_ixs))
        bm_subject_score: Dict[POS, float] = defaultdict(float)
        bm_subject: Dict[POS, POS] = {}
        bm_subject_sim = {}
        bm_object_score: Dict[POS, float] = defaultdict(float)
        bm_object: Dict[POS, POS] = {}
        bm_object_sim = {}
        sim = TermSetPairwiseSimilarity()
        for x in subjects:
            sim.subject_termset[x] = TermInfo(x)
        for x in objects:
            sim.object_termset[x] = TermInfo(x)
        for s_ix, o_ix, j_score in pairs:
            if j_score > bm_subject_score[s_ix]:
                bm_subject_score[s_ix] = j_score
                bm_subject[s_ix] = o_ix
                bm_subject_sim[s_ix] = j_score
            if j_score > bm_object_score[o_ix]:
                bm_object_score[o_ix] = j_score
                bm_object[o_ix] = s_ix
                bm_object_sim[o_ix] = j_score
        scores = []
        for s_ix, t_ix in bm_subject.items():
            s = oix.int_to_curie[s_ix]
            score = bm_subject_score[s_ix]
            sim.subject_best_matches[s] = BestMatch(
                s,
                match_target=oix.int_to_curie[t_ix],
                score=score,
            )
            scores.append(score)
        for s_ix, t_ix in bm_object.items():
            s = oix.int_to_curie[s_ix]
            score = bm_object_score[s_ix]
            sim.object_best_matches[s] = BestMatch(
                s,
                match_target=oix.int_to_curie[t_ix],
                score=score,
            )
            scores.append(score)
        if not scores:
            scores = [0.0]
        sim.average_score = statistics.mean(scores)
        sim.best_score = max(scores)
        return sim
