import logging
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Any, Iterable, Optional, Type, Dict, Union, Tuple, Iterator

from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.metamodelcore import URIorCURIE
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.implementations.sqldb.model import Statements, Edge, HasSynonymStatement, \
    HasTextDefinitionStatement, ClassNode, IriNode, RdfsLabelStatement, DeprecatedNode, EntailedEdge, \
    ObjectPropertyNode, AnnotationPropertyNode, NamedIndividualNode, HasMappingStatement
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, RELATIONSHIP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, SUBSET_CURIE
from oaklib.datamodels import obograph, ontology_metadata
import oaklib.datamodels.validation_datamodel as vdm
from oaklib.datamodels.vocabulary import SYNONYM_PREDICATES, omd_slots, LABEL_PREDICATE, IN_SUBSET
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine


# TODO: move to schemaview
def get_range_xsd_type(sv: SchemaView, rng: str) -> Optional[URIorCURIE]:
    t = sv.get_type(rng)
    if t.uri:
        return t.uri
    elif t.typeof:
        return get_range_xsd_type(sv, t.typeof)
    else:
        raise ValueError(f'No xsd type for {rng}')



@dataclass
class SqlImplementation(RelationGraphInterface, OboGraphInterface, ValidatorInterface, SearchInterface,
                        SubsetterInterface, MappingProviderInterface, ABC):
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

    @property
    def ontology_metadata_model(self):
        if self._ontology_metadata_model is None:
            self._ontology_metadata_model = package_schemaview(ontology_metadata.__name__)
        return self._ontology_metadata_model

    def all_entity_curies(self) -> Iterable[CURIE]:
        s = text('SELECT id FROM class_node WHERE id NOT LIKE "\_:%" ESCAPE "\\"')
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
        preds = []
        preds.append(omd_slots.label.curie)
        if SearchProperty(SearchProperty.ALIAS) in config.properties:
            preds += SYNONYM_PREDICATES
        view = Statements
        q = self.session.query(view.subject).filter(view.predicate.in_(tuple(preds)))
        if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
            q = q.filter(view.value.like(f'{search_term}%'))
        elif config.syntax == SearchTermSyntax(SearchTermSyntax.SQL):
            q = q.filter(view.value.like(search_term))
        elif config.is_partial:
            q = q.filter(view.value.like(f'%{search_term}%'))
        else:
            q = q.filter(view.value == search_term)
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

    def get_simple_mappings_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        m = defaultdict(list)
        for row in self.session.query(HasMappingStatement).filter(HasMappingStatement.subject == curie):
            m[row.predicate].append(row.value)
        return m

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
                n.lbl = v
            else:
                if pred == omd_slots.definition.curie:
                    meta.definition = obograph.DefinitionPropertyValue(val=v)
        return n

    def ancestors(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[
        CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.subject.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.subject == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        logging.debug(f'Ancestors query: {q}')
        for row in q:
            yield row.object

    def descendants(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[
        CURIE]:
        q = self.session.query(EntailedEdge)
        if isinstance(start_curies, list):
            q = q.filter(EntailedEdge.object.in_(tuple(start_curies)))
        else:
            q = q.filter(EntailedEdge.object == start_curies)
        if predicates is not None:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        for row in q:
            yield row.subject

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: ValidatorInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def validate(self, configuration: vdm.ValidationConfiguration = None) -> Iterable[vdm.ValidationResult]:
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

    def _check_for_unknown_slots(self) -> Iterable[vdm.ValidationResult]:
        sv = self.ontology_metadata_model
        preds = [sv.get_uri(s, expand=False) for s in sv.all_slots().values()]
        logging.info(f'Known preds: {len(preds)} -- checking for other uses')
        main_q = self.session.query(Statements).filter(Statements.predicate.not_in(preds)).join(IriNode, Statements.subject == IriNode.id)
        try:
            for row in main_q:
                result = vdm.ValidationResult(subject=row.subject,
                                              predicate=row.predicate,
                                              severity=vdm.SeverityOptions.ERROR,
                                              type=vdm.ValidationResultType.ClosedConstraintComponent.meaning,
                                              info=f'Unknown pred ({row.predicate}) = {row.object} {row.value}'
                                              )
                yield result
        except ValueError as e:
            logging.error(f'EXCEPTION: {e}')
            pass

    def _check_slot(self, slot_name: str, class_name: str = 'Class') -> Iterable[vdm.ValidationResult]:
        """
        Validates all data with respect to a specific slot

        :param slot_name:
        :param class_name:
        :return:
        """
        sv = self.ontology_metadata_model
        class_cls = sv.get_class(class_name)
        # for efficiency we map directly to table/view names rather
        # than querying over rdf:type; this allows for optimization via view materialization
        if class_name == 'Class':
            sqla_cls = ClassNode
        elif class_name == 'ObjectProperty':
            sqla_cls = ObjectPropertyNode
        elif class_name == 'AnnotationProperty':
            sqla_cls = AnnotationPropertyNode
        elif class_name == 'NamedIndividual':
            sqla_cls = NamedIndividualNode
        else:
            raise NotImplementedError(f'cannot handle {class_name}')
        slot = sv.induced_slot(slot_name, class_name)
        if slot.designates_type:
            logging.info(f'Ignoring type designator: {slot_name}')
            return
        logging.info(f'Validating: {slot_name}')
        predicate = sv.get_uri(slot, expand=False)
        is_used = self.session.query(Statements.predicate).filter(Statements.predicate == predicate).first() is not None
        pred_subq = self.session.query(Statements.subject).filter(Statements.predicate == predicate)
        obs_subq = self.session.query(DeprecatedNode.id)
        if (slot.required or slot.recommended) and not slot.identifier:
            # MinCardinality == 1
            if slot.required:
                severity = vdm.SeverityOptions.ERROR
            else:
                severity = vdm.SeverityOptions.WARNING
            logging.info(f'MinCard check: Leaving off: {slot_name} is {severity.text}')
            # exclude blank nodes
            main_q = self.session.query(sqla_cls).join(IriNode, sqla_cls.id == IriNode.id)
            main_q = main_q.filter(sqla_cls.id.not_in(pred_subq))
            main_q = main_q.filter(sqla_cls.id.not_in(obs_subq))
            for row in main_q:
                result = vdm.ValidationResult(subject=row.id,
                                              predicate=predicate,
                                              severity=severity,
                                              type=vdm.ValidationResultType.MinCountConstraintComponent.meaning,
                                              info=f'Missing slot ({slot_name}) for {row.id}'
                                              )
                yield result
        if not is_used:
            return
        if slot.deprecated:
            main_q = self.session.query(Statements.subject).filter(Statements.predicate == predicate)
            main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
            for row in main_q:
                result = vdm.ValidationResult(subject=row.subject,
                                              predicate=predicate,
                                              severity=vdm.SeverityOptions.WARNING,
                                              type=vdm.ValidationResultType.DeprecatedPropertyComponent.meaning,
                                              info=f'Deprecated slot ({slot_name}) for {row.subject}'
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
                result = vdm.ValidationResult(subject=row.subject,
                                              predicate=predicate,
                                              severity=vdm.SeverityOptions.ERROR,
                                              type=vdm.ValidationResultType.MaxCountConstraintComponent.meaning,
                                              info=f'Too many vals for {slot_name}'
                                              )
                yield result
        if slot.range:
            rng = slot.range
            rng_elements = sv.slot_applicable_range_elements(slot)
            # for now we don't handle Union or Any
            if len(rng_elements) < 2:
                logging.info(f'Datatype check: {slot_name} range is {rng_elements}')
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
                    result = vdm.ValidationResult(subject=row.subject,
                                                  predicate=predicate,
                                                  severity=vdm.SeverityOptions.ERROR,
                                                  type=vdm.ValidationResultType.DatatypeConstraintComponent.meaning,
                                                  info=f'Incorrect object type for {slot_name} range = {rng} should_be_iri = {is_object_iri}'
                                                  )
                    yield result
                if rng in sv.all_types():
                    uri = get_range_xsd_type(sv, rng)
                    #uri = rng_type.uri
                    main_q = self.session.query(Statements.subject)
                    main_q = main_q.join(IriNode, Statements.subject == IriNode.id)
                    main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
                    main_q = main_q.filter(Statements.predicate == predicate, Statements.datatype != uri)
                    #print(main_q)
                    for row in main_q:
                        result = vdm.ValidationResult(subject=row.subject,
                                                      predicate=predicate,
                                                      severity=vdm.SeverityOptions.ERROR,
                                                      type=vdm.ValidationResultType.DatatypeConstraintComponent.meaning,
                                                      info=f'Incorrect datatype for {slot_name} expected: {uri} for {rng}'
                                                      )
                        yield result

    def gap_fill_relationships(self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None) -> Iterator[RELATIONSHIP]:
        seed_curies = tuple(seed_curies)
        q = self.session.query(EntailedEdge).filter(EntailedEdge.subject.in_(seed_curies))
        q = q.filter(EntailedEdge.object.in_(seed_curies))
        if predicates:
            q = q.filter(EntailedEdge.predicate.in_(tuple(predicates)))
        rels = []
        for row in q:
            if row.subject != row.object:
                rels.append((row.subject, row.predicate, row.object))
        for rel in transitive_reduction_by_predicate(rels):
            yield rel
