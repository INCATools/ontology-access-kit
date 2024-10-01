# Ontology Metadata Ontology Schema

Schema for ontology metadata

URI: https://w3id.org/oak/ontology-metadata

Name: Ontology-Metadata



## Classes

| Class | Description |
| --- | --- |
| [Annotation](Annotation.md) | A reified property-object pair |
| [AnnotationPropertyMixin](AnnotationPropertyMixin.md) | Groups all annotation property bundles |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasCategory](HasCategory.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasLifeCycle](HasLifeCycle.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasMappings](HasMappings.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasMinimalMetadata](HasMinimalMetadata.md) | Absolute minimum metadata model |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasProvenance](HasProvenance.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HasUserInformation](HasUserInformation.md) | None |
| [Anonymous](Anonymous.md) | Abstract root class for all anonymous (non-named; lacking an identifier) expressions |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AnonymousClassExpression](AnonymousClassExpression.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Restriction](Restriction.md) | None |
| [Any](Any.md) | None |
| [Axiom](Axiom.md) | A logical or non-logical statement |
| [Expression](Expression.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ClassExpression](ClassExpression.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PropertyExpression](PropertyExpression.md) | None |
| [NotObsoleteAspect](NotObsoleteAspect.md) | Auto-classifies anything that is not obsolete |
| [ObsoleteAspect](ObsoleteAspect.md) | Auto-classifies anything that is obsolete |
| [Thing](Thing.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[NamedObject](NamedObject.md) | Anything with an IRI |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Ontology](Ontology.md) | An OWL ontology |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Class](Class.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[NamedIndividual](NamedIndividual.md) | An instance that has a IRI |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Agent](Agent.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[HomoSapiens](HomoSapiens.md) | An individual human being |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Image](Image.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Property](Property.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Subset](Subset.md) | A collection of terms grouped for some purpose |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |



## Slots

| Slot | Description |
| --- | --- |
| [allValuesFrom](allValuesFrom.md) |  |
| [alternative_term](alternative_term.md) |  |
| [annotatedProperty](annotatedProperty.md) |  |
| [annotatedSource](annotatedSource.md) |  |
| [annotatedTarget](annotatedTarget.md) |  |
| [annotations](annotations.md) |  |
| [broadMatch](broadMatch.md) |  |
| [cardinality](cardinality.md) |  |
| [category](category.md) |  |
| [changeNote](changeNote.md) |  |
| [closeMatch](closeMatch.md) |  |
| [comment](comment.md) |  |
| [complementOf](complementOf.md) |  |
| [conformsTo](conformsTo.md) |  |
| [consider](consider.md) |  |
| [contributor](contributor.md) |  |
| [core_property](core_property.md) | abstract grouping of core properties |
| [created](created.md) | when the term came into being |
| [created_by](created_by.md) |  |
| [creation_date](creation_date.md) |  |
| [creator](creator.md) |  |
| [curator_note](curator_note.md) |  |
| [database_cross_reference](database_cross_reference.md) |  |
| [date](date.md) | when the term was updated |
| [date_retrieved](date_retrieved.md) |  |
| [defaultLanguage](defaultLanguage.md) |  |
| [definition](definition.md) |  |
| [definition_source](definition_source.md) |  |
| [depicted_by](depicted_by.md) |  |
| [deprecated](deprecated.md) |  |
| [disconnected_from](disconnected_from.md) |  |
| [disjointWith](disjointWith.md) |  |
| [distinctMembers](distinctMembers.md) |  |
| [domain](domain.md) |  |
| [editor_note](editor_note.md) |  |
| [editor_preferred_term](editor_preferred_term.md) |  |
| [equivalentClass](equivalentClass.md) |  |
| [equivalentProperty](equivalentProperty.md) |  |
| [evidence](evidence.md) |  |
| [exactMatch](exactMatch.md) |  |
| [example_of_usage](example_of_usage.md) |  |
| [excluded_axiom](excluded_axiom.md) |  |
| [excluded_from_QC_check](excluded_from_QC_check.md) |  |
| [excluded_subClassOf](excluded_subClassOf.md) |  |
| [excluded_synonym](excluded_synonym.md) |  |
| [external_ontology](external_ontology.md) |  |
| [has_alternative_id](has_alternative_id.md) | Relates a live term to a deprecated ID that was merged in |
| [has_axiom_label](has_axiom_label.md) |  |
| [has_broad_synonym](has_broad_synonym.md) |  |
| [has_curation_status](has_curation_status.md) |  |
| [has_exact_synonym](has_exact_synonym.md) |  |
| [has_narrow_synonym](has_narrow_synonym.md) |  |
| [has_obo_namespace](has_obo_namespace.md) |  |
| [has_obsolescence_reason](has_obsolescence_reason.md) |  |
| [has_ontology_root_term](has_ontology_root_term.md) |  |
| [has_rank](has_rank.md) |  |
| [has_related_synonym](has_related_synonym.md) |  |
| [has_synonym_type](has_synonym_type.md) |  |
| [hasValue](hasValue.md) |  |
| [id](id.md) | this maps to the URI in RDF |
| [IEDB_alternative_term](IEDB_alternative_term.md) |  |
| [image](image.md) |  |
| [imported_from](imported_from.md) |  |
| [imports](imports.md) |  |
| [in_subset](in_subset.md) | Maps an ontology element to a subset it belongs to |
| [informative_property](informative_property.md) |  |
| [intersectionOf](intersectionOf.md) |  |
| [inverseOf](inverseOf.md) |  |
| [is_a_defining_property_chain_axiom](is_a_defining_property_chain_axiom.md) |  |
| [is_a_defining_property_chain_axiom_where_second_argument_is_reflexive](is_a_defining_property_chain_axiom_where_second_argument_is_reflexive.md) |  |
| [is_class_level](is_class_level.md) |  |
| [is_cyclic](is_cyclic.md) |  |
| [is_inferred](is_inferred.md) |  |
| [is_metadata_tag](is_metadata_tag.md) |  |
| [is_transitive](is_transitive.md) |  |
| [ISA_alternative_term](ISA_alternative_term.md) |  |
| [isDefinedBy](isDefinedBy.md) |  |
| [label](label.md) |  |
| [language](language.md) |  |
| [license](license.md) |  |
| [logical_predicate](logical_predicate.md) |  |
| [match](match.md) |  |
| [match_aspect](match_aspect.md) |  |
| [maxQualifiedCardinality](maxQualifiedCardinality.md) |  |
| [members](members.md) |  |
| [minCardinality](minCardinality.md) |  |
| [minQualifiedCardinality](minQualifiedCardinality.md) |  |
| [narrowMatch](narrowMatch.md) |  |
| [NCIT_definition_source](NCIT_definition_source.md) |  |
| [NCIT_term_source](NCIT_term_source.md) |  |
| [NCIT_term_type](NCIT_term_type.md) |  |
| [never_in_taxon](never_in_taxon.md) |  |
| [notes](notes.md) |  |
| [object](object.md) |  |
| [OBO_foundry_unique_label](OBO_foundry_unique_label.md) |  |
| [oboInOwl_id](oboInOwl_id.md) |  |
| [oboInOwl_ontology](oboInOwl_ontology.md) |  |
| [obsoletion_related_property](obsoletion_related_property.md) | Grouping class for all properties related to lifecycle |
| [onClass](onClass.md) |  |
| [oneOf](oneOf.md) |  |
| [onProperty](onProperty.md) |  |
| [ontology_term_requester](ontology_term_requester.md) |  |
| [page](page.md) |  |
| [predicate](predicate.md) |  |
| [propertyChainAxiom](propertyChainAxiom.md) |  |
| [provenance_property](provenance_property.md) |  |
| [qualifiedCardinality](qualifiedCardinality.md) |  |
| [range](range.md) |  |
| [reification_predicate](reification_predicate.md) |  |
| [sameAs](sameAs.md) |  |
| [seeAlso](seeAlso.md) |  |
| [shortcut_annotation_property](shortcut_annotation_property.md) |  |
| [shorthand](shorthand.md) |  |
| [should_conform_to](should_conform_to.md) |  |
| [someValuesFrom](someValuesFrom.md) |  |
| [source](source.md) |  |
| [subClassOf](subClassOf.md) |  |
| [synonym](synonym.md) |  |
| [temporal_interpretation](temporal_interpretation.md) |  |
| [term_editor](term_editor.md) |  |
| [term_replaced_by](term_replaced_by.md) |  |
| [term_tracker_item](term_tracker_item.md) |  |
| [title](title.md) |  |
| [type](type.md) |  |
| [unionOf](unionOf.md) |  |
| [url](url.md) |  |
| [version_property](version_property.md) |  |
| [versionInfo](versionInfo.md) |  |
| [versionIRI](versionIRI.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [DefinitionConstraintComponent](DefinitionConstraintComponent.md) | An extension of SHACL constraint component for constraining definitions |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [CURIELiteral](CURIELiteral.md) | A string representation of a CURIE |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [IriType](IriType.md) | An IRI |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [LabelType](LabelType.md) | A string that provides a human-readable name for an entity |
| [NarrativeText](NarrativeText.md) | A string that provides a human-readable description of something |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [TidyString](TidyString.md) |  |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |
| [URLLiteral](URLLiteral.md) | A URL representation of a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
| [AllotropePermittedProfile](AllotropePermittedProfile.md) |  |
| [AllotropeRequiredProfile](AllotropeRequiredProfile.md) |  |
| [GoPermittedProfile](GoPermittedProfile.md) |  |
| [GoRecommendedProfile](GoRecommendedProfile.md) |  |
| [GoRequiredProfile](GoRequiredProfile.md) |  |
| [ObiPermittedProfile](ObiPermittedProfile.md) |  |
| [ObiRequiredProfile](ObiRequiredProfile.md) |  |
