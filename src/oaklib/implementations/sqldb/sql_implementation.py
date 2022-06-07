import logging
import math
import shutil
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Any, Iterable, Optional, Type, Dict, Union, Tuple, Iterator

import requests
import semsql.builder.builder as semsql_builder
import sssom
from appdirs import user_cache_dir
from linkml_runtime import SchemaView
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.metamodelcore import URIorCURIE
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from semsql.sqla.semsql import Statements, Edge, HasSynonymStatement, \
    HasTextDefinitionStatement, ClassNode, IriNode, RdfsLabelStatement, DeprecatedNode, EntailedEdge, \
    ObjectPropertyNode, AnnotationPropertyNode, NamedIndividualNode, HasMappingStatement, OntologyNode, \
    RdfTypeStatement, OwlAxiomAnnotation, Node
from oaklib.interfaces import SubsetterInterface
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, RELATIONSHIP, \
    METADATA_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.types import CURIE, SUBSET_CURIE
from oaklib.datamodels import obograph, ontology_metadata
import oaklib.datamodels.ontology_metadata as om
import oaklib.datamodels.validation_datamodel as vdm
from oaklib.datamodels.vocabulary import SYNONYM_PREDICATES, omd_slots, LABEL_PREDICATE, IN_SUBSET, HAS_DBXREF, \
    ALL_MATCH_PREDICATES, IS_A
from oaklib.utilities.graph.networkx_bridge import transitive_reduction_by_predicate
from sqlalchemy import text, update, delete
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine

# TODO: move to schemaview
from sssom.sssom_datamodel import MatchTypeEnum


# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
def download_file(url: str, local_filename: Path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

def get_range_xsd_type(sv: SchemaView, rng: str) -> Optional[URIorCURIE]:
    t = sv.get_type(rng)
    if t.uri:
        return t.uri
    elif t.typeof:
        return get_range_xsd_type(sv, t.typeof)
    else:
        raise ValueError(f'No xsd type for {rng}')


def regex_to_sql_like(regex: str) -> str:
    """
    convert a regex to a LIKE

    TODO: implement various different DBMS flavors https://stackoverflow.com/questions/20794860/regex-in-sql-to-detect-one-or-more-digit

    :param regex:
    :return:
    """
    for c in r'()[]{}|':
        if c in regex:
            raise NotImplementedError(f'Regex engine not implemented for SQL and cannot parse char {c} in {regex}')
    like = regex.replace('.*', '%')
    like = like.replace('.', '_')
    if like.startswith('^'):
        like = like[1:]
    else:
        like = f'%{like}'
    if like.endswith('$'):
        like = like[0:-1]
    else:
        like = f'{like}%'
    logging.info(f'Translated {regex} => {like}')
    return like


@dataclass
class SqlImplementation(RelationGraphInterface, OboGraphInterface, ValidatorInterface, SearchInterface,
                        SubsetterInterface, MappingProviderInterface, PatcherInterface,
                        SemanticSimilarityInterface, MetadataInterface, ABC):
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
            locator = str(self.resource.slug)
            logging.info(f'Locator: {locator}')
            if locator.startswith('obo:'):
                # easter egg feature, to be documented:
                # The selector 'sqlite:obo:ONTOLOGY' will use a pre-generated
                # sqlite db of an OBO ontology after downloading from S3.
                # Note: this can take some time
                db_name = locator.replace('obo:', '') + '.db'
                cache_dir = Path(user_cache_dir('oaklib'))
                cache_dir.mkdir(parents=True, exist_ok=True)
                logging.info(f'Using cache dir: {cache_dir}')
                db_path = cache_dir / db_name
                if not db_path.exists():
                    url = f'https://s3.amazonaws.com/bbop-sqlite/{db_name}'
                    logging.info(f'Downloading from {url} to {db_path}')
                    download_file(url, db_path)
                else:
                    logging.info(f'Using cached db: {db_path}')
                locator = f'sqlite:///{db_path}'
            if locator.endswith('.owl'):
                # this is currently an "Easter Egg" feature. It allows you to specify a locator
                # such as sqlite:/path/to/my.owl
                # then semsql will be invoked to build a sqlite db from this.
                # the same sqlite db will be reused until the timestamp of the owl file changes.
                # the catch is that EITHER the user must have BOTH rdftab and relation-graph installed, OR
                # they should be running through ODK docker
                locator = locator.replace('.owl', '.db').replace('sqlite:', '')
                logging.info(f'Building {locator} using semsql')
                semsql_builder.make(locator)
                locator = f'sqlite:///{locator}'
            else:
                path = Path(locator.replace('sqlite:', '')).absolute()
                locator = f'sqlite:///{path}'
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

    def all_entity_curies(self) -> Iterable[CURIE]:
        s = text('SELECT id FROM class_node WHERE id NOT LIKE "\_:%" ESCAPE "\\"')
        for row in self.engine.execute(s):
            yield row['id']

    def all_relationships(self) -> Iterable[RELATIONSHIP]:
        for row in self.session.query(Edge):
            yield row.subject, row.predicate, row.object

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

    def get_definition_by_curie(self, curie: CURIE) -> Optional[str]:
        for row in self.session.query(HasTextDefinitionStatement).filter(HasTextDefinitionStatement.subject == curie):
            return row.value

    def metadata_map_by_curie(self, curie: CURIE) -> METADATA_MAP:
        m = {'id': curie}
        # subquery = self.session.query(AnnotationPropertyNode.id)
        subquery = self.session.query(RdfTypeStatement.subject).filter(
            RdfTypeStatement.object == 'owl:AnnotationProperty')
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

    def all_ontology_curies(self) -> Iterable[CURIE]:
        for row in self.session.query(OntologyNode):
            yield row.id

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
        for row in self.session.query(Statements.object, Statements.value).filter(Statements.predicate == IN_SUBSET):
            uri = row.object
            if row.object is None:
                logging.warning(f'Subset may be incorrectly encoded as value for {row.value}')
            else:
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

    def set_label_for_curie(self, curie: CURIE, label: str) -> bool:
        stmt = update(Statements).where(Statements.subject == curie and Statements.predicate == LABEL_PREDICATE).values(
            value=label)
        self.session.execute(
            stmt
        )
        self.session.flush()
        if self.autosave:
            self.save()

    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        preds = []
        preds.append(omd_slots.label.curie)
        search_all = SearchProperty(SearchProperty.ANYTHING) in config.properties
        if search_all or SearchProperty(SearchProperty.ALIAS) in config.properties:
            preds += SYNONYM_PREDICATES
        view = Statements

        def make_query(qcol):
            q = self.session.query(view.subject).filter(view.predicate.in_(tuple(preds)))
            if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
                q = q.filter(qcol.like(f'{search_term}%'))
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.SQL):
                q = q.filter(qcol.like(search_term))
            elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
                if self.is_mysql():
                    q = q.filter(qcol.op('regex')(search_term))
                elif self.is_postgres():
                    q = q.filter(qcol.op('~')(search_term))
                else:
                    q = q.filter(qcol.like(regex_to_sql_like(search_term)))
            elif config.is_partial:
                q = q.filter(qcol.like(f'%{search_term}%'))
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

    def get_simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        m = defaultdict(list)
        for row in self.session.query(HasMappingStatement).filter(HasMappingStatement.subject == curie):
            yield row.predicate, row.value

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False, include_annotations=False) -> obograph.Node:
        meta = obograph.Meta()
        n = obograph.Node(id=curie, meta=meta)
        rows = list(self.session.query(Statements).filter(Statements.subject == curie))
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
                if include_annotations:
                    anns = self._axiom_annotations(curie, pred, row.object, row.value)
                else:
                    anns = []
                if pred == omd_slots.definition.curie:
                    meta.definition = obograph.DefinitionPropertyValue(val=v, xrefs=[ann.object for ann in anns])
        return n

    def _axiom_annotations(self, subject: CURIE, predicate: CURIE, object: CURIE, value: Any) -> List[om.Annotation]:
        q = self.session.query(OwlAxiomAnnotation)
        q = q.filter(OwlAxiomAnnotation.subject == subject)
        q = q.filter(OwlAxiomAnnotation.predicate == predicate)
        if object:
            q = q.filter(OwlAxiomAnnotation.object == object)
        if value:
            q = q.filter(OwlAxiomAnnotation.object == value)
        return [om.Annotation(row.annotation_predicate, row.annotation_object) for row in q]


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
    # Implements: RelationGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def entailed_relationships_between(self, subject: CURIE, object: CURIE) -> Iterable[PRED_CURIE]:
        preds = []
        for row in self.session.query(EntailedEdge.predicate).filter(EntailedEdge.subject == subject).filter(
                EntailedEdge.object == object):
            p = row.predicate
            if p not in preds:
                yield p
            preds.append(p)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def all_sssom_mappings(self) -> Iterable[sssom.Mapping]:
        predicates = tuple(ALL_MATCH_PREDICATES)
        base_query = self.session.query(Statements).filter(Statements.predicate.in_(predicates))
        for row in base_query:
            v = row.value if row.value is not None else row.object
            if URIorCURIE.is_valid(v):
                yield sssom.Mapping(subject_id=row.subject,
                                    object_id=v,
                                    predicate_id=row.predicate,
                                    match_type=MatchTypeEnum.Unspecified)
            else:
                if self.strict:
                    raise ValueError(f'not a CURIE: {V}')

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[sssom.Mapping]:
        predicates = tuple(ALL_MATCH_PREDICATES)
        base_query = self.session.query(Statements).filter(Statements.predicate.in_(predicates))
        for row in base_query.filter(Statements.subject == curie):
            yield sssom.Mapping(subject_id=curie,
                                object_id=row.value if row.value is not None else row.object,
                                predicate_id=row.predicate,
                                match_type=MatchTypeEnum.Unspecified)
        # xrefs are stored as literals
        for row in base_query.filter(Statements.value == curie):
            yield sssom.Mapping(subject_id=row.subject,
                                object_id=curie,
                                predicate_id=row.predicate,
                                match_type=MatchTypeEnum.Unspecified)
        # skos mappings are stored as objects
        for row in base_query.filter(Statements.object == curie):
            yield sssom.Mapping(subject_id=row.subject,
                                object_id=curie,
                                predicate_id=row.predicate,
                                match_type=MatchTypeEnum.Unspecified)

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
        main_q = self.session.query(Statements).filter(Statements.predicate.not_in(preds)).join(IriNode,
                                                                                                Statements.subject == IriNode.id)
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
                    # uri = rng_type.uri
                    main_q = self.session.query(Statements.subject)
                    main_q = main_q.join(IriNode, Statements.subject == IriNode.id)
                    main_q = main_q.join(sqla_cls, Statements.subject == sqla_cls.id)
                    main_q = main_q.filter(Statements.predicate == predicate, Statements.datatype != uri)
                    # print(main_q)
                    for row in main_q:
                        result = vdm.ValidationResult(subject=row.subject,
                                                      predicate=predicate,
                                                      severity=vdm.SeverityOptions.ERROR,
                                                      type=vdm.ValidationResultType.DatatypeConstraintComponent.meaning,
                                                      info=f'Incorrect datatype for {slot_name} expected: {uri} for {rng}'
                                                      )
                        yield result

    def gap_fill_relationships(self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None) -> Iterator[
        RELATIONSHIP]:
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
    def get_information_content(self, curie: CURIE, background: CURIE = None,
                                predicates: List[PRED_CURIE] = None):
        num_nodes = self.session.query(Node.id).count()
        q = self.session.query(EntailedEdge.subject)
        q = q.filter(EntailedEdge.object == curie)
        if predicates:
            q = q.filter(EntailedEdge.predicate.in_(predicates))
        num_descs = q.count()
        return -math.log(num_descs / num_nodes) / math.log(2)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def migrate_curies(self, curie_map: Dict[CURIE, CURIE]) -> None:
        for k, v in curie_map.items():
            for cls in [Statements, EntailedEdge]:
                cmd = update(cls).where(cls.subject == k).values(subject=v)
                r = self.session.execute(cmd)
                cmd = update(cls).where(cls.predicate == k).values(predicate=v)
                r = self.session.execute(cmd)
                cmd = update(cls).where(cls.object == k).values(object=v)
                r = self.session.execute(cmd)
        if self.autosave:
            self.save()

    def save(self):
        logging.info(f'Committing and flushing changes')
        self.session.commit()
        self.session.flush()

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MetadataInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        m = self.metadata_map_by_curie(curie)
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
                raise ValueError(f'Unexpected null object/value in {row}')
            axiom_id = row.id
            if axiom_id in axiom_by_id:
                ax = axiom_by_id[axiom_id]
            else:
                ax = om.Axiom(annotatedSource=curie,
                              annotatedProperty=row.predicate,
                              annotatedTarget=v)
                axiom_by_id[axiom_id] = ax
            v = row.annotation_object
            if v is None:
                v = row.annotation_value
            ax.annotations.append(om.Annotation(predicate=row.annotation_predicate,
                                                object=v))
        for ax in axiom_by_id.values():
            visited[(ax.annotatedSource, ax.annotatedProperty, ax.annotatedTarget)] = True
            yield ax
        for k, vs in m.items():
            if not isinstance(vs, list):
                vs = [vs]
            for v in vs:
                if (curie, k, v) not in visited:
                    ax = om.Axiom(annotatedSource=curie,
                                  annotatedProperty=k,
                                  annotatedTarget=v)
                    yield ax
