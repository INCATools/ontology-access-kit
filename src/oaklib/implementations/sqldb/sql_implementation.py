import logging
import math
import shutil
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

import rdflib
import semsql.builder.builder as semsql_builder
from kgcl_schema.datamodel import kgcl
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.metamodelcore import URIorCURIE
from semsql.sqla.semsql import (
    AnnotationPropertyNode,
    ClassNode,
    DeprecatedNode,
    Edge,
    EntailedEdge,
    HasMappingStatement,
    HasSynonymStatement,
    HasTextDefinitionStatement,
    IriNode,
    NamedIndividualNode,
    Node,
    ObjectPropertyNode,
    OntologyNode,
    OwlAxiomAnnotation,
    OwlEquivalentClassStatement,
    OwlSomeValuesFrom,
    Prefix,
    RdfFirstStatement,
    RdfRestStatement,
    RdfsLabelStatement,
    RdfTypeStatement,
    Statements,
)
from sqlalchemy import and_, create_engine, delete, insert, text, update
from sqlalchemy.orm import aliased, sessionmaker
from sssom_schema import Mapping

import oaklib.datamodels.ontology_metadata as om
import oaklib.datamodels.validation_datamodel as vdm
from oaklib.constants import OAKLIB_MODULE
from oaklib.datamodels import obograph, ontology_metadata
from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.datamodels.vocabulary import (
    ALL_MATCH_PREDICATES,
    DEPRECATED_PREDICATE,
    EQUIVALENT_CLASS,
    HAS_DBXREF,
    HAS_EXACT_SYNONYM,
    HAS_SYNONYM_TYPE,
    IN_CATEGORY_PREDS,
    IN_SUBSET,
    IS_A,
    LABEL_PREDICATE,
    RDF_TYPE,
    SEMAPV,
    SYNONYM_PREDICATES,
    omd_slots,
)
from oaklib.implementations.sqldb import SEARCH_CONFIG
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    METADATA_MAP,
    PRED_CURIE,
    PREFIX_MAP,
    RELATIONSHIP,
    RELATIONSHIP_MAP,
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
from oaklib.types import CATEGORY_CURIE, CURIE, SUBSET_CURIE
from oaklib.utilities.basic_utils import get_curie_prefix, pairs_as_dict

__all__ = [
    "get_range_xsd_type",
    "regex_to_sql_like",
    "SqlImplementation",
]


def _is_blank(curie: CURIE) -> bool:
    return curie.startswith("_:")


def _mapping(m: Mapping):
    # enhances a mapping with sources
    # TODO: move to sssom utils
    m.subject_source = get_curie_prefix(m.subject_id)
    m.object_source = get_curie_prefix(m.object_id)
    return m


def get_range_xsd_type(sv: SchemaView, rng: str) -> Optional[URIorCURIE]:
    t = sv.get_type(rng)
    if t.uri:
        return t.uri
    elif t.typeof:
        return get_range_xsd_type(sv, t.typeof)
    else:
        raise ValueError(f"No xsd type for {rng}")


def regex_to_sql_like(regex: str) -> str:
    """
    convert a regex to a LIKE

    TODO: implement various different DBMS flavors
    https://stackoverflow.com/questions/20794860/regex-in-sql-to-detect-one-or-more-digit

    :param regex:
    :return:
    """
    for c in r"()[]{}|":
        if c in regex:
            raise NotImplementedError(
                f"Regex engine not implemented for SQL and cannot parse char {c} in {regex}"
            )
    like = regex.replace(".*", "%")
    like = like.replace(".", "_")
    if like.startswith("^"):
        like = like[1:]
    else:
        like = f"%{like}"
    if like.endswith("$"):
        like = like[0:-1]
    else:
        like = f"{like}%"
    logging.info(f"Translated {regex} => {like}")
    return like


def _is_quoted_url(curie: CURIE):
    return curie.startswith("<")


@dataclass
class SqlImplementation(
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
    ABC,
):
    """
    A :class:`OntologyInterface` implementation that wraps a SQL Relational Database

    This could be a local file (accessed via SQL Lite) or a local/remote server (e.g PostgreSQL)

    The schema is assumed to follow the `semantic-sql <https://github.com/incatools/semantic-sql>`_ schema

    This uses SQLAlchemy ORM Models:

    - :class:`Statements`
    - :class:`Edge`
    """

    # TODO: use SQLA types
    engine: Any = None
    _session: Any = None
    _connection: Any = None
    _ontology_metadata_model: SchemaView = None
    _prefix_map: PREFIX_MAP = None
    _information_content_cache: Dict[Tuple[CURIE, Set[PRED_CURIE]], float] = None

    def __post_init__(self):
        if self.engine is None:
            locator = str(self.resource.slug)
            logging.info(f"Locator: {locator}")
            if locator.startswith("obo:"):
                # easter egg feature, to be documented:
                # The selector 'sqlite:obo:ONTOLOGY' will use a pre-generated
                # sqlite db of an OBO ontology after downloading from S3.
                # Note: this can take some time
                prefix = locator[len("obo:") :]
                # Option 1 uses direct URL construction:
                url = f"https://s3.amazonaws.com/bbop-sqlite/{prefix}.db"
                db_path = OAKLIB_MODULE.ensure(url=url)
                # Option 2 uses botocore to interface with the S3 API directly:
                # db_path = OAKLIB_MODULE.ensure_from_s3(s3_bucket="bbop-sqlite", s3_key=f"{prefix}.db")
                locator = f"sqlite:///{db_path}"
            if locator.endswith(".owl"):
                # this is currently an "Easter Egg" feature. It allows you to specify a locator
                # such as sqlite:/path/to/my.owl
                # then semsql will be invoked to build a sqlite db from this.
                # the same sqlite db will be reused until the timestamp of the owl file changes.
                # the catch is that EITHER the user must have BOTH rdftab and relation-graph installed, OR
                # they should be running through ODK docker
                locator = locator.replace(".owl", ".db").replace("sqlite:", "")
                logging.info(f"Building {locator} using semsql")
                semsql_builder.make(locator)
                locator = f"sqlite:///{locator}"
            else:
                path = Path(locator.replace("sqlite:", "")).absolute()
                locator = f"sqlite:///{path}"
            logging.info(f"Locator, post-processed: {locator}")
            self.engine = create_engine(locator)

    @property
    def session(self):
        if self._session is None:
            session_cls = sessionmaker(self.engine)
            self._session = session_cls()
        return self._session

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.engine.connect()
        return self._session

    @property
    def ontology_metadata_model(self):
        if self._ontology_metadata_model is None:
            self._ontology_metadata_model = package_schemaview(ontology_metadata.__name__)
        return self._ontology_metadata_model

    def is_mysql(self):
        # TODO
        return False

    def is_postgres(self):
        # TODO
        return False

    def prefix_map(self) -> PREFIX_MAP:
        if self._prefix_map is None:
            self._prefix_map = {row.prefix: row.base for row in self.session.query(Prefix)}
        return self._prefix_map

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        # TODO: figure out how to pass through ESCAPE at SQL Alchemy level
        # s = text('SELECT id FROM class_node WHERE id NOT LIKE "\_:%" ESCAPE "\\"')  # noqa W605
        q = self.session.query(Node)
        if owl_type:
            subquery = self.session.query(RdfTypeStatement.subject).filter(
                RdfTypeStatement.object == owl_type
            )
            q = q.filter(Node.id.in_(subquery))
        if filter_obsoletes:
            obs_subq = self.session.query(DeprecatedNode.id)
            q = q.filter(Node.id.not_in(obs_subq))
        logging.info(f"Query: {q}")
        for row in q:
            if row:
                # if not _is_blank(row.id) and not row.id.startswith("<"):
                if not _is_blank(row.id):
                    yield row.id

    def obsoletes(self) -> Iterable[CURIE]:
        for row in self.session.query(DeprecatedNode):
            yield row.id

    def all_relationships(self) -> Iterable[RELATIONSHIP]:
        for row in self.session.query(Edge):
            yield row.subject, row.predicate, row.object

    def label(self, curie: CURIE) -> Optional[str]:
        s = text("SELECT value FROM rdfs_label_statement WHERE subject = :curie")
        for row in self.engine.execute(s, curie=curie):
            return row["value"]

    def labels(self, curies: Iterable[CURIE], allow_none=True) -> Iterable[Tuple[CURIE, str]]:
        curies = list(curies)
        has_label = set()
        for row in self.session.query(RdfsLabelStatement).filter(
            RdfsLabelStatement.subject.in_(tuple(curies))
        ):
            yield row.subject, row.value
            if allow_none:
                has_label.add(row.subject)
        if allow_none:
            for curie in curies:
                if curie not in has_label:
                    yield curie, None

    def curies_by_label(self, label: str) -> List[CURIE]:
        q = self.session.query(RdfsLabelStatement)
        q = q.filter(RdfsLabelStatement.value == label)
        return [row.subject for row in q]

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [self.label(curie)]
        for row in self.session.query(HasSynonymStatement).filter(
            HasSynonymStatement.subject == curie
        ):
            m[row.predicate].append(row.value)
        return m

    def definition(self, curie: CURIE) -> Optional[str]:
        for row in self.session.query(HasTextDefinitionStatement).filter(
            HasTextDefinitionStatement.subject == curie
        ):
            return row.value

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        m = {"id": curie}
        # subquery = self.session.query(AnnotationPropertyNode.id)
        subquery = self.session.query(RdfTypeStatement.subject).filter(
            RdfTypeStatement.object == "owl:AnnotationProperty"
        )
        q = self.session.query(Statements)
        q = q.filter(Statements.predicate.in_(subquery))
        for row in q.filter(Statements.subject == curie):
            if row.value is not None:
                v = row.value
            elif row.object is not None:
                v = row.object
            else:
                v = None
            if row.predicate in m:
                if not isinstance(m[row.predicate], list):
                    m[row.predicate] = [m[row.predicate]]
                m[row.predicate].append(v)
            else:
                m[row.predicate] = v
        return m

    def ontologies(self) -> Iterable[CURIE]:
        for row in self.session.query(OntologyNode):
            yield row.id

    def _get_subset_curie(self, curie: str) -> str:
        if "#" in curie:
            return curie.split("#")[-1]
        else:
            return curie

    def _subset_uri_to_curie_map(self) -> Dict[str, CURIE]:
        m = {}
        for row in self.session.query(Statements.object).filter(Statements.predicate == IN_SUBSET):
            uri = row.object
            m[uri] = self._get_subset_curie(row.object)
        return m

    def _subset_curie_to_uri_map(self) -> Dict[CURIE, str]:
        m = {}
        for row in self.session.query(Statements.object, Statements.value).filter(
            Statements.predicate == IN_SUBSET
        ):
            uri = row.object
            if row.object is None:
                logging.warning(f"Subset may be incorrectly encoded as value for {row.value}")
            else:
                m[self._get_subset_curie(row.object)] = uri
        return m

    def subsets(self) -> Iterable[SUBSET_CURIE]:
        for s in self._subset_curie_to_uri_map().keys():
            yield s

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        sm = self._subset_curie_to_uri_map()
        for row in self.session.query(Statements.subject).filter(
            Statements.predicate == IN_SUBSET, Statements.object == sm[subset]
        ):
            yield self._get_subset_curie(row.subject)

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        for row in self.session.query(Statements).filter(
            Statements.predicate == IN_SUBSET, Statements.subject.in_(list(curies))
        ):
            yield row.subject, self._get_subset_curie(row.object)

    def terms_categories(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CATEGORY_CURIE]]:
        for row in self.session.query(Statements).filter(
            Statements.predicate.in_(IN_CATEGORY_PREDS), Statements.subject.in_(list(curies))
        ):
            yield row.subject, self._get_subset_curie(row.object)

    def _execute(self, stmt):
        self.session.execute(stmt)
        self.session.flush()
        if self.autosave:
            self.save()

    def set_label(self, curie: CURIE, label: str) -> bool:
        stmt = (
            update(Statements)
            .where(and_(Statements.subject == curie, Statements.predicate == LABEL_PREDICATE))
            .values(value=label)
        )
        self._execute(stmt)

    def basic_search(
        self, search_term: str, config: SearchConfiguration = SEARCH_CONFIG
    ) -> Iterable[CURIE]:
        preds = []
        preds.append(omd_slots.label.curie)
        search_all = SearchProperty(SearchProperty.ANYTHING) in config.properties
        if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
            preds += SYNONYM_PREDICATES
        view = Statements

        def make_query(qcol):
            q = self.session.query(view.subject).filter(view.predicate.in_(tuple(preds)))
            if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
                q = q.filter(qcol.like(f"{search_term}%"))
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.SQL):
                q = q.filter(qcol.like(search_term))
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
                if self.is_mysql():
                    q = q.filter(qcol.op("regex")(search_term))
                elif self.is_postgres():
                    q = q.filter(qcol.op("~")(search_term))
                else:
                    q = q.filter(qcol.like(regex_to_sql_like(search_term)))
            elif config.is_partial:
                q = q.filter(qcol.like(f"%{search_term}%"))
            else:
                q = q.filter(qcol == search_term)
            return q

        q = make_query(view.value)
        for row in q.distinct():
            yield str(row.subject)
        if search_all or SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
            q = make_query(view.subject)
            for row in q.distinct():
                yield str(row.subject)

    def outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None, entailed=False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        if entailed:
            tbl = EntailedEdge
        else:
            tbl = Edge
        q = self.session.query(tbl).filter(tbl.subject == curie)
        if predicates:
            q = q.filter(tbl.predicate.in_(predicates))
        logging.debug(f"Querying outgoing, curie={curie}, predicates={predicates}, q={q}")
        for row in q:
            yield row.predicate, row.object
        if not predicates or RDF_TYPE in predicates:
            q = self.session.query(RdfTypeStatement.object).filter(
                RdfTypeStatement.subject == curie
            )
            cls_subq = self.session.query(ClassNode.id)
            q = q.filter(RdfTypeStatement.object.in_(cls_subq))
            for row in q:
                yield RDF_TYPE, row.object
        if tbl == Edge and (not predicates or EQUIVALENT_CLASS in predicates):
            q = self.session.query(OwlEquivalentClassStatement.object).filter(
                OwlEquivalentClassStatement.subject == curie
            )
            cls_subq = self.session.query(ClassNode.id)
            q = q.filter(OwlEquivalentClassStatement.object.in_(cls_subq))
            for row in q:
                yield EQUIVALENT_CLASS, row.object

    def outgoing_relationship_map(self, *args, **kwargs) -> RELATIONSHIP_MAP:
        return pairs_as_dict(self.outgoing_relationships(*args, **kwargs))

    def entailed_outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self.outgoing_relationships(curie, predicates, entailed=True)

    def incoming_relationship_map(self, curie: CURIE) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for row in self.session.query(Edge).filter(Edge.object == curie):
            rmap[row.predicate].append(row.subject)
        return rmap

    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        if include_tbox:
            for r in self._tbox_relationships(
                subjects, predicates, objects, include_entailed=include_entailed
            ):
                yield r
            for r in self._equivalent_class_relationships(subjects, predicates, objects):
                yield r
            if subjects or objects:
                for s, p, o in self._equivalent_class_relationships(objects, predicates, subjects):
                    yield o, p, s
        if include_abox:
            for r in self._rdf_type_relationships(subjects, predicates, objects):
                yield r
            for r in self._object_property_assertion_relationships(subjects, predicates, objects):
                yield r

    def _tbox_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_entailed: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        if include_entailed:
            tbl = EntailedEdge
        else:
            tbl = Edge
        q = self.session.query(tbl)
        if subjects:
            q = q.filter(tbl.subject.in_(tuple(subjects)))
        if predicates:
            q = q.filter(tbl.predicate.in_(tuple(predicates)))
        if objects:
            q = q.filter(tbl.object.in_(tuple(objects)))
        logging.info(f"Tbox query: {q}")
        for row in q:
            yield row.subject, row.predicate, row.object

    def _object_property_assertion_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
    ) -> Iterator[RELATIONSHIP]:
        q = self.session.query(Statements)
        if subjects:
            q = q.filter(Statements.subject.in_(tuple(subjects)))
        if predicates:
            predicates = set(predicates).difference({IS_A, RDF_TYPE})
            if not predicates:
                return
            q = q.filter(Statements.predicate.in_(tuple(predicates)))
        else:
            op_subq = self.session.query(ObjectPropertyNode.id)
            q = q.filter(Statements.predicate.in_(op_subq))
        if objects:
            q = q.filter(Statements.object.in_(tuple(objects)))
        for row in q:
            yield row.subject, row.predicate, row.object

    def _rdf_type_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
    ) -> Iterator[RELATIONSHIP]:
        if predicates and RDF_TYPE not in predicates:
            return
        q = self.session.query(Statements).filter(Statements.predicate == RDF_TYPE)
        if subjects:
            q = q.filter(Statements.subject.in_(tuple(subjects)))
        if objects:
            q = q.filter(Statements.object.in_(tuple(objects)))
        cls_subq = self.session.query(ClassNode.id)
        q = q.filter(Statements.object.in_(cls_subq))
        for row in q:
            yield row.subject, row.predicate, row.object

    def _equivalent_class_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
    ) -> Iterator[RELATIONSHIP]:
        if predicates and EQUIVALENT_CLASS not in predicates:
            return
        q = self.session.query(Statements).filter(Statements.predicate == EQUIVALENT_CLASS)
        if subjects:
            q = q.filter(Statements.subject.in_(tuple(subjects)))
        if objects:
            q = q.filter(Statements.object.in_(tuple(objects)))
        cls_subq = self.session.query(ClassNode.id)
        q = q.filter(Statements.object.in_(cls_subq))
        for row in q:
            yield row.subject, row.predicate, row.object

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        for row in self.session.query(HasMappingStatement).filter(
            HasMappingStatement.subject == curie
        ):
            yield row.predicate, row.value

    def clone(self, resource: Any) -> None:
        if self.resource.scheme == "sqlite":
            if resource.scheme == "sqlite":
                shutil.copyfile(self.resource.slug, resource.slug)
                new_oi = type(self)(resource)
                return new_oi
        raise NotImplementedError("Can only clone sqlite to sqlite")

    def dump(self, path: str = None, syntax: str = None):
        if syntax is None or syntax == "ttl":
            g = rdflib.Graph()
            bnodes = {}

            def tr(n: str, v: str = None, datatype: str = None):
                if n:
                    if n.startswith("_"):
                        if n not in bnodes:
                            bnodes[n] = rdflib.BNode()
                        return bnodes[n]
                    else:
                        return rdflib.URIRef(self.curie_to_uri(n))
                else:
                    lit = rdflib.Literal(v, datatype=datatype)
                    return lit

            for row in self.session.query(Statements):
                s = tr(row.subject)
                p = tr(row.predicate)
                o = tr(row.object, row.value, row.datatype)
                logging.debug(f"Triple {s} {p} {o}")
                g.add((s, p, o))
            logging.info(f"Dumping to {path}")
            g.serialize(path, format=syntax)
        elif syntax == "sqlite":
            raise NotImplementedError
        else:
            raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False, include_metadata=False) -> obograph.Node:
        meta = obograph.Meta()
        n = obograph.Node(id=curie, meta=meta)
        rows = list(self.session.query(Statements).filter(Statements.subject == curie))

        def _anns_to_xrefs_and_meta(parent_pv: obograph.PropertyValue, anns: List[om.Annotation]):
            parent_pv.xrefs = [ann.object for ann in anns if ann.predicate == HAS_DBXREF]
            pvs = [
                obograph.BasicPropertyValue(pred=ann.predicate, val=ann.object)
                for ann in anns
                if ann.predicate != HAS_DBXREF
            ]
            if pvs:
                parent_pv.meta = obograph.Meta(basicPropertyValues=pvs)

        for row in rows:
            if row.value is not None:
                v = row.value
            elif row.object is not None:
                v = row.object
            else:
                continue
            pred = row.predicate
            if pred == omd_slots.label.curie:
                n.lbl = v
            else:
                if include_metadata:
                    anns = self._axiom_annotations(curie, pred, row.object, row.value)
                else:
                    anns = []
                if pred == omd_slots.definition.curie:
                    meta.definition = obograph.DefinitionPropertyValue(val=v)
                    _anns_to_xrefs_and_meta(meta.definition, anns)
                else:
                    pv = obograph.BasicPropertyValue(pred=pred, val=v)
                    _anns_to_xrefs_and_meta(pv, anns)
                    meta.basicPropertyValues.append(pv)
        return n

    def synonym_property_values(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Iterator[Tuple[CURIE, obograph.SynonymPropertyValue]]:
        if isinstance(subject, CURIE):
            subject = [subject]
        q = self.session.query(Statements).filter(Statements.subject.in_(tuple(subject)))
        q = q.filter(Statements.predicate.in_(SYNONYM_PREDICATES))
        for row in q:
            spv = obograph.SynonymPropertyValue(pred=row.predicate, val=row.value)
            anns = self._axiom_annotations(row.subject, row.predicate, value=row.value)
            for ann in anns:
                if ann.predicate == HAS_SYNONYM_TYPE:
                    spv.synonymType = ann.object
                if ann.predicate == HAS_DBXREF:
                    spv.xrefs.append(ann.object)
            yield row.subject, spv

    def _axiom_annotations(
        self, subject: CURIE, predicate: CURIE, object: CURIE = None, value: Any = None
    ) -> List[om.Annotation]:
        q = self.session.query(OwlAxiomAnnotation)
        q = q.filter(OwlAxiomAnnotation.subject == subject)
        q = q.filter(OwlAxiomAnnotation.predicate == predicate)
        if object:
            q = q.filter(OwlAxiomAnnotation.object == object)
        if value:
            q = q.filter(OwlAxiomAnnotation.value == value)
        return [
            om.Annotation(
                row.annotation_predicate,
                row.annotation_value if row.annotation_value is not None else row.annotation_object,
            )
            for row in q
        ]

    def ancestors(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.subject.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.subject == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        logging.debug(f"Ancestors query: {q}")
        for row in q:
            yield row.object

    def multi_ancestors(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[RELATIONSHIP]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.subject.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.subject == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        logging.debug(f"Ancestors query, start from {start_curies}: {q}")
        for row in q:
            yield row.subject, row.predicate, row.object

    def descendants(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.object.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.object == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        for row in q:
            yield row.subject

    def _rdf_list(self, bnode: str) -> Iterable[str]:
        for row in self.session.query(RdfFirstStatement).filter(RdfFirstStatement.subject == bnode):
            yield row.object
        for row in self.session.query(RdfRestStatement.object).filter(
            RdfRestStatement.subject == bnode
        ):
            for x in self._rdf_list(row.object):
                yield x

    def _ixn_definition(self, ixn: str, subject: CURIE) -> Optional[LogicalDefinitionAxiom]:
        ldef = LogicalDefinitionAxiom(definedClassId=subject)
        n = 0
        for ixn_node in self._rdf_list(ixn):
            n += 1
            if _is_blank(ixn_node):
                svfq = self.session.query(OwlSomeValuesFrom).filter(
                    OwlSomeValuesFrom.id == ixn_node
                )
                svfq = list(svfq)
                if svfq:
                    if len(svfq) > 1:
                        raise ValueError(f"Incorrect rdf structure for equiv axioms for {ixn_node}")
                    svf = svfq[0]
                    ldef.restrictions.append(
                        ExistentialRestrictionExpression(
                            propertyId=svf.on_property, fillerId=svf.filler
                        )
                    )
                else:
                    ldef = None
                    break
            else:
                ldef.genusIds.append(ixn_node)
        if n and ldef:
            return ldef

    def logical_definitions(self, subjects: Iterable[CURIE]) -> Iterable[LogicalDefinitionAxiom]:
        q = self.session.query(OwlEquivalentClassStatement)
        q = q.filter(OwlEquivalentClassStatement.subject.in_(tuple(subjects)))
        for eq_row in q:
            ixn_q = self.session.query(Statements).filter(
                and_(
                    Statements.subject == eq_row.object,
                    Statements.predicate == "owl:intersectionOf",
                )
            )
            for ixn in ixn_q:
                ldef = self._ixn_definition(ixn.object, eq_row.subject)
                if ldef:
                    yield ldef

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: RelationGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def entailed_relationships_between(self, subject: CURIE, object: CURIE) -> Iterable[PRED_CURIE]:
        preds = []
        for row in (
            self.session.query(EntailedEdge.predicate)
            .filter(EntailedEdge.subject == subject)
            .filter(EntailedEdge.object == object)
        ):
            p = row.predicate
            if p not in preds:
                yield p
            preds.append(p)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def sssom_mappings_by_source(self, subject_or_object_source: str = None) -> Iterable[Mapping]:
        predicates = tuple(ALL_MATCH_PREDICATES)
        base_query = self.session.query(Statements).filter(Statements.predicate.in_(predicates))
        for row in base_query:
            v = row.value if row.value is not None else row.object
            # TODO: this check is slow
            if URIorCURIE.is_valid(v):
                if row.subject.startswith("_:"):
                    continue
                mpg = Mapping(
                    subject_id=row.subject,
                    object_id=v,
                    predicate_id=row.predicate,
                    mapping_justification=SEMAPV.UnspecifiedMatching.value,
                )
                _mapping(mpg)
                if subject_or_object_source:
                    # TODO: consider moving to query for efficiency
                    if (
                        mpg.subject_source != subject_or_object_source
                        and mpg.object_source != subject_or_object_source
                    ):
                        continue
                yield mpg
            else:
                if self.strict:
                    raise ValueError(f"not a CURIE: {v}")

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[Mapping]:
        predicates = tuple(ALL_MATCH_PREDICATES)
        base_query = self.session.query(Statements).filter(Statements.predicate.in_(predicates))
        for row in base_query.filter(Statements.subject == curie):
            mpg = Mapping(
                subject_id=curie,
                object_id=row.value if row.value is not None else row.object,
                predicate_id=row.predicate,
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            yield _mapping(mpg)
        # xrefs are stored as literals
        for row in base_query.filter(Statements.value == curie):
            mpg = Mapping(
                subject_id=row.subject,
                object_id=curie,
                predicate_id=row.predicate,
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            yield _mapping(mpg)
        # skos mappings are stored as objects
        for row in base_query.filter(Statements.object == curie):
            mpg = Mapping(
                subject_id=row.subject,
                object_id=curie,
                predicate_id=row.predicate,
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            yield _mapping(mpg)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: ValidatorInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def validate(
        self, configuration: vdm.ValidationConfiguration = None
    ) -> Iterable[vdm.ValidationResult]:
        if configuration and configuration.schema_path:
            sv = SchemaView(configuration.schema_path)
            self._ontology_metadata_model = sv
        else:
            sv = self.ontology_metadata_model
        for slot_name in sv.all_slots():
            for r in self._check_slot(slot_name):
                yield r
        for r in self._check_for_unknown_slots():
            yield r

    def _missing_value(
        self, predicate_table: Type, type_table: Type = ClassNode
    ) -> Iterable[CURIE]:
        pred_subq = self.session.query(predicate_table.subject)
        obs_subq = self.session.query(DeprecatedNode.id)
        main_q = self.session.query(type_table).join(IriNode, type_table.id == IriNode.id)
        for row in main_q.filter(type_table.id.not_in(pred_subq)).filter(
            type_table.id.not_in(obs_subq)
        ):
            yield row.id

    def term_curies_without_definitions(self) -> Iterable[CURIE]:
        return self._missing_value(HasTextDefinitionStatement)

    def term_curies_without_labels(self) -> Iterable[CURIE]:
        return self._missing_value(RdfsLabelStatement)

    def _check_for_unknown_slots(self) -> Iterable[vdm.ValidationResult]:
        sv = self.ontology_metadata_model
        preds = [sv.get_uri(s, expand=False) for s in sv.all_slots().values()]
        logging.info(f"Known preds: {len(preds)} -- checking for other uses")
        main_q = (
            self.session.query(Statements)
            .filter(Statements.predicate.not_in(preds))
            .join(IriNode, Statements.subject == IriNode.id)
        )
        try:
            for row in main_q:
                result = vdm.ValidationResult(
                    subject=row.subject,
                    predicate=row.predicate,
                    severity=vdm.SeverityOptions.ERROR,
                    type=vdm.ValidationResultType.ClosedConstraintComponent.meaning,
                    info=f"Unknown pred ({row.predicate}) = {row.object} {row.value}",
                )
                yield result
        except ValueError as e:
            logging.error(f"EXCEPTION: {e}")
            pass

    def _check_slot(
        self, slot_name: str, class_name: str = "Class"
    ) -> Iterable[vdm.ValidationResult]:
        """
        Validates all data with respect to a specific slot

        :param slot_name:
        :param class_name:
        :return:
        """
        sv = self.ontology_metadata_model
        # for efficiency we map directly to table/view names rather
        # than querying over rdf:type; this allows for optimization via view materialization
        if class_name == "Class":
            sqla_cls = ClassNode
        elif class_name == "ObjectProperty":
            sqla_cls = ObjectPropertyNode
        elif class_name == "AnnotationProperty":
            sqla_cls = AnnotationPropertyNode
        elif class_name == "NamedIndividual":
            sqla_cls = NamedIndividualNode
        else:
            raise NotImplementedError(f"cannot handle {class_name}")
        slot = sv.induced_slot(slot_name, class_name)
        if slot.designates_type:
            logging.info(f"Ignoring type designator: {slot_name}")
            return
        logging.info(f"Validating: {slot_name}")
        predicate = sv.get_uri(slot, expand=False)
        is_used = (
            self.session.query(Statements.predicate)
            .filter(Statements.predicate == predicate)
            .first()
            is not None
        )
        pred_subq = self.session.query(Statements.subject).filter(Statements.predicate == predicate)
        obs_subq = self.session.query(DeprecatedNode.id)
        if (slot.required or slot.recommended) and not slot.identifier:
            # MinCardinality == 1
            if slot.required:
                severity = vdm.SeverityOptions.ERROR
            else:
                severity = vdm.SeverityOptions.WARNING
            logging.info(f"MinCard check: Leaving off: {slot_name} is {severity.text}")
            # exclude blank nodes
            main_q = self.session.query(sqla_cls).join(IriNode, sqla_cls.id == IriNode.id)
            main_q = main_q.filter(sqla_cls.id.not_in(pred_subq))
            main_q = main_q.filter(sqla_cls.id.not_in(obs_subq))
            for row in main_q:
                result = vdm.ValidationResult(
                    subject=row.id,
                    predicate=predicate,
                    severity=severity,
                    type=vdm.ValidationResultType.MinCountConstraintComponent.meaning,
                    info=f"Missing slot ({slot_name}) for {row.id}",
                )
                yield result
        if not is_used:
            return
        if slot.deprecated:
            main_q = self.session.query(Statements.subject).filter(
                Statements.predicate == predicate
            )
            main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
            for row in main_q:
                result = vdm.ValidationResult(
                    subject=row.subject,
                    predicate=predicate,
                    severity=vdm.SeverityOptions.WARNING,
                    type=vdm.ValidationResultType.DeprecatedPropertyComponent.meaning,
                    info=f"Deprecated slot ({slot_name}) for {row.subject}",
                )
                yield result
        if not slot.multivalued:
            # MaxCardinality == 1
            # TODO
            is_object_iri = slot.range in sv.all_classes()
            st1 = aliased(Statements)
            st2 = aliased(Statements)
            main_q = self.session.query(st1.subject).join(st2, st1.subject == st2.subject)
            main_q = main_q.filter(st1.predicate == predicate)
            main_q = main_q.filter(st2.predicate == predicate)
            if is_object_iri:
                main_q = main_q.filter(st1.object != st2.object)
            else:
                main_q = main_q.filter(st1.value != st2.value)
            main_q = main_q.join(sqla_cls, st1.subject == sqla_cls.id)
            for row in main_q:
                result = vdm.ValidationResult(
                    subject=row.subject,
                    predicate=predicate,
                    severity=vdm.SeverityOptions.ERROR,
                    type=vdm.ValidationResultType.MaxCountConstraintComponent.meaning,
                    info=f"Too many vals for {slot_name}",
                )
                yield result
        if slot.range:
            rng = slot.range
            rng_elements = sv.slot_applicable_range_elements(slot)
            # for now we don't handle Union or Any
            if len(rng_elements) < 2:
                logging.info(f"Datatype check: {slot_name} range is {rng_elements}")
                is_object_iri = rng in sv.all_classes()
                if is_object_iri:
                    constr = Statements.object.is_(None)
                else:
                    constr = Statements.value.is_(None)
                main_q = self.session.query(Statements.subject)
                main_q = main_q.join(IriNode, Statements.subject == IriNode.id)
                main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
                main_q = main_q.filter(Statements.predicate == predicate, constr)
                for row in main_q:
                    result = vdm.ValidationResult(
                        subject=row.subject,
                        predicate=predicate,
                        severity=vdm.SeverityOptions.ERROR,
                        type=vdm.ValidationResultType.DatatypeConstraintComponent.meaning,
                        info=f"Incorrect object type for {slot_name} range = {rng} should_be_iri = {is_object_iri}",
                    )
                    yield result
                if rng in sv.all_types():
                    uri = get_range_xsd_type(sv, rng)
                    # uri = rng_type.uri
                    main_q = self.session.query(Statements.subject)
                    main_q = main_q.join(IriNode, Statements.subject == IriNode.id)
                    main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
                    main_q = main_q.filter(
                        Statements.predicate == predicate, Statements.datatype != uri
                    )
                    for row in main_q:
                        result = vdm.ValidationResult(
                            subject=row.subject,
                            predicate=predicate,
                            severity=vdm.SeverityOptions.ERROR,
                            type=vdm.ValidationResultType.DatatypeConstraintComponent.meaning,
                            info=f"Incorrect datatype for {slot_name} expected: {uri} for {rng}",
                        )
                        yield result

    def gap_fill_relationships(
        self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None
    ) -> Iterator[RELATIONSHIP]:
        seed_curies = tuple(seed_curies)
        q = self.session.query(EntailedEdge).filter(EntailedEdge.subject.in_(seed_curies))
        q = q.filter(EntailedEdge.object.in_(seed_curies))
        q = q.filter(EntailedEdge.subject != EntailedEdge.object)
        if predicates:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        for row in q:
            if row.subject != row.object:
                e1 = aliased(EntailedEdge)
                e2 = aliased(EntailedEdge)
                q2 = self.session.query(e1, e2)
                q2 = q2.filter(e1.subject == row.subject)
                q2 = q2.filter(e1.object.in_(seed_curies))
                q2 = q2.filter(e1.object == e2.subject)
                q2 = q2.filter(e2.object == row.object)
                q2 = q2.filter(e1.subject != e1.object)
                q2 = q2.filter(e2.subject != e2.object)
                if predicates:
                    q2 = q2.filter(e1.predicate.in_(tuple(predicates)))
                    q2 = q2.filter(e2.predicate.in_(tuple(predicates)))
                redundant = False
                for e1row, e2row in q2:
                    if predicates is None:
                        redundant = True
                    else:
                        if e1row.predicate in predicates:
                            if e2row.predicate in predicates or e2row.predicate == IS_A:
                                redundant = True
                        elif e2row.predicate in predicates:
                            if e1row.predicate == IS_A:
                                redundant = True
                    if redundant:
                        break
                if not redundant:
                    yield row.subject, row.predicate, row.object

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SemSim
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def get_information_content(
        self, curie: CURIE, background: CURIE = None, predicates: List[PRED_CURIE] = None
    ):
        if self._information_content_cache is None:
            self._information_content_cache = {}
        if predicates is None:
            key = curie, None
        else:
            key = curie, tuple(set(predicates))
        if key not in self._information_content_cache:
            num_nodes = self.session.query(Node.id).count()
            q = self.session.query(EntailedEdge.subject)
            q = q.filter(EntailedEdge.object == curie)
            if predicates:
                q = q.filter(EntailedEdge.predicate.in_(predicates))
            num_descs = q.count()
            ic = -math.log(num_descs / num_nodes) / math.log(2)
            self._information_content_cache[key] = ic
        else:
            logging.debug(f"Using cached value for {key}")
        return self._information_content_cache[key]

    def all_by_all_pairwise_similarity(
        self,
        subjects: Iterable[CURIE],
        objects: Iterable[CURIE],
        predicates: List[PRED_CURIE] = None,
    ) -> Iterator[TermPairwiseSimilarity]:
        def tuples_to_map(relationships: Iterable[RELATIONSHIP]) -> Dict[CURIE, List[CURIE]]:
            rmap = defaultdict(list)
            for r in relationships:
                rmap[r[0]].append(r[2])
            return rmap

        subjects_ancs = tuples_to_map(self.multi_ancestors(list(subjects), predicates=predicates))
        objects_ancs = tuples_to_map(self.multi_ancestors(list(objects), predicates=predicates))
        logging.info(f"SUBJECT ANCS={len(subjects_ancs)}")
        logging.info(f"OBJECT ANCS={len(objects_ancs)}")
        for s, s_ancs in subjects_ancs.items():
            for o, o_ancs in objects_ancs.items():
                logging.info(f"s={s} o={o}")
                yield self.pairwise_similarity(
                    s, o, predicates=predicates, subject_ancestors=s_ancs, object_ancestors=o_ancs
                )

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        # TODO: add an operation for this to KGCL
        for k, v in curie_map.items():
            for cls in [Statements, EntailedEdge]:
                cmd = update(cls).where(cls.subject == k).values(subject=v)
                self.session.execute(cmd)
                cmd = update(cls).where(cls.predicate == k).values(predicate=v)
                self.session.execute(cmd)
                cmd = update(cls).where(cls.object == k).values(object=v)
                self.session.execute(cmd)
        if self.autosave:
            self.save()

    def _set_predicate_value(
        self, subject: CURIE, predicate: PRED_CURIE, value: str, datatype: str
    ):
        stmt = delete(Statements).where(
            and_(Statements.subject == subject, Statements.predicate == predicate)
        )
        self._execute(stmt)
        stmt = insert(Statements).values(
            subject=subject, predicate=predicate, value=value, datatype=datatype
        )
        self._execute(stmt)

    def apply_patch(self, patch: kgcl.Change) -> None:
        if isinstance(patch, kgcl.NodeChange):
            about = patch.about_node
            if isinstance(patch, kgcl.NodeRename):
                self.set_label(patch.about_node, patch.new_value)
            elif isinstance(patch, kgcl.NewSynonym):
                # TODO: synonym type
                self._execute(
                    insert(Statements).values(
                        subject=about, predicate=HAS_EXACT_SYNONYM, value=patch.new_value
                    )
                )
            elif isinstance(patch, kgcl.NodeObsoletion):
                self._set_predicate_value(
                    about, DEPRECATED_PREDICATE, value="true", datatype="xsd:string"
                )
            elif isinstance(patch, kgcl.NodeDeletion):
                self._execute(delete(Statements).where(Statements.subject == about))
            elif isinstance(patch, kgcl.NameBecomesSynonym):
                label = self.label(about)
                self.apply_patch(
                    kgcl.NodeRename(id=f"{patch.id}-1", about_node=about, new_value=patch.new_value)
                )
                self.apply_patch(
                    kgcl.NewSynonym(id=f"{patch.id}-2", about_node=about, new_value=label)
                )
            else:
                raise NotImplementedError
        elif isinstance(patch, kgcl.EdgeChange):
            about = patch.about_edge
            if isinstance(patch, kgcl.EdgeCreation):
                self._execute(
                    insert(Statements).values(
                        subject=patch.subject, predicate=patch.predicate, object=patch.object
                    )
                )
                logging.warning("entailed_edge is now stale")
            elif isinstance(patch, kgcl.EdgeDeletion):
                self._execute(
                    delete(Statements).where(
                        and_(
                            Statements.subject == patch.subject,
                            Statements.predicate == patch.predicate,
                            Statements.object == patch.object,
                        )
                    )
                )
                logging.warning("entailed_edge is now stale")
            elif isinstance(patch, kgcl.NodeMove):
                raise NotImplementedError
                # self._execute(delete(Statements).where(and_(Statements.subject==patch.subject,
                #                                            Statements.predicate==patch.predicate,
                #                                            Statements.object==patch.object)))
                logging.warning("entailed_edge is now stale")
            else:
                raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        else:
            raise NotImplementedError
        if self.autosave:
            self.save()

    def save(
        self,
    ):
        logging.info("Committing and flushing changes")
        self.session.commit()
        self.session.flush()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MetadataInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        m = self.entity_metadata_map(curie)
        q = self.session.query(OwlAxiomAnnotation)
        q = q.filter(OwlAxiomAnnotation.subject == curie)
        axiom_by_id = {}
        visited = {}
        for row in q:
            if row.value is not None:
                v = row.value
            elif row.object is not None:
                v = row.object
            else:
                raise ValueError(f"Unexpected null object/value in {row}")
            axiom_id = row.id
            if axiom_id in axiom_by_id:
                ax = axiom_by_id[axiom_id]
            else:
                ax = om.Axiom(
                    annotatedSource=curie, annotatedProperty=row.predicate, annotatedTarget=v
                )
                axiom_by_id[axiom_id] = ax
            v = row.annotation_object
            if v is None:
                v = row.annotation_value
            ax.annotations.append(om.Annotation(predicate=row.annotation_predicate, object=v))
        for ax in axiom_by_id.values():
            visited[(ax.annotatedSource, ax.annotatedProperty, ax.annotatedTarget)] = True
            yield ax
        for k, vs in m.items():
            if not isinstance(vs, list):
                vs = [vs]
            for v in vs:
                if (curie, k, v) not in visited:
                    if not _is_quoted_url(curie):
                        ax = om.Axiom(annotatedSource=curie, annotatedProperty=k, annotatedTarget=v)
                        yield ax

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: DifferInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def compare_term_in_two_ontologies(
        self, other_ontology: BasicOntologyInterface, curie: CURIE, other_curie: CURIE = None
    ) -> Any:
        if other_curie is None:
            other_curie = curie
        logging.info(f"Comparing {curie} with {other_curie}")
        if isinstance(other_ontology, SqlImplementation):

            def nullify_subject(row):
                return f"{row.predicate} {row.object} {row.value} {row.datatype} {row.language}"

            this_rows = [
                nullify_subject(row)
                for row in self.session.query(Statements).filter(Statements.subject == curie)
            ]
            other_rows = [
                nullify_subject(row)
                for row in other_ontology.session.query(Statements).filter(
                    Statements.subject == other_curie
                )
            ]
            this_only = set(this_rows).difference(set(other_rows))
            other_only = set(other_rows).difference(set(this_rows))
            return this_only, other_only
        else:
            raise NotImplementedError(
                f"other ontology {other_ontology} must implement SqlInterface"
            )
