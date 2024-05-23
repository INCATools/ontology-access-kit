import itertools
import logging
import re
import secrets
import sys
from typing import Iterator, Iterable, Dict, IO, Optional, List, Tuple, Union

from oaklib import BasicOntologyInterface
from oaklib.datamodels.search import create_search_configuration
from oaklib.datamodels.vocabulary import OWL_CLASS, OWL_OBJECT_PROPERTY, IS_A, PART_OF, DEVELOPS_FROM, RDF_TYPE, \
    EQUIVALENT_CLASS
from oaklib.interfaces import OboGraphInterface, SearchInterface, OntologyInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.subsets.slimmer_utils import filter_redundant

# A list whose members are either strings (search terms, curies, or directives)
# or nested lists.
# TODO: Replace this with an explicit query model with boolean operations
NESTED_LIST = Union[List[str], List["NESTED_LIST"]]

def onto_query(query_terms: NESTED_LIST, adapter: BasicOntologyInterface) -> List[CURIE]:
    """
    Turn list of tokens that represent a term query into a list of curies.

    :param query_terms:
    :param adapter:
    :return:
    """
    return list(query_terms_iterator(query_terms, adapter))


def query_terms_iterator(query_terms: NESTED_LIST, adapter: BasicOntologyInterface) -> Iterator[CURIE]:
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
                    v = _process_predicates_arg(v)
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
            # CURIE
            chain_results(term)
        elif re.match(r"^http(\S+)$", term):
            # URI
            chain_results(term)
        elif re.match(r"^\.predicates=(\S*)$", term):
            logging.warning("Deprecated: pass as parameter instead")
            m = re.match(r"^\.predicates=(\S*)$", term)
            predicates = _process_predicates_arg(m.group(1))
        elif term == ".and":
            # boolean term: consume the result of the query and intersect
            rest = list(query_terms_iterator(query_terms, adapter))
            for x in results:
                if x in rest:
                    yield x
            query_terms = []
        elif term == ".xor":
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
            # boolean term: consume the result of the query and subtract
            rest = list(query_terms_iterator(query_terms, adapter))
            for x in results:
                if x not in rest:
                    yield x
            query_terms = []
        elif term == ".or":
            # or is implicit
            pass
        elif term.startswith(".all"):
            chain_results(adapter.entities(filter_obsoletes=False))
        elif term.startswith(".classes"):
            chain_results(adapter.entities(owl_type=OWL_CLASS))
        elif term.startswith(".relations"):
            chain_results(adapter.entities(owl_type=OWL_OBJECT_PROPERTY))
        elif term.startswith(".rand"):
            params = _parse_params(term)
            sample_size = params.get("n", "100")
            entities = list(adapter.entities())
            sample = [
                entities[secrets.randbelow(len(entities))] for x in range(1, int(sample_size))
            ]
            chain_results(sample)
        elif term.startswith(".in"):
            # subset query
            subset = query_terms[0]
            query_terms = query_terms[1:]
            chain_results(adapter.subset_members(subset))
        elif term.startswith(".is_obsolete"):
            chain_results(adapter.obsoletes())
        elif term.startswith(".non_obsolete"):
            chain_results(adapter.entities(filter_obsoletes=True))
        elif term.startswith(".dangling"):
            chain_results(adapter.dangling())
        elif term.startswith(".filter"):
            # arbitrary python expression
            expr = query_terms[0]
            query_terms = query_terms[1:]
            chain_results(eval(expr, {"impl": adapter, "terms": results}))  # noqa
        elif term.startswith(".query"):
            # arbitrary SPARQL query
            params = _parse_params(term)
            prefixes = params.get("prefixes", None)
            query = query_terms[0]
            query_terms = query_terms[1:]
            chain_results([list(v.values())[0] for v in adapter.query(query, prefixes=prefixes)])
        elif term.startswith(".desc"):
            # graph query: descendants
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if isinstance(adapter, OboGraphInterface):
                chain_results(adapter.descendants(rest, predicates=this_predicates))
            else:
                raise NotImplementedError
        elif term.startswith(".sub"):
            # graph query: is-a descendants
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if isinstance(adapter, OboGraphInterface):
                chain_results(adapter.descendants(rest, predicates=[IS_A]))
            else:
                raise NotImplementedError
        elif term.startswith(".child"):
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
            # graph query: siblings
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            parents = [
                o for _s, _p, o in adapter.relationships(subjects=rest, predicates=this_predicates)
            ]
            sibs = [
                s for s, _p, _o in adapter.relationships(objects=parents, predicates=this_predicates)
            ]
            chain_results(sibs)
        elif term.startswith(".anc"):
            # graph query: ancestors
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if isinstance(adapter, OboGraphInterface):
                chain_results(adapter.ancestors(rest, predicates=this_predicates))
            else:
                raise NotImplementedError
        elif term.startswith(".mrca"):
            # graph query: most recent common ancestors
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            if isinstance(adapter, SemanticSimilarityInterface):
                chain_results(
                    adapter.setwise_most_recent_common_ancestors(rest, predicates=this_predicates)
                )
            else:
                raise NotImplementedError
        elif term.startswith(".nr"):
            # graph query: non-redundant
            params = _parse_params(term)
            this_predicates = params.get("predicates", predicates)
            rest = list(query_terms_iterator([query_terms[0]], adapter))
            query_terms = query_terms[1:]
            chain_results(filter_redundant(adapter, rest, this_predicates))
        else:
            # term is not query syntax: feed directly to search
            if not isinstance(adapter, SearchInterface):
                raise NotImplementedError(f"Search not implemented for {type(adapter)}")
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


def _process_predicates_arg(
    predicates_str: str,
    expected_number: Optional[int] = None,
    exclude_predicates_str: Optional[str] = None,
    impl: Optional[OntologyInterface] = None,
) -> Optional[List[PRED_CURIE]]:
    if predicates_str is None and exclude_predicates_str is None:
        return None
    if predicates_str is None:
        inputs = []
    elif "," in predicates_str:
        inputs = predicates_str.split(",")
    else:
        inputs = predicates_str.split("+")
    preds = [_shorthand_to_pred_curie(p) for p in inputs]
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


def _shorthand_to_pred_curie(shorthand: str) -> PRED_CURIE:
    if shorthand == "i":
        return IS_A
    elif shorthand == "p":
        return PART_OF
    elif shorthand == "d":
        return DEVELOPS_FROM
    elif shorthand == "t":
        return RDF_TYPE
    elif shorthand == "e":
        return EQUIVALENT_CLASS
    else:
        return shorthand
