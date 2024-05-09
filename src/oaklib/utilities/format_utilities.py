"""
Utilities for working with formats

See https://github.com/INCATools/ontology-access-kit/issues/687
"""

from enum import Enum


class OntologyModel(str, Enum):
    """
    Enumerated types for ontology models.

    A model is an abstract representation of an ontology that is potentially
    serializable in multiple syntaxes.
    """

    OWL = "owl"
    """W3C OWL2 Ontology Model"""

    SKOS = "skos"
    """W3C SKOS Ontology Model"""

    SDO_RDFS = "sdo_rdfs"
    """Schema.org RDFS Ontology Model"""

    OBOFORMAT = "oboformat"
    """OBO Format Ontology Model. Always serialized as obo format"""

    OBOGRAPHS = "obographs"
    """OBO Graphs Ontology Model"""


MODEL_ALLOWED_SYNTAXES = {
    OntologyModel.OWL: [
        "ttl",
        "rdfxml",
        "n3",
        "nt",
        "pretty-xml",
        "trix",
        "trig",
        "ofn",
        "owx",
        "omn",
        "obo",
    ],
    OntologyModel.SKOS: ["ttl", "rdfxml", "n3", "nt", "pretty-xml", "trix", "trig"],
    OntologyModel.OBOFORMAT: ["obo"],
    OntologyModel.OBOGRAPHS: ["json", "yaml"],
}


OBOGRAPHS_SYNTAX_ALIAS_MAP = {
    "json": "json",
    "obojson": "json",
    "yaml": "yaml",
    "obograph": "json",
    "obographjson": "json",
    "obographyaml": "yaml",
}


RDFLIB_SYNTAX_ALIAS_MAP = {
    "owl": "turtle",
    "ttl": "turtle",
    "rdfxml": "xml",
}
