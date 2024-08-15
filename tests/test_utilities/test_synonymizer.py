import pytest
from kgcl_schema.grammar.render_operations import render

from oaklib import get_adapter
from oaklib.datamodels.synonymizer_datamodel import RuleSet, Synonymizer
from oaklib.utilities.lexical.synonymizer import apply_synonymizer, apply_synonymizer_to_terms
from tests import CYTOPLASM, INPUT_DIR, NUCLEAR_MEMBRANE, NUCLEUS

TEST_SIMPLE_ONT = INPUT_DIR / "go-nucleus-simple.obo"


@pytest.mark.parametrize(
    "rule,input,expected",
    [
        (
            {"match": "world", "replacement": "universe"},
            "hello world",
            [(True, "hello universe", None)],
        ),
        (
            {"match": "world", "replacement": "universe", "qualifier": "broad"},
            "hello world",
            [(True, "hello universe", "broad")],
        ),
        (
            {"match": "world", "replacement": "universe"},
            "hello universe",
            [(False, "hello universe", None)],
        ),
        (
            {"match": r"hello (\w+)", "replacement": r"\1, hello"},
            "hello world",
            [(True, "world, hello", None)],
        ),
        ({"match": r"\bfoo\b", "replacement": "bar"}, "foo baz", [(True, "bar baz", None)]),
        ({"match": r"\bfoo\b", "replacement": "bar"}, "foo-baz", [(True, "bar-baz", None)]),
        ({"match": r"\bfoo\b", "replacement": "bar"}, "<foo-baz>", [(True, "<bar-baz>", None)]),
        ({"match": r"\bfoo\b", "replacement": "bar"}, "baz foo", [(True, "baz bar", None)]),
        ({"match": r"\bfoo\b", "replacement": "bar"}, "food baz", [(False, "food baz", None)]),
    ],
)
def test_synonymizer(rule, input, expected):
    s = Synonymizer(**rule)
    results = list(apply_synonymizer(input, [s]))
    assert results == expected


@pytest.mark.parametrize(
    "ruleset,include_all,terms,expected",
    [
        (
            Synonymizer(match=r"nuclear (\w+)", replacement=r"\1 of nucleus"),
            False,
            [NUCLEUS, NUCLEAR_MEMBRANE],
            ["create exact synonym 'membrane of nucleus' for GO:0031965"],
        ),
        (
            Synonymizer(match=r"nuclear (\w+)", replacement=r"\1 of nucleus", match_scope="label"),
            False,
            [NUCLEUS, NUCLEAR_MEMBRANE],
            ["create exact synonym 'membrane of nucleus' for GO:0031965"],
        ),
        (
            Synonymizer(match=r"nuclear (\w+)", replacement=r"\1 of nucleus", match_scope="exact"),
            False,
            [NUCLEUS, NUCLEAR_MEMBRANE],
            [],
        ),
        (
            Synonymizer(
                match=r"nucleus",
                replacement="NUCLEUS",
                match_scope="definition",
                qualifier="definition",
            ),
            True,
            [CYTOPLASM],
            [
                (
                    "change definition of GO:0005737 from 'All of the contents of a cell excluding "
                    "the plasma membrane and nucleus, but including other subcellular structures.' "
                    "to 'All of the contents of a cell excluding the plasma membrane and "
                    "NUCLEUS, but including other subcellular structures.'"
                )
            ],
        ),
        (
            Synonymizer(
                match=r"All of the contents",
                replacement="XYZ",
                in_place=True,
            ),
            True,
            [CYTOPLASM],
            [
                (
                    "change definition of GO:0005737 from 'All of the contents of a cell excluding "
                    "the plasma membrane and nucleus, but including other subcellular structures.' "
                    "to 'XYZ of a cell excluding the plasma membrane and "
                    "nucleus, but including other subcellular structures.'"
                )
            ],
        ),
    ],
)
def test_syonymizer_on_terms(ruleset, include_all, terms, expected):
    # adapter = get_adapter(f"simpleobo:{TEST_SIMPLE_ONT}")
    adapter = get_adapter(f"{TEST_SIMPLE_ONT}")
    if isinstance(ruleset, Synonymizer):
        ruleset = RuleSet(rules=[ruleset])
    changes = list(apply_synonymizer_to_terms(adapter, terms, ruleset, include_all=include_all))
    changes_strs = []
    for change in changes:
        change_str = render(change)
        print(change_str)
        changes_strs.append(change_str)

    assert set(changes_strs) == set(expected)
