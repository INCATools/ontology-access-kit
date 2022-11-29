import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Tuple, Union

from rdflib import OWL, RDF, RDFS, URIRef

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.datamodels.vocabulary import (
    HAS_DEFINITION_URI,
    IS_A,
    PART_OF,
    RDF_TYPE,
    SKOS_ALT_LABEL,
)
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
    _sparql_values,
)
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.implementations.ubergraph.ubergraph_implementation import RelationGraphEnum
from oaklib.implementations.wikidata import SEARCH_CONFIG
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP, RELATIONSHIP_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, PRED_CURIE, URI
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate

DEFAULT_CURIE_MAP = {
    IS_A: "http://www.wikidata.org/prop/direct/P279",
    RDF_TYPE: "http://www.wikidata.org/prop/direct/P31",
    PART_OF: "http://www.wikidata.org/prop/direct/P361",
    HAS_DEFINITION_URI: "http://schema.org/description",
}


@dataclass
class WikidataImplementation(
    AbstractSparqlImplementation,
    RelationGraphInterface,
    SearchInterface,
    OboGraphInterface,
    MappingProviderInterface,
    SemanticSimilarityInterface,
    SubsetterInterface,
    TextAnnotatorInterface,
):
    """
    Wraps the wikidata sparql endpoint

    See: `<https://github.com/INCATools/wikidata>`_

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in wikidata

    An wikidataImplementation can be initialed by:

        .. code:: python

           >>>  oi = WikidataImplementation.create()

        The default wikidata endpoint will be assumed

    """

    wikidata_curie_map: Dict[str, str] = field(default_factory=lambda: DEFAULT_CURIE_MAP)

    def __post_init__(self):
        super().__post_init__()
        self.multilingual = True

    def _default_url(self) -> str:
        return "http://query.wikidata.org/sparql"

    def _alias_predicates(self) -> List[PRED_CURIE]:
        return [SKOS_ALT_LABEL]

    def _is_blazegraph(self) -> bool:
        """
        Currently wikidata uses blazegraph
        """
        return True

    def curie_to_uri(self, curie: CURIE, strict: bool = False) -> URI:
        if curie in self.wikidata_curie_map:
            return self.wikidata_curie_map[curie]
        return super().curie_to_uri(curie, strict=strict)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def basic_search(
        self, search_term: str, config: SearchConfiguration = SEARCH_CONFIG
    ) -> Iterable[CURIE]:
        if ":" in search_term and " " not in search_term:
            logging.debug(f"Not performing search on what looks like a CURIE: {search_term}")
            return
        query = SparqlQuery(
            select=["?s"],
            where=[
                f"""
                            SERVICE wikibase:mwapi {{
                              bd:serviceParam wikibase:endpoint "www.wikidata.org";
                                wikibase:api "EntitySearch";
                                mwapi:search "{search_term}";
                                mwapi:language "en".
                                ?s wikibase:apiOutputItem mwapi:item.
                                ?num wikibase:apiOrdinal true.
                            }}
                            """
            ],
        )
        if config.limit is not None:
            query.limit = config.limit
        bindings = self._query(query)
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RelationGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _get_outgoing_edges_by_curie(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=["?p", "?o"], where=[f"{query_uri} ?p ?o", "FILTER (isIRI(?o))"])
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(_sparql_values("p", pred_uris))
        bindings = self._query(query.query_str())
        for row in bindings:
            obj = self.uri_to_curie(row["o"]["value"])
            if obj.startswith("wikidata:statement/"):
                # TODO: filter ahead of time
                continue
            pred = self.uri_to_curie(row["p"]["value"])
            yield pred, obj

    def _get_incoming_edges_by_curie(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(select=["?s", "?p"], where=[f"?s ?p {query_uri}"])
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(_sparql_values("p", pred_uris))
        bindings = self._query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row["p"]["value"])
            subj = self.uri_to_curie(row["s"]["value"])
            yield pred, subj

    def outgoing_relationship_map(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, obj in self._get_outgoing_edges_by_curie(curie):
            rmap[pred].append(obj)
        return rmap

    def incoming_relationship_map(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, s in self._get_incoming_edges_by_curie(curie):
            rmap[pred].append(s)
        return rmap

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _from_subjects_chunked(
        self, subjects: List[CURIE], predicates: List[PRED_CURIE] = None, **kwargs
    ):
        size = 10
        while len(subjects) > 0:
            next_subjects = subjects[0:size]
            subjects = subjects[size:]
            for r in self._from_subjects(next_subjects, predicates, **kwargs):
                yield r

    def _from_subjects(
        self,
        subjects: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        graph: str = None,
        object_is_literal=False,
        object_is_language_tagged=False,
        where=None,
    ) -> Iterable[Tuple[CURIE, PRED_CURIE, CURIE]]:
        if where is None:
            where = []
        subject_uris = [self.curie_to_sparql(curie) for curie in subjects]
        if predicates:
            predicate_uris = [self.curie_to_sparql(curie) for curie in predicates]
        else:
            predicate_uris = None
        query = SparqlQuery(
            select=["?s ?p ?o"],
            distinct=True,
            graph=graph,
            where=[
                "?s ?p ?o",
                _sparql_values("s", subject_uris),
                _sparql_values("p", predicate_uris),
            ]
            + where,
        )
        if self.multilingual and object_is_literal:
            query.where.append(f'FILTER (LANG(?o) = "{self.preferred_language}")')
        bindings = self._query(query.query_str())
        for row in bindings:
            v = row["o"]["value"]
            if not object_is_literal:
                v = self.uri_to_curie(v)
            yield (self.uri_to_curie(row["s"]["value"]), self.uri_to_curie(row["p"]["value"]), v)

    def _object_properties(self) -> List[PRED_CURIE]:
        return list(set([t[0] for t in self._triples(None, RDF.type, OWL.ObjectProperty)]))

    def node(self, curie: CURIE) -> obograph.Node:
        params = dict(id=curie, lbl=self.label(curie))
        return obograph.Node(**params)

    def ancestor_graph(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> obograph.Graph:
        ancs = list(self.ancestors(start_curies, predicates))
        logging.info(f"NUM ANCS: {len(ancs)}")
        edges = []
        nodes = {}
        for rel in self._from_subjects_chunked(ancs, predicates, where=[]):
            edges.append(obograph.Edge(sub=rel[0], pred=rel[1], obj=rel[2]))
        logging.info(f"NUM EDGES: {len(edges)}")
        for rel in self._from_subjects_chunked(ancs, [RDFS.label], object_is_literal=True):
            id = rel[0]
            nodes[id] = obograph.Node(id=id, lbl=rel[2])
        logging.info(f"NUM NODES: {len(nodes)}")
        return obograph.Graph(id="query", nodes=list(nodes.values()), edges=edges)

    def relationships_to_graph(self, relationships: Iterable[RELATIONSHIP]) -> obograph.Graph:
        relationships = list(relationships)
        edges = [obograph.Edge(sub=s, pred=p, obj=o) for s, p, o in relationships]
        node_ids = set()
        for rel in relationships:
            node_ids.update(list(rel))
        nodes = {}
        for s, _, o in self._from_subjects_chunked(
            list(node_ids), [RDFS.label], object_is_literal=True
        ):
            nodes[s] = obograph.Node(id=s, lbl=o)
        logging.info(f"NUM EDGES: {len(edges)}")
        return obograph.Graph(id="query", nodes=list(nodes.values()), edges=edges)

    def ancestors(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        if predicates is None:
            raise NotImplementedError("Unbound predicates not supported for Wikidata")
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [_sparql_values("s", query_uris)]
        pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
        pred_uris_j = "|".join(pred_uris)
        where.append(f"?s ({pred_uris_j})* ?o")
        query = SparqlQuery(select=["?o"], distinct=True, where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["o"]["value"])

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
    ) -> Iterable[CURIE]:
        if predicates is None:
            raise NotImplementedError("Unbound predicates not supported for Wikidata")
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [_sparql_values("o", query_uris)]
        pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
        pred_uris_j = "|".join(pred_uris)
        where.append(f"?s ({pred_uris_j})* ?o")
        if not reflexive:
            where.append("?s != ?o")
        query = SparqlQuery(select=["?s"], distinct=True, where=where)
        print(query.query_str())
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: Subsetter
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def gap_fill_relationships(
        self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None
    ) -> Iterator[RELATIONSHIP]:
        # TODO: compare with https://api.triplydb.com/s/_mZ9q_-rg
        query_uris = [self.curie_to_sparql(curie) for curie in seed_curies]
        where = ["?s ?p ?o", _sparql_values("s", query_uris), _sparql_values("o", query_uris)]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("p", pred_uris))
        query = SparqlQuery(select=["?s ?p ?o"], where=where)
        bindings = self._query(query.query_str())
        # TODO: remove redundancy
        rels = []
        for row in bindings:
            rels.append(
                (
                    self.uri_to_curie(row["s"]["value"]),
                    self.uri_to_curie(row["p"]["value"]),
                    self.uri_to_curie(row["o"]["value"]),
                )
            )
        for rel in transitive_reduction_by_predicate(rels):
            yield rel

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SemSim
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def common_ancestors(
        self, subject: CURIE, object: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        s_uri = self.curie_to_sparql(subject)
        o_uri = self.curie_to_sparql(object)
        where = [f"{s_uri} ?sp ?a", f"{o_uri} ?op ?a", "?a a owl:Class"]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("sp", pred_uris))
            where.append(_sparql_values("op", pred_uris))
        query = SparqlQuery(select=["?a"], distinct=True, where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["a"]["value"])

    def most_recent_common_ancestors(
        self, subject: CURIE, object: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        s_uri = self.curie_to_sparql(subject)
        o_uri = self.curie_to_sparql(object)
        where = [f"{s_uri} ?sp ?a", f"{o_uri} ?op ?a", "?a a owl:Class"]
        where2 = [f"{s_uri} ?sp2 ?a2", f"{o_uri} ?op2 ?a2", "?a2 ?ap2 ?a", "FILTER( ?a != ?a2)"]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("sp", pred_uris))
            where.append(_sparql_values("op", pred_uris))
            where2.append(_sparql_values("sp2", pred_uris))
            where2.append(_sparql_values("op2", pred_uris))
            where2.append(_sparql_values("ap2", pred_uris))
        query = SparqlQuery(select=["?a"], distinct=True, where=where)
        subq = SparqlQuery(select=["?a2"], where=where2)
        query.add_not_in(subq)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["a"]["value"])

    def get_information_content(
        self, curie: CURIE, background: CURIE = None, predicates: List[PRED_CURIE] = None
    ) -> float:
        if predicates is not None:
            raise NotImplementedError("Only predetermined predicates allowed")
        ics = self._get_anns(curie, URIRef(RelationGraphEnum.normalizedInformationContent.value))
        if len(ics) > 1:
            raise ValueError(f"Multiple ICs for {curie} = {ics}")
        return float(ics[0])

    def pairwise_similarity(
        self, subject: CURIE, object: CURIE = None, predicates: List[PRED_CURIE] = None
    ) -> TermPairwiseSimilarity:
        s_uri = self.curie_to_sparql(subject)
        o_uri = self.curie_to_sparql(object)
        where = [
            f"{s_uri} ?sp ?a",
            f"{o_uri} ?op ?a",
            "?a a owl:Class",
            f"?a <{RelationGraphEnum.normalizedInformationContent.value}> ?ic",
        ]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("sp", pred_uris))
            where.append(_sparql_values("op", pred_uris))
        query = SparqlQuery(select=["?a", "?ic"], distinct=True, where=where)
        bindings = self._query(query.query_str())
        ics = {
            self.uri_to_curie(row["a"]["value"]): float(self.uri_to_curie(row["ic"]["value"]))
            for row in bindings
        }
        max_ic = max(list(ics.values()))
        best_mrcas = [a for a in ics if ics[a] == max_ic]
        mrca = best_mrcas[0]
        sim = TermPairwiseSimilarity(subject_id=subject, object_id=object, ancestor_id=mrca)
        for curie, label in self.labels([subject, object, mrca]):
            if label is None:
                continue
            # print(f'C={curie} L={label}')
            if curie == subject:
                sim.subject_label = label
            if curie == object:
                sim.object_label = label
            if curie == mrca:
                sim.ancestor_label = label
        sim.ancestor_information_content = max_ic
        return sim
