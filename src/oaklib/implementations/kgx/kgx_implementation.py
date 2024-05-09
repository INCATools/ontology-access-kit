import logging
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Type

import rdflib
import sqlalchemy.orm
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.introspection import package_schemaview
from sqlalchemy import Column, MetaData, String, Table, create_engine
from sqlalchemy.orm import declarative_base, registry

import oaklib.datamodels.ontology_metadata as om
from oaklib.datamodels import obograph, ontology_metadata
from oaklib.datamodels.association import Association
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    ALL_MATCH_PREDICATES,
    BIOLINK_CATEGORY,
    DISJOINT_WITH,
    HAS_DBXREF,
    HAS_EXACT_SYNONYM,
    HAS_SYNONYM_TYPE,
    IN_CATEGORY_PREDS,
    IN_SUBSET,
    IS_A,
    LABEL_PREDICATE,
    RDF_TYPE,
    SYNONYM_PREDICATES,
    TERM_REPLACED_BY,
    omd_slots,
)
from oaklib.implementations.sqldb import SEARCH_CONFIG
from oaklib.implementations.sqldb.sql_implementation import (
    _python_value,
    regex_to_sql_like,
)
from oaklib.interfaces import SubsetterInterface, TextAnnotatorInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    METADATA_MAP,
    PRED_CURIE,
    PREFIX_MAP,
    RELATIONSHIP,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.interfaces.differ_interface import DifferInterface
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CATEGORY_CURIE, CURIE, SUBSET_CURIE
from oaklib.utilities.identifier_utils import synonym_type_code_from_curie
from oaklib.utilities.iterator_utils import chunk

__all__ = [
    "KGXImplementation",
]


class SqlSchemaError(Exception):
    """Raised when there are issues with the version of the SQL DDL uses"""

    pass


class ViewNotFoundError(SqlSchemaError):
    """Raised when a SQL view is not found"""

    pass


OBJECT_CLOSURE_VIEW = """
CREATE VIEW edges_with_object_closure AS
WITH RECURSIVE split(subject, predicate, object, entailed_object, ancestors_str) AS (
      SELECT e.subject, e.predicate, e.object, null, object_closure || '|' FROM denormalized_edges AS e
      UNION ALL
      SELECT
      subject, predicate, object,
      substr(ancestors_str, 0, instr(ancestors_str, '|')),
      substr(ancestors_str, instr(ancestors_str, '|')+1)
      FROM split WHERE ancestors_str!=''
  ) SELECT subject, predicate, object, entailed_object FROM split;
"""

SUBJECT_CLOSURE_VIEW = """
CREATE VIEW edges_with_subject_closure AS
WITH RECURSIVE split(subject, predicate, object, entailed_subject, ancestors_str) AS (
      SELECT e.subject, e.predicate, e.object, null, subject_closure || '|' FROM denormalized_edges AS e
      UNION ALL
      SELECT
      subject, predicate, object,
      substr(ancestors_str, 0, instr(ancestors_str, '|')),
      substr(ancestors_str, instr(ancestors_str, '|')+1)
      FROM split WHERE ancestors_str!=''
  ) SELECT subject, predicate, object, entailed_subject FROM split;
"""


Base = declarative_base()


class Node:
    """A node in a KGX graph."""

    __tablename__ = "nodes"
    id = Column(String, primary_key=True)
    name = Column(String)


class NodeProperty(Base):
    """A node-property pair."""

    __tablename__ = "node_properties"
    __derived_from__ = "nodes"
    subject = Column(String, primary_key=True)
    predicate = Column(String, primary_key=True)
    value = Column(String, primary_key=True, nullable=True)
    object = Column(String, primary_key=True, nullable=True)


class Edge:
    """An edge in a KGX graph."""

    __tablename__ = "edges"
    id = Column(String, primary_key=True)
    subject = Column(String)
    predicate = Column(String)
    object = Column(String)


class DenormalizedEdge:
    """A denormalized edge in a KGX graph."""

    __tablename__ = "denormalized_edges"
    subject_closure = Column(String)
    object_closure = Column(String)
    subject_label = Column(String)
    object_label = Column(String)


class EdgeWithObjectClosure(Base):
    """Entailed edge including entailed object."""

    __tablename__ = "edges_with_object_closure"
    subject = Column(String, primary_key=True)
    predicate = Column(String, primary_key=True)
    object = Column(String, primary_key=True)
    entailed_object = Column(String, primary_key=True)


class EdgeWithSubjectClosure(Base):
    """Entailed edge including entailed subject."""

    __tablename__ = "edges_with_subject_closure"
    subject = Column(String, primary_key=True)
    predicate = Column(String, primary_key=True)
    object = Column(String, primary_key=True)
    entailed_subject = Column(String, primary_key=True)


class EdgeProperty(Base):
    """An edge-property pair."""

    __tablename__ = "edge_properties"
    __derived_from__ = "edges"
    subject = Column(String, primary_key=True)
    predicate = Column(String, primary_key=True)
    value = Column(String, primary_key=True, nullable=True)
    object = Column(String, primary_key=True, nullable=True)


@dataclass
class KGXImplementation(
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
    # AssociationProviderInterface,
    ClassEnrichmentCalculationInterface,
    TextAnnotatorInterface,
    SummaryStatisticsInterface,
    OwlInterface,
    DumperInterface,
):
    """
    A :class:`OntologyInterface` implementation that wraps a KGX Relational Database.

    This could be a local file (accessed via SQL Lite) or a local/remote server (e.g PostgreSQL).

    >>> from oaklib import get_adapter
    >>> oi = get_adapter('../semantic-sql/db/monarch-kg.db')

    The schema is assumed to follow the `semantic-sql <https://github.com/incatools/semantic-sql>`_ schema.

    This uses SQLAlchemy ORM Models:

    - :class:`NodeProperty`
    - :class:`Edge`

    See Also
    --------
    - `Tutorial <https://incatools.github.io/ontology-access-kit/intro/tutorial07.html>`_
    - `SQL Implementation <https://incatools.github.io/ontology-access-kit/implementations/sqldb.html>`_

    """

    # TODO: use SQLA types
    engine: Any = None
    _session: Any = None
    _connection: Any = None
    _ontology_metadata_model: SchemaView = None
    _prefix_map: PREFIX_MAP = None
    _information_content_cache: Dict[Tuple, float] = None

    max_items_for_in_clause: int = field(default_factory=lambda: 1000)

    def __post_init__(self):
        if self.engine is None:
            locator = str(self.resource.slug)
            logging.info(f"Locator: {locator}")
            if locator.startswith("kghub:"):
                raise NotImplementedError("kghub not yet implemented")
            else:
                path = Path(locator.replace("kgx:", "")).absolute()
                if not path.exists():
                    raise FileNotFoundError(f"File does not exist: {path}")
                locator = f"sqlite:///{path}"
            logging.info(f"Locator, post-processed: {locator}")
            self.engine = create_engine(locator)
            self._add_orm_mappings()

    def _add_orm_mappings(self):
        # https://stackoverflow.com/questions/2574105/sqlalchemy-dynamic-mapping/2575016#2575016
        engine = self.engine
        metadata = MetaData()
        colmap = self._introspect()
        mapper_registry = registry()
        # metadata.reflect(bind=engine)
        for (cls, table_name), cols in colmap.items():
            t = Table(
                table_name,
                metadata,
                Column("id", String, primary_key=True),
                *(Column(col, String) for col in cols),
            )
            mapper_registry.map_imperatively(cls, t)
        self._session = sqlalchemy.orm.create_session(bind=engine, autocommit=False, autoflush=True)
        self._add_missing_tables()

    def _introspect(self) -> Dict[Tuple[Type, str], List[str]]:
        engine = self.engine
        metadata = MetaData()
        logging.info(f"Reflecting using {engine}")
        metadata.reflect(bind=engine)
        colmap = defaultdict(list)
        for cls in [Node, Edge, DenormalizedEdge]:
            tables = [table for table in metadata.sorted_tables if table.name == cls.__tablename__]
            if len(tables) != 1:
                raise RuntimeError(f"Expected 1 table for {cls}, got {len(tables)}")
            table = tables[0]
            k = (cls, table.name)
            logging.info(f"Importing {table.name}")
            for column in table.columns:
                if column.name == "id":
                    continue
                colmap[k].append(column.name)
        return colmap

    def _add_missing_tables(self):
        engine = self.engine
        metadata = MetaData()
        metadata.reflect(bind=engine)
        for cls in [NodeProperty]:
            tables = [table for table in metadata.sorted_tables if table.name == cls.__tablename__]
            if len(tables) == 0:
                logging.info(f"Creating table {cls.__tablename__}")
                cls.__table__.create(bind=engine)
                self._populate_table(cls)

    def _populate_table(self, cls: Type[Base]):
        session = self.session
        engine = self.engine
        metadata = MetaData(bind=engine)
        metadata.reflect(bind=engine)
        [source_table] = [
            table for table in metadata.sorted_tables if table.name == cls.__derived_from__
        ]
        pmap = {
            "name": (LABEL_PREDICATE, False),
            "category": (BIOLINK_CATEGORY, True),
            "synonym": (HAS_EXACT_SYNONYM, True),
        }
        for col in source_table.columns:
            col_name = col.name
            (pred, multivalued) = pmap.get(col_name, (col_name, False))
            # TODO: properly handle multivalued
            sql = (
                f"INSERT INTO node_properties (subject, predicate, value) "
                f"SELECT id, '{pred}', {col_name} FROM {source_table.name}"
            )
            session.execute(sql)
        session.commit()

    @property
    def session(self):
        if self._session is None:
            raise AssertionError("Session not initialized")
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

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        q = self.session.query(Node.id)
        logging.debug(f"Entities Query: {q}")
        for row in q:
            print(row)
            yield row[0]

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        raise NotImplementedError("TODO: add to monarch dump")

    def all_relationships(self) -> Iterable[RELATIONSHIP]:
        for row in self.session.query(Edge):
            yield row.subject, row.predicate, row.object

    def label(self, curie: CURIE, **kwargs) -> Optional[str]:
        q = self.session.query(Node.name).filter(Node.id == curie)
        logging.debug(f"Label query: {q} // {curie}")
        for row in q:
            return row[0]

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, **kwargs
    ) -> Iterable[Tuple[CURIE, str]]:
        for curie_it in chunk(curies, self.max_items_for_in_clause):
            curr_curies = list(curie_it)
            has_label = set()
            q = self.session.query(Node.id, Node.name).filter(Node.id.in_(tuple(curr_curies)))
            logging.debug(f"Labels query: {q}")
            for row in q:
                yield row.id, row.name
                if allow_none:
                    has_label.add(row.id)
            if allow_none:
                for curie in curr_curies:
                    if curie not in has_label:
                        yield curie, None

    def curies_by_label(self, label: str) -> List[CURIE]:
        q = self.session.query(Node.id)
        q = q.filter(Node.name == label)
        return list(set([row[0] for row in q]))

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [self.label(curie)]
        for row in self.session.query(NodeProperty).filter(
            NodeProperty.subject == curie, NodeProperty.predicate == HAS_EXACT_SYNONYM
        ):
            m[row.predicate].append(row.value)
        return m

    def entity_metadata_map(self, curie: CURIE, include_all_triples=False) -> METADATA_MAP:
        m = defaultdict(list)
        m["id"] = [curie]
        q = self.session.query(NodeProperty)
        for row in q.filter(NodeProperty.subject == curie):
            if row.value is not None:
                v = _python_value(row.value, row.datatype)
            elif row.object is not None:
                v = row.object
            else:
                v = None
            m[row.predicate].append(v)
        self.add_missing_property_values(curie, m)
        return dict(m)

    def ontologies(self) -> Iterable[CURIE]:
        yield "TODO"

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
        return self.entity_metadata_map(ontology, include_all_triples=True)

    def _get_subset_curie(self, curie: str) -> str:
        if "#" in curie:
            return curie.split("#")[-1]
        else:
            return curie

    def _subset_uri_to_curie_map(self) -> Dict[str, CURIE]:
        m = {}
        for row in self.session.query(NodeProperty.object).filter(
            NodeProperty.predicate == IN_SUBSET
        ):
            uri = row.object
            m[uri] = self._get_subset_curie(row.object)
        return m

    def _subset_curie_to_uri_map(self) -> Dict[CURIE, str]:
        m = {}
        for row in self.session.query(NodeProperty.object, NodeProperty.value).filter(
            NodeProperty.predicate == IN_SUBSET
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
        if subset not in sm:
            raise ValueError(f"Subset {subset} not found in {sm}")
        for row in self.session.query(NodeProperty.subject).filter(
            NodeProperty.predicate == IN_SUBSET, NodeProperty.object == sm[subset]
        ):
            yield self._get_subset_curie(row.subject)

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        for row in self.session.query(NodeProperty).filter(
            NodeProperty.predicate == IN_SUBSET, NodeProperty.subject.in_(list(curies))
        ):
            yield row.subject, self._get_subset_curie(row.object)

    def terms_categories(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CATEGORY_CURIE]]:
        for row in self.session.query(NodeProperty).filter(
            NodeProperty.predicate.in_(IN_CATEGORY_PREDS), NodeProperty.subject.in_(list(curies))
        ):
            yield row.subject, self._get_subset_curie(row.object)

    def _execute(self, stmt):
        self.session.execute(stmt)
        self.session.flush()
        if self.autosave:
            self.save()

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        if config is None:
            config = SEARCH_CONFIG
        if config.force_case_insensitive:
            # in sqlite, LIKEs are case insensitive
            if config.syntax:
                if config.syntax != SearchTermSyntax(SearchTermSyntax.SQL):
                    raise ValueError(
                        f"Cannot force case insensitive search with syntax {config.syntax}"
                    )
            else:
                config.syntax = SearchTermSyntax(SearchTermSyntax.SQL)
        preds = []
        preds.append(omd_slots.label.curie)
        search_all = SearchProperty(SearchProperty.ANYTHING) in config.properties
        if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
            preds += SYNONYM_PREDICATES
        if search_all or SearchProperty(SearchProperty.MAPPED_IDENTIFIER) in config.properties:
            preds += ALL_MATCH_PREDICATES
        view = NodeProperty

        def make_query(qcol, preds, scol=view.subject):
            q = self.session.query(scol).filter(view.predicate.in_(tuple(preds)))
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

        q = make_query(view.value, preds)
        for row in q.distinct():
            if row.subject.startswith("_:"):
                continue
            yield str(row.subject)
        if search_all or SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
            q = make_query(view.subject, preds)
            for row in q.distinct():
                yield str(row.subject)
        if search_all or SearchProperty(SearchProperty.REPLACEMENT_IDENTIFIER) in config.properties:
            q = make_query(view.subject, [TERM_REPLACED_BY], view)
            for row in q.distinct():
                yield str(row.object) if row.object else str(row.value)

    def relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        include_dangling: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        if subjects is not None:
            # materialize iterators
            subjects = list(subjects)
        if subjects is not None and len(subjects) > self.max_items_for_in_clause:
            logging.info(
                f"Chunking {len(subjects)} subjects into subqueries to avoid large IN clauses"
            )
            for subjects_it in chunk(subjects, self.max_items_for_in_clause):
                for r in self.relationships(
                    list(subjects_it),
                    predicates,
                    objects,
                    include_tbox=include_tbox,
                    include_abox=include_abox,
                    include_entailed=include_entailed,
                    include_dangling=include_dangling,
                ):
                    yield r
            return
        if objects is not None and len(objects) > self.max_items_for_in_clause:
            logging.info(
                f"Chunking {len(objects)} objects into subqueries to avoid large IN clauses"
            )
            for objects_it in chunk(objects, self.max_items_for_in_clause):
                for r in self.relationships(
                    subjects,
                    predicates,
                    list(objects_it),
                    include_tbox=include_tbox,
                    include_abox=include_abox,
                    include_entailed=include_entailed,
                    include_dangling=include_dangling,
                ):
                    yield r
            return
        if include_entailed:
            tbl = DenormalizedEdge
        else:
            tbl = Edge
        q = self.session.query(tbl)
        if subjects:
            q = q.filter(tbl.subject.in_(tuple(subjects)))
        if predicates:
            q = q.filter(tbl.predicate.in_(tuple(predicates)))
        if objects:
            q = q.filter(tbl.object.in_(tuple(objects)))
        if not include_dangling:
            subq = self.session.query(Edge.subject)
            q = q.filter(tbl.object.in_(subq))
        logging.info(f"Tbox query: {q}")
        for row in q:
            yield row.subject, row.predicate, row.object

    def outgoing_relationships(
        self, curie: CURIE, predicates: Optional[List[PRED_CURIE]] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for _, p, o in self.relationships([curie], predicates):
            yield p, o

    def incoming_relationships(
        self, curie: CURIE, predicates: Optional[List[PRED_CURIE]] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        for s, p, _ in self.relationships(predicates=predicates, objects=[curie]):
            yield p, s

    def clone(self, resource: Any) -> None:
        if self.resource.scheme == "sqlite":
            if resource.scheme == "sqlite":
                shutil.copyfile(self.resource.slug, resource.slug)
                new_oi = type(self)(resource)
                return new_oi
        raise NotImplementedError("Can only clone sqlite to sqlite")

    def as_rdflib_graph(self) -> rdflib.Graph:
        g = rdflib.Graph()
        bnodes = {}

        uri_re = re.compile(r"^<(.*)>$")

        def tr(n: str, v: str = None, datatype: str = None):
            if n:
                uri_match = uri_re.match(n)
                if n.startswith("_"):
                    if n not in bnodes:
                        bnodes[n] = rdflib.BNode()
                    return bnodes[n]
                elif uri_match:
                    return rdflib.URIRef(uri_match.group(1))
                else:
                    return rdflib.URIRef(self.curie_to_uri(n))
            else:
                lit = rdflib.Literal(v, datatype=datatype)
                return lit

        for row in self.session.query(NodeProperty):
            s = tr(row.subject)
            p = tr(row.predicate)
            o = tr(row.object, row.value, row.datatype)
            logging.debug(f"Triple {s} {p} {o}")
            g.add((s, p, o))
        return g

    def dump(self, path: str = None, syntax: str = None, **kwargs):
        """
        Implements :ref:`dump`.

        Supported syntaxes:

        - ttl
        - json

        :param path:
        :param syntax:
        :param kwargs:
        :return:
        """
        if syntax is None:
            syntax = "ttl"
        if syntax == "ttl":
            g = self.as_rdflib_graph()
            logging.info(f"Dumping to {path}")
            g.serialize(path, format=syntax)
        elif syntax == "json":
            g = self.as_obograph(expand_curies=True)
            gd = obograph.GraphDocument(graphs=[g])
            json_dumper.dump(gd, path)
        elif syntax == "sqlite":
            raise NotImplementedError
        else:
            super().dump(path, syntax)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: AssocationProviderInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def associations(self, *args, **kwargs) -> Iterator[Association]:
        q = self._associations_query(*args, **kwargs)
        for row in q:
            yield Association(row.subject, row.predicate, row.object)

    def _associations_query(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        query: sqlalchemy.orm.Query = None,
    ) -> Any:
        tc = DenormalizedEdge
        if query:
            q = query
        else:
            if object_closure_predicates and objects:
                tc = EdgeWithObjectClosure
            if subject_closure_predicates and subjects:
                if tc == EdgeWithObjectClosure:
                    raise ValueError("Can't do both subject and object closure")
                tc = EdgeWithSubjectClosure
            q = self.session.query(tc)
        if property_filter:
            raise NotImplementedError
        if subjects:
            if subject_closure_predicates:
                q = q.filter(tc.entailed_subject.in_(tuple(subjects)))
            else:
                q = q.filter(tc.subject.in_(tuple(subjects)))
        if predicates:
            if predicate_closure_predicates:
                raise NotImplementedError
            else:
                q = q.filter(tc.predicate.in_(tuple(predicates)))
        if objects:
            if object_closure_predicates:
                q = q.filter(tc.entailed_object.in_(tuple(objects)))
            else:
                q = q.filter(tc.object.in_(tuple(objects)))
        logging.info(f"Association query: {q}")
        return q

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> obograph.Node:
        meta = obograph.Meta()
        uri = self.curie_to_uri(curie) if expand_curies else curie
        n = obograph.Node(id=uri, meta=meta)
        q = self.session.query(NodeProperty).filter(NodeProperty.subject == curie)
        builtin_preds = [RDF_TYPE, IS_A, DISJOINT_WITH]
        q = q.filter(NodeProperty.predicate.not_in(builtin_preds))
        rows = list(q)

        def _anns_to_xrefs_and_meta(parent_pv: obograph.PropertyValue, anns: List[om.Annotation]):
            parent_pv.xrefs = [ann.object for ann in anns if ann.predicate == HAS_DBXREF]
            if isinstance(parent_pv, obograph.SynonymPropertyValue):
                synonym_types = [ann.object for ann in anns if ann.predicate == HAS_SYNONYM_TYPE]
                if len(synonym_types) > 0:
                    parent_pv.synonymType = synonym_type_code_from_curie(synonym_types[0])
                    if len(synonym_types) > 1:
                        logging.warning(
                            f"Ignoring multiple synonym types: {synonym_types} for {curie}"
                        )
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
                elif pred in SYNONYM_PREDICATES:
                    # TODO: handle in a separate util
                    if pred.startswith("oio:"):
                        pred = pred.replace("IAO:", "IAO_")
                        scope_pred = pred.replace("oio:", "")
                    else:
                        scope_pred = "hasExactSynonym"
                    pv = obograph.SynonymPropertyValue(pred=scope_pred, val=v)
                    _anns_to_xrefs_and_meta(pv, anns)
                    meta.synonyms.append(pv)
                elif pred == HAS_DBXREF:
                    pv = obograph.XrefPropertyValue(val=v)
                    _anns_to_xrefs_and_meta(pv, anns)
                    meta.xrefs.append(pv)
                elif pred == IN_SUBSET:
                    meta.subsets.append(v)
                else:
                    pv = obograph.BasicPropertyValue(pred=pred, val=v)
                    _anns_to_xrefs_and_meta(pv, anns)
                    meta.basicPropertyValues.append(pv)
        return n

    def nodes(self, expand_curies=False) -> Iterator[Node]:
        """
        Yields all nodes in all graphs

        :param expand_curies:
        :return:
        """
        for e in self.entities():
            if not e.startswith("<"):
                n = self.node(e, include_metadata=True, expand_curies=expand_curies)
                if n.lbl:
                    yield n
