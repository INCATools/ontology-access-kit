.. _embedding_provider_interface:

Embedding Provider Interface
----------------------------

Provides vector embeddings for ontology entities, as numpy matrices or pandas
DataFrames, together with operations derived from them: pairwise and all-by-all
similarity, nearest-neighbour search, and set-wise (best match average) comparison.

Implementations:

- :ref:`ols_implementation` serves precomputed embeddings for several models
  (see ``embedding_models()``), cached locally so OLS is only asked once per
  term and model. The cache follows the OAK ``--caching`` policy (default: refresh
  after 1 month). OLS reports similarity as ``(1 + cosine) / 2``; OAK converts this
  back to plain cosine.
- Any adapter that can compute ancestors (e.g. ``sqlite``) provides the ``closure``
  model, in which each term is a multi-hot vector of its reflexive ancestors. This
  puts classic ontology-based similarity on the same footing as learned embeddings;
  e.g. Jaccard over closure vectors is identical to ancestor-set Jaccard.
  Adapters that can compute information content also provide ``closure_ic``, where
  each ancestor is weighted by its IC; weighted Jaccard over these vectors is simGIC.
  Set ``closure_embedding_predicates`` (e.g. ``[IS_A, PART_OF]``) to follow other
  relations.

.. code-block:: python

    >>> from oaklib import get_adapter
    >>> ols = get_adapter("ols:hp")  # doctest: +SKIP
    >>> ids, matrix = ols.entity_embeddings(["HP:0001159", "HP:0006101"])  # doctest: +SKIP
    >>> ols.embedding_similarity("HP:0001159", "HP:0006101", model="text-embedding-3-small_pca512")  # doctest: +SKIP
    >>> list(ols.nearest_entities_to_text("webbed fingers", limit=5))  # doctest: +SKIP

See the :ref:`embeddings_examples` notebooks for worked examples, and the
``embedding-models``, ``embeddings``, ``nearest-entities`` and ``embedding-similarity``
commands for command-line access.

.. currentmodule:: oaklib.interfaces.embedding_provider_interface

.. autoclass:: EmbeddingProviderInterface
    :members:
