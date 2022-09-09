import importlib
import logging
import pkgutil

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
]

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("oakext_") or name.startswith("oakx_")
}

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
    }
)
for name, module in discovered_plugins.items():
    try:
        implementation_resolver.synonyms.update(module.schemes)
    except AttributeError:
        logging.info(f"Plugin {name} does not declare schemes")
