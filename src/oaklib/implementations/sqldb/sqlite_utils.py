import logging
import subprocess
from pathlib import Path
from typing import List


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

    :param path:
    :param csv_file:
    :param table_name:
    :param cat_cmd:
    :param cols:
    :return:
    """
    # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
    if cat_cmd is None:
        cat_cmd = ["cat"]
    db_name = Path(path).resolve()
    csv_file = Path(csv_file).resolve()
    csv_file = str(csv_file).replace("\\", "\\\\")
    if cols:
        col_tups = [f"{c} TEXT" for c in cols]
        ddl = f'CREATE TABLE {table_name}({", ".join(col_tups)});'
        pipe_subprocess(["echo", f"{ddl}"], ["sqlite3", str(db_name)])
        # cat = subprocess.run(['echo', f'{ddl}'], check=True, capture_output=True)
        # result = subprocess.run(['sqlite3', str(db_name)], input=cat.stdout, capture_output=True)
    if cat_cmd is None:
        cat_cmd = ["cat"]
    print(csv_file)
    cmd = [
        "sqlite3",
        str(db_name),
        "-cmd",
        ".mode csv",
        '.separator "\t"',
        f".import '|cat -' {table_name}",
    ]
    result = pipe_subprocess(cat_cmd + [csv_file], cmd)
    # cat = subprocess.Popen(cat_cmd + [csv_file], stdout=subprocess.PIPE)
    # result = subprocess.run(,
    #                        stdin=cat.stdout,
    #                        check=True,
    #                        capture_output=True)
    if result.stderr:
        logging.error(result.stderr)
    return result
