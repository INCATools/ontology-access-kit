.. _enrichment:

Enrichment and Over-Representation Analysis
===========================================

Background
----------

Enrichment analysis (also known as over-representation analysis) is a statistical method used to identify ontology terms that are significantly over-represented in a set of entities. This is a common technique in bioinformatics and other fields to gain biological insights from large datasets, such as gene expression experiments or genetic studies.

The basic idea behind enrichment analysis is to:

1. Take a set of entities of interest (e.g., genes from a disease study)
2. Find the ontology terms associated with these entities (see the :ref:`OAK guide on associations <associations>` for more details on how entities like genes are linked to ontology terms)
3. Determine which terms are statistically over-represented compared to what would be expected by chance
4. Rank and filter these terms to identify meaningful patterns

OAK provides a comprehensive suite of tools for performing enrichment analysis with any ontology and association set. This makes it possible to identify patterns in your data using domain knowledge encoded in ontologies.

An important aspect of OAK's enrichment analysis is that it takes into account the full ontology graph structure when performing calculations. As described in the :ref:`guide on relationships and graphs <relationships-and-graphs>`, the choice of :term:`Predicates<Predicate>` (edge types) is critical. For example, when analyzing gene annotations to GO terms, you typically want to include both :term:`SubClassOf` and :term:`PartOf` relationships for roll-up, whereas in disease-phenotype analysis, typically only :term:`SubClassOf` relationships are used. This "rolling up" of annotations ensures that if an entity is associated with a specific term, it is also considered to be associated with all ancestors of that term following the selected predicates.

Concepts
--------

Statistical Significance in Enrichment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The core of enrichment analysis is determining if an ontology term is statistically over-represented in your entity set. This is typically done using statistical tests like the hypergeometric test (Fisher's exact test).

Given:

- N: Total number of entities in the background
- n: Number of entities in your study set
- K: Number of entities associated with a specific term in the background
- k: Number of entities associated with that term in your study set

The probability (p-value) of observing at least k entities associated with the term by chance is:

.. math::

    P(X \geq k) = \sum_{i=k}^{min(n, K)} \frac{{K \choose i}{N-K \choose n-i}}{{N \choose n}}

Lower p-values indicate that the term is significantly over-represented in your study set.

Redundancy Filtering
^^^^^^^^^^^^^^^^^^^

A common challenge in enrichment analysis is dealing with redundant results. Because ontologies have hierarchical structures as described in the :ref:`guide on relationships and graphs <relationships-and-graphs>`, terms that are closely related in the hierarchy often appear together in the results. This can make it difficult to interpret the findings.

OAK provides redundancy filtering to address this issue. When enabled, it removes terms that are either:

- Ancestors of more significant terms (subsumed by a child term)
- Descendants of more significant terms (subsumed by a parent term)

Just like with other graph traversal operations in OAK, redundancy filtering considers the specific :term:`Predicates<Predicate>` you select. For example, when working with GO, you typically want to use both :term:`SubClassOf` and :term:`PartOf` relationships for redundancy filtering, whereas with HPO, you might only use :term:`SubClassOf`.

This filtering helps to produce a more concise and interpretable set of enriched terms, focusing on the most specific and statistically significant results.

Performing Enrichment Analysis
------------------------------

Using the Command Line
^^^^^^^^^^^^^^^^^^^^^

The basic syntax for enrichment analysis in OAK is:

.. code-block:: bash

    runoak -i [ONTOLOGY] -g [ASSOCIATION_FILE] -G [ASSOCIATION_TYPE] enrichment -p [PREDICATES] -U [ENTITY_SET]

Notice the ``-p`` parameter, which specifies which :term:`Predicates<Predicate>` to follow when traversing the ontology graph. As explained in the :ref:`relationships and graphs guide <relationships-and-graphs>`, selecting appropriate predicates is crucial for correct semantic interpretation.

Here's a practical example using the Human Phenotype Ontology (HPO) and gene-phenotype associations:

.. code-block:: bash

    # First, normalize our gene IDs to a standard format
    runoak -i translator: normalize .idfile genes-list.txt -M NCBIGene -o normalized-genes.tsv
    
    # Then perform enrichment analysis (using only is-a/subClassOf relationships)
    runoak -i sqlite:obo:hp -G hpoa_g2p -g hpoa_g2p.tsv enrichment -p i -U normalized-genes.tsv \
        -O csv --autolabel -o results.tsv

To apply redundancy filtering:

.. code-block:: bash

    runoak -i sqlite:obo:hp -G hpoa_g2p -g hpoa_g2p.tsv enrichment -p i -U normalized-genes.tsv \
        -O csv --autolabel --filter-redundant -o filtered-results.tsv
        
For Gene Ontology enrichment, you would typically include both is-a and part-of relationships:

.. code-block:: bash

    runoak -i sqlite:obo:go -G gaf -g gene_associations.gaf enrichment -p i,p -U gene-list.tsv \
        -O csv --autolabel --filter-redundant -o go-enrichment.tsv

Visualizing Results
^^^^^^^^^^^^^^^^^^

OAK provides visualization capabilities for enrichment results:

.. code-block:: bash

    # Create a visualization of the top 15 enriched terms
    runoak -i sqlite:obo:hp viz -p i .idfile top-15-results.tsv -O png -o enrichment-results.png

Programmatic Interface
^^^^^^^^^^^^^^^^^^^^^

You can also perform enrichment analysis programmatically using the Python API. The :class:`ClassEnrichmentCalculationInterface` provides methods for sophisticated enrichment analysis, with access to all the same parameters available in the command line.

.. code-block:: python

    from oaklib import get_adapter
    from oaklib.interfaces import ClassEnrichmentCalculationInterface
    from oaklib.datamodels.vocabulary import IS_A, PART_OF

    # Initialize adapters
    ontology_adapter = get_adapter("sqlite:obo:hp")
    enrichment_adapter = ClassEnrichmentCalculationInterface(ontology_adapter)
    
    # Load your entity set
    with open("normalized-genes.tsv", "r") as f:
        study_set = [line.strip() for line in f]
    
    # Perform enrichment analysis
    # Note how we explicitly specify which predicates to follow
    results = enrichment_adapter.calculate_enrichment(
        subjects=study_set,
        predicates=[IS_A],  # For HPO, we use only is-a relationships
        filter_redundant=True
    )
    
    # For GO, we would use both is-a and part-of:
    # predicates=[IS_A, PART_OF]
    
    # Process results
    for result in results:
        print(f"{result.term_id} | {result.term_label} | p-value: {result.p_value}")

Interpreting Results
-------------------

Enrichment results typically include the following information for each term:

- **Term ID and Label**: The ontology term identifier and its readable name
- **p-value**: The statistical significance (lower is more significant)
- **Adjusted p-value**: Corrected for multiple testing (e.g., using Benjamini-Hochberg)
- **Fold Enrichment**: How many times more frequent the term is in your set vs. expected by chance
- **Study Count**: Number of entities in your set associated with this term
- **Study Total**: Total number of entities in your study set
- **Population Count**: Number of entities in the background associated with this term
- **Population Total**: Total number of entities in the background

When interpreting results, consider:

1. Focus on terms with low p-values (typically < 0.05 after adjustment)
2. Look for biological patterns among the significant terms
3. Consider the fold enrichment to understand the magnitude of over-representation
4. Examine redundancy-filtered results to get a clearer picture of distinct patterns

Advanced Options
---------------

Pseudo-enrichment
^^^^^^^^^^^^^^^

In some cases, you may want to perform enrichment analysis without having actual association files. OAK supports "pseudo-enrichment" where each term is associated with itself:

.. code-block:: bash

    runoak -i sqlite:obo:hp enrichment --pseudo-enrichment -U term-list.txt

Custom Background Sets
^^^^^^^^^^^^^^^^^^^^^

By default, the background set includes all entities in the association file. You can specify a custom background:

.. code-block:: bash

    runoak -i sqlite:obo:hp -G hpoa_g2p -g hpoa_g2p.tsv enrichment \
        -U study-genes.tsv -B background-genes.tsv

Cross-Ontology Enrichment
^^^^^^^^^^^^^^^^^^^^^^^^^

OAK can perform enrichment analysis across different ontologies if you have the appropriate association data:

.. code-block:: bash

    # Enrichment of GO terms using HPO gene associations
    runoak -i sqlite:obo:go -G hpoa_g2p -g hpoa_g2p.tsv enrichment -U gene-list.tsv

Companion Notebooks
------------------

To explore enrichment analysis in more depth, check out the following notebooks:

- `Enrichment Analysis Command Examples <https://incatools.github.io/ontology-access-kit/examples/Commands/Enrichment.html>`_
- `GO Annotation Enrichment <https://incatools.github.io/ontology-access-kit/examples/Ontologies/GO/Annotation-Analysis.html>`_

These notebooks provide practical examples that demonstrate how to apply the concepts discussed in this guide, particularly how to correctly specify :term:`Predicates<Predicate>` for different ontologies and analysis contexts.

Further Reading
--------------

- `Gene Ontology enrichment analysis <https://doi.org/10.1093/bioinformatics/btp713>`_
- `The Gene Ontology resource: enriching a GOld mine <https://doi.org/10.1093/nar/gkaa1113>`_
- `A comparative evaluation of annotation-based and expression-based phenotypic similarities for human diseases <https://doi.org/10.1186/s12859-020-03923-6>`_