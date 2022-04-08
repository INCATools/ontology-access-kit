from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Any, Iterable, Optional, Type, Dict, Union, Tuple

from oaklib.implementations.sqldb.model import Statements, Edge, HasSynonymStatement, \
    HasTextDefinitionStatement, ClassNode, IriNode, RdfsLabelStatement, DeprecatedNode, EntailedEdge
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface, SearchConfiguration
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, SUBSET_CURIE
from oaklib.datamodels import obograph
from oaklib.datamodels.vocabulary import SYNONYM_PREDICATES, omd_slots, LABEL_PREDICATE, IN_SUBSET
from sqlalchemy import select, text, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@dataclass
class SqlImplementation(RelationGraphInterface, OboGraphInterface, ValidatorInterface, SearchInterface, ABC):
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

    def __post_init__(self):
        if self.engine is None:
            self.engine = create_engine(self.resource.slug)  ## TODO


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


    def all_entity_curies(self) -> Iterable[CURIE]:
        s = text('SELECT id FROM class_node WHERE id NOT LIKE "_:%"')
        for row in self.engine.execute(s):
            yield row['id']


    def get_label_by_curie(self, curie: CURIE) -> Optional[str]:
        s = text('SELECT value FROM rdfs_label_statement WHERE subject = :curie')
        for row in self.engine.execute(s, curie=curie):
            return row['value']

    def get_labels_for_curies(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, str]]:
        for row in self.session.query(RdfsLabelStatement).filter(RdfsLabelStatement.subject.in_(tuple(list(curies)))):
            yield row.subject, row.value

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [self.get_label_by_curie(curie)]
        for row in self.session.query(HasSynonymStatement).filter(HasSynonymStatement.subject == curie):
            m[row.predicate].append(row.value)
        return m

    def _get_subset_curie(self, curie: str) -> str:
        if '#' in curie:
            return curie.split('#')[-1]
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
        for row in self.session.query(Statements.object).filter(Statements.predicate == IN_SUBSET):
            uri = row.object
            m[self._get_subset_curie(row.object)] = uri
        return m

    def all_subset_curies(self) -> Iterable[SUBSET_CURIE]:
        for s in self._subset_curie_to_uri_map().keys():
            yield s

    def curies_by_subset(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        sm = self._subset_curie_to_uri_map()
        for row in self.session.query(Statements.subject).filter(Statements.predicate == IN_SUBSET,
                                                                Statements.object == sm[subset]):
            yield self._get_subset_curie(row.subject)


    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        search_term = f'%{search_term}%'
        preds = []
        if config.include_label:
            preds.append(omd_slots.label.curie)
        if config.include_aliases:
            preds += SYNONYM_PREDICATES
        view = Statements
        q = self.session.query(view.subject).filter(view.predicate.in_(tuple(preds))).filter(view.value.like(search_term))
        for row in q.distinct():
            yield str(row.subject)

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for row in self.session.query(Edge).filter(Edge.subject == curie):
            rmap[row.predicate].append(row.object)
        return rmap

    def get_incoming_relationships_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for row in self.session.query(Edge).filter(Edge.object == curie):
            rmap[row.predicate].append(row.subject)
        return rmap

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE) -> obograph.Node:
        meta = obograph.Meta()
        n = obograph.Node(id=curie, meta=meta)
        for row in self.session.query(Statements).filter(Statements.subject == curie):
            if row.value is not None:
                v = row.value
            elif row.object is not None:
                v = row.object
            else:
                continue
            pred = row.predicate
            if pred == omd_slots.label.curie:
                n.label = v
            else:
                if pred == omd_slots.definition.curie:
                    meta.definition = obograph.DefinitionPropertyValue(val=v)
        return n

    def ancestors(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.subject.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.subject == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        for row in q:
            yield row.object

    def descendants(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.object.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.object == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        for row in q:
            yield row.subject

    ## QC
    def _missing_value(self, predicate_table: Type, type_table: Type = ClassNode) -> Iterable[CURIE]:
        pred_subq = self.session.query(predicate_table.subject)
        obs_subq = self.session.query(DeprecatedNode.id)
        main_q = self.session.query(type_table).join(IriNode, type_table.id == IriNode.id)
        for row in main_q.filter(type_table.id.not_in(pred_subq)).filter(type_table.id.not_in(obs_subq)):
            yield row.id

    def term_curies_without_definitions(self) -> Iterable[CURIE]:
        return self._missing_value(HasTextDefinitionStatement)

    def term_curies_without_labels(self) -> Iterable[CURIE]:
        return self._missing_value(RdfsLabelStatement)




