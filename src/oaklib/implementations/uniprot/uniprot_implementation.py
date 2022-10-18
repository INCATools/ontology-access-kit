"""
Adapter for UniProt endpoint (experimental).

.. warning ::

    this is currently highly incomplete

This is an adapter for the uniprot triplestore, which includes:

- entries for individual proteins
- triples connecting these proteins to other IRIs, including vocabulary terms

The adapter treats all entries as ontology elements, such that they can
be queried by normal OAK methods.

Associations between proteins and vocabulary terms (e.g. EC, keywords, GO) are
treated *both* as ontology edges and as associations.

Note that using this adapter will automatically load a uniprot prefix map that
maps uniprot namespaces to conventional OBO prefixes.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional

from oaklib.datamodels.association import Association
from oaklib.datamodels.vocabulary import OWL_SAME_AS, RDF_SEE_ALSO
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP, RELATIONSHIP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE

__all__ = [
    "UniprotImplementation",
]

UNIPROT_PREFIX_MAP = {
    "up": "http://purl.uniprot.org/core/",
    "updb": "http://purl.uniprot.org/database/",
    "UniProtKB": "http://purl.uniprot.org/uniprot/",
    "UniProtKB-KW": "http://purl.uniprot.org/keywords/",
    "PMID": "http://purl.uniprot.org/citations/",
    "uniprot_annotation": "http://purl.uniprot.org/annotation/",
    "uniprot.proteome": "http://purl.uniprot.org/proteome/",
    "uniprot.database": "http://purl.uniprot.org/database/",
    "NCBITaxon": "http://purl.uniprot.org/taxonomy/",
    "InterPro": "http://purl.uniprot.org/interpro/",
    "embl_cds": "http://purl.uniprot.org/embl-cds/",
    "RHEA": "http://rdf.rhea-db.org/",
    "EC": "http://purl.uniprot.org/enzyme/",
}
"""Maps uniprot namespaces to conventional prefixes."""


@dataclass
class UniprotImplementation(
    AbstractSparqlImplementation,
    RelationGraphInterface,
    SearchInterface,
    OboGraphInterface,
    MappingProviderInterface,
    SemanticSimilarityInterface,
    SubsetterInterface,
    AssociationProviderInterface,
):
    """
    Wraps the Uniprot sparql endpoint.

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in Uniprot

    An UniprotImplementation can be initialed by:

        .. code:: python

           >>>  oi = UniprotImplementation()

    The default Uniprot endpoint will be assumed

    """

    def _default_url(self) -> str:
        return "https://sparql.uniprot.org/sparql"

    def _is_blazegraph(self) -> bool:
        return False

    def _mapping_predicates(self):
        return [RDF_SEE_ALSO, OWL_SAME_AS]

    def prefix_map(self) -> PREFIX_MAP:
        pmap = super().prefix_map()
        return {**pmap, **UNIPROT_PREFIX_MAP}

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

    def entities(self, **kwargs):
        raise NotImplementedError("Unbounded queries forbidden")

    def dump(self, path: str = None, syntax: str = None):
        raise NotImplementedError("Dump not allowed on Uniprot")

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        """
        Uniprot implementation of :ref:`relationships`

        .. warning ::

           for IS_A queries, we use rdfs:subClassOf, which in uniprot, includes
           the full closure.

        :param subjects: can be proteins, keywords, taxa, classification terms, etc
        :param predicates: uniprot predicates
        :param objects: as subjects
        :param include_tbox: not implemented, uniprot conflates distinction
        :param include_abox: not implemented, uniprot conflates distinction
        :param include_entailed: TODO
        :return:
        """

        exclude_predicates = [
            "up:mappedCitation",
            "up:mappedAnnotation",
            "up:attribution",
            "up:citation",
            "rdf:object",
            "rdf:subject",
        ]
        if predicates is not None:
            predicates = list(predicates)
            exclude_predicates = list(set(exclude_predicates).difference(predicates))
        query = SparqlQuery(
            select=["?s", "?p", "?o"],
            where=[
                "?s ?p ?o",
                "FILTER (isIRI(?s))",
                "FILTER (isIRI(?o))",
            ],
        )
        for exclude_predicate in exclude_predicates:
            query.add_filter(f"?p != {exclude_predicate}")
        if subjects is not None:
            query.add_values("s", [self.curie_to_sparql(x) for x in subjects])
        if predicates is not None:
            query.add_values("p", [self.curie_to_sparql(x) for x in predicates])
        if objects is not None:
            query.add_values("o", [self.curie_to_sparql(x) for x in objects])
        logging.info(f"REL: {query.query_str()}")
        bindings = self._query(query, prefixes=UNIPROT_PREFIX_MAP)
        for row in bindings:
            subj = self.uri_to_curie(row["s"]["value"])
            pred = self.uri_to_curie(row["p"]["value"])
            obj = self.uri_to_curie(row["o"]["value"])
            yield subj, pred, obj

    def associations(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
    ) -> Iterator[Association]:
        """
        Uniprot implementation of :ref:`associations`

        To query for all associations for a protein:

            >>> for assoc in oi.associations(["UniProtKB:Q62226"]):
            >>>     print(assoc)

        To query for all associations to a keyword, including closures

            >>> for assoc in oi.associations(
            >>>         objects=["UniProtKB-KW:9993"],
            >>>         object_closure_predicates=[IS_A]):
            >>>     print(assoc)

        Note: this may be slow

        :param subjects: typically Uniprot entries
        :param predicates: defaults to up:classifiedWith
        :param objects: can be GO, EC, KW, ...
        :param property_filter: not implemented
        :param subject_closure_predicates: not implemented (proteins are "flat")
        :param predicate_closure_predicates: not implemented (uniprot predicate hierarchy is "flat")
        :param object_closure_predicates: e.g. IS_A
        :param include_modified: not implemented
        :return:
        """
        query = SparqlQuery(
            select=["?s", "?p", "?o"],
            where=[
                "?s ?p ?o",
                "FILTER (isIRI(?s))",
                "FILTER (isIRI(?o))",
            ],
        )
        if predicates is None:
            predicates = ["up:classifiedWith"]
        if subjects is not None:
            query.add_values("s", [self.curie_to_sparql(x) for x in subjects])
        if predicates is not None:
            query.add_values("p", [self.curie_to_sparql(x) for x in predicates])
        if objects is not None:
            if object_closure_predicates is None or object_closure_predicates != []:
                query.where.append("?o ?closure_predicate ?o_anc")
                if object_closure_predicates:
                    query.add_values(
                        "closure_predicate",
                        [self.curie_to_sparql(x) for x in object_closure_predicates],
                    )
                query.add_values("o_anc", [self.curie_to_sparql(x) for x in objects])
            else:
                query.add_values("o", [self.curie_to_sparql(x) for x in objects])
        logging.info(f"REL: {query.query_str()}")
        bindings = self._query(query, prefixes=UNIPROT_PREFIX_MAP)
        for row in bindings:
            subj = self.uri_to_curie(row["s"]["value"])
            pred = self.uri_to_curie(row["p"]["value"])
            obj = self.uri_to_curie(row["o"]["value"])
            yield Association(subject=subj, predicate=pred, object=obj)
