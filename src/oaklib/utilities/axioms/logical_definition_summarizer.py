from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE


class LogicalDefinitionElementRole(Enum):
    DEFINED_CLASS = "defined_class"
    GENUS = "genus"
    PREDICATE = "predicate"
    FILLER = "filler"
    SIGNATURE = "signature"
    META = "meta"


class Config(BaseModel):
    row_represents: Optional[List[LogicalDefinitionElementRole]] = None
    column_represents: Optional[List[LogicalDefinitionElementRole]] = None
    cell_represents: Optional[List[LogicalDefinitionElementRole]] = None


def parse_axes_to_config(config: str) -> Config:
    sep = ","
    parts = [parse_config_element(x) for x in config.split(sep)]
    row_represents = parts[0]
    column_represents = parts[1] if len(parts) > 1 else None
    cell_represents = parts[2] if len(parts) > 2 else None
    return Config(
        row_represents=row_represents,
        column_represents=column_represents,
        cell_represents=cell_represents,
    )


def parse_config_element(config: str) -> [LogicalDefinitionElementRole]:
    sep = "+"
    if sep in config:
        return [parse_config_element(v)[0] for v in config.split("+")]
    for x in LogicalDefinitionElementRole:
        if x.value.startswith(config):
            return [x]


def logical_definitions_to_matrix(
    adapter: OboGraphInterface,
    ldefs: List[LogicalDefinitionAxiom],
    config: Config = None,
    sort_values: bool = True,
) -> List[Dict[str, List[Any]]]:
    """
    Converts a list of logical definition axioms to a table.

    The axes are determined by the configuration object. The user can control both
    what each row corresponds to and what each column corresponds to.

    :param adapter: OAK adapter for performing lookups
    :param ldefs: list of logical definition axioms to summarize
    :param config: axis configuration
    :param sort_values: sort values in each cell
    :return: list of row objects
    """
    if not config:
        config = Config()
    row_represents, column_represents = config.row_represents, config.column_represents
    rows = []

    def _cell_val(
        ldef: LogicalDefinitionAxiom,
        element: Optional[Union[CURIE, ExistentialRestrictionExpression]] = None,
        cell_represents: List[LogicalDefinitionElementRole] = None,
    ) -> Any:
        if element is not None:
            return element
        else:
            # if LogicalDefinitionElementRole.FILLER in cell_represents:
            #    return ldef.definedClassId
            return ldef.definedClassId

    def _col_name(curie: CURIE) -> str:
        lbl = adapter.label(curie)
        if lbl:
            return lbl.replace(" ", "_")
        else:
            return curie

    if not row_represents:
        row_represents = [LogicalDefinitionElementRole.DEFINED_CLASS]

    if LogicalDefinitionElementRole.DEFINED_CLASS in row_represents:
        if len(row_represents) > 1:
            raise ValueError(
                f"Cannot have more than one row_representing for defined_class: {row_represents}"
            )
        for ldef in ldefs:
            row = defaultdict(list)
            row["defined_class"] = [ldef.definedClassId]
            ok = False
            if LogicalDefinitionElementRole.PREDICATE in column_represents:
                for x in ldef.genusIds:
                    row["genus"].append(x)
                for x in ldef.restrictions:
                    row[_col_name(x.propertyId)].append(x.fillerId)
                ok = True
            if LogicalDefinitionElementRole.FILLER in column_represents:
                for x in ldef.genusIds:
                    row["genus"].append(x)
                for x in ldef.restrictions:
                    row[_col_name(x.fillerId)].append(x.propertyId)
                ok = True
            if LogicalDefinitionElementRole.GENUS in column_represents:
                # for x in ldef.restrictions:
                #    row[_col_name(x.fillerId)].extend([x.propertyId, x.fillerId])
                for x in ldef.genusIds:
                    row[_col_name(x)].append(_cell_val(ldef))
                ok = True
            if LogicalDefinitionElementRole.META in column_represents:
                for x in ldef.genusIds:
                    row["genus"].append(x)
                for x in ldef.restrictions:
                    row["differentia"].append((x.propertyId, x.fillerId))
                ok = True
            if not ok:
                raise ValueError(
                    f"Invalid column_represents: {column_represents} for row: {row_represents}"
                )
            rows.append(row)
    else:
        row_ix = {}
        for ldef in ldefs:
            pk_vals = []
            if LogicalDefinitionElementRole.GENUS in row_represents:
                pk_vals = ldef.genusIds
            if LogicalDefinitionElementRole.PREDICATE in row_represents:
                pk_vals = [x.propertyId for x in ldef.restrictions]
            if LogicalDefinitionElementRole.FILLER in row_represents:
                pk_vals = [x.fillerId for x in ldef.restrictions]
                if column_represents is None:
                    column_represents = [LogicalDefinitionElementRole.PREDICATE]
            if not pk_vals:
                raise ValueError(f"Invalid row_represents: {row_represents}")
            for pk_val in pk_vals:
                if pk_val not in row_ix:
                    row = defaultdict(list)
                    row_ix[pk_val] = row
                row = row_ix[pk_val]
                row[row_represents[0].value] = [pk_val]
                ok = False
                if LogicalDefinitionElementRole.GENUS in column_represents:
                    genus_ids = ldef.genusIds if ldef.genusIds else ["NO_GENUS"]
                    for x in genus_ids:
                        row[_col_name(x)].append(_cell_val(ldef))
                    ok = True
                if LogicalDefinitionElementRole.FILLER in column_represents:
                    fillers = [x.fillerId for x in ldef.restrictions]
                    if not fillers:
                        fillers = ["NO_FILLER"]
                    for x in fillers:
                        row[_col_name(x)].append(_cell_val(ldef))
                    ok = True
                if LogicalDefinitionElementRole.PREDICATE in column_represents:
                    preds = [x.propertyId for x in ldef.restrictions]
                    if not preds:
                        preds = ["NO_PREDICATE"]
                    for x in preds:
                        row[_col_name(x)].append(_cell_val(ldef))
                    ok = True
                if not ok:
                    raise ValueError(
                        f"Invalid column_represents: {column_represents} for row: {row_represents}"
                    )
        rows = list(row_ix.values())
    cols = set()
    for row in rows:
        cols.update(row.keys())
    for row in rows:
        for col in cols:
            if col not in row:
                row[col] = [""]
            if sort_values:
                row[col] = sorted(row[col])
    return rows
