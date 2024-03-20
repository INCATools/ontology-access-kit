import pytest
from oaklib import BasicOntologyInterface, get_adapter
from oaklib.implementations.tabular.robot_template_implementation import template_slice
from oaklib.interfaces.dumper_interface import DumperInterface

from tests import INPUT_DIR, OUTPUT_DIR

TEMPLATES = INPUT_DIR / "obi-templates"
SAVED_TEMPLATES = OUTPUT_DIR / "obi-templates-modified"

BRAIN_SPECIMEN = "OBI:0002516"
LOW_GRADE_OVARIAN_TUMOR = "OBI:0002217"
NASAL_ASPIRATE_SPECIMEN = "OBI:0002780"


@pytest.fixture
def adapter() -> BasicOntologyInterface:
    """
    Get adapter fixture
    """
    return get_adapter(f"robottemplate:{TEMPLATES}")


def test_basic_ontology_adapter(adapter):
    """
    Test entities
    """
    entities = list(adapter.entities())
    assert BRAIN_SPECIMEN in entities
    assert LOW_GRADE_OVARIAN_TUMOR in entities
    m = {}
    for e, lbl in adapter.labels(entities):
        # print(e, lbl)
        m[e] = lbl
    assert m[BRAIN_SPECIMEN] == "brain specimen"
    assert m[LOW_GRADE_OVARIAN_TUMOR] == "Low grade ovarian tumor"
    assert adapter.label(BRAIN_SPECIMEN) == "brain specimen"
    assert adapter.label(LOW_GRADE_OVARIAN_TUMOR) == "Low grade ovarian tumor"
    assert adapter.curies_by_label("brain specimen") == [BRAIN_SPECIMEN]
    assert adapter.definition(BRAIN_SPECIMEN) == "A specimen that is derived from brain."
    assert set(adapter.entity_aliases(NASAL_ASPIRATE_SPECIMEN)) == {
        "nasal wash specimen",
        "nasopharyngeal aspirate",
    }


def test_patcher(adapter):
    adapter.set_label(BRAIN_SPECIMEN, "FOO")
    if not isinstance(adapter, DumperInterface):
        raise ValueError("Adapter does not support dumping")
    assert adapter.label(BRAIN_SPECIMEN) == "FOO"
    adapter.dump(SAVED_TEMPLATES)
    adapter2 = get_adapter(f"robottemplate:{SAVED_TEMPLATES}")
    assert adapter2.label(BRAIN_SPECIMEN) == "FOO"


@pytest.mark.parametrize(
    "spec_cols,template,expected",
    [
        (
            ["LABEL"],
            {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"},
            [{"LABEL": "foo"}, {"LABEL": "bar"}],
        ),
        (
            ["LABEL"],
            {"id": "ID", "name": "A rdfs:label", "definition": "A DEFINITION"},
            [{"LABEL": "foo"}, {"LABEL": "bar"}],
        ),
        (
            ["LABEL"],
            {"id": "ID", "name": "A rdfs:label SPLIT=|", "definition": "A DEFINITION"},
            [{"LABEL": ["foo"]}, {"LABEL": ["bar"]}],
        ),
        (
            ["LABEL"],
            {"id": "ID", "name": "LABEL SPLIT=|", "definition": "A DEFINITION"},
            [{"LABEL": ["foo"]}, {"LABEL": ["bar"]}],
        ),
        (
            ["ID"],
            {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"},
            [{"ID": "X:1"}, {"ID": "X:2"}],
        ),
        (
            None,
            {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"},
            [
                {"A DEFINITION": None, "ID": "X:1", "LABEL": "foo"},
                {"A DEFINITION": "A bar", "ID": "X:2", "LABEL": "bar"},
            ],
        ),
    ],
)
def test_template_slice(spec_cols, template, expected):
    rows = [{"id": "X:1", "name": "foo"}, {"id": "X:2", "name": "bar", "definition": "A bar"}]
    assert template_slice(template, rows, spec_cols) == expected
