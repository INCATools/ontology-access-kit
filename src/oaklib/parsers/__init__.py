from functools import cache

from class_resolver import ClassResolver

from oaklib.parsers.association_parser import AssociationParser
from oaklib.parsers.gaf_association_parser import GafAssociationParser
from oaklib.parsers.hpoa_association_parser import HpoaAssociationParser

__all__ = [
    "get_association_parser_resolver",
    # Concrete classes
    "AssociationParser",
    "GafAssociationParser",
]

GAF = "gaf"
HPOA = "hpoa"
KGX = "kgx"


@cache
def get_association_parser_resolver() -> ClassResolver[AssociationParser]:
    association_parser_resolver: ClassResolver[AssociationParser] = ClassResolver.from_subclasses(
        AssociationParser,
        suffix="AssociationParser",
    )
    association_parser_resolver.synonyms.update(
        {
            GAF: GafAssociationParser,
            HPOA: HpoaAssociationParser,
        }
    )

    return association_parser_resolver
