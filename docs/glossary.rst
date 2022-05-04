Glossary
========

.. glossary::

   Ontology
    A flexible concept loosely encompassing any collection of ontology elements and statements or relationships connecting them

   Ontology element
    A discrete part of an :term:`Ontology`, with a unique persistent identifier

   Term
    A core element in an ontology, typically a :term:`Class`, but sometimes used to include instances or relationship types

   Concept
    See :term:`Term`

   CURIE
    A |CURIE| is a compact :term:`URI`

   URI
    A Uniform Resource Indicator, a generalization of URL. Most people think of URLs as being solely for addresses for web pages (or APIs) but in semantic web technologies, URLs can serve as actual identifiers for entities like ontology terms.

   Class
    An |Ontology element| that formally represents something that can be instantiated. For example, the class "heart"

   Mapping
    See SSSOM

   Graph
    Formally...

   OWL
    See...

   RDF
    See...

   OBO Format
    See...

   Iterator
    We...

   Interface
    See :ref:`interfaces`

   Implementation
    See :ref:`implementations`

   Datamodel
    See :ref:`datamodels`



   Named Individual
    An |Ontology element| that represents an instance of a class. . For example, the instance "John" or "John's heart".
    Note that instances are not commonly represented in ontologies

   Property
    An |Ontology element| that represents an attribute or a characteristic of an element.
    In |OWL|, properties are divided into disjoint categories:
      * |ObjectProperty|
      * |AnnotationProperty|
      * |DatatypeProperty|

   Relationship
    A |Relationship| is a type connection between two ontology elements. The first element is called the |subject|,
    and the second one the |object|, with the type of connection being the |Relationship Type|.
    Sometimes Relationships are equated with |Triple|s in |RDF| but this can be confusing, because some relationships
    map to *multiple* triples when following the OWL RDF serialization. An example is the relationship "finger part-of hand",
    which in OWL is represented using a |Existential Restriction| that maps to 4 triples.

   Relationship Type
    An |Ontology element| that represents the type of a |Relationship|.
    Typically corresponds to an |ObjectProperty| in |OWL|

   Subset
    An |Ontology element| that represents a named collection of elements, typically grouped for some purpose

