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
        return f'SELECT {self.select_str()} WHERE {{ {w} }}'