import logging
from abc import ABC
from typing import Any, Dict, Iterable, List, Optional, Union

from linkml_runtime.dumpers import json_dumper

from oaklib.datamodels.ontology_metadata import DefinitionConstraintComponent
from oaklib.datamodels.synonymizer_datamodel import RuleSet
from oaklib.datamodels.validation_datamodel import (
    MappingValidationResult,
    RepairConfiguration,
    RepairOperation,
    SeverityOptions,
    ValidationConfiguration,
    ValidationResult,
)
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE
from oaklib.interfaces import MappingProviderInterface, OboGraphInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.lexical.synonymizer import apply_synonymizer
from oaklib.utilities.publication_utils.pubmed_wrapper import PubmedWrapper


class ValidatorInterface(BasicOntologyInterface, ABC):
    """
    Multi-faceted ontology validator.

    This interface defines a number of different validation processes

    The overall goal is to support the following

    - validating against OntologyMetadata schema
    - lexical checks
    - wrapping reasoning
    - structural graph checks

    Specific implementations may choose to implement efficient methods for this.
    For example, a SQL implementation can quickly determine all terms
    missing definitions with a query over an indexed table.

    Currently the main implementation for this is the SqlDatabase implementation,
    this implements a generic property check using the OntologyMetadata datamodel

    See:

     - `OntologyMetadata <https://incatools.github.io/ontology-access-kit/datamodels/ontology-metadata/>`_
    """

    def term_curies_without_definitions(self) -> Iterable[CURIE]:
        """
        Yields all entities that do not have a definition.

        :return:
        """
        # Implementations are advise to implement more efficient interfaces for their back-end
        for curie in self.entities():
            if self.definition(curie) is None:
                yield curie

    def validate(self, configuration: ValidationConfiguration = None) -> Iterable[ValidationResult]:
        """
        Validate entire ontology or wrapped ontologies.

        Validation results might be implementation specific

        - reasoners will yield logical problems
        - shape checkers or schema checkers like SHACL or LinkML will return closed-world structural violations
        - specialized implementations may yield lexical or other kinds of problems
        :return:
        """
        raise NotImplementedError

    def validate_mappings(
        self,
        entities: Iterable[CURIE] = None,
        adapters: Dict[str, BasicOntologyInterface] = None,
        configuration: ValidationConfiguration = None,
    ) -> Iterable[MappingValidationResult]:
        """
        Validate mappings for a set of entities.

        Different adapters may implement different aspects of mapping validation.

        It includes:

        - checking cardinality of mappings (e.g. skos:exactMatch should be 1:1)
        - looking up mapped entities to check they are not obsolete
        - using AI to validate the content of mappings

        :param entities: entities to validate mappings for (None=all)
        :param adapters: adapter mapping to look up external entities
        :param configuration: validation configuration
        :return:
        """
        from oaklib.utilities.mapping.mapping_validation import validate_mappings

        if not isinstance(self, MappingProviderInterface):
            raise ValueError(f"Cannot validate mappings on {self}")
        mappings = list(self.sssom_mappings(entities))
        for errors, m in validate_mappings(mappings, adapters=adapters):
            for error in errors:
                result = MappingValidationResult(
                    subject_id=m.subject_id,
                    object_id=m.object_id,
                    predicate_id=m.predicate_id,
                    info=error,
                )
                yield result

    def validate_synonyms(
        self,
        entities: Iterable[CURIE] = None,
        adapters: Dict[str, BasicOntologyInterface] = None,
        configuration: ValidationConfiguration = None,
        synonymizer_rules: Optional[RuleSet] = None,
    ) -> Iterable[ValidationResult]:
        """
        Validate synonyms for a set of entities.

        Different adapters may implement different aspects of synonym validation.

        It includes:

        - checking for duplicates
        - looking up mapped entities to check they are not obsolete
        - ensuring that a referenced synonym is still supported
        - using AI to validate the content of mappings

        :param entities: entities to validate mappings for (None=all)
        :param adapters: adapter mapping to look up external entities
        :param configuration: validation configuration
        :return:
        """

        if not isinstance(self, OboGraphInterface):
            raise ValueError(f"Cannot validate synonyms on {self}")
        nodes = [self.node(n, include_metadata=True) for n in entities]
        for node in nodes:
            if node is None:
                continue
            syns = node.meta.synonyms
            for syn in syns:
                if syn.xrefs:
                    for xref in syn.xrefs:
                        from oaklib.utilities.mapping.mapping_validation import (
                            lookup_mapping_adapter,
                        )

                        ext_adapter = lookup_mapping_adapter(xref, adapters)
                        if ext_adapter is None:
                            continue
                        if not isinstance(ext_adapter, OboGraphInterface):
                            raise ValueError(f"Cannot validate synonyms on {ext_adapter}")
                        ext_node = ext_adapter.node(xref, include_metadata=True)
                        ext_syns = ext_node.meta.synonyms
                        # normalize to lower case for comparison
                        # TODO: allow configurability of case rules
                        synonym_forms = {syn.val}
                        if synonymizer_rules:
                            for _, syn_form, _ in apply_synonymizer(
                                syn.val, synonymizer_rules.rules
                            ):
                                synonym_forms.add(syn_form.lower())
                        ext_syn_vals = [x.val.lower() for x in ext_syns]
                        if not synonym_forms.intersection(ext_syn_vals):
                            yield ValidationResult(
                                subject=node.id,
                                predicate=syn.pred,
                                object=xref,
                                object_str=syn.val,
                                severity=SeverityOptions(SeverityOptions.ERROR),
                                type="oio:SynonymNotFound",
                                info=f"synonym not found in {xref}",
                            )

    def validate_definitions(
        self,
        entities: Iterable[CURIE] = None,
        adapters: Dict[str, BasicOntologyInterface] = None,
        configuration: ValidationConfiguration = None,
        skip_text_annotation=False,
        **kwargs,
    ) -> Iterable[ValidationResult]:
        """
        Validate text definitions for a set of entities.

        Different adapters may implement different aspects of mapping validation.

        It includes:

        - testing definitions are present
        - validating the text definition against the SRS rubric
        - using AI to align the definition against any references

        :param entities:
        :param configuration:
        :param kwargs:
        :return:
        """
        from oaklib.utilities.validation.definition_ontology_rule import DefinitionOntologyRule

        definition_rule = DefinitionOntologyRule(skip_text_annotation=skip_text_annotation)
        entities = list(entities) if entities else self.entities(filter_obsoletes=True)

        def _contract(url):
            return url.replace("https://w3id.org/oak/ontology-metadata/DCC.", "oaklib.om:DCC#")

        for r in definition_rule.evaluate(self, entities=entities):
            r.type = _contract(r.type)
            yield r
        if configuration and configuration.lookup_references:
            for entity_it in chunk(entities):
                for entity, defn, metadata in self.definitions(
                    entity_it,
                    include_metadata=True,
                ):
                    if not metadata:
                        continue
                    for _k, vs in metadata.items():
                        refs = self.lookup_references(vs, adapters=adapters)
                        for ref, obj in refs.items():
                            if obj is not None and not obj:
                                yield ValidationResult(
                                    subject=entity,
                                    predicate=HAS_DEFINITION_CURIE,
                                    object=ref,
                                    object_str=defn,
                                    severity=SeverityOptions(SeverityOptions.ERROR),
                                    type=_contract(
                                        DefinitionConstraintComponent.ReferenceNotFound.meaning
                                    ),
                                    info=f"publication not found: {ref}",
                                )
                                continue
                            if isinstance(obj, dict) and obj.get("retracted", False):
                                yield ValidationResult(
                                    subject=entity,
                                    predicate=HAS_DEFINITION_CURIE,
                                    object=ref,
                                    severity=SeverityOptions(SeverityOptions.ERROR),
                                    type=_contract(
                                        DefinitionConstraintComponent.ReferenceIsRetracted.meaning
                                    ),
                                    info=f"publication is retracted: {obj.get('title', obj)}",
                                )

    def validate_relationships(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Optional[Iterable[CURIE]] = None,
        objects: Optional[Iterable[CURIE]] = None,
        configuration: ValidationConfiguration = None,
    ):
        raise NotImplementedError

    def repair(
        self, configuration: RepairConfiguration = None, dry_run=False
    ) -> Iterable[RepairOperation]:
        """
        Finds problems and fixes them.

        :param configuration:
        :param dry_run:
        :return:
        """
        raise NotImplementedError

    def check_external_references(self):
        raise NotImplementedError

    def is_coherent(self) -> bool:
        """
        True if the ontology is logically coherent, as determined by deductive reasoning
        (e.g. an OWL reasoner)

        :return: true if coherent
        """
        raise NotImplementedError

    def unsatisfiable_classes(self, exclude_nothing=True) -> Iterable[CURIE]:
        """
        Yields all classes that are unsatisfiable, as determined by deductive reasoning
        (e.g. an OWL reasoner)

        :param exclude_nothing: if True (default) do not include the tautological owl:Nothing
        :return: class curie iterator
        """
        raise NotImplementedError

    def lookup_references(
        self, references: List[CURIE], adapters: Dict[str, BasicOntologyInterface] = None, **kwargs
    ) -> Dict[CURIE, Union[bool, Dict[str, Any]]]:
        """
        Lookup references in external ontologies.

        :param references: list of CURIEs to look up
        :param adapters: adapter mapping to look up external entities
        :param kwargs: additional arguments
        :return: mapping between CURIEs and pub objects
        """
        if None in references:
            logging.warning(f"Null in references: {references}")
            references = [r for r in references if r]
        pubmed_wrapper = PubmedWrapper()
        pub_prefixes = ["PMID", "DOI", "PMC", "PMCID"]
        publication_ids = [
            x for x in references if any(x.upper().startswith(y) for y in pub_prefixes)
        ]
        objs = pubmed_wrapper.objects_by_ids(publication_ids)
        # seed with Nones
        obj_map = {pmid: False for pmid in references if pmid.startswith("PMID")}
        for x in objs:
            obj_map[x["id"]] = x
        for x in references:
            # split out the prefix
            prefix, _ = x.split(":", 1)
            if prefix.upper() in pub_prefixes:
                continue
            if adapters is not None:
                if prefix in adapters:
                    adapter = adapters[prefix]
                    if not isinstance(adapter, OboGraphInterface):
                        continue
                    obj = adapter.node(x)
                    obj_map[x] = json_dumper.to_dict(obj)
        return obj_map
