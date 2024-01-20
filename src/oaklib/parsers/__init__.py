from functools import cache

from class_resolver import ClassResolver

from oaklib.parsers.association_parser import AssociationParser
from oaklib.parsers.gaf_association_parser import GafAssociationParser
from oaklib.parsers.gencc_association_parser import GenCCAssociationParser
from oaklib.parsers.hpoa_association_parser import HpoaAssociationParser
from oaklib.parsers.hpoa_g2d_association_parser import HpoaG2DAssociationParser
from oaklib.parsers.hpoa_g2p_association_parser import HpoaG2PAssociationParser
from oaklib.parsers.mim2gene_association_parser import MedgenMimG2DAssociationParser
from oaklib.parsers.pairwise_association_parser import PairwiseAssociationParser
from oaklib.parsers.phaf_association_parser import PhafAssociationParser

__all__ = [
    "get_association_parser_resolver",
    # Concrete classes
    "AssociationParser",
    "PairwiseAssociationParser",
    "GafAssociationParser",
    "GenCCAssociationParser",
    "HpoaAssociationParser",
    "HpoaG2PAssociationParser",
    "PhafAssociationParser",
    "MedgenMimG2DAssociationParser",
]


GAF = "gaf"
"""Gene Ontology GAF syntax"""

G2T = "g2t"
"""Simple pairwise gene to term 2 column syntax"""

HPOA = "hpoa"
"""HPO Annotation syntax"""

HPOA_G2P = "hpoa_g2p"
"""HPO Gene-to-Phenotype syntax"""

HPOA_G2D = "hpoa_g2d"
"""HPO Gene-to-Disease syntax"""

GENCC = "gencc"
"""GenCC CSV format"""

MEDGEN_MIM_G2D = "medgen_mim_g2d"
"""Medgen/NCBI MIM G2D format"""

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
            HPOA_G2D: HpoaG2DAssociationParser,
            PHAF: PhafAssociationParser,
            GENCC: GenCCAssociationParser,
            MEDGEN_MIM_G2D: MedgenMimG2DAssociationParser,
        }
    )

    return association_parser_resolver
