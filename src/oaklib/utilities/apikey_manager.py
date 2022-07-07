"""
Functions for managing and accessing API keys

See `<https://github.com/ActiveState/appdirs>`_
"""

import logging
from pathlib import Path

from appdirs import user_config_dir

from oaklib.datamodels.vocabulary import APP_NAME

APIKEY_SUFFIX = "apikey.txt"


def get_apikey_path(system: str) -> Path:
    """
    Gets the path to where the API key is stored

    :param system: e.g "bioportal"
    :return:
    """
    p = Path(user_config_dir(APP_NAME)) / f"{system}-{APIKEY_SUFFIX}"
    logging.info(f"API KEY path = {p}")
    return p


def get_apikey_value(system: str) -> str:
    """
    Gets the value of a specific API key

    :param system: e.g "bioportal"
    :return:
    """
    path = get_apikey_path(system)
    if not path.exists():
        raise ValueError(f"No API key found in: {path}")
    with open(path) as stream:
        return stream.readlines()[0].strip()


def set_apikey_value(system: str, val: str) -> None:
    """
    Sets the value for a specific API key

    :param system: e.g. "bioportal"
    :param val: API key value
    :return:
    """
    dir = Path(user_config_dir(APP_NAME))
    dir.mkdir(exist_ok=True, parents=True)
    with open(get_apikey_path(system), "w", encoding="utf-8") as stream:
        stream.write(val)
