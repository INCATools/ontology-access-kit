import logging
import math
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

from rdflib import OWL, RDF, RDFS

from oaklib.datamodels import obograph
from oaklib.datamodels.similarity import (
    InformationContentCorpusEnum,
    InformationContentMethod,
    InformationContentScaleEnum,
)
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
    _as_rdf_obj,
    _sparql_values,
)
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP, RELATIONSHIP_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import GraphTraversalMethod, OboGraphInterface
from oaklib.interfaces.rdf_interface import TRIPLE
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.usages_interface import UsagesInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate
from oaklib.utilities.iterator_utils import chunk

LARGE_TERM_REFERENCE_COUNT = 100000
"""Terms with more references than this are counted individually when computing IC."""

__all__ = [
    "RelationGraphEnum",
    "UbergraphImplementation",
]


class RelationGraphEnum(Enum):
    """
    triples in UG are organized into different graphs
    """

    ontology = "http://reasoner.renci.org/ontology"
    redundant = "http://reasoner.renci.org/redundant"
    nonredundant = "http://reasoner.renci.org/nonredundant"
    normalizedInformationContent = "http://reasoner.renci.org/vocab/normalizedInformationContent"
    normalizedSubClassInformationContent = (
        "http://reasoner.renci.org/vocab/normalizedSubClassInformationContent"
    )
    referenceCount = "http://reasoner.renci.org/vocab/referenceCount"


@dataclass
class UbergraphImplementation(
    AbstractSparqlImplementation,
    RelationGraphInterface,
    SearchInterface,
    OboGraphInterface,
    MappingProviderInterface,
    SemanticSimilarityInterface,
    SubsetterInterface,
    SummaryStatisticsInterface,
    UsagesInterface,
):
    """
    Wraps the Ubergraph sparql endpoint

    See: `<https://github.com/INCATools/ubergraph>`_

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in Ubergraph

    An UbergraphImplementation can be initialed by:

    >>> from oaklib.implementations.ubergraph.ubergraph_implementation import UbergraphImplementation
    >>> adapter = UbergraphImplementation()

    or

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("ubergraph:")

    to use a specific ontology or named graph within ubergraph:

    >>> adapter = get_adapter("ubergraph:cl")

    Information content scores are returned as log2 bits, consistent with other adapters.
    Set ``normalized_information_content`` to get Ubergraph's native 0-100 scores instead.
    """

    normalized_information_content: bool = False
    """If True, return Ubergraph's native normalized (0-100) IC scores rather than log2 bits."""

    _ic_background_count: Optional[int] = None

    def _default_url(self) -> str:
        return "https://ubergraph.apps.renci.org/sparql"

    def _is_blazegraph(self) -> bool:
        """
        Currently Ubergraph uses blazegraph
        """
        return True

    @property
    def named_graph(self) -> Optional[str]:
        if not self.resource or self.resource.slug is None:
            return None
        else:
            ont = self.resource.slug
            if ont:
                for g in self.list_of_named_graphs():
                    if f"/{ont}." in g or f"/{ont}-base" in g:
                        return g
                logging.warning(f"No graph named: {ont}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RelationGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _get_outgoing_edges_by_curie(
        self, curie: CURIE, graph: RelationGraphEnum, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(
            select=["?p", "?o"],
            where=[f"GRAPH <{graph.value}> {{ {query_uri} ?p ?o }}", "?o a owl:Class"],
        )
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row["p"]["value"])
            obj = self.uri_to_curie(row["o"]["value"])
            yield pred, obj

    def _get_incoming_edges_by_curie(
        self, curie: CURIE, graph: RelationGraphEnum, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[CURIE, CURIE]]:
        query_uri = self.curie_to_sparql(curie)
        query = SparqlQuery(
            select=["?s", "?p"],
            where=[f"GRAPH <{graph.value}> {{ ?s ?p {query_uri}  }}", "?s a owl:Class"],
        )
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            query.where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            pred = self.uri_to_curie(row["p"]["value"])
            subj = self.uri_to_curie(row["s"]["value"])
            yield pred, subj

    def outgoing_relationship_map(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, obj in self._get_outgoing_edges_by_curie(
            curie, graph=RelationGraphEnum.nonredundant
        ):
            rmap[pred].append(obj)
        return rmap

    def incoming_relationship_map(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for pred, s in self._get_incoming_edges_by_curie(
            curie, graph=RelationGraphEnum.nonredundant
        ):
            rmap[pred].append(s)
        return rmap

    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        if invert:
            for s, p, o in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
                exclude_blank=exclude_blank,
            ):
                yield o, p, s
            return
        query = SparqlQuery(select=["?s", "?p", "?o"], where=["?s ?p ?o"])
        if not include_entailed:
            query.graph = RelationGraphEnum.nonredundant.value
        if subjects:
            query.where.append(_sparql_values("s", [self.curie_to_sparql(x) for x in subjects]))
        if predicates:
            query.where.append(_sparql_values("p", [self.curie_to_sparql(x) for x in predicates]))
        if objects:
            query.where.append(_sparql_values("o", [self.curie_to_sparql(x) for x in objects]))
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            sub = self.uri_to_curie(row["s"]["value"])
            pred = self.uri_to_curie(row["p"]["value"])
            obj = self.uri_to_curie(row["o"]["value"])
            yield sub, pred, obj

    def entailed_outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._get_outgoing_edges_by_curie(
            curie, graph=RelationGraphEnum.redundant, predicates=predicates
        )

    def entailed_incoming_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self._get_incoming_edges_by_curie(
            curie, graph=RelationGraphEnum.redundant, predicates=predicates
        )

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraph
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _values(self, var: str, in_list: Optional[List[str]]) -> str:
        if in_list is None:
            return ""
        else:
            return f'VALUES ?{var} {{ {" ".join(in_list)} }}'

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
        # print(f'G={graph} Q={query.query_str()}')
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            v = row["o"]["value"]
            if not object_is_literal:
                v = self.uri_to_curie(v)
            yield (self.uri_to_curie(row["s"]["value"]), self.uri_to_curie(row["p"]["value"]), v)

    def _object_properties(self) -> List[PRED_CURIE]:
        return list(set([t[0] for t in self._triples(None, RDF.type, OWL.ObjectProperty)]))

    def ancestor_graph(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> obograph.Graph:
        ancs = list(self.ancestors(start_curies, predicates))
        logging.info(f"NUM ANCS: {len(ancs)}")
        edges = []
        nodes = {}
        for rel in self._from_subjects_chunked(
            ancs, predicates, graph=RelationGraphEnum.nonredundant.value, where=[]
        ):
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
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        if method and method == GraphTraversalMethod.HOP:
            raise NotImplementedError("HOP not implemented for ubergraph")
        # TODO: DRY
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        # the redundant graph holds the reflexive transitive closure of subClassOf and
        # existential relationships; other graphs include non-hierarchical axioms
        where = [
            f"GRAPH <{RelationGraphEnum.redundant.value}> {{ ?s ?p ?o }}",
            "?o a owl:Class",
            _sparql_values("s", query_uris),
        ]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("p", pred_uris))
        query = SparqlQuery(select=["?o"], distinct=True, where=where)
        if not reflexive:
            query.add_filter("?o != ?s")
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["o"]["value"])

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive=True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        if method and method == GraphTraversalMethod.HOP:
            raise NotImplementedError("HOP not implemented for ubergraph")
        # TODO: DRY
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [
            f"GRAPH <{RelationGraphEnum.redundant.value}> {{ ?s ?p ?o }}",
            "?s a owl:Class",
            _sparql_values("o", query_uris),
        ]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("p", pred_uris))
        query = SparqlQuery(select=["?s"], distinct=True, where=where)
        if not reflexive:
            query.add_filter("?s != ?o")
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["s"]["value"])

    def dump(self, path: str = None, syntax: str = None):
        raise NotImplementedError("Dump not allowed on ubergraph")

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
        bindings = self._sparql_query(query.query_str())
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
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        subject_ancestors: List[CURIE] = None,
        object_ancestors: List[CURIE] = None,
        include_owl_thing: bool = True,
    ) -> Iterable[CURIE]:
        if subject_ancestors is not None and object_ancestors is not None:
            yield from super().common_ancestors(
                subject,
                object,
                predicates,
                subject_ancestors=subject_ancestors,
                object_ancestors=object_ancestors,
                include_owl_thing=include_owl_thing,
            )
            return
        s_uri = self.curie_to_sparql(subject)
        o_uri = self.curie_to_sparql(object)
        where = [f"{s_uri} ?sp ?a", f"{o_uri} ?op ?a", "?a a owl:Class"]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("sp", pred_uris))
            where.append(_sparql_values("op", pred_uris))
        query = SparqlQuery(select=["?a"], distinct=True, where=where)
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["a"]["value"])

    def most_recent_common_ancestors(
        self,
        subject: CURIE,
        object: CURIE,
        predicates: List[PRED_CURIE] = None,
        include_owl_thing: bool = True,
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
        bindings = self._sparql_query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["a"]["value"])

    def get_information_content(
        self, curie: CURIE, background: CURIE = None, predicates: List[PRED_CURIE] = None
    ) -> Optional[float]:
        ics = list(self.information_content_scores([curie], object_closure_predicates=predicates))
        if len(ics) > 1:
            raise ValueError(f"Multiple ICs for {curie} = {ics}")
        if not ics:
            return None
        return ics[0][1]

    def information_content_scores(
        self,
        curies: Optional[Iterable[CURIE]] = None,
        predicates: List[PRED_CURIE] = None,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
        term_to_entities_map: Dict[CURIE, List[CURIE]] = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Yields entity-score pairs using the IC scores precomputed by Ubergraph.

        Ubergraph precomputes IC for each class from the redundant (entailed, reflexive)
        graph, see `<https://github.com/INCATools/ubergraph/blob/master/ic.dl>`_:

            IC(t) = -log(count(t) / N) / log(N) * 100

        where N is the number of terms in the redundant graph, and count(t) is the number
        of terms related to t by ``rdfs:subClassOf`` or any existential relation
        (``normalizedInformationContent``), or by ``rdfs:subClassOf`` only
        (``normalizedSubClassInformationContent``, used when the closure predicates are
        just ``rdfs:subClassOf``). Scores are scaled to 0-100, so the log base is
        irrelevant.

        Unless ``normalized_information_content`` is set, scores are converted to log2 bits,
        ``score / 100 * log2(N)``, where N is recovered from the stored ``referenceCount``
        of any term (see :meth:`information_content_background_count`).

        These are fetched directly in a single query per chunk, avoiding the generic
        approach of first enumerating every entity in the triplestore.

        If other closure predicates, associations, or a preloaded IC map are requested,
        this falls back to the generic implementation.
        """
        ic_enum = self._precomputed_ic_predicate(object_closure_predicates)
        if ic_enum is None and curies is not None:
            yield from self._information_content_scores_by_counting(
                curies, object_closure_predicates
            )
            return
        if (
            ic_enum is None
            or use_associations
            or term_to_entities_map
            or self.cached_information_content_map is not None
        ):
            if ic_enum is None:
                logging.warning(
                    "Ubergraph only has precomputed IC for subClassOf or subClassOf+existential "
                    "closures; computing IC for all terms with other predicates requires "
                    "enumerating all entities and may be very slow"
                )
            yield from super().information_content_scores(
                curies,
                predicates=predicates,
                object_closure_predicates=object_closure_predicates,
                use_associations=use_associations,
                term_to_entities_map=term_to_entities_map,
                **kwargs,
            )
            return
        # IC triples live in the merged ontology graph, not the per-ontology named graphs,
        # so queries are passed as strings to avoid restricting them to the named graph
        ic_pred = f"<{ic_enum.value}>"
        if curies is None:
            query = SparqlQuery(select=["?s", "?ic"], where=[f"?s {ic_pred} ?ic"])
            ng = self.named_graph
            if ng:
                query.where.append(f"GRAPH <{ng}> {{ ?s a owl:Class }}")
            for row in self._sparql_query(query.query_str()):
                yield self.uri_to_curie(row["s"]["value"]), self._ic_from_score(row["ic"]["value"])
            return
        for curie_chunk in chunk(curies):
            query = SparqlQuery(select=["?s", "?ic"], where=[f"?s {ic_pred} ?ic"])
            query.add_values("s", [self.curie_to_sparql(c) for c in curie_chunk])
            for row in self._sparql_query(query.query_str()):
                yield self.uri_to_curie(row["s"]["value"]), self._ic_from_score(row["ic"]["value"])

    def _information_content_scores_by_counting(
        self, curies: Iterable[CURIE], object_closure_predicates: List[PRED_CURIE]
    ) -> Iterator[Tuple[CURIE, float]]:
        """
        Computes IC for arbitrary closure predicates by counting reflexive descendants in the
        redundant graph, using the same background set as Ubergraph's precomputed scores.

        For ``rdfs:subClassOf`` this gives identical results to
        ``normalizedSubClassInformationContent``.

        Counting is fast for most terms, but can take seconds for very general terms with
        millions of descendants, which make a batched query time out. Terms are therefore
        split using Ubergraph's precomputed ``referenceCount`` (the count over all predicates,
        an upper bound): small terms are counted in one batched query, and large terms are
        counted individually, in parallel.
        """
        n = self.information_content_background_count()
        pred_uris = [self.curie_to_sparql(p) for p in object_closure_predicates]
        redundant = RelationGraphEnum.redundant.value
        for curie_chunk in chunk(curies):
            # reference counts also serve to filter out unknown terms
            query = SparqlQuery(
                select=["?o", "?c"],
                where=[
                    _sparql_values("o", [self.curie_to_sparql(c) for c in curie_chunk]),
                    f"?o <{RelationGraphEnum.referenceCount.value}> ?c",
                ],
            )
            reference_counts = {
                self.uri_to_curie(row["o"]["value"]): int(row["c"]["value"])
                for row in self._sparql_query(query.query_str())
            }
            small = [c for c, rc in reference_counts.items() if rc <= LARGE_TERM_REFERENCE_COUNT]
            large = [c for c, rc in reference_counts.items() if rc > LARGE_TERM_REFERENCE_COUNT]
            # counts exclude the term itself, which is added below
            counts = {}
            if small:
                query = SparqlQuery(
                    select=["?o", "(COUNT(DISTINCT ?s) AS ?c)"],
                    where=[
                        _sparql_values("o", [self.curie_to_sparql(c) for c in small]),
                        _sparql_values("p", pred_uris),
                        f"GRAPH <{redundant}> {{ ?s ?p ?o }}",
                        "FILTER (?s != ?o)",
                    ],
                )
                # not restricted to the named graph, for consistency with precomputed scores
                for row in self._sparql_query(query.query_str() + " GROUP BY ?o"):
                    counts[self.uri_to_curie(row["o"]["value"])] = int(row["c"]["value"])
            large_queries = []
            for curie in large:
                uri = self.curie_to_sparql(curie)
                query = SparqlQuery(
                    select=["(COUNT(DISTINCT ?s) AS ?c)"],
                    where=[
                        _sparql_values("p", pred_uris),
                        f"GRAPH <{redundant}> {{ ?s ?p {uri} }}",
                        f"FILTER (?s != {uri})",
                    ],
                )
                large_queries.append(query.query_str())
            large_results = self._sparql_queries_concurrently(large_queries)
            for curie, rows in zip(large, large_results, strict=True):
                counts[curie] = int(rows[0]["c"]["value"]) if rows else 0
            for curie in reference_counts:
                count = counts.get(curie, 0) + 1
                score = -math.log(count / n) / math.log(n) * 100
                yield curie, self._ic_from_score(score)

    def _precomputed_ic_predicate(
        self, object_closure_predicates: Optional[List[PRED_CURIE]]
    ) -> Optional[RelationGraphEnum]:
        """Returns the precomputed IC predicate for the closure predicates, if there is one."""
        if not object_closure_predicates:
            return RelationGraphEnum.normalizedInformationContent
        if list(object_closure_predicates) == [IS_A]:
            return RelationGraphEnum.normalizedSubClassInformationContent
        return None

    def information_content_method(
        self,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
    ) -> InformationContentMethod:
        if use_associations or self.cached_information_content_map is not None:
            return super().information_content_method(
                object_closure_predicates=object_closure_predicates,
                use_associations=use_associations,
            )
        scale = (
            InformationContentScaleEnum.normalized
            if self.normalized_information_content
            else InformationContentScaleEnum.log2_bits
        )
        return InformationContentMethod(
            scale=scale,
            corpus=InformationContentCorpusEnum.ontology,
            closure_predicates=list(object_closure_predicates or []),
            background_count=self.information_content_background_count(),
            source="ubergraph",
        )

    def information_content_background_count(self) -> int:
        """
        Returns N, the number of terms in the background set used by Ubergraph to compute IC.

        This is not stored directly, but can be recovered from any term with a reference
        count c > 1 and normalized score s, since s = 100 * (1 - ln(c) / ln(N)):

            ln(N) = ln(c) / (1 - s / 100)

        :return: background count
        """
        if self._ic_background_count is None:
            query = SparqlQuery(
                select=["?c", "?ic"],
                where=[
                    f"?s <{RelationGraphEnum.referenceCount.value}> ?c",
                    f"?s <{RelationGraphEnum.normalizedInformationContent.value}> ?ic",
                    "FILTER (?c > 1)",
                ],
                limit=1,
            )
            rows = self._sparql_query(query.query_str())
            if not rows:
                raise ValueError("Cannot determine IC background count from Ubergraph")
            c = int(rows[0]["c"]["value"])
            score = float(rows[0]["ic"]["value"])
            self._ic_background_count = round(math.exp(math.log(c) / (1 - score / 100)))
            logging.info(f"Ubergraph IC background count={self._ic_background_count}")
        return self._ic_background_count

    def _ic_from_score(self, score: Union[str, float]) -> float:
        """Convert a normalized Ubergraph IC score to log2 bits, unless native scores requested."""
        score = float(score)
        if self.normalized_information_content:
            return score
        return score / 100 * math.log2(self.information_content_background_count())

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SummaryStatisticsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _statistics_graph(self) -> Optional[str]:
        # asserted axioms, for either the selected ontology or all ontologies
        return self.named_graph or RelationGraphEnum.ontology.value

    def _descendants_pattern(self, var: str, roots: List[CURIE]) -> str:
        root_uris = " ".join(self.curie_to_sparql(r) for r in roots)
        return (
            f"VALUES ?_root {{ {root_uris} }} "
            f"GRAPH <{RelationGraphEnum.redundant.value}> {{ {var} rdfs:subClassOf ?_root }}"
        )

    def _relation_graph_count_queries(
        self, graph: RelationGraphEnum, filters: List[str]
    ) -> Dict[str, str]:
        """
        Queries counting edges by predicate in one of the relation graphs.

        For all of Ubergraph, a single grouped count times out, so the predicates are
        listed, and each is counted separately, which is fast.
        """
        ng = self.named_graph
        if ng:
            # relation graphs are not partitioned by ontology
            filters = filters + [f"GRAPH <{ng}> {{ ?s a owl:Class }}"]
        if filters:
            q = (
                f"SELECT ?p (COUNT(*) AS ?n) WHERE {{ GRAPH <{graph.value}> {{ ?s ?p ?o }} "
                f"{' '.join(filters)} }} GROUP BY ?p"
            )
            return {f"{graph.name}": q}
        rows = self._sparql_query(
            f"SELECT DISTINCT ?p WHERE {{ GRAPH <{graph.value}> {{ ?s ?p ?o }} }}"
        )
        queries = {}
        for row in rows:
            p = row["p"]["value"]
            queries[f"{graph.name}_{p}"] = (
                f"SELECT ?p (COUNT(*) AS ?n) WHERE {{ "
                f"GRAPH <{graph.value}> {{ ?s <{p}> ?o }} BIND(<{p}> AS ?p) }} GROUP BY ?p"
            )
        return queries

    def _edge_count_by_predicate_queries(self, filters: List[str]) -> Dict[str, str]:
        return self._relation_graph_count_queries(RelationGraphEnum.nonredundant, filters)

    def _entailed_edge_count_by_predicate_queries(self, filters: List[str]) -> Dict[str, str]:
        return self._relation_graph_count_queries(RelationGraphEnum.redundant, filters)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RdfInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def extract_triples(
        self,
        seed_curies: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        strategy=None,
        map_to_curies=True,
    ) -> Iterator[TRIPLE]:
        seed_uris = [self.curie_to_sparql(c) for c in seed_curies]
        # Note that some triplestores will have performance issues with this query
        traverse_preds = [
            "rdfs:subClassOf",
            "owl:onProperty",
            "owl:someValuesFrom",
            "owl:annotatedSource",
            "owl:equivalentClass",
        ]
        if predicates:
            # note that predicates are only used in the ABox - for a RelationGraph-implementing
            # triplestore this will also include TBox existentials
            traverse_preds = list(set(traverse_preds + predicates))
        query = SparqlQuery(
            select=["?s", "?p", "?o"],
            graph=[RelationGraphEnum.ontology.value],
            where=[
                "?s ?p ?o ." f'?seed ({"|".join(traverse_preds)})* ?s',
                _sparql_values("seed", seed_uris),
            ],
        )
        bindings = self._sparql_query(query)
        n = 0
        for row in bindings:
            n += 1
            triple = (row["s"], row["p"], row["o"])
            if map_to_curies:
                yield tuple([self.uri_to_curie(v["value"]) for v in list(triple)])
            else:
                yield tuple([_as_rdf_obj(v) for v in list(triple)])
        logging.info(f"Total triples: {n}")
