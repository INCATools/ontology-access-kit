import subprocess
from pathlib import Path
from typing import Dict, List

import pandas as pd
from sqlalchemy import create_engine


def pipe_subprocess(cmd1: List[str], cmd2: List[str]):
    # https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes
    # https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes
    cat = subprocess.run(cmd1, check=True, capture_output=True)
    return subprocess.run(cmd2, input=cat.stdout, capture_output=True)


def sqlite_bulk_load(
    path: str, csv_file: str, table_name: str, cat_cmd=None, cols: List[str] = None
):
    """
    Bulk load a CSV into a SQLite database

    This is compatible with the old implementation that used shell commands to
    load the csv to sqlite which was not usable cross platform.
    Param "cat_cmd" is now useless.

    :param path:
    :param csv_file:
    :param table_name:
    :param cat_cmd:
    :param cols:
    :return:
    """
    read_csv_args = dict(sep="\t", comment="!", header=None, names=cols)
    sqlite_bulk_load2(path, csv_file, table_name, read_csv_args)


def sqlite_bulk_load2(
    path: str,
    csv_file: str,
    table_name: str,
    read_csv_args: Dict = None,
) -> None:
    """
    Bulk load a CSV into a SQLite database

    :param path:
    :param csv_file:
    :param table_name:
    :param read_csv_args
    """
    db_name = Path(path).resolve()
    csv_file = Path(csv_file).resolve()
    engine = create_engine("sqlite:///" + str(db_name))

    if "chunksize" in read_csv_args and read_csv_args.get("chunksize") is not None:
        with pd.read_csv(csv_file, **read_csv_args) as reader:
            for chunk in reader:
                chunk.to_sql(table_name, engine, if_exists="append", index=False)
    else:
        df = pd.read_csv(csv_file, **read_csv_args)
        df.to_sql(table_name, engine, if_exists="append", index=False)
