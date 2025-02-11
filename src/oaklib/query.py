"""Representation and execution of complex boolean queries.

See also `<https://incatools.github.io/ontology-access-kit/howtos/use-oak-expression-language.html>`_.
"""

import itertools
import logging
import re
import secrets
import sys
from enum import Enum
from typing import IO, Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel

from oaklib import BasicOntologyInterface
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.vocabulary import (
    DEVELOPS_FROM,
    DISJOINT_WITH,
    ENABLED_BY,
    ENABLES,
    EQUIVALENT_CLASS,
    HAS_DIRECT_INPUT,
    HAS_INPUT,
    HAS_OUTPUT,
    HAS_PART,
    IS_A,
    NEGATIVELY_REGULATES,
    OCCURS_IN,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    PART_OF,
    POSITIVELY_REGULATES,
    RDF_TYPE,
    RDFS_DOMAIN,
    RDFS_RANGE,
    REGULATES,
    SUBPROPERTY_OF,
)
from oaklib.interfaces import (
    OboGraphInterface,
    SearchInterface,
    SubsetterInterface,
)
from oaklib.interfaces.obograph_interface import GraphTraversalMethod
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.subsets.slimmer_utils import filter_redundant

# A list whose members are either strings (search terms, curies, or directives)
# or nested lists.
# TODO: Replace this with an explicit query model with boolean operations
NESTED_LIST = Union[List[str], List["NESTED_LIST"]]

TERM = Union["Query", str, List[str]]


class OperatorEnum(str, Enum):
    """Boolean operators for queries."""

    AND = "and"
    OR = "or"
    NOT = "not"


class FunctionEnum(str, Enum):
    """Enumeration of types of functions for queries."""

    ANCESTOR = "anc"
    """Ancestor query."""

    DESCENDANT = "desc"
    SUBCLASS = "sub"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sib"
    MRCA = "mrca"
    NON_REDUNDANT = "nr"
    GAP_FILL = "gap_fill"
    QUERY = "query"


class Query(BaseModel):
    """
    Base class for query terms.

    Queries can be composed recursively via operator overloading.

    Example:

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import IS_A
        >>> adapter = get_adapter("sqlite:obo:cl")
        >>> neuron_q = descendant_of("CL:0000540", predicates=[IS_A])
        >>> forebrain_q = descendant_of("UBERON:0001890", predicates=[IS_A, PART_OF])
        >>> intersection_q = neuron_q & forebrain_q
        >>> for x in sorted(intersection_q.execute(adapter)):
        ...     print(x, adapter.label(x))
        <BLANKLINE>
        ...
        CL:1001502 mitral cell
        ...

    The above code is equivalent to:

        runoak -i sqlite:obo:cl info .sub CL:0000540 .and .desc//p=i,p UBERON:0001890
    """

    description: Optional[str] = None

    def __and__(self, other: "Query"):
        return BooleanQuery(operator="and", left=self, right=self._as_query_term(other))

    def __or__(self, other: "Query"):
        return BooleanQuery(operator="or", left=self, right=self._as_query_term(other))

    def __sub__(self, other: "Query"):
        return BooleanQuery(operator="not", left=self, right=self._as_query_term(other))

    def execute(self, adapter: BasicOntologyInterface, labels=False, **kwargs):
        """
        Execute the query on the given adapter.

         Example:

            >>> from oaklib import get_adapter
            >>> adapter = get_adapter("sqlite:obo:cl")
            >>> q = subclass_of("CL:0000540")
            >>> assert "CL:0000617" in q.execute(adapter)

        :param adapter:
        :param labels:
        :param kwargs:
        :return:
        """
        return onto_query(self, adapter, labels=labels)

    def _as_query_term(self, other: "Query") -> "Query":
        if isinstance(other, Query):
            return other
        if isinstance(other, str):
            return SimpleQueryTerm(term=other)
        raise ValueError(f"Cannot convert {other} to a QueryTerm")


class BooleanQuery(Query):
    operator: OperatorEnum
    left: Query
    right: Optional[Query] = None

    def as_list(self):
        """
        Convert the query to a list of tokens.

        :return:
        """
        if not self.right:
            return [f".{self.operator}"] + self.left.as_list()
        else:
            return self.left.as_list() + [f".{self.operator}"] + self.right.as_list()


class SimpleQueryTerm(Query):
    term: str

    def as_list(self):
        return [self.term]


class FunctionQuery(Query):
    """
    A query component that is a function call.
    """

    function: Optional[FunctionEnum] = None
    parameters: Optional[Dict[str, Any]] = None
    argument: Optional[Union[str, Query, List[str]]] = None

    def as_list(self):
        arg = self.argument
        if isinstance(arg, Query):
            arg = arg.as_list()
        if self.function:
            if self.parameters:

                def _flatten(v):
                    if isinstance(v, list):
                        return ",".join(v)
                    return v

                param_str = "//" + "//".join(
                    [f"{k}={_flatten(v)}" for k, v in self.parameters.items()]
                )
            else:
                param_str = ""
            return [f".{self.function}{param_str}"] + [arg]
        else:
            return [arg]


def subclass_of(term: TERM, description: Optional[str] = None) -> FunctionQuery:
    """
    Returns an entailed subClassOf query.

    Example:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> q = subclass_of("CL:0000540")
    >>> assert "CL:0000617" in q.execute(adapter)

    :param term:
    :param description:
    :return:
    """
    return FunctionQuery(function=FunctionEnum.SUBCLASS, argument=term, description=description)


def descendant_of(
    term: TERM, predicates: Optional[List[PRED_CURIE]] = None, description: Optional[str] = None
) -> FunctionQuery:
    """
    Returns a descendant query.

    Example:

    >>> from oaklib import get_adapter
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> q = descendant_of("CL:0000540", predicates=[IS_A])
    >>> assert "CL:0000617" in q.execute(adapter)

    :param term:
    :param predicates:
    :param description:
    :return:
    """
    return FunctionQuery(
        function=FunctionEnum.DESCENDANT,
        argument=term,
        description=description,
        parameters={"predicates": predicates},
    )


def ancestor_of(
    term: Union[str, Query],
    predicates: Optional[List[PRED_CURIE]] = None,
    description: Optional[str] = None,
) -> FunctionQuery:
    """
    Returns an ancestor query.

    Example:

    >>> from oaklib import get_adapter
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> q = ancestor_of("CL:0000540", predicates=[IS_A])
    >>> assert "CL:0000000" in q.execute(adapter)

    :param term:
    :param predicates:
    :param description:
    :return:
    """
    return FunctionQuery(
        function=FunctionEnum.ANCESTOR,
        argument=term,
        description=description,
        parameters={"predicates": predicates},
    )


def non_redundant(
    term: TERM, predicates: Optional[List[PRED_CURIE]] = None, description: Optional[str] = None
) -> FunctionQuery:
    """
    Returns a query that when executed will return the non-redundant subset of the input set.

    Example:

    >>> from oaklib import get_adapter
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> q = non_redundant(["interneuron", "neuron", "GABA-ergic synapse"], predicates=[IS_A])
    >>> q.execute(adapter, labels=True)
    [('CL:0000099', 'interneuron'), ('GO:0098982', 'GABA-ergic synapse')]

    :param term:
    :param predicates:
    :param description:
    :return:
    """
    return FunctionQuery(
        function=FunctionEnum.NON_REDUNDANT,
        argument=term,
        description=description,
        parameters={"predicates": predicates},
    )


def gap_fill(
    term: Union[str, Query],
    predicates: Optional[List[PRED_CURIE]] = None,
    description: Optional[str] = None,
) -> FunctionQuery:
    """
    Returns a query that when executed will fill in edges between nodes in the input set.

    Example:

    >>> from oaklib import get_adapter
    >>> from oaklib.datamodels.vocabulary import IS_A
    >>> adapter = get_adapter("sqlite:obo:cl")
    >>> q = gap_fill(["CL:0002145", "CL:0002169", "lung", "respiratory airway"], predicates=[IS_A, PART_OF])
    >>> rels = q.execute(adapter, labels=True)
    >>> for r in sorted(rels):
    ...     print(r)
    <BLANKLINE>
    ...
    (('CL:0002169', 'basal cell of olfactory epithelium'),
     ('BFO:0000050', 'part of'), ('UBERON:0001005', 'respiratory airway'))
    ...

    :param term:
    :param predicates:
    :param description:
    :return:
    """
    return FunctionQuery(
        function=FunctionEnum.GAP_FILL,
        argument=term,
        description=description,
        parameters={"predicates": predicates},
    )


def onto_query(
    query_terms: Union[Query, NESTED_LIST], adapter: BasicOntologyInterface, labels=False
) -> List[Union[CURIE, Tuple[CURIE, str]]]:
    """
    Turn list of tokens that represent a term query into a list of curies.

    Examples
    --------

    Simple atomic queries
    ~~~~~~~~~~~~~~~~~~~~~

    First connect to the cell ontology:

    >>> from oaklib import get_adapter
    >>> cl = get_adapter("sqlite:obo:cl")

    Simple query (using list-of-terms syntax):

    >>> onto_query(["neuron"], cl)
     ['CL:0000540']

    Equivalent query using QueryTerm classes:

    >>> onto_query(SimpleQueryTerm(term="neuron"), cl)
    ['CL:0000540']

    Equivalent using IDs not labels:

    >>> onto_query(["CL:0000540"], cl)
    ['CL:0000540']

    Getting back labels in results:

    >>> onto_query(["CL:0000540"], cl, labels=True)
    [('CL:0000540', 'neuron')]

    Graph queries
    ~~~~~~~~~~~~~

    Ancestor query (using list-of-terms syntax):

    >>> ancs = onto_query([".anc//p=i", "CL:0000540"], cl)
    >>> assert "CL:0000000" in ancs

    Equivalent using query objects:

    >>> q = FunctionQuery(function=FunctionEnum.ANCESTOR, parameters={"p": "i"}, argument="CL:0000540")
    >>> ancs2 = onto_query(q, cl)
    >>> assert set(ancs2) == set(ancs)

    Next we will create two separate queries for:

    - subclasses of interneuron (entailed)
    - neurons that are located in the eyeball

    We will then manually intersect these two sets,
    to find the neurons that are both interneurons and located in the eyeball.

    First the neuron query. We use the subclasses convenience predicate:

    >>> subq = FunctionQuery(
    ...               function=FunctionEnum.SUBCLASS,
    ...               argument="interneuron", description="Entailed subclasses of interneuron")
    >>> interneurons = onto_query(subq, cl)

    Next we will query for neurons located in the eyeball, using has-soma-location:

    >>> locq = FunctionQuery(function=FunctionEnum.DESCENDANT,
    ...                  parameters={"predicates": ["RO:0002100"]},
    ...                  argument="UBERON:0010230",
    ...                  description="soma location in eyeball")
    >>> eye_cells = onto_query(locq, cl)

    We can compare this with list syntax:

    >>> locq.as_list()
    ['.desc//predicates=RO:0002100', 'UBERON:0010230']

    Now doing the intersection in python:

    >>> both = set(eye_cells).intersection(set(interneurons))
    >>> for x in sorted(both):
    ...    print(x, cl.label(x))
    <BLANKLINE>
    ...
    CL:0004217 H1 horizontal cell
    ...


    Boolean queries
    ~~~~~~~~~~~~~~~

    Rather than doing the set intersection manually, we can use intersections in the query syntax. This
    has a number of examples - implementations can choose to implement this efficiently.

    >>> ixnq = subq & locq
    >>> ixnq.as_list()
    ['.sub', 'interneuron', '.and', '.desc//predicates=RO:0002100', 'UBERON:0010230']
    >>> both2 = onto_query(ixnq, cl)
    >>> for x in sorted(both2):
    ...    print(x, cl.label(x))
    <BLANKLINE>
    ...
    CL:0004217 H1 horizontal cell
    ...
    >>> assert set(both2) == both

    We can also add a MINUS operator

    >>> h1 = "CL:0004217"
    >>> ixnq2 = ixnq - h1
    >>> ixnq2.as_list()
    ['.sub', 'interneuron', '.and', '.desc//predicates=RO:0002100', 'UBERON:0010230', '.not', 'CL:0004217']
    >>> both3 = onto_query(ixnq2, cl)
    >>> assert h1 not in both3
    >>> assert set(both3) == set(both2) - {h1}

    Search queries
    ~~~~~~~~~~~~~~

    TODO - document search queries

    :param query_terms:
    :param adapter:
    :param labels:
    :return:
    """
    if isinstance(query_terms, Query):
        query_terms = query_terms.as_list()
    if not isinstance(query_terms, list):
        query_terms = [query_terms]
    results = list(query_terms_iterator(query_terms, adapter))
    if labels:
        if results:
            # results are either entities or edges
            if isinstance(results[0], str):
                results = list(adapter.labels(results))
            else:
                # get all distinct s, p, o in all results
                all_ids = set(
                    [r[0] for r in results] + [r[1] for r in results] + [r[2] for r in results]
                )
                labels = {r[0]: r[1] for r in adapter.labels(all_ids)}
                results = [
                    (
                        (r[0], labels.get(r[0], None)),
                        (r[1], labels.get(r[1], None)),
                        (r[2], labels.get(r[2], None)),
                    )
                    for r in results
                ]
    return results


def query_terms_iterator(
    query_terms: NESTED_LIST, adapter: BasicOntologyInterface
) -> Iterator[CURIE]:
    """
    Turn list of tokens that represent a term query into an iterator for curies.

    For examples, see test_cli

    :param query_terms:
    :param adapter:
    :return:
    """
    # TODO: reimplement using an explicit query model
    results: Iterable[CURIE] = iter([])
    predicates = None
    if isinstance(query_terms, tuple):
        query_terms = list(query_terms)

    def _parse_params(s: str) -> Dict:
        # some query terms are parameterized using the syntax
        # .<TOKEN>//<P1>=<V1>//<P2>=<V2>...
        d = {}
        m = re.match(r"\.\w+//(.+)", s)
        if m:
            for p in m.group(1).split("//"):
                if "=" not in p:
                    raise ValueError(f"All arguments must be of param=val form, got {p} in {s}")
                [k, v] = p.split("=")
                if k == "p":
                    k = "predicates"
                if k == "predicates":
                    v = process_predicates_arg(v)
                if k == "prefixes":
                    v = v.split(",")
                d[k] = v
        return d

    def chain_results(v):
        if isinstance(v, str):
            v = iter([v])
        nonlocal results
        results = itertools.chain(results, v)

    # queries can be nested using square brackets
    query_terms = nest_list_of_terms(query_terms)
    logging.debug(f"Query terms: {query_terms}")

    while len(query_terms) > 0:
        # process each query term. A query term is either:
        # 1. local, in which case is appends to the result iterator
        # 2. global, where it applies all subsequent terms
        term = query_terms[0]
        query_terms = query_terms[1:]
        if term == "-":
            # read from stdin
            chain_results(curies_from_file(sys.stdin))
        elif isinstance(term, list):
            chain_results(query_terms_iterator(term, adapter))
        elif term.startswith(".load="):
            # load a file of IDs
            fn = term.replace(".load=", "")
            with open(fn) as file:
                chain_results(curies_from_file(file))
        elif term.startswith(".idfile"):
            # load a file of IDs
            fn = query_terms.pop(0)
            logging.info(f"Reading ids from {fn}")
            file = open(fn)
            chain_results(curies_from_file(file))
        elif term.startswith(".termfile"):
            # load a file of queries
            fn = query_terms.pop(0)
            with open(fn) as file:
                lines = [line.strip() for line in file.readlines()]
                query_terms = lines + query_terms
        elif re.match(r"^([\w\-\.]+):(\S+)$", term):
            logging.debug(f"CURIE: {term}")
            if term.endswith(","):
                logging.info(f"Removing trailing comma from {term}")
                term = term[:-1]
            # CURIE
            chain_results(term)
        elif re.match(r"^http(\S+)$", term):
            logging.debug(f"URI: {term}")
            # URI
            chain_results(term)
        elif re.match(r"^\.predicates=(\S*)$", term):
            logging.debug(f"Predicates: {term}")
            logging.warning("Deprecated: pass as parameter instead")
            m = re.match(r"^\.predicates=(\S*)$", term)
            predicates = process_predicates_arg(m.group(1))
        elif term == ".and":
            logging.debug("AND")
            # boolean term: consume the result of the query and intersect
            rest = list(query_terms_iterator(query_terms, adapter))
            for x in results:
                if x in rest:
                    yield x
            query_terms = []
        elif term == ".xor":
            logging.debug("XOR")
            # boolean term: consume the result of the query and xor
            rest = list(query_terms_iterator(query_terms, adapter))
            remaining = []
            for x in results:
                if x not in rest:
                    yield x
                else:
                    remaining.append(x)
            for x in rest:
                if x not in remaining:
                    yield x
            query_terms = []
        elif term == ".not" or term == ".minus":
            logging.debug("Minus")
            # boolean term: consume the result of the query and subtract
            rest = list(query_terms_iterator(query_terms, adapter))
            for x in results:
                if x not in rest:
                    yield x
            query_terms = []
        elif term == ".or":
            logging.debug("OR")
            # or is implicit
            pass
        elif term.startswith(".all"):
            logging.debug("All")
            chain_results(adapter.entities(filter_obsoletes=False))
        elif term.startswith(".classes"):
            logging.debug("Classes")
            chain_results(adapter.entities(owl_type=OWL_CLASS))
        elif term.startswith(".relations"):
            logging.debug("Relations")
            chain_results(adapter.entities(owl_type=OWL_OBJECT_PROPERTY))
        elif term.startswith(".rand"):
            logging.debug(f"Random: {term}")
            params = _parse_params(term)
            sample_size = params.get("n", "100")
            entities = set(adapter.entities())
            sample = secrets.SystemRandom().sample(entities, int(sample_size))
            chain_results(sample)
        elif term.startswith(".sample"):
            logging.debug(f"Sampling: {term}")
            params = _parse_params(term)
            sample_size = params.get("n", "100")
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            try:
                sample = secrets.SystemRandom().sample(rest, int(sample_size))
            except ValueError as e:
                logging.error(f"Error sampling {sample_size} / {len(rest)}: {e}")
                raise e
            chain_results(sample)
        elif term == ".in":
            logging.debug(f"IN: {term}")
            # subset query
            subset = query_terms[0]
            query_terms = query_terms[1:]
            chain_results(adapter.subset_members(subset))
        elif term.startswith(".root"):
            logging.debug(f"Roots: {term}")
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            id_prefixes = params.get("prefix", [])
            annotated_roots = bool(params.get("annotated", False))
            roots = adapter.roots(
                predicates=this_predicates, id_prefixes=id_prefixes, annotated_roots=annotated_roots
            )
            chain_results(roots)
        elif term.startswith(".leaf"):
            logging.debug(f"Leafs: {term}")
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            leafs = adapter.leafs(predicates=this_predicates)
            chain_results(leafs)
        elif term.startswith(".is_obsolete"):
            logging.debug("Obsolete")
            chain_results(adapter.obsoletes())
        elif term.startswith(".non_obsolete"):
            logging.debug("Non-obsolete")
            chain_results(adapter.entities(filter_obsoletes=True))
        elif term.startswith(".dangling"):
            logging.debug("Dangling")
            chain_results(adapter.dangling())
        elif term.startswith(".filter"):
            logging.debug(f"Filter: {term}")
            # arbitrary python expression
            expr = query_terms[0]
            query_terms = query_terms[1:]
            chain_results(eval(expr, {"impl": adapter, "terms": results}))  # noqa
        elif term.startswith(".query"):
            logging.debug(f"Query: {term}")
            # arbitrary SPARQL or SQL query (implementation specific)
            params = _parse_params(term)
            prefixes = params.get("prefixes", None)
            query = query_terms[0]
            query_terms = query_terms[1:]
            chain_results([list(v.values())[0] for v in adapter.query(query, prefixes=prefixes)])
        elif term.startswith(".desc"):
            logging.debug(f"Descendants: {term}")
            # graph query: descendants
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if not isinstance(adapter, OboGraphInterface):
                raise NotImplementedError
            chain_results(adapter.descendants(rest, predicates=this_predicates))
        elif term.startswith(".sub"):
            logging.debug(f"Subclasses: {term}")
            # graph query: is-a descendants
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if not isinstance(adapter, OboGraphInterface):
                raise NotImplementedError
            chain_results(adapter.descendants(rest, predicates=[IS_A]))
        elif term.startswith(".child"):
            logging.debug(f"Children: {term}")
            # graph query: children
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            children = [
                s for s, _p, _o in adapter.relationships(objects=rest, predicates=this_predicates)
            ]
            chain_results(children)
        elif term.startswith(".parent"):
            logging.debug(f"Parents: {term}")
            # graph query: parents
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            parents = [
                o for _s, _p, o in adapter.relationships(subjects=rest, predicates=this_predicates)
            ]
            chain_results(parents)
        elif term.startswith(".sib"):
            logging.debug(f"Siblings: {term}")
            # graph query: siblings
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            parents = [
                o for _s, _p, o in adapter.relationships(subjects=rest, predicates=this_predicates)
            ]
            sibs = [
                s
                for s, _p, _o in adapter.relationships(objects=parents, predicates=this_predicates)
            ]
            chain_results(sibs)
        elif term.startswith(".anc"):
            logging.debug(f"Anc: {term}")
            # graph query: ancestors
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            this_method = params.get("method", None)
            if this_method is not None:
                this_method = GraphTraversalMethod(this_method)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if isinstance(adapter, OboGraphInterface):
                chain_results(
                    adapter.ancestors(rest, predicates=this_predicates, method=this_method)
                )
            else:
                raise NotImplementedError
        elif term.startswith(".numparent"):
            logging.debug(f"NumParents: {term}")
            # graph query: parents
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            this_max = params.get("max", None)
            if this_max is not None:
                this_max = int(this_max)
            this_min = int(params.get("min", 0))
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            matches = []
            counts = {x: 0 for x in rest}
            for s, _, _o in adapter.relationships(subjects=rest, predicates=this_predicates):
                counts[s] += 1
            for s, num in counts.items():
                if this_max is not None and num > this_max:
                    continue
                if num >= this_min:
                    matches.append(s)
            chain_results(matches)
        elif term.startswith(".numchild"):
            logging.debug(f"NumChildren: {term}")
            # graph query: parents
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            this_max = params.get("max", None)
            if this_max is not None:
                this_max = int(this_max)
            this_min = int(params.get("min", 0))
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            matches = []
            counts = {x: 0 for x in rest}
            for _s, _, o in adapter.relationships(objects=rest, predicates=this_predicates):
                counts[o] += 1
            for o, num in counts.items():
                if this_max is not None and num > this_max:
                    continue
                if num >= this_min:
                    matches.append(o)
            chain_results(matches)
        elif term.startswith(".intermediates"):
            logging.debug(f"Intermediates: {term}")
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if not isinstance(adapter, SubsetterInterface):
                raise NotImplementedError
            gap_filled_nodes = set(rest)
            for s, _p, o in adapter.gap_fill_relationships(rest, predicates=this_predicates):
                gap_filled_nodes.add(s)
                gap_filled_nodes.add(o)
            if yaml.safe_load(params.get("reflexive", "false")):
                chain_results(rest)
            chain_results(gap_filled_nodes)
        elif term.startswith(".multimrca"):
            logging.debug(f"Multi-MRCA: {term}")
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if not isinstance(adapter, SemanticSimilarityInterface):
                raise NotImplementedError
            chain_results(
                {
                    ca
                    for _s, _o, ca in adapter.multiset_most_recent_common_ancestors(
                        rest, predicates=this_predicates
                    )
                }
            )
            if yaml.safe_load(params.get("reflexive", "false")):
                chain_results(rest)
        elif term.startswith(".mrca"):
            logging.debug(f"MRCA: {term}")
            # graph query: most recent common ancestors
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if not isinstance(adapter, SemanticSimilarityInterface):
                raise NotImplementedError
            chain_results(
                adapter.setwise_most_recent_common_ancestors(rest, predicates=this_predicates)
            )
            if yaml.safe_load(params.get("reflexive", "false")):
                chain_results(rest)
        elif term.startswith(".nr"):
            logging.debug(f"Non-redundant: {term}")
            # graph query: non-redundant
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            chain_results(filter_redundant(adapter, rest, this_predicates))
        elif term.startswith(".gap_fill"):
            logging.debug(f"Gap fill: {term}")
            if not isinstance(adapter, SubsetterInterface):
                raise NotImplementedError
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            chain_results(adapter.gap_fill_relationships(rest, predicates=this_predicates))
        elif term.startswith(".where"):
            logging.debug(f"Where: {term}")
            # graph query: descendants
            params = _parse_params(term)
            raise ValueError("`.where` is not implemented yet")
        else:
            logging.debug(f"Atomic term: {term}")
            # term is not query syntax: feed directly to search
            if not isinstance(adapter, SearchInterface):
                raise NotImplementedError(f"Search not implemented for {type(adapter)}")
            if term.endswith(","):
                logging.info(f"Removing trailing comma from {term}")
                term = term[:-1]
            cfg = create_search_configuration(term)
            logging.info(f"Search config: {term} => {cfg}")
            chain_results(adapter.basic_search(cfg.search_terms[0], config=cfg))
    yield from results


def curies_from_file(
    file: IO, adapter: Optional[BasicOntologyInterface] = None, allow_labels=False, strict=False
) -> Iterator[CURIE]:
    """
    yield an iterator over CURIEs by parsing a file.

    The file can contain any content, so long as each line
    starts with a CURIE followed by whitespace -- the remainder of the line
    is ignored

    :param file:
    :param adapter: if provided, will be used to resolve CURIEs
    :param allow_labels: if true, will allow inputs to be labels
    :param strict: if true, will raise an error if a CURIE cannot be resolved
    :return:
    """
    line_no = 0
    if allow_labels and not adapter:
        raise ValueError("Must provide an adapter to resolve labels")
    for line in file.readlines():
        line = line.strip()
        if not line:
            continue
        line_no += 1
        if ":" in line or not allow_labels:
            m = re.match(r"^(\S+)", line)
            curie = m.group(1)
            if curie == "id" and line_no == 1:
                continue
            yield curie
        elif allow_labels:
            candidates = adapter.curies_by_label(line.strip())
            if strict and len(candidates) != 1:
                raise ValueError(
                    f"Could not resolve label {line} to a single CURIE, got {candidates}"
                )
            yield from candidates


def nest_list_of_terms(terms: List[str]) -> NESTED_LIST:
    """
    Gives a list of terms (typically passed on command line),
    replace blocks between '[', ..., ']' with nested lists of the contents

    :param terms:
    :return:
    """
    nested, rest = _nest_list_of_terms(terms)
    if rest:
        raise ValueError(f"Unparsed: {rest}")
    return nested


def _nest_list_of_terms(terms: List[str]) -> Tuple[NESTED_LIST, List[str]]:
    nested = []
    while len(terms) > 0:
        term = terms[0]
        terms = terms[1:]
        if term == "[":
            nxt, rest = _nest_list_of_terms(terms)
            terms = rest
            nested.append(nxt)
        elif term == "]":
            return nested, terms
        else:
            nested.append(term)
    return nested, []


def process_predicates_arg(
    predicates_str: str,
    expected_number: Optional[int] = None,
    exclude_predicates_str: Optional[str] = None,
    impl: Optional[BasicOntologyInterface] = None,
) -> Optional[List[PRED_CURIE]]:
    """
    Process a string of predicates into a list of PRED_CURIEs.

    Example:

        >>> process_predicates_arg("FOO:123")
        ['FOO:123']

        >>> process_predicates_arg("i")
        ['rdfs:subClassOf']

        >>> process_predicates_arg("i,p")
        ['rdfs:subClassOf', 'BFO:0000050']

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:ro")
        >>> process_predicates_arg("i,part of", impl=adapter)
        ['rdfs:subClassOf', 'BFO:0000050']

    Include entailed subproperties:

        >>> for p in sorted(process_predicates_arg("sub(i, connected to)", impl=adapter)):
        ...     print(p, adapter.label(p))
        <BLANKLINE>
        ...
        RO:0002103 synapsed by
        ...
        rdfs:subClassOf None


    :param predicates_str:
    :param expected_number:
    :param exclude_predicates_str:
    :param impl:
    :return:
    """
    if predicates_str is None and exclude_predicates_str is None:
        return None
    if predicates_str.startswith("sub("):
        if not isinstance(impl, OboGraphInterface):
            raise ValueError("Must provide an BasicOntologyInterface to use sub()")

        # sub(FOO:123) => FOO:123
        preds = process_predicates_arg(
            predicates_str[4:-1],
            expected_number=expected_number,
            exclude_predicates_str=exclude_predicates_str,
            impl=impl,
        )
        preds_expanded = set(preds)
        # note that RG doesn't pre-computed relation closure;
        # use HOP method
        for desc_p in impl.descendants(
            preds,
            predicates=[SUBPROPERTY_OF],
            method=GraphTraversalMethod.HOP,
            reflexive=True,
        ):
            preds_expanded.add(desc_p)
        return list(preds_expanded)

    if predicates_str is None:
        inputs = []
    elif "," in predicates_str:
        inputs = predicates_str.split(",")
    else:
        inputs = predicates_str.split("+")
    inputs = [i.strip() for i in inputs]
    preds = []
    for p in inputs:
        next_preds = _shorthand_to_pred_curie(p)
        if isinstance(next_preds, list):
            preds.extend(next_preds)
        else:
            preds.append(next_preds)

    def _expand(p: str):
        if ":" in p:
            return p
        if impl is None:
            return p
        p_ids = impl.curies_by_label(p)
        if len(p_ids) > 1:
            raise ValueError(f"Ambiguous: {p} => {p_ids}")
        if p_ids:
            return p_ids[0]
        return p

    preds = [_expand(p) for p in preds]
    if exclude_predicates_str:
        if "," in exclude_predicates_str:
            exclude_inputs = exclude_predicates_str.split(",")
        else:
            exclude_inputs = exclude_predicates_str.split("+")
        exclude_preds = [_shorthand_to_pred_curie(p) for p in exclude_inputs]
        if not preds:
            if not impl or not isinstance(impl, BasicOntologyInterface):
                raise ValueError("Must provide an BasicOntologyInterface to exclude predicates")
            preds = list(impl.entities(owl_type=OWL_OBJECT_PROPERTY))
        preds = [p for p in preds if p not in exclude_preds]
        logging.info(f"Excluding predicates: {exclude_preds} yields: {preds}")
    if expected_number and len(preds) != expected_number:
        raise ValueError(f"Expected {expected_number} parses of {predicates_str}, got: {preds}")
    return preds


def _shorthand_to_pred_curie(shorthand: str) -> Union[PRED_CURIE, List[PRED_CURIE]]:
    # TODO: replace with a transparent lookup table
    if shorthand == "i":
        return IS_A
    elif shorthand == "p":
        return PART_OF
    elif shorthand == "h":
        return HAS_PART
    elif shorthand == "o":
        return OCCURS_IN
    elif shorthand == "d":
        return DEVELOPS_FROM
    elif shorthand == "en":
        return [ENABLES, ENABLED_BY]
    elif shorthand == "io":
        return [HAS_INPUT, HAS_OUTPUT, HAS_DIRECT_INPUT]
    elif shorthand == "r":
        return [REGULATES, NEGATIVELY_REGULATES, POSITIVELY_REGULATES]
    elif shorthand == "t":
        return RDF_TYPE
    elif shorthand == "e":
        return EQUIVALENT_CLASS
    elif shorthand == "owl":
        return [IS_A, RDF_TYPE, EQUIVALENT_CLASS, DISJOINT_WITH, RDFS_DOMAIN, RDFS_RANGE]
    else:
        return shorthand
