"""
Functions for managing and accessing API keys via :mod:`pystow`.
"""

import pystow

from oaklib.datamodels.vocabulary import APP_NAME

__all__ = [
    "get_apikey_value",
    "set_apikey_value",
]


def get_apikey_value(system: str) -> str:
    """
    Gets the value of a specific API key

    :param system: e.g "bioportal"
    :return:
    """
    return pystow.get_config(APP_NAME, system)


def set_apikey_value(system: str, val: str) -> None:
    """
    Sets the value for a specific API key

    :param system: e.g. "bioportal"
    :param val: API key value
    :return:
    """
    pystow.write_config(APP_NAME, system, val)
