import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
)

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface


@dataclass
class TabularFile:
    name: str
    """logical name."""

    path: Path
    """path to the file."""

    format: str
    """format of the file."""

    delimiter: str = "\t"
    """delimiter for the file."""

    rows: List[Dict[str, Any]] = None
    """rows of the file."""

    metadata: Any = None


@dataclass
class TabularImplementation(
    BasicOntologyInterface,
):
    """
    Simple implementation backed by a directory of tabular files.
    """

    root_folder: Path = None
    tabfile_map: Dict[str, TabularFile] = None
    default_file_suffix: str = ".tsv"

    def __post_init__(self):
        if self.resource.local_path:
            self.root_folder = Path(self.resource.local_path)
        self.sync_files()

    def sync_files(self):
        """
        Load the tabular files from the root folder.

        :return:
        """
        self.initialize_tabfile_map()
        self.load_tabfiles()

    def initialize_tabfile_map(self):
        """
        Initialize tabfile_map by reading from the root folder.

        :return:
        """
        if not self.tabfile_map:
            self.tabfile_map = {}
        for root, _dirs, files in os.walk(self.root_folder):
            for file in files:
                if file.endswith(self.default_file_suffix):
                    name = file[: -len(self.default_file_suffix)]
                    path = Path(root) / file
                    self.tabfile_map[name] = TabularFile(name, path=path, format="tsv")

    def load_tabfiles(self):
        """
        Load the tabular files into memory as a dictionary of lists using csvreader.

        :return:
        """
        for tabfile in self.tabfile_map.values():
            with open(tabfile.path, "r") as f:
                reader = csv.DictReader(f, delimiter=tabfile.delimiter)
                tabfile.rows = list(reader)

    def dump(self, path: str = None, syntax: str = None, clean=False, **kwargs):
        """
        Dump the tabular files to a folder.

        :param path: path to the folder.
        :param syntax: syntax of the file.
        :param kwargs: additional arguments.
        :param clean: clean the folder before dumping.
        :return:
        """
        path = Path(path)
        if clean and path.exists():
            # walk the directory and remove all files
            for root, _dirs, files in os.walk(path):
                for file in files:
                    fullpath = Path(root) / file
                    fullpath.unlink()
            path.rmdir()
        path.mkdir(exist_ok=True, parents=True)
        for name, tabfile in self.tabfile_map.items():
            outpath = path / f"{name}.tsv"
            with open(outpath, "w", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=tabfile.rows[0].keys(), delimiter=tabfile.delimiter
                )
                writer.writeheader()
                writer.writerows(tabfile.rows)
                f.flush()  # Explicit flush, usually redundant inside a with block
        return path
