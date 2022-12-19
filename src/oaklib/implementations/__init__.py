from functools import cache

from class_resolver import ClassResolver

from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.gilda import GildaImplementation
from oaklib.implementations.ols import (
    BaseOlsImplementation,
    OlsImplementation,
    TIBOlsImplementation,
)
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.ontoportal.agroportal_implementation import (
    AgroPortalImplementation,
)
from oaklib.implementations.ontoportal.bioportal_implementation import (
    BioPortalImplementation,
)
from oaklib.implementations.ontoportal.ecoportal_implementation import (
    EcoPortalImplementation,
)
from oaklib.implementations.ontoportal.matportal_implementation import (
    MatPortalImplementation,
)
from oaklib.implementations.ontoportal.ontoportal_implementation_base import (
    OntoPortalImplementationBase,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
from oaklib.implementations.sparql.lov_implementation import LovImplementation
from oaklib.implementations.sparql.oak_metamodel_implementation import (
    OakMetaModelImplementation,
)
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph.ubergraph_implementation import (
    UbergraphImplementation,
)
from oaklib.implementations.wikidata.wikidata_implementation import (
    WikidataImplementation,
)
from oaklib.interfaces import OntologyInterface

__all__ = [
    "get_implementation_resolver",
    # Concrete classes
    "AgroPortalImplementation",
    "BioPortalImplementation",
    "EcoPortalImplementation",
    "MatPortalImplementation",
    "OlsImplementation",
    "TIBOlsImplementation",
    "OntobeeImplementation",
    "ProntoImplementation",
    "SimpleOboImplementation",
    "SqlImplementation",
    "UbergraphImplementation",
    "LovImplementation",
    "SparqlImplementation",
    "WikidataImplementation",
    "FunOwlImplementation",
    "GildaImplementation",
    "OakMetaModelImplementation",
]


@cache
def get_implementation_resolver() -> ClassResolver[OntologyInterface]:
    implementation_resolver: ClassResolver[OntologyInterface] = ClassResolver.from_subclasses(
        OntologyInterface,
        suffix="Implementation",
        skip={
            OntoPortalImplementationBase,
            BaseOlsImplementation,
        },
    )
    implementation_resolver.synonyms.update(
        {
            "obolibrary": ProntoImplementation,
            "prontolib": ProntoImplementation,
            "simpleobo": SimpleOboImplementation,
            "sqlite": SqlImplementation,
            "rdflib": SparqlImplementation,
            "oak": OakMetaModelImplementation,
        }
    )

    # Plugins which want to register an implementation should use
    # the entrypoint group "oaklib.plugins". The name of the entry
    # point will be used as a possible match against the input scheme
    # prefix. The value of the entry point should be an implementation
    # class.
    #
    # See also:
    # https://packaging.python.org/en/latest/specifications/entry-points/
    # https://class-resolver.readthedocs.io/en/latest/api/class_resolver.ClassResolver.html#class_resolver.ClassResolver.register_entrypoint
    implementation_resolver.register_entrypoint("oaklib.plugins")

    return implementation_resolver
