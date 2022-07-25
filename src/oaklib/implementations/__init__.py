from class_resolver import ClassResolver

from oaklib.implementations.bioportal.agroportal_implementation import (
    AgroportalImplementation,
)
from oaklib.implementations.bioportal.bioportal_implementation import (
    BioportalImplementation,
)
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.gilda import GildaImplementation
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.lov_implementation import LovImplementation
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
    "implementation_resolver",
    # Concrete classes
    "AgroportalImplementation",
    "BioportalImplementation",
    "OlsImplementation",
    "OntobeeImplementation",
    "ProntoImplementation",
    "SqlImplementation",
    "UbergraphImplementation",
    "LovImplementation",
    "SparqlImplementation",
    "WikidataImplementation",
    "FunOwlImplementation",
    "GildaImplementation",
]

implementation_resolver: ClassResolver[OntologyInterface] = ClassResolver.from_subclasses(
    OntologyInterface,
    suffix="Implementation",
)
implementation_resolver.synonyms.update(
    {
        "obolibrary": ProntoImplementation,
        "prontolib": ProntoImplementation,
        "sqlite": SqlImplementation,
        "rdflib": SparqlImplementation,
    }
)
