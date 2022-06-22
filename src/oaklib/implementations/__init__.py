from class_resolver import ClassResolver

from oaklib.interfaces import OntologyInterface
from oaklib.implementations.bioportal.bioportal_implementation import (
    BioportalImplementation,
)
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph.ubergraph_implementation import (
    UbergraphImplementation,
)

__all__ = [
    "implementation_resolver",
    # Concrete classes
    "BioportalImplementation",
    "OlsImplementation",
    "OntobeeImplementation",
    "ProntoImplementation",
    "SqlImplementation",
    "UbergraphImplementation",
]

implementation_resolver: ClassResolver[OntologyInterface] = ClassResolver.from_subclasses(
    OntologyInterface,
    default=SqlImplementation,
    suffix="Implementation",
)
