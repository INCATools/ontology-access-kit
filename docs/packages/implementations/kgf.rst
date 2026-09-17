.. _kgf:

KGF
===

The KGF adapter wraps a *Knowledge Graph Framework* service: a read-only HTTP API over
immutable, versioned RDF bundles. The reference deployment is the FRINK / Proto-OKN
service at `<https://apps.okn.us/kgf>`_, which serves several dozen knowledge graphs,
including Ubergraph, Babel, SPOKE and a number of environmental and social-science
graphs.

Selectors
---------

The selector is ``kgf:`` followed by a dataset identifier, as listed by
``GET https://apps.okn.us/kgf``:

.. code-block:: bash

    runoak -i kgf:ubergraph info GO:0005634

Bundles are versioned. By default the release the service marks as ``current`` is used;
a specific release can be pinned with ``@``:

.. code-block:: bash

    runoak -i kgf:ubergraph@v0.0.2 info GO:0005634

To reach a dataset on a different KGF deployment, give its full URL:

.. code-block:: bash

    runoak -i kgf:https://apps.okn.us/kgf/sockg info 'https://idir.uta.edu/sockg-ontology/individuals/Crop.48'

Identifiers
-----------

KGF speaks IRIs; OAK speaks CURIEs. The adapter contracts IRIs using OAK's default
prefix map extended with the prefixes the bundle's manifest declares, so OBO terms
compress the way they do elsewhere in OAK (``GO:0005634``, not ``obo:GO_0005634``),
while bundle-specific vocabularies still get readable prefixes. IRIs can also be passed
in directly wherever a CURIE is accepted.

KGF skolemizes blank nodes into ``urn:fdc:…:kgf:bnode:…`` IRIs. The adapter treats these
as anonymous: they are excluded from :meth:`entities`, from relationship results, and
from search results.

What is supported
-----------------

KGF offers triple pattern fragments, node description, a full-text index and batch label
lookup, which is enough for:

- :class:`~oaklib.interfaces.basic_ontology_interface.BasicOntologyInterface`: labels,
  definitions, synonyms, metadata, relationships, entity and obsoletion listings
- :class:`~oaklib.interfaces.obograph_interface.OboGraphInterface`: nodes, edges and the
  graph walks built on them, such as ``ancestors`` and ``descendants``
- :class:`~oaklib.interfaces.search_interface.SearchInterface`
- :class:`~oaklib.interfaces.mapping_provider_interface.MappingProviderInterface`

Search runs against the bundle's full-text index, which is token-based: there is no
substring or wildcard matching. Exact and partial searches are answered by the index;
starts-with searches (``runoak search 'l^nucleol'``) use KGF's ordered term scan instead,
which is case sensitive and looks at a bounded number of literals. Regular expression
and SQL search syntaxes are not supported and raise ``NotImplementedError``.

Which predicates count as labels is taken from the bundle manifest's ``predicate_roles``,
so search and label lookup work on graphs that name things with something other than
``rdfs:label`` (SOCKG, for instance, also uses ``dcterms:title``).

Performance
-----------

KGF exposes triple patterns rather than a query language, so a query that would be one
SPARQL request elsewhere becomes one or more HTTP requests here. Node-level operations
fetch the whole node in a single ``describe`` call and cache it, so looking up a label,
definition and synonyms for the same term costs one request in total. Whole-graph
operations (:meth:`entities`, :meth:`obsoletes`) page through the service and are slow on
the larger bundles.

Graph walks such as ``ancestors`` and ``descendants`` visit one node per request, so they
cost roughly one request per node reached. This bites hardest on bundles that already
materialize their entailed edges: asking Ubergraph for the descendants of a general term
reaches tens of thousands of nodes.

Code
----

.. currentmodule:: oaklib.implementations.kgf.kgf_implementation

.. autoclass:: KGFImplementation
    :members:
