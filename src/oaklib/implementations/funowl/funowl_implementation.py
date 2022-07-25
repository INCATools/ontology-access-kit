import logging
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional

import rdflib
from funowl import IRI, AnnotationAssertion, Axiom, Declaration, OntologyDocument
from funowl.converters.functional_converter import to_python
from funowl.writers.FunctionalWriter import FunctionalWriter
from kgcl_schema.datamodel import kgcl

from oaklib.datamodels.vocabulary import (
    DEFAULT_PREFIX_MAP,
    DEPRECATED_PREDICATE,
    LABEL_PREDICATE,
    OBO_PURL,
)
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP
from oaklib.interfaces.owl_interface import OwlInterface, ReasonerConfiguration
from oaklib.types import CURIE, URI


@dataclass
class FunOwlImplementation(OwlInterface):
    """
    An experimental partial implementation of :ref:`OwlInterface`

    Wraps FunOWL

    `<https://github.com/hsolbrig/funowl>`_

    """

    ontology_document: OntologyDocument = None

    def __post_init__(self):
        if self.ontology_document is None:
            resource = self.resource
            if resource is None:
                doc = OntologyDocument()
            else:
                # print(resource)
                doc = to_python(str(resource.local_path))
            self.ontology_document = doc
        if self.functional_writer is None:
            self.functional_writer = FunctionalWriter()
            for prefix in doc.prefixDeclarations:
                self.functional_writer.bind(prefix.prefixName, prefix.fullIRI)

    @property
    def _ontology(self):
        return self.ontology_document.ontology

    def prefix_map(self) -> PREFIX_MAP:
        # TODO
        return DEFAULT_PREFIX_MAP

    def entity_iri_to_curie(self, entity: IRI) -> CURIE:
        uri = entity.to_rdf(self.functional_writer.g)
        return self.uri_to_curie(str(uri))

    def curie_to_entity_iri(self, curie: CURIE) -> IRI:
        return IRI(self.curie_to_uri(curie))

    def uri_to_curie(self, uri: URI, strict=True) -> Optional[CURIE]:
        # TODO: do not hardcode OBO
        pm = self.prefix_map()
        for k, v in pm.items():
            if uri.startswith(v):
                return uri.replace(v, f"{k}:")
        if uri.startswith(OBO_PURL):
            uri = uri.replace(OBO_PURL, "")
            return uri.replace("_", ":")
        return uri

    def label(self, curie: CURIE) -> str:
        labels = [
            a.value for a in self.annotation_assertion_axioms(curie, property=LABEL_PREDICATE)
        ]
        if labels:
            if len(labels) > 1:
                logging.warning(f"Multiple labels for {curie} = {labels}")
            label = labels[0]
            rdf_v = label.to_rdf(self.functional_writer.g)
            if isinstance(rdf_v, rdflib.Literal):
                return rdf_v.value
            else:
                raise ValueError(f"Label must be literal, not {label}")

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        for ax in self._ontology.axioms:
            if isinstance(ax, Declaration):
                uri = ax.v.full_uri(self.functional_writer.g)
                yield self.uri_to_curie(str(uri))

    def axioms(self, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[Axiom]:
        ont = self._ontology
        for axiom in ont.axioms:
            yield axiom

    def set_axioms(self, axioms: List[Axiom]) -> None:
        self._ontology.axioms = axioms

    def dump(self, path: str = None, syntax: str = None):
        if syntax is None or syntax == "ofn":
            out = self.ontology_document.to_functional(self.functional_writer)
        elif syntax == "ttl":
            out = self.ontology_document.to_rdf(self.functional_writer.g)
        else:
            out = str(self.ontology_document)
        if path is None:
            print(out)
        elif isinstance(path, str):
            with open(path, "wb") as file:
                file.write(str(out))
        else:
            path.write(str(out))

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _set_annotation_predicate_value(self, subject: CURIE, property: CURIE, value: Any):
        for axiom in self.annotation_assertion_axioms(subject, property):
            self._ontology.axioms.remove(axiom)
        self._ontology.axioms.append(
            AnnotationAssertion(
                subject=self.curie_to_entity_iri(subject),
                property=self.curie_to_entity_iri(property),
                value=value,
            )
        )

    def apply_patch(self, patch: kgcl.Change) -> None:
        if isinstance(patch, kgcl.NodeChange):
            about = patch.about_node
            if isinstance(patch, kgcl.NodeRename):
                self._set_annotation_predicate_value(about, LABEL_PREDICATE, patch.new_value)
            elif isinstance(patch, kgcl.NewSynonym):
                raise NotImplementedError
            elif isinstance(patch, kgcl.NodeObsoletion):
                self._set_annotation_predicate_value(about, DEPRECATED_PREDICATE, value=True)
            elif isinstance(patch, kgcl.NodeDeletion):
                raise NotImplementedError
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
            raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        else:
            raise NotImplementedError
