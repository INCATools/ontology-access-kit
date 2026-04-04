import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, cast

import pyhornedowl
import rdflib
from kgcl_schema.datamodel import kgcl
from pyhornedowl.model import (
    IRI,
    AnnotatedComponent,
    Annotation,
    AnnotationAssertion,
    Component,
    DatatypeLiteral,
    DeclareAnnotationProperty,
    DeclareClass,
    DeclareDataProperty,
    DeclareDatatype,
    DeclareNamedIndividual,
    DeclareObjectProperty,
    LanguageLiteral,
    ObjectSomeValuesFrom,
    SimpleLiteral,
    SubClassOf,
)

from oaklib.datamodels.vocabulary import (
    DEPRECATED_PREDICATE,
    HAS_DEFINITION_CURIE,
    HAS_EXACT_SYNONYM,
    IS_A,
    LABEL_PREDICATE,
)
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG
from oaklib.interfaces.owl_interface import OwlInterface, ReasonerConfiguration
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)
DECLARATION_TYPES = (
    DeclareClass,
    DeclareObjectProperty,
    DeclareAnnotationProperty,
    DeclareDataProperty,
    DeclareNamedIndividual,
    DeclareDatatype,
)
LITERAL_TYPES = (SimpleLiteral, DatatypeLiteral, LanguageLiteral)
XSD_BOOLEAN = "http://www.w3.org/2001/XMLSchema#boolean"


@dataclass
class FunOwlImplementation(OwlInterface, PatcherInterface, SearchInterface):
    """
    An experimental partial implementation of :ref:`OwlInterface`

    This adapter keeps the historical ``funowl`` selector and class name, but now
    uses py-horned-owl as the OWL parser and object model.
    """

    ontology_document: Optional[pyhornedowl.PyIndexedOntology] = None

    def __post_init__(self):
        resource = self.resource
        local_path = None if resource is None else resource.local_path
        if self.ontology_document is None:
            if local_path is None:
                doc = pyhornedowl.PyIndexedOntology()
            else:
                local_path = Path(local_path)
                logger.info("Loading %s into py-horned-owl", local_path)
                doc = pyhornedowl.open_ontology_from_file(str(local_path))
                if local_path.suffix in {".ofn", ".omn"}:
                    self.prefix_map().update(self._extract_prefix_declarations(local_path))
            self.ontology_document = doc
        self.functional_writer = self.ontology_document

    @staticmethod
    def _extract_prefix_declarations(path: Path) -> Mapping[str, str]:
        prefix_map = {}
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"Prefix\(\s*([^=]+?)\s*=\s*<([^>]+)>\s*\)", text):
            prefix = match.group(1).strip()
            if prefix.endswith(":"):
                prefix = prefix[:-1]
            prefix_map[prefix] = match.group(2)
        return prefix_map

    @property
    def _ontology(self) -> pyhornedowl.PyIndexedOntology:
        return self.ontology_document

    def owl_ontology(self) -> pyhornedowl.PyIndexedOntology:
        return self._ontology

    def _sync_prefix_mapping(self, curie: CURIE) -> None:
        if ":" not in curie:
            return
        prefix, _, _ = curie.partition(":")
        if prefix in self.prefix_map():
            try:
                self._ontology.add_prefix_mapping(prefix, self.prefix_map()[prefix])
            except Exception:
                logger.debug("Could not sync prefix mapping for %s", prefix, exc_info=True)

    def entity_iri_to_curie(self, entity: IRI) -> CURIE:
        return cast(CURIE, self.uri_to_curie(str(entity), use_uri_fallback=True))

    def curie_to_entity_iri(self, curie: CURIE) -> IRI:
        self._sync_prefix_mapping(curie)
        return IRI.parse(self.curie_to_uri(curie))

    def curie_to_class(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.clazz(self.curie_to_uri(curie))

    def curie_to_object_property(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.object_property(self.curie_to_uri(curie))

    def curie_to_annotation_property(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.annotation_property(self.curie_to_uri(curie))

    def _coerce_annotation_value(self, value: Any):
        if isinstance(value, LITERAL_TYPES) or isinstance(value, IRI):
            return value
        if isinstance(value, bool):
            return DatatypeLiteral(str(value).lower(), IRI.parse(XSD_BOOLEAN))
        return SimpleLiteral(str(value))

    def _single_valued_assignment(self, curie: CURIE, property: CURIE) -> Optional[str]:
        values = self._ontology.get_annotations(self.curie_to_uri(curie), self.curie_to_uri(property))
        if values:
            if len(values) > 1:
                logger.warning("Multiple values for %s %s = %s", curie, property, values)
            return values[0]
        return None

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        return self._single_valued_assignment(curie, HAS_DEFINITION_CURIE)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        return self._single_valued_assignment(curie, LABEL_PREDICATE)

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        for axiom in self._ontology.get_axioms():
            component = axiom.component
            if isinstance(component, DECLARATION_TYPES):
                iri = self._entity_iri(component.first)
                if iri is None:
                    continue
                yield self.entity_iri_to_curie(iri)

    def axioms(self, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[Component]:
        for axiom in self._ontology.get_axioms():
            yield axiom.component

    def _add_axiom(self, axiom: Component) -> None:
        if isinstance(axiom, AnnotatedComponent):
            self._ontology.add_axiom(axiom.component, set(axiom.ann))
        else:
            self._ontology.add_axiom(axiom)

    def set_axioms(self, axioms: List[Component]) -> None:
        for axiom in list(self._ontology.get_axioms()):
            self._ontology.remove_axiom(axiom.component)
        for axiom in axioms:
            self._add_axiom(axiom)

    def dump(self, path: Optional[str] = None, syntax: Optional[str] = None, **kwargs):
        syntax = syntax or "ofn"
        if syntax == "ofn":
            out = self._ontology.save_to_string("ofn")
        elif syntax in {"ttl", "turtle"}:
            rdfxml = self._ontology.save_to_string("owl")
            g = rdflib.Graph()
            g.parse(data=rdfxml, format="xml")
            out = g.serialize(format="ttl")
        elif syntax in {"owl", "owx"}:
            out = self._ontology.save_to_string(syntax)
        else:
            out = self._ontology.save_to_string(syntax)
        if path is None:
            print(out)
        elif isinstance(path, (str, Path)):
            Path(path).write_text(str(out), encoding="utf-8")
        else:
            path.write(str(out))

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _set_annotation_predicate_value(self, subject: CURIE, property: CURIE, value: Any):
        for axiom in list(self.annotation_assertion_axioms(subject, property)):
                    self._ontology.remove_axiom(axiom)
        self._ontology.add_axiom(
            AnnotationAssertion(
                self.curie_to_entity_iri(subject),
                Annotation(
                    self.curie_to_annotation_property(property),
                    self._coerce_annotation_value(value),
                ),
            )
        )

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Optional[Mapping[PRED_CURIE, Any]] = None,
        configuration: kgcl.Configuration = None,
        strict=False,
    ) -> Optional[kgcl.Change]:
        if isinstance(patch, kgcl.NodeChange):
            about = patch.about_node
            if isinstance(patch, kgcl.NodeRename):
                self._set_annotation_predicate_value(about, LABEL_PREDICATE, patch.new_value)
            elif isinstance(patch, kgcl.NodeTextDefinitionChange):
                self._set_annotation_predicate_value(about, HAS_DEFINITION_CURIE, patch.new_value)
            elif isinstance(patch, kgcl.NewSynonym):
                self._ontology.add_axiom(
                    AnnotationAssertion(
                        self.curie_to_entity_iri(about),
                        Annotation(
                            self.curie_to_annotation_property(HAS_EXACT_SYNONYM),
                            self._coerce_annotation_value(patch.new_value),
                        ),
                    )
                )
            elif isinstance(patch, kgcl.NodeObsoletion):
                self._set_annotation_predicate_value(about, DEPRECATED_PREDICATE, value=True)
            elif isinstance(patch, kgcl.NodeDeletion):
                raise NotImplementedError("Deletions not supported yet")
            elif isinstance(patch, kgcl.NodeCreation):
                self._set_annotation_predicate_value(about, LABEL_PREDICATE, patch.name)
            elif isinstance(patch, kgcl.NameBecomesSynonym):
                label = self.label(about)
                self.apply_patch(
                    kgcl.NodeRename(id=f"{patch.id}-1", about_node=about, new_value=patch.new_value)
                )
                self.apply_patch(
                    kgcl.NewSynonym(id=f"{patch.id}-2", about_node=about, new_value=label)
                )
            else:
                raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        elif isinstance(patch, kgcl.EdgeChange):
            subject = self.curie_to_class(patch.subject)
            object = self.curie_to_class(patch.object)
            if isinstance(patch, kgcl.EdgeCreation):
                if patch.predicate == IS_A or patch.predicate == "is_a":
                    self._ontology.add_axiom(SubClassOf(subject, object))
                else:
                    predicate = self.curie_to_object_property(patch.predicate)
                    self._ontology.add_axiom(
                        SubClassOf(subject, ObjectSomeValuesFrom(predicate, object))
                    )
            else:
                raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        else:
            raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        return patch
