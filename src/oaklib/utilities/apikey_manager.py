import logging
import os
from pathlib import Path
from appdirs import user_data_dir
from oaklib.datamodels.vocabulary import APP_NAME

APIKEY_SUFFIX = 'apikey.txt'

def get_apikey_path(system: str) -> Path:
    p = Path(user_data_dir(APP_NAME)) / f'{system}-{APIKEY_SUFFIX}'
    logging.info(f'API KEY path = {p}')
    return p

def get_apikey_value(system: str) -> str:
    path = get_apikey_path(system)
    if not path.exists():
        raise ValueError(f'No API key found in: {path}')
    with open(path) as stream:
        return stream.readlines()[0].strip()

def set_apikey_value(system: str, val: str) -> str:
    dir = Path(user_data_dir(APP_NAME))
    dir.mkdir(exist_ok=True, parents=True)
    with open(get_apikey_path(system), 'w', encoding='utf-8') as stream:
        stream.write(val)

