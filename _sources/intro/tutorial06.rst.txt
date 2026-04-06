Part 6: Working With OWL
========================

OAK exposes an experimental ``funowl`` adapter for local OWL files.
The selector name is historical; the adapter is now backed by
`py-horned-owl <https://github.com/ontology-tools/py-horned-owl>`_.
Plain local ``.owl``, ``.ofn``, ``.omn``, and ``.owx`` paths default to this
adapter; explicit schemes such as ``sqlite:foo.owl`` still override that
default.


OWL Datamodel
--------------

See :ref:`funowl`

OwlInterface
------------

``OwlInterface`` is the low-level OAK view for working with OWL axioms and OWL-
specific structures directly.

Loading a local OWL file
^^^^^^^^^^^^^^^^^^^^^^^^

For local files, plain ``.owl``, ``.ofn``, ``.omn``, and ``.owx`` paths now
default to the horned-owl-backed OWL adapter:

.. code-block:: python

   from oaklib import get_adapter

   oi = get_adapter("path/to/my-ontology.owl")
   print(type(oi).__name__)

If you want a different backend, be explicit in the selector:

.. code-block:: python

   sqlite_oi = get_adapter("sqlite:path/to/my-ontology.owl")
   sparql_oi = get_adapter("sparql:path/to/my-ontology.owl")

Inspecting asserted OWL axioms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can iterate over raw axioms, or use helpers for common axiom types:

.. code-block:: python

   from oaklib import get_adapter

   oi = get_adapter("path/to/my-ontology.owl")

   for axiom in oi.subclass_axioms(subclass="GO:0005634"):
       print(type(axiom).__name__, axiom)

   labels = list(
       oi.annotation_assertion_axioms(
           subject="GO:0005634",
           property="rdfs:label",
       )
   )

   eq_axioms = list(oi.equivalence_axioms(about="GO:0031965"))

If you need the underlying horned-owl ontology object, use:

.. code-block:: python

   ontology = oi.owl_ontology()
   print(type(ontology).__name__)

Projected graph operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

The horned-owl adapter also projects a graph view from supported OWL patterns,
so graph-oriented APIs can often be used alongside axiom APIs:

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
   ancestors = list(oi.ancestors("GO:0005634", predicates=["rdfs:subClassOf"]))

Logical definitions are exposed in OBO Graph form:

.. code-block:: python

   ldefs = list(oi.logical_definitions(subjects=["GO:0031965"]))
   for ldef in ldefs:
       print(ldef.definedClassId, ldef.genusIds, ldef.restrictions)

Reasoning status
^^^^^^^^^^^^^^^^

``OwlInterface`` does not currently provide a pluggable OWL reasoner. In the
current horned-owl-backed implementation:

- ``reasoner_configurations()`` returns an empty list
- axiom filtering does not accept a ``ReasonerConfiguration``
- ``include_entailed=True`` on graph methods gives a lightweight projected
  closure over supported OWL patterns, not full OWL reasoning

For precomputed closure and broader graph-style querying, the recommended
production path remains the :ref:`sql_implementation`. For external OWL
reasoners, see the ROBOT plugin below.

ROBOT Plugin
------------

See `oakx-robot <https://github.com/INCATools/oakx-robot>`_
