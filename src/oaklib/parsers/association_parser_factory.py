from typing import Type

from oaklib.parsers import AssociationParser


def get_association_parser(syntax: str, *args, **kwargs) -> Type[AssociationParser]:
    # return SCHEME_DICT[scheme]
    from oaklib.parsers import get_association_parser_resolver

    cls = get_association_parser_resolver().lookup(syntax)
    return cls(*args, **kwargs)
