from collections import defaultdict
from dataclasses import dataclass
from typing import List, Any, Iterable, Optional

from obolib.implementations.sqldb.model import Statements, Edge, HasOioSynonymStatement, HasSynonymStatement
from obolib.implementations.sqldb.sqldb import SqlDatabaseProvider
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    SearchConfiguration
from obolib.interfaces.obograph_interface import OboGraphInterface
from obolib.interfaces.relation_graph_interface import RelationGraphInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE
from obolib.vocabulary import obograph
from obolib.vocabulary.vocabulary import SYNONYM_PREDICATES, omd_slots, LABEL_PREDICATE
from sqlalchemy import select, text
from sqlalchemy.orm import sessionmaker


@dataclass
class SqlImplementation(RelationGraphInterface, OboGraphInterface):
    """
    A :class:`OntologyInterface` implementation that wraps a SQL Relational Database

    This could be a local file (accessed via SQL Lite) or a local/remote server (e.g PostgreSQL)

    The schema is assumed to follow the `semantic-sql <https://github.com/cmungall/semantic-sql>`_ schema

    This uses SQLAlchemy ORM Models:

    - :class:`Statements`
    - :class:`Edge`
    """
    engine: Any
    _session: Any = None
    _connection: Any = None

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

    @classmethod
    def create(cls, resource: OntologyResource = None) -> "SqlImplementation":
        engine = SqlDatabaseProvider.create_engine(resource)
        return SqlImplementation(engine)

    def all_entity_curies(self) -> Iterable[CURIE]:
        s = text('SELECT id FROM class_node WHERE id NOT LIKE "_:%"')
        for row in self.engine.execute(s):
            yield row['id']


    def get_label_by_curie(self, curie: CURIE) -> Optional[str]:
        s = text('SELECT value FROM rdfs_label_statement WHERE subject = :curie')
        for row in self.engine.execute(s, curie=curie):
            return row['value']

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [self.get_label_by_curie(curie)]
        for row in self.session.query(HasSynonymStatement).filter(HasSynonymStatement.subject == curie):
            m[row.predicate].append(row.value)
        return m

    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        search_term = f'%{search_term}%'
        print(search_term)
        preds = []
        if config.include_label:
            preds.append(omd_slots.label.curie)
        if config.include_aliases:
            preds += SYNONYM_PREDICATES
        print(f'PREDS = {preds}')
        view = Statements
        q = self.session.query(view.subject).filter(view.predicate.in_(tuple(preds))).filter(view.value.like(search_term))
        for row in q.distinct():
            yield str(row.subject)

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        rmap = defaultdict(list)
        for row in self.session.query(Edge).filter(Edge.subject == curie):
            rmap[row.predicate].append(row.object)
        return rmap

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




