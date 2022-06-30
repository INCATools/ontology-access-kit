# Ontology Metadata Ontology Schema

Schema for ontology metadata

URI: http://purl.obolibrary.org/obo/omo/schema
Name: Ontology-Metadata

## Classes

| Class | Description |
| --- | --- |
| [Annotation](Annotation.md) | None |
| [AnnotationProperty](AnnotationProperty.md) | None |
| [AnnotationPropertyMixin](AnnotationPropertyMixin.md) | Groups all annotation property bundles |
| [Anonymous](Anonymous.md) | Abstract root class for all anonymous (non-named; lacking an identifier) expressions |
| [AnonymousClassExpression](AnonymousClassExpression.md) | None |
| [Any](Any.md) | None |
| [Axiom](Axiom.md) | None |
| [Class](Class.md) | None |
| [ClassExpression](ClassExpression.md) | None |
| [Expression](Expression.md) | None |
| [HasCategory](HasCategory.md) | None |
| [HasLifeCycle](HasLifeCycle.md) | None |
| [HasMappings](HasMappings.md) | None |
| [HasMinimalMetadata](HasMinimalMetadata.md) | Absolute minimum metadata model |
| [HasProvenance](HasProvenance.md) | None |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |
| [HasUserInformation](HasUserInformation.md) | None |
| [NamedIndividual](NamedIndividual.md) | None |
| [NamedObject](NamedObject.md) | Anything with an IRI |
| [NotObsoleteAspect](NotObsoleteAspect.md) | Auto-classifies anything that is not obsolete |
| [ObjectProperty](ObjectProperty.md) | None |
| [ObsoleteAspect](ObsoleteAspect.md) | Auto-classifies anything that is obsolete |
| [Ontology](Ontology.md) | An OWL ontology |
| [Property](Property.md) | None |
| [PropertyExpression](PropertyExpression.md) | None |
| [Restriction](Restriction.md) | None |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |
| [Thing](Thing.md) | None |
| [TransitiveProperty](TransitiveProperty.md) | None |


## Slots

| Slot | Description |
| --- | --- |
| [allValuesFrom](allValuesFrom.md) | None |
| [alternative_term](alternative_term.md) | None |
| [annotatedProperty](annotatedProperty.md) | None |
| [annotatedSource](annotatedSource.md) | None |
| [annotatedTarget](annotatedTarget.md) | None |
| [annotations](annotations.md) | None |
| [broadMatch](broadMatch.md) | None |
| [cardinality](cardinality.md) | None |
| [category](category.md) | None |
| [changeNote](changeNote.md) | None |
| [closeMatch](closeMatch.md) | None |
| [comment](comment.md) | None |
| [complementOf](complementOf.md) | None |
| [conformsTo](conformsTo.md) | None |
| [consider](consider.md) | None |
| [contributor](contributor.md) | None |
| [core_property](core_property.md) | abstract grouping of core properties |
| [created](created.md) | when the term came into being |
| [created_by](created_by.md) | None |
| [creation_date](creation_date.md) | None |
| [creator](creator.md) | None |
| [curator_note](curator_note.md) | None |
| [database_cross_reference](database_cross_reference.md) | None |
| [date](date.md) | when the term was updated |
| [date_retrieved](date_retrieved.md) | None |
| [defaultLanguage](defaultLanguage.md) | None |
| [definition](definition.md) | None |
| [definition_source](definition_source.md) | None |
| [depicted_by](depicted_by.md) | None |
| [deprecated](deprecated.md) | None |
| [disconnected_from](disconnected_from.md) | None |
| [disjointWith](disjointWith.md) | None |
| [distinctMembers](distinctMembers.md) | None |
| [domain](domain.md) | None |
| [editor_note](editor_note.md) | None |
| [editor_preferred_term](editor_preferred_term.md) | None |
| [equivalentClass](equivalentClass.md) | None |
| [equivalentProperty](equivalentProperty.md) | None |
| [evidence](evidence.md) | None |
| [exactMatch](exactMatch.md) | None |
| [example_of_usage](example_of_usage.md) | None |
| [excluded_axiom](excluded_axiom.md) | None |
| [excluded_from_QC_check](excluded_from_QC_check.md) | None |
| [excluded_subClassOf](excluded_subClassOf.md) | None |
| [excluded_synonym](excluded_synonym.md) | None |
| [external_ontology](external_ontology.md) | None |
| [has_alternative_id](has_alternative_id.md) | Relates a live term to a deprecated ID that was merged in |
| [has_axiom_label](has_axiom_label.md) | None |
| [has_broad_synonym](has_broad_synonym.md) | None |
| [has_curation_status](has_curation_status.md) | None |
| [has_exact_synonym](has_exact_synonym.md) | None |
| [has_narrow_synonym](has_narrow_synonym.md) | None |
| [has_obo_namespace](has_obo_namespace.md) | None |
| [has_obsolescence_reason](has_obsolescence_reason.md) | None |
| [has_ontology_root_term](has_ontology_root_term.md) | None |
| [has_rank](has_rank.md) | None |
| [has_related_synonym](has_related_synonym.md) | None |
| [has_synonym_type](has_synonym_type.md) | None |
| [hasValue](hasValue.md) | None |
| [id](id.md) | this maps to the URI in RDF |
| [IEDB_alternative_term](IEDB_alternative_term.md) | None |
| [image](image.md) | None |
| [imported_from](imported_from.md) | None |
| [imports](imports.md) | None |
| [in_subset](in_subset.md) | Maps an ontology element to a subset it belongs to |
| [informative_property](informative_property.md) | None |
| [intersectionOf](intersectionOf.md) | None |
| [inverseOf](inverseOf.md) | None |
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) | None |
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) | None |
| [is_class_level](is_class_level.md) | None |
| [is_cyclic](is_cyclic.md) | None |
| [is_inferred](is_inferred.md) | None |
| [is_metadata_tag](is_metadata_tag.md) | None |
| [is_transitive](is_transitive.md) | None |
| [ISA_alternative_term](ISA_alternative_term.md) | None |
| [isDefinedBy](isDefinedBy.md) | None |
| [label](label.md) | None |
| [license](license.md) | None |
| [logical_predicate](logical_predicate.md) | None |
| [match](match.md) | None |
| [match_aspect](match_aspect.md) | None |
| [maxQualifiedCardinality](maxQualifiedCardinality.md) | None |
| [members](members.md) | None |
| [minCardinality](minCardinality.md) | None |
| [minQualifiedCardinality](minQualifiedCardinality.md) | None |
| [narrowMatch](narrowMatch.md) | None |
| [NCIT_definition_source](NCIT_definition_source.md) | None |
| [NCIT_term_source](NCIT_term_source.md) | None |
| [NCIT_term_type](NCIT_term_type.md) | None |
| [never_in_taxon](never_in_taxon.md) | None |
| [notes](notes.md) | None |
| [object](object.md) | None |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | None |
| [oboInOwl_id](oboInOwl_id.md) | None |
| [oboInOwl_ontology](oboInOwl_ontology.md) | None |
| [obsoletion_related_property](obsoletion_related_property.md) | Grouping class for all properties related to lifecycle |
| [onClass](onClass.md) | None |
| [oneOf](oneOf.md) | None |
| [onProperty](onProperty.md) | None |
| [ontology_term_requester](ontology_term_requester.md) | None |
| [page](page.md) | None |
| [predicate](predicate.md) | None |
| [propertyChainAxiom](propertyChainAxiom.md) | None |
| [provenance_property](provenance_property.md) | None |
| [qualifiedCardinality](qualifiedCardinality.md) | None |
| [range](range.md) | None |
| [reification_predicate](reification_predicate.md) | None |
| [sameAs](sameAs.md) | None |
| [seeAlso](seeAlso.md) | None |
| [shortcut_annotation_property](shortcut_annotation_property.md) | None |
| [shorthand](shorthand.md) | None |
| [should_conform_to](should_conform_to.md) | None |
| [someValuesFrom](someValuesFrom.md) | None |
| [source](source.md) | None |
| [subClassOf](subClassOf.md) | None |
| [synonym](synonym.md) | None |
| [temporal_interpretation](temporal_interpretation.md) | None |
| [term_editor](term_editor.md) | None |
| [term_replaced_by](term_replaced_by.md) | None |
| [term_tracker_item](term_tracker_item.md) | None |
| [title](title.md) | None |
| [type](type.md) | None |
| [unionOf](unionOf.md) | None |
| [url](url.md) | None |
| [version_property](version_property.md) | None |
| [versionInfo](versionInfo.md) | None |
| [versionIRI](versionIRI.md) | None |


## Enumerations

| Enumeration | Description |
| --- | --- |


## Subsets

| Subset | Description |
| --- | --- |
| [AllotropePermittedProfile](AllotropePermittedProfile.md) | None |
| [AllotropeRequiredProfile](AllotropeRequiredProfile.md) | None |
| [GoPermittedProfile](GoPermittedProfile.md) | None |
| [GoRecommendedProfile](GoRecommendedProfile.md) | None |
| [GoRequiredProfile](GoRequiredProfile.md) | None |
| [ObiPermittedProfile](ObiPermittedProfile.md) | None |
| [ObiRequiredProfile](ObiRequiredProfile.md) | None |
