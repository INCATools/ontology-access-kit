from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from oaklib.datamodels.obograph import (
    ExistentialRestrictionExpression,
    LogicalDefinitionAxiom,
)
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.obograph_utils import depth_first_ordering


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


def sort_entities(
    adapter: OboGraphInterface,
    entities: List[CURIE],
    traversal_order_predicates: Optional[List[PRED_CURIE]] = None,
) -> List[CURIE]:
    graph = adapter.ancestor_graph(entities, predicates=traversal_order_predicates)
    sorted_entities = [x for x in depth_first_ordering(graph) if x in entities]
    return sorted_entities + [x for x in entities if x not in sorted_entities]


def logical_definitions_to_matrix(
    adapter: OboGraphInterface,
    ldefs: List[LogicalDefinitionAxiom],
    config: Config = None,
    traversal_order_predicates: Optional[List[PRED_CURIE]] = None,
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

    curie_to_col_name = {}

    def _col_name(curie: CURIE) -> str:
        lbl = adapter.label(curie)
        if lbl:
            cn = lbl.replace(" ", "_")
        else:
            cn = curie
        curie_to_col_name[curie] = cn
        return cn

    if not row_represents:
        row_represents = [LogicalDefinitionElementRole.DEFINED_CLASS]

    pk = None
    if LogicalDefinitionElementRole.DEFINED_CLASS in row_represents:
        if len(row_represents) > 1:
            raise ValueError(
                f"Cannot have more than one row_representing for defined_class: {row_represents}"
            )
        for ldef in ldefs:
            row = defaultdict(list)
            pk = "defined_class"
            row[pk] = [ldef.definedClassId]
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
                pk = row_represents[0].value
                row[pk] = [pk_val]
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
    cols = []
    for row in rows:
        for k in row.keys():
            if k not in cols:
                cols.append(k)
    for row in rows:
        for col in cols:
            if col not in row:
                row[col] = [""]
            if sort_values:
                row[col] = sorted(row[col])
    if traversal_order_predicates is None:
        traversal_order_predicates = [IS_A]
    if traversal_order_predicates:
        sorted_row_ids = sort_entities(
            adapter, [row[pk][0] for row in rows], traversal_order_predicates
        )
        rows = sorted(rows, key=lambda row: sorted_row_ids.index(row[pk][0]))
        sorted_col_ids = sort_entities(
            adapter, list(curie_to_col_name.keys()), traversal_order_predicates
        )
        fixed_cols = [col for col in cols if col not in curie_to_col_name.values()]
        ordered_cols = fixed_cols + [curie_to_col_name[col] for col in sorted_col_ids]
        rows = [{col: row[col] for col in ordered_cols} for row in rows]
    return rows
