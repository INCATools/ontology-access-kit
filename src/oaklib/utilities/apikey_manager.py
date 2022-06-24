"""
Functions for managing and accessing API keys via :mod:`pystow`.
"""

import pystow

__all__ = [
    "get_apikey_value",
    "set_apikey_value",
]

APP_NAME = "oak"


def get_apikey_value(key: str) -> str:
    """
    Get the value of the given configuration key.

    :param key: e.g "bioportal" for the BioPortal API token
    :return: The API key associated with the system

    Configuration can be set in the following ways:

    1. Set `OAKLIB_{key}` in the environment
    2. Create a configuration file `~/.config/oaklib.ini`
       and set the `[oaklib]` section in it with the given key
    3. Use the :func:`set_apikey_value` function to directly
       create a configuration file
    """
    return pystow.get_config(APP_NAME, key)


def set_apikey_value(key: str, value: str) -> None:
    """
    Set the value for a given configuration key.

    :param key: e.g. "bioportal"
    :param value: API key value
    """
    pystow.write_config(APP_NAME, key, value)
