import inspect
import itertools
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, List, Optional, Tuple, Type, Union

# TODO: add funowl to dependencies
import funowl
from funowl import (
    IRI,
    AnnotationAssertion,
    AsymmetricObjectProperty,
    Axiom,
    Class,
    ClassExpression,
    DisjointClasses,
    EquivalentClasses,
    IrreflexiveObjectProperty,
    Literal,
    ObjectAllValuesFrom,
    ObjectIntersectionOf,
    ObjectPropertyChain,
    ObjectPropertyExpression,
    ObjectSomeValuesFrom,
    ObjectUnionOf,
    Ontology,
    ReflexiveObjectProperty,
    SubClassOf,
    SubObjectPropertyOf,
    SymmetricObjectProperty,
    TransitiveObjectProperty,
)
from funowl.writers import FunctionalWriter

from oaklib.datamodels.vocabulary import (
    OWL_ASYMMETRIC_PROPERTY,
    OWL_IRREFLEXIVE_PROPERTY,
    OWL_REFLEXIVE_PROPERTY,
    OWL_SYMMETRIC_PROPERTY,
    OWL_TRANSITIVE_PROPERTY,
)
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class OwlProfile(Enum):
    EL = "EL"
    DL = "DL"
    OWL_FULL = "OWL-Full"
    RL = "RL"
    QC = "QL"


@dataclass
class ReasonerConfiguration:
    reasoner: str = None
    reasoner_version: str = None
    implements_profiles: List[OwlProfile] = None


@dataclass
class AxiomFilter:
    type: Optional[Type[Axiom]] = None
    about: Optional[Union[CURIE, List[CURIE]]] = None
    references: Optional[CURIE] = None
    func: Callable = None
    ontologies: Optional[List[CURIE]] = None

    def set_type(self, axiom_type: Union[str, Type[Axiom]]) -> None:
        if isinstance(axiom_type, str):
            matches = [obj for n, obj in inspect.getmembers(funowl) if n == axiom_type]
            if len(matches) == 1:
                self.type = matches[0]
            elif len(matches) == 0:
                raise ValueError(f"No such axiom type: {axiom_type}")
            else:
                raise ValueError(f"Multiple matches {axiom_type} => {matches}")
        else:
            self.type = axiom_type


@dataclass
class OwlInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as an OWL ontology using an OWL datamodel

    We leverage the :ref:`_funowl_datamodel`

    Currently there is one implementation, the :ref:`funowl_implementation`

    In future the SqlDatabase implementation will implement this, as well as:

    - owlery
    - robot/owlapi via py4j
    """

    functional_writer: FunctionalWriter = None

    def owl_ontology(self) -> Ontology:
        raise NotImplementedError

    def axioms(self, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[Axiom]:
        raise NotImplementedError

    def filter_axioms(
        self, conditions: AxiomFilter, reasoner: Optional[ReasonerConfiguration] = None
    ) -> Iterable[Axiom]:
        if reasoner is not None:
            raise ValueError
        for axiom in self.axioms(reasoner=reasoner):
            if self._axiom_matches(axiom, conditions):
                yield axiom

    def set_axioms(self, axioms: List[Axiom]) -> None:
        raise NotImplementedError

    def subclass_axioms(
        self,
        subclass: CURIE = None,
        superclass: CURIE = None,
        reasoner: Optional[ReasonerConfiguration] = None,
    ) -> Iterable[SubClassOf]:
        """
        Gets all SubClassOf axioms matching criterion

        :param subclass: if specified, constrains to axioms where this is the subclass
        :param superclass: if specified, constrains to axioms where this is the superclass
        :param reasoner:
        :return:
        """
        for axiom in self.axioms(reasoner=reasoner):
            if isinstance(axiom, SubClassOf):
                if subclass is not None:
                    m = False
                    if isinstance(axiom.subClassExpression, IRI):
                        if self._entity_matches(axiom.subClassExpression, subclass):
                            m = True
                    if not m:
                        continue
                if superclass is not None:
                    m = False
                    if isinstance(axiom.superClassExpression, IRI):
                        if self._entity_matches(axiom.superClassExpression, subclass):
                            m = True
                    if not m:
                        continue
                yield axiom

    def equivalence_axioms(
        self,
        about: CURIE = None,
        references: CURIE = None,
        reasoner: Optional[ReasonerConfiguration] = None,
    ) -> Iterable[EquivalentClasses]:
        """
        All EquivalentClasses axioms matching criteria

        :param about:
        :param references:
        :param reasoner:
        :return:
        """
        return self.filter_axioms(
            reasoner=reasoner,
            conditions=AxiomFilter(type=EquivalentClasses, about=about, references=references),
        )

    def annotation_assertion_axioms(
        self, subject: CURIE = None, property: CURIE = None, value: Any = None
    ) -> Iterable[AnnotationAssertion]:
        """
        Filters all matching annotation axioms

        :param subject:
        :param property:
        :param value:
        :return:
        """
        for axiom in self.axioms():
            # TODO: use indexing to speed this up
            if isinstance(axiom, AnnotationAssertion):
                if subject is not None:
                    if not self._entity_matches(axiom.subject, subject):
                        continue
                if property is not None:
                    if not self._entity_matches(axiom.property, property):
                        continue
                if value is not None:
                    if not self._entity_matches(axiom.value, value):
                        continue
                yield axiom

    def disjoint_pairs(self, subjects: Iterable[CURIE] = None) -> Iterable[Tuple[CURIE, CURIE]]:
        """
        Gets all disjoint pairs of entities

        :param subjects:
        :return:
        """
        for axiom in self.axioms():
            if isinstance(axiom, DisjointClasses):
                if isinstance(axiom.classExpressions, list):
                    for c1, c2 in itertools.combinations(axiom.classExpressions, 2):
                        if not subjects or (c1 in subjects or c2 in subjects):
                            yield c1, c2

    def is_disjoint(self, subject: CURIE, object: CURIE) -> bool:
        """
        Checks if two entities are declared or entailed disjoint.

        :param subject:
        :param object:
        :return:
        """
        raise NotImplementedError

    def owl_classes(self) -> Iterable[Class]:
        raise NotImplementedError

    def owl_individuals(self) -> Iterable[Class]:
        raise NotImplementedError

    def is_satisfiable(self, curie: CURIE) -> bool:
        """
        Note: this may move to the validation interface

        :param curie:
        :return:
        """
        raise NotImplementedError

    def reasoner_configurations(self) -> List[ReasonerConfiguration]:
        """
        Lists all available reasoner configurations

        :return:
        """
        return []

    def entity_iri_to_curie(self, entity: IRI) -> CURIE:
        raise NotImplementedError

    def _entity_matches(self, entity: Any, curie: Union[CURIE, Any]):
        if isinstance(entity, IRI):
            return curie == self.entity_iri_to_curie(entity)
        elif isinstance(entity, Literal):
            return curie == entity
        else:
            return False

    def _axiom_matches(self, axiom: Axiom, conditions: AxiomFilter) -> bool:
        if conditions.type is not None:
            if not isinstance(axiom, conditions.type):
                return False
        if conditions.about is not None:
            if isinstance(conditions.about, list):
                if not any(e for e in self._axiom_is_about_curies(axiom) if e in conditions.about):
                    return False
            else:
                if not any(e for e in self._axiom_is_about_curies(axiom) if e == conditions.about):
                    return False
        if conditions.references is not None:
            if not any(
                e for e in self._axiom_references_curies(axiom) if e == conditions.references
            ):
                return False
        return True

    def axiom_is_about(self, axiom: Axiom) -> Iterable[IRI]:
        """
        Gives an axiom, yield all of the entity IRIs which this axiom is *about*

        For example, a SubClassOf axiom is about the IRI in the subClassOf expression

        We use a consistent definition of *about* as in the OWLAPI

        :param axiom:
        :return: entity IRI iterator
        """
        if isinstance(axiom, SubClassOf):
            for e in self._expression_is_about(axiom.subClassExpression):
                yield e
        elif isinstance(axiom, EquivalentClasses):
            for x in axiom.classExpressions:
                for e in self._expression_is_about(x):
                    yield e
        else:
            # TODO: all axiom types
            pass

    def axiom_references(self, axiom: Axiom) -> Iterable[IRI]:
        """
        Gives an axiom, yield all of the entity IRIs which this axiom references
        (i.e. entities in the signature)

        :param axiom:
        :return: entity IRI iterator
        """
        if isinstance(axiom, SubClassOf):
            for e in self._expression_references(axiom.subClassExpression):
                yield e
            for e in self._expression_references(axiom.superClassExpression):
                yield e
        elif isinstance(axiom, EquivalentClasses) or isinstance(axiom, DisjointClasses):
            for x in axiom.classExpressions:
                for e in self._expression_references(x):
                    yield e
        else:
            # TODO: all axiom types
            pass

    def _expression_references(
        self, ex: Union[ClassExpression, ObjectPropertyExpression]
    ) -> Iterable[IRI]:
        # TODO: generalize signature
        if isinstance(ex, IRI):
            # https://github.com/hsolbrig/funowl/issues/19
            try:
                if ex.full_uri(self.functional_writer.g):
                    yield ex
            except AttributeError:
                pass
        elif isinstance(ex, ObjectIntersectionOf) or isinstance(ex, ObjectUnionOf):
            for x in ex.classExpressions:
                for r in self._expression_references(x):
                    yield r
        elif isinstance(ex, ObjectSomeValuesFrom) or isinstance(ex, ObjectAllValuesFrom):
            for x in self._expression_references(ex.objectPropertyExpression):
                yield x
            for x in self._expression_references(ex.classExpression):
                yield x

    def _expression_is_about(self, ex: ClassExpression) -> Iterable[IRI]:
        # TODO: generalize signature
        if isinstance(ex, IRI):
            yield ex

    def _axiom_references_curies(self, axiom: Axiom) -> Iterable[CURIE]:
        for e in self.axiom_references(axiom):
            yield self.entity_iri_to_curie(e)

    def _axiom_is_about_curies(self, axiom: Axiom) -> List[CURIE]:
        return [self.entity_iri_to_curie(e) for e in self.axiom_is_about(axiom)]

    def property_characteristics(self, property: CURIE) -> Iterable[CURIE]:
        """
        Gets all property characteristics for a given property

        :param property:
        :return:
        """
        pc_tuples = [
            (TransitiveObjectProperty, OWL_TRANSITIVE_PROPERTY),
            (SymmetricObjectProperty, OWL_SYMMETRIC_PROPERTY),
            (AsymmetricObjectProperty, OWL_ASYMMETRIC_PROPERTY),
            (ReflexiveObjectProperty, OWL_REFLEXIVE_PROPERTY),
            (IrreflexiveObjectProperty, OWL_IRREFLEXIVE_PROPERTY),
        ]
        pcs = tuple([pc[0] for pc in pc_tuples])
        for axiom in self.axioms():
            if isinstance(axiom, pcs):
                for pc, pc_curie in pc_tuples:
                    if isinstance(axiom, pc):
                        if isinstance(axiom.objectPropertyExpression, IRI):
                            if self.entity_iri_to_curie(axiom.objectPropertyExpression) == property:
                                yield pc_curie

    def transitive_object_properties(self) -> Iterable[CURIE]:
        """
        Gets all transitive object properties

        :return:
        """
        for axiom in self.axioms():
            if isinstance(axiom, TransitiveObjectProperty):
                if isinstance(axiom.objectPropertyExpression, IRI):
                    yield self.entity_iri_to_curie(axiom.objectPropertyExpression)

    def simple_subproperty_of_chains(self) -> Iterable[Tuple[CURIE, List[CURIE]]]:
        """
        Gets all property chains of where the super property is a chain of IRIs

        :return:
        """
        for axiom in self.axioms():
            if isinstance(axiom, SubObjectPropertyOf):
                if isinstance(axiom.superObjectPropertyExpression, ObjectPropertyChain):
                    if isinstance(axiom.subObjectPropertyExpression, IRI):
                        chain_exprs = axiom.superObjectPropertyExpression.objectPropertyExpressions
                        if all(isinstance(p, IRI) for p in chain_exprs):
                            chain = [self.entity_iri_to_curie(p) for p in chain_exprs]
                            yield self.entity_iri_to_curie(axiom.subObjectPropertyExpression), chain
