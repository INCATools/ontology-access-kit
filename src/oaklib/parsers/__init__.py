from functools import cache

from class_resolver import ClassResolver

from oaklib.parsers.association_parser import AssociationParser
from oaklib.parsers.gaf_association_parser import GafAssociationParser
from oaklib.parsers.hpoa_association_parser import HpoaAssociationParser
from oaklib.parsers.phaf_association_parser import PhafAssociationParser

__all__ = [
    "get_association_parser_resolver",
    # Concrete classes
    "AssociationParser",
    "PairwiseAssociationParser",
    "GafAssociationParser",
    "HpoaAssociationParser",
    "HpoaG2PAssociationParser",
    "PhafAssociationParser",
]

from oaklib.parsers.hpoa_g2p_association_parser import HpoaG2PAssociationParser
from oaklib.parsers.pairwise_association_parser import PairwiseAssociationParser

GAF = "gaf"
"""Gene Ontology GAF syntax"""

G2T = "g2t"
"""Simple pairwise gene to term 2 column syntax"""

HPOA = "hpoa"
"""HPO Annotation syntax"""

HPOA_G2P = "hpoa_g2p"
"""HPO Gene-to-Phenotype syntax"""

KGX = "kgx"
"""KGX TSV syntax"""

PHAF = "phaf"
"""PomBase Phenotype Association Format"""


@cache
def get_association_parser_resolver() -> ClassResolver[AssociationParser]:
    """
    Get a class resolver for association parsers.

    :return: ClassResolver
    """
    association_parser_resolver: ClassResolver[AssociationParser] = ClassResolver.from_subclasses(
        AssociationParser,
        suffix="AssociationParser",
    )
    association_parser_resolver.synonyms.update(
        {
            GAF: GafAssociationParser,
            HPOA: HpoaAssociationParser,
            G2T: PairwiseAssociationParser,
            HPOA_G2P: HpoaG2PAssociationParser,
            PHAF: PhafAssociationParser,
        }
    )

    return association_parser_resolver
