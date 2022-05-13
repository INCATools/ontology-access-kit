# Ontology-Metadata

Schema for ontology metadata

URI: http://purl.obolibrary.org/obo/omo/schema

## Classes

| Class | Description |
| --- | --- |
| [Any](Any.md) | None | 
| [AnnotationPropertyMixin](AnnotationPropertyMixin.md) | Groups all annotation property bundles | 
| [HasMinimalMetadata](HasMinimalMetadata.md) | Absolute minimum metadata model | 
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms | 
| [HasMappings](HasMappings.md) | None | 
| [HasProvenance](HasProvenance.md) | None | 
| [HasLifeCycle](HasLifeCycle.md) | None | 
| [HasCategory](HasCategory.md) | None | 
| [HasUserInformation](HasUserInformation.md) | None | 
| [Thing](Thing.md) | None | 
| [NamedObject](NamedObject.md) | Anything with an IRI | 
| [Ontology](Ontology.md) | An OWL ontology | 
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies | 
| [Class](Class.md) | None | 
| [Property](Property.md) | None | 
| [AnnotationProperty](AnnotationProperty.md) | None | 
| [ObjectProperty](ObjectProperty.md) | None | 
| [TransitiveProperty](TransitiveProperty.md) | None | 
| [NamedIndividual](NamedIndividual.md) | None | 
| [Axiom](Axiom.md) | None | 
| [Subset](Subset.md) | A collection of terms grouped for some purpose | 
| [Anonymous](Anonymous.md) | Abstract root class for all anonymous (non-named; lacking an identifier) expressions | 
| [AnonymousClassExpression](AnonymousClassExpression.md) | None | 
| [Restriction](Restriction.md) | None | 
| [Expression](Expression.md) | None | 
| [ClassExpression](ClassExpression.md) | None | 
| [PropertyExpression](PropertyExpression.md) | None | 
| [ObsoleteAspect](ObsoleteAspect.md) | Auto-classifies anything that is obsolete | 
| [NotObsoleteAspect](NotObsoleteAspect.md) | Auto-classifies anything that is not obsolete | 


## Slots

| Slot | Description |
| --- | --- |
| [core_property](core_property.md) | abstract grouping of core properties | 
| [id](id.md) | this maps to the URI in RDF | 
| [label](label.md) | None | 
| [definition](definition.md) | None | 
| [title](title.md) | None | 
| [match_aspect](match_aspect.md) | None | 
| [match](match.md) | None | 
| [broadMatch](broadMatch.md) | None | 
| [closeMatch](closeMatch.md) | None | 
| [exactMatch](exactMatch.md) | None | 
| [narrowMatch](narrowMatch.md) | None | 
| [database_cross_reference](database_cross_reference.md) | None | 
| [informative_property](informative_property.md) | None | 
| [comment](comment.md) | None | 
| [category](category.md) | None | 
| [image](image.md) | None | 
| [example_of_usage](example_of_usage.md) | None | 
| [changeNote](changeNote.md) | None | 
| [has_curation_status](has_curation_status.md) | None | 
| [defaultLanguage](defaultLanguage.md) | None | 
| [has_ontology_root_term](has_ontology_root_term.md) | None | 
| [conformsTo](conformsTo.md) | None | 
| [license](license.md) | None | 
| [depicted_by](depicted_by.md) | None | 
| [page](page.md) | None | 
| [version_property](version_property.md) | None | 
| [versionIRI](versionIRI.md) | None | 
| [versionInfo](versionInfo.md) | None | 
| [obsoletion_related_property](obsoletion_related_property.md) | Grouping class for all properties related to lifecycle | 
| [deprecated](deprecated.md) | None | 
| [term_replaced_by](term_replaced_by.md) | None | 
| [has_obsolescence_reason](has_obsolescence_reason.md) | None | 
| [consider](consider.md) | None | 
| [has_alternative_id](has_alternative_id.md) | None | 
| [temporal_interpretation](temporal_interpretation.md) | None | 
| [never_in_taxon](never_in_taxon.md) | None | 
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) | None | 
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) | None | 
| [provenance_property](provenance_property.md) | None | 
| [contributor](contributor.md) | None | 
| [creator](creator.md) | None | 
| [created](created.md) | when the term came into being | 
| [date](date.md) | when the term was updated | 
| [source](source.md) | None | 
| [created_by](created_by.md) | None | 
| [creation_date](creation_date.md) | None | 
| [date_retrieved](date_retrieved.md) | None | 
| [editor_note](editor_note.md) | None | 
| [term_editor](term_editor.md) | None | 
| [definition_source](definition_source.md) | None | 
| [curator_note](curator_note.md) | None | 
| [term_tracker_item](term_tracker_item.md) | None | 
| [ontology_term_requester](ontology_term_requester.md) | None | 
| [imported_from](imported_from.md) | None | 
| [has_axiom_label](has_axiom_label.md) | None | 
| [shortcut_annotation_property](shortcut_annotation_property.md) | None | 
| [disconnected_from](disconnected_from.md) | None | 
| [excluded_axiom](excluded_axiom.md) | None | 
| [excluded_from_QC_check](excluded_from_QC_check.md) | None | 
| [excluded_subClassOf](excluded_subClassOf.md) | None | 
| [excluded_synonym](excluded_synonym.md) | None | 
| [should_conform_to](should_conform_to.md) | None | 
| [has_rank](has_rank.md) | None | 
| [alternative_term](alternative_term.md) | None | 
| [ISA_alternative_term](ISA_alternative_term.md) | None | 
| [IEDB_alternative_term](IEDB_alternative_term.md) | None | 
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) | None | 
| [synonym](synonym.md) | None | 
| [editor_preferred_term](editor_preferred_term.md) | None | 
| [has_exact_synonym](has_exact_synonym.md) | None | 
| [has_narrow_synonym](has_narrow_synonym.md) | None | 
| [has_related_synonym](has_related_synonym.md) | None | 
| [has_broad_synonym](has_broad_synonym.md) | None | 
| [has_synonym_type](has_synonym_type.md) | None | 
| [has_obo_namespace](has_obo_namespace.md) | None | 
| [in_subset](in_subset.md) | Maps an ontology element to a subset it belongs to | 
| [reification_predicate](reification_predicate.md) | None | 
| [annotatedProperty](annotatedProperty.md) | None | 
| [annotatedSource](annotatedSource.md) | None | 
| [annotatedTarget](annotatedTarget.md) | None | 
| [imports](imports.md) | None | 
| [logical_predicate](logical_predicate.md) | None | 
| [cardinality](cardinality.md) | None | 
| [complementOf](complementOf.md) | None | 
| [disjointWith](disjointWith.md) | None | 
| [distinctMembers](distinctMembers.md) | None | 
| [equivalentClass](equivalentClass.md) | None | 
| [sameAs](sameAs.md) | None | 
| [equivalentProperty](equivalentProperty.md) | None | 
| [hasValue](hasValue.md) | None | 
| [intersectionOf](intersectionOf.md) | None | 
| [inverseOf](inverseOf.md) | None | 
| [maxQualifiedCardinality](maxQualifiedCardinality.md) | None | 
| [members](members.md) | None | 
| [minCardinality](minCardinality.md) | None | 
| [minQualifiedCardinality](minQualifiedCardinality.md) | None | 
| [onClass](onClass.md) | None | 
| [onProperty](onProperty.md) | None | 
| [oneOf](oneOf.md) | None | 
| [propertyChainAxiom](propertyChainAxiom.md) | None | 
| [qualifiedCardinality](qualifiedCardinality.md) | None | 
| [allValuesFrom](allValuesFrom.md) | None | 
| [someValuesFrom](someValuesFrom.md) | None | 
| [unionOf](unionOf.md) | None | 
| [domain](domain.md) | None | 
| [range](range.md) | None | 
| [isDefinedBy](isDefinedBy.md) | None | 
| [seeAlso](seeAlso.md) | None | 
| [type](type.md) | None | 
| [subClassOf](subClassOf.md) | None | 
| [oboInOwl_id](oboInOwl_id.md) | None | 
| [oboInOwl_ontology](oboInOwl_ontology.md) | None | 
| [is_class_level](is_class_level.md) | None | 
| [is_cyclic](is_cyclic.md) | None | 
| [is_inferred](is_inferred.md) | None | 
| [is_metadata_tag](is_metadata_tag.md) | None | 
| [is_transitive](is_transitive.md) | None | 
| [notes](notes.md) | None | 
| [shorthand](shorthand.md) | None | 
| [url](url.md) | None | 
| [evidence](evidence.md) | None | 
| [external_ontology](external_ontology.md) | None | 
| [NCIT_definition_source](NCIT_definition_source.md) | None | 
| [NCIT_term_type](NCIT_term_type.md) | None | 
| [NCIT_term_source](NCIT_term_source.md) | None | 


## Enums

| Enums | Description |
| --- | --- |

