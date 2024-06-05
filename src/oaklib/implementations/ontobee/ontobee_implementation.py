from dataclasses import dataclass
from typing import Optional

from oaklib.implementations.sparql.abstract_sparql_implementation import (
    AbstractSparqlImplementation,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.usages_interface import UsagesInterface

ONTOBEE_MERGED_GRAPH_PREFIX = "http://purl.obolibrary.org/obo/merged/"


@dataclass
class OntobeeImplementation(
    AbstractSparqlImplementation,
    SearchInterface,
    MappingProviderInterface,
    OboGraphInterface,
    UsagesInterface,
):
    """
    An OAK adapter that standardizes access to the Ontobee sparql endpoint.

    Ontobee is the default linked data server for most OBO Foundry library ontologies.
    Ontobee has also been used for many non-OBO ontologies.

    To access this use the ``ontobee:`` :term:`Input Selector`:

    - ``ontobee:`` - the default ontobee endpoint
    - ``ontobee:uberon`` - the uberon subgraph on ontobee

    This adapter implements:

    - :ref:`basic_ontology_interface`
    - :ref:`search_interface`
    - :ref:`mapping_provider_interface`
    - :ref:`obograph_interface`

    .. note ::

        To see the full range of methods implemented, see the documentation for the interfaces above.

    An OntobeeImplementation can be initialized directly:

    >>> from oaklib.implementations import OntobeeImplementation
    >>> oi = OntobeeImplementation()

    The default ontobee endpoint will be assumed

    Alternatively, use a selector:

    >>> from oaklib import get_adapter
    >>> oi = get_adapter("ontobee:")

    Or to access a specific ontology, such as the Vaccine Ontology:

    >>> oi = get_adapter("ontobee:vo")

    After that you can use any of the methods that OntoBee implements; e.g.

    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> # uncomment to test
    >>> # for a in oi.ancestors("UBERON:0002398", predicates=[IS_A]):
    >>> #    print(a)

    Command Line
    ------------

    .. code-block:: bash

        $ runoak -i ontobee:uberon ancestors -p i UBERON:0002398

    Notes
    -----
    This is a specialization the :ref:`sparql` implementation to
    allow access for ontologies on the `Ontobee <https://www.ontobee.org/>`_ linked data server.

    See: `<https://www.ontobee.org/>`_

    """

    def _default_url(self) -> str:
        return "http://sparql.hegroup.org/sparql"

    @property
    def named_graph(self) -> Optional[str]:
        if self.resource.slug is None:
            return None
        else:
            return f"{ONTOBEE_MERGED_GRAPH_PREFIX}{self.resource.slug.upper()}"
