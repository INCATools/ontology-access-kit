"""An in-memory sqlite index for simple associations."""

import logging
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, List, Tuple

from semsql.sqla.semsql import TermAssociation
from sqlalchemy import Column, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from oaklib.datamodels.association import Association
from oaklib.types import CURIE, PRED_CURIE

COLS = ["id", "subject", "predicate", "object", "evidence_type", "publication", "source"]


class DenormalizedAssociation:
    """A denormalized association. (for future extension)"""

    __tablename__ = "denormalized_term_association"
    subject_id = Column(String)
    subject_label = Column(String)
    object_id = Column(String)
    object_label = Column(String)
    predicate_id = Column(String)
    predicate_label = Column(String)
    subject_closure_json = Column(String)
    object_closure_json = Column(String)
    subject_property_values_json = Column(String)
    object_property_values_json = Column(String)
    association_property_values_json = Column(String)


@dataclass
class AssociationIndex:
    """
    A sqlite in-memory index for a collection of associations.
    """

    _connection: sqlite3.Connection = None
    _session: Session = None
    _engine: Engine = None
    _associations_by_spo: Dict[Tuple[CURIE, PRED_CURIE, CURIE], List[Association]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def create(self):
        connection_string: str = "sqlite:///:memory:"
        engine = create_engine(connection_string)
        con = engine.raw_connection()
        # con = sqlite3.connect(":memory:")
        con.execute(f"create table term_association({','.join(COLS)})")
        self._connection = con
        session_cls = sessionmaker(engine)
        self._session = session_cls()
        self._engine = engine

    def populate(self, associations: Iterable[Association]):
        associations = list(associations)
        tups = [
            (a.subject, a.predicate, a.object, a.primary_knowledge_source) for a in associations
        ]
        logging.info(f"Bulk loading {len(tups)} associations")
        self._connection.executemany(
            "insert into term_association(subject, predicate, object, source) values (?,?,?,?)",
            tups,
        )
        for a in associations:
            tup = (a.subject, a.predicate, a.object)
            self._associations_by_spo[tup].append(a)

    def lookup(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
    ) -> Iterator[Association]:
        session = self._session
        q = session.query(TermAssociation)
        union_cutoff = 200
        if property_filter:
            raise NotImplementedError
        if subjects:
            subjects = list(subjects)
            if len(subjects) < union_cutoff:
                q = q.filter(TermAssociation.subject.in_(tuple(subjects)))
        if predicates:
            q = q.filter(TermAssociation.predicate.in_(tuple(predicates)))
        if objects:
            q = q.filter(TermAssociation.object.in_(tuple(objects)))
        logging.info(f"Association index lookup: {q}")
        for row in q:
            tup = (row.subject, row.predicate, row.object)
            if subjects and len(subjects) < union_cutoff:
                if row.subject not in subjects:
                    continue
            yield from self._associations_by_spo[tup]
