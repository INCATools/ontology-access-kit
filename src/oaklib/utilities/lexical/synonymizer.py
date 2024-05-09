import re
from typing import Iterable, Iterator, List, Optional, Tuple

from kgcl_schema.datamodel import kgcl
from pronto import Definition

from oaklib.datamodels.synonymizer_datamodel import RuleSet, Synonymizer
from oaklib.datamodels.vocabulary import (
    EXTENDED_SCOPE_TO_SYNONYM_PRED_MAP,
)
from oaklib.interfaces import BasicOntologyInterface
from oaklib.types import CURIE


def apply_synonymizer(
    term: str, rules: List[Synonymizer], scope_predicate: Optional[CURIE] = None
) -> Iterator[Tuple[bool, str, str]]:
    """
    Apply synonymizer rules declared in the given match-rules.yaml file.

    The basic concept is looking for regex in labels and replacing the ones that match
    with the string passed in 'match.replacement'. Also set qualifier ('match.qualifier')
    as to whether the replacement is an 'exact', 'broad', 'narrow', or 'related' synonym.

    Note: This function yields all intermediate results (for each rule applied)
    as opposed to a final result. The reason being we only want to return a "True"
    synonymized result. If the term is not synonymized, then the result will be just
    the term and a default qualifier. In the case of multiple synonyms, the actual result
    will be the latest synonymized result.In other words, all the rules have been
    implemented on the term to finally produce the result.

    :param term: Original label.
    :param rules: Synonymizer rules from match-rules.yaml file.
    :yield: A Tuple stating [if the label changed, new label, qualifier]
    """
    for rule in rules:
        if not scope_matches(rule, scope_predicate):
            continue
        tmp_term_2 = term
        term = re.sub(rule.match, rule.replacement, term)

        if tmp_term_2 != term:
            yield True, term.strip(), rule.qualifier
        else:
            yield False, term.strip(), rule.qualifier


def apply_synonymizer_to_terms(
    adapter: BasicOntologyInterface,
    terms: Iterable[CURIE],
    ruleset: RuleSet,
    include_all=False,
) -> Iterator[kgcl.NewSynonym]:
    """
    Apply synonymizer rules to a list of terms.

    Note synonymizer despite its name is not just for synonyms. It can be used to
    replace definitions, labels, ...

    :param adapter:
    :param terms:
    :param ruleset:
    :param include_all:
    :return:
    """
    pred_to_qual = {v: k for k, v in EXTENDED_SCOPE_TO_SYNONYM_PRED_MAP.items()}
    n = 0
    for curie in terms:
        tvs = list(adapter.entity_alias_map(curie).items())
        if include_all:
            defn = adapter.definition(curie)
            if defn:
                if isinstance(defn, Definition):
                    defn = str(defn)
                tvs.append(("definition", [defn]))
        for scope_pred, aliases in tvs:
            if aliases is not None:
                for alias in aliases:
                    if alias:
                        for rule in ruleset.rules:
                            for replaced, new_alias, qualifier in apply_synonymizer(
                                alias, [rule], scope_pred
                            ):
                                if replaced:
                                    if qualifier is None or qualifier == "":
                                        if rule.in_place or scope_pred == "definition":
                                            # preserves the original synonym type
                                            qualifier = pred_to_qual.get(
                                                scope_pred, scope_pred
                                            ).lower()
                                        else:
                                            qualifier = "exact"
                                    n += 1
                                    change_id = f"kgcl_change_id_{n}"
                                    if qualifier == "label":
                                        change = kgcl.NodeRename(
                                            id=change_id,
                                            about_node=curie,
                                            old_value=alias,
                                            new_value=new_alias,
                                        )
                                    elif qualifier == "definition":
                                        change = kgcl.NodeTextDefinitionChange(
                                            id=change_id,
                                            about_node=curie,
                                            old_value=alias,
                                            new_value=new_alias,
                                        )
                                    else:
                                        if rule.in_place:
                                            change = kgcl.SynonymReplacement(
                                                id=change_id,
                                                about_node=curie,
                                                old_value=alias,
                                                new_value=new_alias,
                                            )
                                        else:
                                            change = kgcl.NewSynonym(
                                                id=change_id,
                                                about_node=curie,
                                                old_value=alias,
                                                new_value=new_alias,
                                                qualifier=qualifier,
                                            )
                                    yield change


def scope_matches(rule: Synonymizer, scope_predicate: Optional[CURIE]) -> bool:
    """
    Check if the rule scope matches the scope_predicate.

    >>> scope_matches(Synonymizer(match_scope="EXACT"), "oio:hasExactSynonym")
    True
    >>> scope_matches(Synonymizer(match_scope="EXACT"), "oio:hasRelatedSynonym")
    False
    >>> scope_matches(Synonymizer(match_scope="*"), "oio:hasRelatedSynonym")
    True
    >>> scope_matches(Synonymizer(), "oio:hasExactSynonym")
    True

    :param rule: Synonymizer rule.
    :param scope_predicate: Scope predicate.
    :return: True if the rule scope matches the scope_predicate.
    """
    if scope_predicate is None:
        return True
    if rule.match_scope is None:
        return True
    if rule.match_scope == "*" or rule.match_scope == "":
        return True
    rule_match_scope = rule.match_scope.upper()
    if rule_match_scope == scope_predicate.upper():
        return True
    if rule_match_scope in EXTENDED_SCOPE_TO_SYNONYM_PRED_MAP:
        rule_match_scope_predicate = EXTENDED_SCOPE_TO_SYNONYM_PRED_MAP[rule_match_scope]
        if rule_match_scope_predicate == scope_predicate:
            return True
    return False
