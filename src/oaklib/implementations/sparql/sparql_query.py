from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Union

from oaklib.types import URI

VAR_NAME = str
WHERE_CLAUSE = str
DELETE_CLAUSE = str
INSERTCLAUSE = str


@dataclass
class SparqlQuery:
    """
    Represents a SPARQL query
    """

    distinct: bool = None
    select: List[VAR_NAME] = None
    graph: Optional[Union[URI, List[URI]]] = None
    where: List[WHERE_CLAUSE] = None
    limit: int = None

    def add_not_in(self, subquery: "SparqlQuery"):
        self.where.append(f"FILTER NOT EXISTS {{ {subquery.where_str()} }}")

    def add_filter(self, cond: str):
        self.where.append(f"FILTER ( {cond} )")

    def add_values(self, var: str, vals: Optional[List[str]]):
        if vals is not None:
            self.where.append(f'VALUES ?{var} {{ {" ".join(vals)} }}')

    def select_str(self):
        distinct = "DISTINCT " if self.distinct else ""
        return f'{distinct}{" ".join(self.select)} '

    def where_str(self):
        return ". ".join([w for w in self.where if w])

    def query_str(self):
        """
        Generate the SPARQL query string
        :return:
        """
        w = self.where_str()
        if self.graph:
            if isinstance(self.graph, list):
                # clone to avoid mutation
                q = deepcopy(self)
                q.add_values("g", [f"<{g}>" for g in self.graph])
                w = q.where_str()
                w = f"GRAPH ?g {{ {w} }}"
            else:
                w = f"GRAPH <{self.graph}> {{ {w} }}"
        q = f"SELECT {self.select_str()} WHERE {{ {w} }}"
        if self.limit is not None:
            q += f" LIMIT {self.limit}"
        return q


@dataclass
class SparqlUpdate(SparqlQuery):
    insert: List[WHERE_CLAUSE] = None
    delete: List[WHERE_CLAUSE] = None

    def insert_str(self):
        return ". ".join([w for w in self.insert if w])

    def delete_str(self):
        return ". ".join([w for w in self.delete if w])

    def query_str(self):
        """
        Generate the SPARQL update string
        :return:
        """

        q = f"""
        DELETE {{ {self.delete_str()} }}
        INSERT {{ {self.insert_str()} }}
        WHERE {{ {self.where_str()} }}
        """
        if self.graph:
            q = f"WITH <{self.graph}> {q}"
        return q
