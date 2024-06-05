"""
This package serves as the master index for all implementations.
"""

from functools import cache

from class_resolver import ClassResolver

from oaklib.implementations.aggregator.aggregator_implementation import (
    AggregatorImplementation,
)
from oaklib.implementations.agrkb.agrkb_implementation import AGRKBImplementation
from oaklib.implementations.amigo.amigo_implementation import AmiGOImplementation
from oaklib.implementations.cx.cx_implementation import CXImplementation
from oaklib.implementations.funowl.funowl_implementation import FunOwlImplementation
from oaklib.implementations.gilda import GildaImplementation
from oaklib.implementations.kgx.kgx_implementation import KGXImplementation
from oaklib.implementations.llm_implementation import LLMImplementation
from oaklib.implementations.monarch.monarch_implementation import MonarchImplementation
from oaklib.implementations.ncbi.ncbi_gene_implementation import NCBIGeneImplementation
from oaklib.implementations.ncbi.pubmed_implementation import PubMedImplementation
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
from oaklib.implementations.pantherdb.pantherdb_implementation import (
    PantherDBImplementation,
)
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.quickgo.quickgo_implementation import QuickGOImplementation
from oaklib.implementations.semsimian.semsimian_implementation import (
    SemSimianImplementation,
)
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
from oaklib.implementations.sparql.lov_implementation import LovImplementation
from oaklib.implementations.sparql.oak_metamodel_implementation import (
    OakMetaModelImplementation,
)
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.tabular.robot_template_implementation import RobotTemplateImplementation
from oaklib.implementations.translator.translator_implementation import (
    TranslatorImplementation,
)
from oaklib.implementations.ubergraph.ubergraph_implementation import (
    UbergraphImplementation,
)
from oaklib.implementations.uniprot.uniprot_implementation import UniprotImplementation
from oaklib.implementations.wikidata.wikidata_implementation import (
    WikidataImplementation,
)
from oaklib.interfaces import OntologyInterface

__all__ = [
    "get_implementation_resolver",
    # Concrete classes
    "AggregatorImplementation",
    "AgroPortalImplementation",
    "AGRKBImplementation",
    "AmiGOImplementation",
    "BioPortalImplementation",
    "CXImplementation",
    "EcoPortalImplementation",
    "MatPortalImplementation",
    "OlsImplementation",
    "TIBOlsImplementation",
    "MonarchImplementation",
    "NCBIGeneImplementation",
    "OntobeeImplementation",
    "ProntoImplementation",
    "QuickGOImplementation",
    "SimpleOboImplementation",
    "SqlImplementation",
    "UbergraphImplementation",
    "LovImplementation",
    "SparqlImplementation",
    "WikidataImplementation",
    "PantherDBImplementation",
    "PubMedImplementation",
    "FunOwlImplementation",
    "GildaImplementation",
    "LLMImplementation",
    "KGXImplementation",
    "RobotTemplateImplementation",
    "UniprotImplementation",
    "TranslatorImplementation",
    "OakMetaModelImplementation",
    "SemSimianImplementation",
]


@cache
def get_implementation_resolver() -> ClassResolver[OntologyInterface]:
    """
    Get a class resolver for all implementations (adapters).

    See `<https://class-resolver.readthedocs.io/>`_

    Note that typical OAK users should never need to call this directly;
    this is used by OAK to dynamically select the right implementation given
    a selector descriptions

    As far as possible we try and use generic mechanisms to resolve.

    Any class specified in __all__ above will be checked to see if it inherits from
    OntologyInterface.

    If the class name ends with "Implementation" (which is the convention in OAK
    for all implementations), then it should be available here, wiith a descriptor
    name that is downcases class name, with "Implementation" removed.

    :return: A ClassResolver capable of resolving an OntologyInterface implementation
    """
    implementation_resolver: ClassResolver[OntologyInterface] = ClassResolver.from_subclasses(
        OntologyInterface,
        suffix="Implementation",
        skip={
            OntoPortalImplementationBase,
            BaseOlsImplementation,
        },
    )
    # if an implementation uses a shorthand name that is
    # different from the class name (minus Implementation), then
    # it should be added here
    implementation_resolver.synonyms.update(
        {
            "obolibrary": ProntoImplementation,
            "prontolib": ProntoImplementation,
            "simpleobo": SimpleOboImplementation,
            "sqlite": SqlImplementation,
            "rdflib": SparqlImplementation,
            "oak": OakMetaModelImplementation,
            "cx": CXImplementation,
            "ndexbio": CXImplementation,
            "semsimian": SemSimianImplementation,
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
