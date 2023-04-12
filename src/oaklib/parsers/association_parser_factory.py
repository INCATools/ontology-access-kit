from typing import Type

from oaklib.parsers import AssociationParser


def get_association_parser(syntax: str, *args, **kwargs) -> Type[AssociationParser]:
    """
    Get an association parser for a given syntax

    :param syntax:
    :param args:
    :param kwargs:
    :return:
    """
    if syntax is None:
        raise ValueError("syntax must be specified")
    from oaklib.parsers import get_association_parser_resolver

    cls = get_association_parser_resolver().lookup(syntax)
    return cls(*args, **kwargs)
