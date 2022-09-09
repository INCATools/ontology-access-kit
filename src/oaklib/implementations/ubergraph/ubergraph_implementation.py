import logging
import math
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator, List, Optional, Tuple, Union

from rdflib import OWL, RDF, RDFS, URIRef

from oaklib.datamodels import obograph
from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
    _as_rdf_obj,
    _sparql_values,
)
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP, RELATIONSHIP_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.rdf_interface import TRIPLE
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate
from oaklib.utilities.semsim.similarity_utils import setwise_jaccard_similarity

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


@dataclass
class UbergraphImplementation(
    AbstractSparqlImplementation,
    RelationGraphInterface,
    SearchInterface,
    OboGraphInterface,
    MappingProviderInterface,
    SemanticSimilarityInterface,
    SubsetterInterface,
):
    """
    Wraps the Ubergraph sparql endpoint

    See: `<https://github.com/INCATools/ubergraph>`_

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in Ubergraph

    An UbergraphImplementation can be initialed by:

        .. code:: python

           >>>  oi = UbergraphImplementation.create()

        The default ubergraph endpoint will be assumed

    """

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
        bindings = self._query(query.query_str())
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
        bindings = self._query(query.query_str())
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
    ) -> Iterator[RELATIONSHIP]:
        query = SparqlQuery(select=["?s", "?p", "?o"], where=["?s ?p ?o"])
        query.graph = RelationGraphEnum.nonredundant.value
        if subjects:
            query.where.append(_sparql_values("s", [self.curie_to_sparql(x) for x in subjects]))
        if predicates:
            query.where.append(_sparql_values("p", [self.curie_to_sparql(x) for x in predicates]))
        if objects:
            query.where.append(_sparql_values("o", [self.curie_to_sparql(x) for x in objects]))
        bindings = self._query(query.query_str())
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
        bindings = self._query(query.query_str())
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
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        # TODO: DRY
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = [
            "?s ?p ?o",
            "?o a owl:Class",
            # f'?p a owl:ObjectProperty',
            _sparql_values("s", query_uris),
        ]
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(_sparql_values("p", pred_uris))
        query = SparqlQuery(select=["?o"], distinct=True, where=where)
        bindings = self._query(query.query_str())
        for row in bindings:
            yield self.uri_to_curie(row["o"]["value"])

    def descendants(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        # TODO: DRY
        query_uris = [self.curie_to_sparql(curie) for curie in start_curies]
        where = ["?s ?p ?o", "?s a owl:Class", f'VALUES ?o {{ {" ".join(query_uris)} }}']
        if predicates:
            pred_uris = [self.curie_to_sparql(pred) for pred in predicates]
            where.append(f'VALUES ?p {{ {" ".join(pred_uris)} }}')
        query = SparqlQuery(select=["?s"], distinct=True, where=where)
        bindings = self._query(query.query_str())
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
        sim.jaccard_similarity = setwise_jaccard_similarity(
            list(self.ancestors(subject, predicates=predicates)),
            list(self.ancestors(object, predicates=predicates)),
        )
        sim.phenodigm_score = math.sqrt(sim.jaccard_similarity * sim.ancestor_information_content)
        return sim

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
        bindings = self._query(query)
        n = 0
        for row in bindings:
            n += 1
            triple = (row["s"], row["p"], row["o"])
            if map_to_curies:
                yield tuple([self.uri_to_curie(v["value"]) for v in list(triple)])
            else:
                yield tuple([_as_rdf_obj(v) for v in list(triple)])
        logging.info(f"Total triples: {n}")
