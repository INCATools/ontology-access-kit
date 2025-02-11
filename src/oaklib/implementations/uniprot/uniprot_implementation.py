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

import requests

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels.association import Association
from oaklib.datamodels.vocabulary import OWL_SAME_AS, RDFS_SEE_ALSO
from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.implementations.sparql.sparql_query import SparqlQuery
from oaklib.interfaces import SubsetterInterface, TextAnnotatorInterface
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

UNIPROT_API_URL = "https://rest.uniprot.org/uniprotkb"

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
    TextAnnotatorInterface,
):
    """
    Wraps the Uniprot sparql endpoint.

    This is a specialization of the more generic :class:`.SparqlImplementation`, which
    has knowledge of some of the specialized patterns found in Uniprot

    An UniprotImplementation can be initialed by:

    >>> from oaklib.implementations.uniprot.uniprot_implementation import UniprotImplementation
    >>> adapter = UniprotImplementation()

    or

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("uniprot:")

    The default Uniprot endpoint will be assumed

    """

    def _default_url(self) -> str:
        return "https://sparql.uniprot.org/sparql"

    def _is_blazegraph(self) -> bool:
        return False

    def _mapping_predicates(self):
        return [RDFS_SEE_ALSO, OWL_SAME_AS]

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
        include_entailed: bool = False,
        exclude_blank: bool = True,
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
        bindings = self._sparql_query(query, prefixes=UNIPROT_PREFIX_MAP)
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
        **kwargs,
    ) -> Iterator[Association]:
        """
        Uniprot implementation of :ref:`associations`

        To query for some associations for a protein:

        >>> import itertools
        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("uniprot:")
        >>> # for demo purposes we pick the first N
        >>> for assoc in itertools.islice(adapter.associations(["UniProtKB:Q62226"]), 5):
        ...     print(assoc.subject, assoc.predicate, assoc.object)
        <BLANKLINE>
        UniProtKB:Q62226 up:classifiedWith GO:...
        ...

        To query for all associations to a keyword, including closures

        >>> from oaklib.datamodels.vocabulary import IS_A
        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("uniprot:")
        >>> assocs = adapter.associations(
        ...         objects=["UniProtKB-KW:9993"],
        ...         object_closure_predicates=[IS_A])

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
        if subjects:
            yield from self._associations_via_api(
                subjects,
                predicates,
                objects,
            )
            return
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
        bindings = self._sparql_query(query, prefixes=UNIPROT_PREFIX_MAP)
        for row in bindings:
            subj = self.uri_to_curie(row["s"]["value"])
            pred = self.uri_to_curie(row["p"]["value"])
            obj = self.uri_to_curie(row["o"]["value"])
            yield Association(subject=subj, predicate=pred, object=obj)

    def _associations_via_api(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        add_closure_fields: bool = False,
        **kwargs,
    ) -> Iterator[Association]:
        if not subjects:
            raise ValueError("subjects must be specified")
        subjects = list(subjects)
        for subject in subjects:
            acc = subject
            if subject.startswith("UniProtKB:"):
                acc = subject.split(":")[1]
            params = {
                "format": "json",
            }
            response = requests.get(f"{UNIPROT_API_URL}/{acc}", params, timeout=TIMEOUT_SECONDS)
            logging.info(f"URL: {response.url}")
            if response.status_code != 200:
                raise ValueError(f"Could not find {subject}")
            data = response.json()
            for assoc in self._parse_uniprot_json(subject, data):
                yield assoc

    def _parse_uniprot_json(
        self, subject: CURIE, data: dict, databases: List[str] = None
    ) -> Iterator[Association]:
        if not databases:
            databases = ["GO", "EC", "KW", "Reactome", "Interpro", "Pfam", "KEGG"]
        label_property_by_database = {
            "GO": "GoTerm",
            "Reactome": "PathwayName",
        }
        gene_name = data["genes"][0].get("geneName", {}).get("value", None)
        for xref in data.get("uniProtKBCrossReferences", []):
            # print(xref)
            database = xref["database"]
            if database not in databases:
                continue
            # translate list of {key: key, value: value} to dict
            props = {x["key"]: x["value"] for x in xref.get("properties", [])}
            evidences = [(props.get("GoEvidenceType", None), None)]
            if "evidences" in xref:
                evidences = [
                    (x["evidenceCode"], f'{x["source"]}:{x["id"]}') for x in xref["evidences"]
                ]
            for evidence_type, pubs in evidences:
                object_id = xref["id"]
                if ":" not in object_id:
                    # unbanana
                    object_id = f"{database}:{object_id}"
                object_label = props.get(
                    label_property_by_database.get(database, "EntryName"), None
                )
                if database == "GO":
                    object_label = object_label[2:]
                assoc = Association(
                    subject=subject,
                    subject_label=gene_name,
                    object=object_id,
                    object_label=object_label,
                    evidence_type=evidence_type,
                    publications=pubs,
                )
                yield assoc
        for comment in data.get("comments", []):
            typ = comment.get("commentType", None)
            # print(comment)
            if typ is None:
                continue
            if typ == "FUNCTION":
                continue
            elif typ == "CATALYTIC ACTIVITY":
                reaction = comment["reaction"]
                if "ecNumber" in reaction:
                    object_id = f"EC:{reaction['ecNumber']}"
                else:
                    object_id = reaction["reactionCrossReferences"][0]["id"]
                object_label = reaction["name"]
                evidences = reaction.get("evidences", [])
            else:
                continue
            for evidence in evidences:
                assoc = Association(
                    subject=subject,
                    subject_label=gene_name,
                    object=object_id,
                    object_label=object_label,
                    evidence_type=evidence["evidenceCode"],
                    publications=f'{evidence["source"]}:{evidence["id"]}',
                )
                yield assoc
