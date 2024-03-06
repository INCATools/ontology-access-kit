FHIR Conversions
================

:term:`FHIR` (Fast Healthcare Interoperability Resources) is a standard for exchanging healthcare data.

OAK includes methods for converting ontologies or ontology fragments to FHIR CodeSystems.
However, there is no agreed-upon standard way of converting ontologies to FHIR, because
each ontology has its own conventions and metadata vocabularies, and FHIR makes some
assumptions that don't hold for ontologies in OBO such as all terms belonging to
the same code system.

For this reason we make FHIR conversion highly configurable to suit the needs
of a particular project or FHIR server.

CLI
---

Here we will use the OAK ``dump`` command to export an entire ontology to FHIR.

The general pattern for the ``dump`` command is from the CLI is:

.. code-block:: bash

    $ runoak -i INPUT dump -O FORMAT -o OUTPUT-FILE

For dumping to the FHIR json serialization, use ``fhirjson`` as the format:

.. code-block:: bash

    $ runoak -i INPUT dump -O fhirjson -o OUTPUT-FILE


The `fhirjson` format includes a --config-file / -c parameter for its additional parameters.


Example:

.. code-block:: bash

    $ runoak --i go-nucleus.obo dump -o CodeSystem-go-nucleus.json -O fhirjson -c tests/input/fhir_config_example.json

Config file
-----------

See :ref:`obo_graph_to_fhir_converter` for the full list of options.

Options:  

code_system_id: _The code system ID to use for identification on the server uploaded to.
See: https://hl7.org/fhir/resource-definitions.html#Resource.id

code_system_url: _Canonical URL for the code system.
See: https://hl7.org/fhir/codesystem-definitions.html#CodeSystem.url

native_uri_stems: _A comma-separated list of URI stems that will be used to determine whether a
concept is native to the CodeSystem. For example, for OMIM, the following URI stems are native:
https://omim.org/entry/, https://omim.org/phenotypicSeries/PS

include_all_predicates (default=True): Include the maximal amount of predicates. Changes the default behavior from
only exporting: IS_A

use_curies_native_concepts (default=False): _FHIR conventionally uses codes for references to
concepts that are native to a given CodeSystem. With this option, references will be CURIEs instead.

use_curies_foreign_concepts (default=False): _Typical FHIR CodeSystems do not contain any
concepts that are not native to that CodeSystem. In cases where they do appear, this converter defaults to URIs for
references, unless this flag is present, in which case the converter will attempt to construct CURIEs.

predicate_period_replacement (default=False): _Predicates URIs populated into `CodeSystem.
concept.property.code` and `CodeSystem.concept.property.code`, but the popular FHIR server "HAPI" has a bug in which
periods '.' cause errors. If this flag is present, periods will be replaced with underscores '_'.

Example:


.. code-block:: json

    {
        "code_system_id": "HPO",
        "code_system_url": "http://purl.obolibrary.org/obo/hp.owl",
            "native_uri_stems": [
                "http://purl.obolibrary.org/obo/HP_"
            ],
        "include_all_predicates": true,
        "use_curies_native_concepts": false,
        "use_curies_foreign_concepts": false,
        "predicate_period_replacement": true
    }
