import csv
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import IO, Any, Dict, List, Union

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, LABEL_PREDICATE
from oaklib.interfaces.obograph_interface import OboGraphInterface

COLUMN_NAME = str
ROW = Dict[COLUMN_NAME, Any]

ID_KEY = "id"
LABEL_KEY = "label"
DEFINITION_KEY = "definition"
ANCESTORS_KEY = "ancestors"
MAPPINGS_KEY = "mappings"

LIST_PATTERN = re.compile(r"\[(.*)\]")


@dataclass
class ColumnDependency:
    """
    Models an interdependency between an identifier column and a column with a dependent value
    """

    primary_key: COLUMN_NAME
    relation: str
    dependent_column: COLUMN_NAME
    parameters: Dict[str, Any] = None
    ignore_inconsistencies: bool = None
    allow_missing_values: bool = None
    missing_value_token: str = None
    fuzzy_match: bool = None


@dataclass
class TableMetadata:
    """
    A configuration for table filling
    """

    dependencies: List[ColumnDependency] = None
    delimiter: str = None

    def set_ignore_inconsistencies(self, v: bool):
        """
        Sets global value for ignoring inconsistencies for all dependencies

        :param v:
        :return:
        """
        for d in self.dependencies:
            d.ignore_inconsistencies = v

    def set_allow_missing_values(self, v: bool):
        """
        Sets global value for ignoring missing values for all dependencies

        :param v:
        :return:
        """
        for d in self.dependencies:
            d.allow_missing_values = v

    def set_missing_value_token(self, v: bool):
        """
        Sets global value for ignoring missing values for all dependencies

        This also sets each dependencies to allow for missing values, provided
        v is set

        :param v:
        :return:
        """
        for d in self.dependencies:
            d.missing_value_token = v
            if v:
                d.allow_missing_values = True


def apply_dict(
    rows: List[ROW],
    mapping: Dict[str, Any],
    from_col: COLUMN_NAME,
    to_col: COLUMN_NAME,
    dependency: ColumnDependency,
):
    for row in rows:
        if row.get(to_col) is None:
            from_val = row[from_col]
            new_to_val = mapping.get(from_val)
            if not new_to_val:
                msg = f"No corresponding value in {from_col} for: {from_val}"
                if not dependency.allow_missing_values:
                    raise ValueError(msg)
                else:
                    logging.debug(msg)
                    if dependency.missing_value_token is not None:
                        row[to_col] = dependency.missing_value_token
            else:
                row[to_col] = new_to_val


def parse_table(input_file: IO, delimiter="\t") -> List[ROW]:
    """
    Parses a file into rows, replacing empty lines with None values

    :param input_file:
    :param delimiter:
    :return:
    """
    reader = csv.DictReader(filter(lambda row: row[0] != "#", input_file), delimiter=delimiter)
    rows = [row for row in reader]
    for row in rows:
        for col in row.keys():
            v = row[col]
            if v == "":
                row[col] = None
            m = LIST_PATTERN.match(v)
            if m:
                row[col] = m.group(1).split("|")
    return rows


def write_table(
    rows: List[ROW], output_file: IO, comments: List[str] = None, delimiter="\t", list_delimiter="|"
) -> None:
    """Writes a list of rows to a file, replacing None values with empty strings.

    :param rows: List of rows in dict format.
    :param output_file: Target location to write output.
    :param comments: A list of comments in the table.
    :param delimiter: File delimiter., defaults to "\t"
    :param list_delimiter: List delimiter., defaults to "|"
    """
    if comments and len(comments) > 0:
        for comment in comments:
            output_file.write(comment)

    cols = list(rows[0].keys())
    writer = csv.DictWriter(output_file, fieldnames=cols, delimiter=delimiter)
    writer.writeheader()
    for row in rows:
        for col in row.keys():
            v = row[col]
            if v is None:
                row[col] = ""
            if isinstance(v, list):
                row[col] = list_delimiter.join(v)
        writer.writerow(row)


@dataclass
class TableFiller:
    """
    An engine for filling in missing columns in tables based on metadata about these columns
    """

    ontology_interface: BasicOntologyInterface = None

    def fill_table_file(
        self, input_file: IO, output_file: IO, table_metadata: TableMetadata = None
    ):
        """
        As :ref:`fill_table`, but input is passed as a file

        :param input_file:
        :param output_file:
        :param table_metadata:
        :return:
        """
        if table_metadata and table_metadata.delimiter:
            delim = table_metadata.delimiter
        else:
            delim = "\t"
        rows = parse_table(input_file, delimiter=delim)
        self.fill_table(rows, table_metadata)
        write_table(rows, output_file, delimiter=delim)

    def fill_table(self, rows: List[ROW], table_metadata: TableMetadata = None):
        """
        Fills in missing values for a list of rows

        :param rows: list of rows, which each row is a dict. Edited in place.
        :param table_metadata:
        :return:
        """
        if table_metadata is None:
            table_metadata = self.infer_metadata(rows[0])
        if not table_metadata.dependencies:
            table_metadata.dependencies = self.infer_metadata(rows[0]).dependencies
        for dependency in table_metadata.dependencies:
            self.fill_table_column(rows, dependency)
            if not dependency.allow_missing_values:
                for row in rows:
                    if not row.get(dependency.primary_key):
                        raise ValueError(f"Missing primary key value for row: {row}")
                    if not row.get(dependency.dependent_column):
                        raise ValueError(f"Missing dependent value for row: {row}")

    def fill_table_column(self, rows: List[ROW], dependency: ColumnDependency):
        pk = dependency.primary_key
        dc = dependency.dependent_column
        rel = dependency.relation
        oi = self.ontology_interface
        pk_vals = {
            r.get(pk) for r in rows if r.get(pk, None) is not None and r.get(dc, None) is None
        }
        dc_vals = {
            r.get(dc) for r in rows if r.get(dc, None) is not None and r.get(pk, None) is None
        }
        fwd_mapping = {}
        rev_mapping = {}
        # Note to developers: it may be tempting to genericize the code below,
        # but be very careful before doing this. Logic for different properties
        # may be subtly different, and over-genericizing may lead to overly
        # abstract or less efficient code
        if rel == LABEL_KEY:
            if pk_vals:
                for curie, label in oi.labels(list(pk_vals)):
                    fwd_mapping[curie] = label
            if dc_vals:
                for v in dc_vals:
                    curies = oi.curies_by_label(v)
                    if len(curies) == 1:
                        rev_mapping[v] = curies[0]
                    elif len(curies) == 0:
                        if not dependency.allow_missing_values:
                            raise ValueError(f"Label {v} is not a label for any CURIE")
                    else:
                        raise ValueError(f"Label {v} has mappings: {curies}")
        elif rel == DEFINITION_KEY:
            if pk_vals:
                for curie in pk_vals:
                    defn = oi.definition(curie)
                    fwd_mapping[curie] = defn
            if dc_vals:
                raise NotImplementedError
        elif rel == ANCESTORS_KEY:
            if pk_vals:
                if isinstance(oi, OboGraphInterface):
                    for curie in pk_vals:
                        params = dependency.parameters
                        if not params:
                            params = {}
                        ancs = list(oi.ancestors(curie, **params))
                        fwd_mapping[curie] = ancs
                else:
                    raise ValueError(f"{oi} must implement OboGraphInterface for ancestors option")
            if dc_vals:
                raise NotImplementedError
        elif rel == MAPPINGS_KEY:
            if pk_vals:
                if isinstance(oi, BasicOntologyInterface):
                    for curie in pk_vals:
                        params = dependency.parameters
                        if not params:
                            params = {}
                        mappings = [x for _, x in oi.simple_mappings_by_curie(curie)]
                        fwd_mapping[curie] = mappings
                else:
                    raise ValueError(f"{oi} must implement OboGraphInterface for ancestors option")
            if dc_vals:
                raise NotImplementedError
        else:
            raise NotImplementedError(f"Rel = {rel}")
        apply_dict(rows, fwd_mapping, pk, dc, dependency)
        apply_dict(rows, rev_mapping, dc, pk, dependency)

    def infer_metadata(self, row: ROW) -> TableMetadata:
        """
        Infers the metadata given a sample row, based entirely on conventions

        :param row:
        :return:
        """
        tm = TableMetadata(dependencies=[])
        for k in [LABEL_KEY, DEFINITION_KEY, MAPPINGS_KEY, ANCESTORS_KEY]:
            if k in row:
                tm.dependencies.append(ColumnDependency(ID_KEY, k, k))
        inferred = defaultdict(dict)
        for col in row.keys():
            for sep in ["_", ".", " ", "-"]:
                if sep in col:
                    parts = col.split(sep)
                    if len(parts) > 1:
                        base_col = parts.pop()
                        base_name = sep.join(parts)
                        if base_col == ID_KEY:
                            inferred[base_name][ID_KEY] = col
                        if base_col == "identifier":
                            inferred[base_name][ID_KEY] = col
                        if base_col == LABEL_KEY:
                            inferred[base_name][LABEL_KEY] = col
                        if base_col == "name":
                            inferred[base_name][LABEL_KEY] = col
                        if base_col == DEFINITION_KEY:
                            inferred[base_name][DEFINITION_KEY] = col
        for v in inferred.values():
            if ID_KEY in v:
                id_col = v[ID_KEY]
                if LABEL_KEY in v:
                    tm.dependencies.append(ColumnDependency(id_col, LABEL_KEY, v[LABEL_KEY]))
                if DEFINITION_KEY in v:
                    tm.dependencies.append(
                        ColumnDependency(id_col, DEFINITION_KEY, v[DEFINITION_KEY])
                    )

        return tm

    def extract_metadata_from_linkml(
        self, schema: Union[str, SchemaDefinition], class_name: str = None
    ) -> TableMetadata:
        """
        Extract dependencies using a LinkML schema

        The primary_key in the dependency is the slot that is designated the identifier

        Labels, definitions, etc are determined from the slot_ur

        For example, with the following schema

        .. code-block ::

            classes:
              Person:
                attributes:
                  id:
                    identifier: true
                  name:
                    slot_uri: rdfs:label

        The label dependency between id and name is determined.

        TODO: use the new LinkML mapping datamodel to determine dependencies in denormalized schemas,
        such as SSSOM

        :param schema:
        :param class_name: Optional, if it can be inferred
        :return:
        """
        tm = TableMetadata(dependencies=[])
        schemaview = SchemaView(schema)
        if class_name is None:
            non_roots = [
                cn
                for cn, c in schemaview.all_classes().items()
                if not c.tree_root and not c.mixin and not c.abstract
            ]
            if len(non_roots) > 1:
                raise ValueError(f"Multiple candidate classes: {non_roots}")
            elif not non_roots:
                raise ValueError("No candidate classes")
            else:
                class_name = non_roots[0]
        pk_col = schemaview.get_identifier_slot(class_name)
        for slot in schemaview.class_induced_slots(class_name):
            slot_uri = schemaview.get_uri(slot)
            if slot_uri == LABEL_PREDICATE:
                rel = LABEL_KEY
            elif slot_uri == HAS_DEFINITION_CURIE:
                rel = DEFINITION_KEY
            else:
                rel = None
            if rel:
                dep = ColumnDependency(pk_col.name, rel, slot.name)
                tm.dependencies.append(dep)
        return tm
