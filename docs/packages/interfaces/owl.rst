.. _owl_interface:

OWL Interface
-------------

.. currentmodule:: oaklib.interfaces.owl_interface

``OwlInterface`` exposes OWL axioms and OWL-specific helpers directly, without
forcing everything through a graph abstraction.

Quick examples
^^^^^^^^^^^^^^

Load a local OWL ontology using the default selector logic:

.. code-block:: python

   from oaklib import get_adapter

   oi = get_adapter("path/to/my-ontology.owl")

Inspect common OWL axiom types:

.. code-block:: python

   from oaklib import get_adapter

   oi = get_adapter("path/to/my-ontology.owl")

   subclass_axioms = list(oi.subclass_axioms(subclass="GO:0005634"))
   label_axioms = list(
       oi.annotation_assertion_axioms(
           subject="GO:0005634",
           property="rdfs:label",
       )
   )
   eq_axioms = list(oi.equivalence_axioms(about="GO:0031965"))

Project graph-style relationships from OWL axioms:

.. code-block:: python

   from oaklib import get_adapter

   oi = get_adapter("path/to/my-ontology.owl")

   direct = list(oi.relationships(subjects=["GO:0005634"]))
   entailed = list(
       oi.relationships(
           subjects=["GO:0005634"],
           include_entailed=True,
       )
   )

Reasoning
^^^^^^^^^

``OwlInterface`` does not currently expose a general OWL reasoner. The
horned-owl-backed implementation can still provide a lightweight projected
closure for graph APIs when ``include_entailed=True`` is used, but that should
not be interpreted as complete OWL reasoning.

.. autoclass:: OwlInterface
    :members:
