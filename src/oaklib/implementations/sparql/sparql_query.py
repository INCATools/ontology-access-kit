from dataclasses import dataclass
from typing import List, Optional

from oaklib.types import URI

VAR_NAME = str
WHERE_CLAUSE = str


@dataclass
class SparqlQuery:
    """
    Represents a SPARQL query
    """
    distinct: bool = None
    select: List[VAR_NAME] = None
    graph: Optional[URI] = None
    where: List[WHERE_CLAUSE] = None
    limit: int = None

    def add_not_in(self, subquery: "SparqlQuery"):
        self.where.append(f'FILTER NOT EXISTS {{ {subquery.where_str()} }}')

    def add_filter(self, cond: str):
        self.where.append(f'FILTER ( {cond} )')

    def add_values(self, var: str, vals: List[str]):
        self.where.append(f'VALUES ?{var} {{ {" ".join(vals)} }}')

    def select_str(self):
        distinct = 'DISTINCT ' if self.distinct else ''
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
            w = f'GRAPH <{self.graph}> {{ {w} }}'
        q = f'SELECT {self.select_str()} WHERE {{ {w} }}'
        if self.limit is not None:
            q += f' LIMIT {self.limit}'
        return q