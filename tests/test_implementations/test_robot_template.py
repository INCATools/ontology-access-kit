import kgcl_schema.grammar.parser as kgcl_parser
import pytest
from kgcl_schema.datamodel import kgcl
from linkml_runtime.dumpers import yaml_dumper

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.implementations.tabular.robot_template_implementation import (
    template_modify,
    template_slice,
)
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.utilities.kgcl_utilities import tidy_change_object
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
    changes = [f"rename {BRAIN_SPECIMEN} from 'brain specimen' to 'brain sample'"]
    if not isinstance(adapter, PatcherInterface):
        raise ValueError("Adapter does not support patching")
    for change in changes:
        print(f"Applying: {change}")
        change_obj = kgcl_parser.parse_statement(change)
        tidy_change_object(change_obj)
        print(yaml_dumper.dumps(change_obj))
        assert isinstance(change_obj, kgcl.NodeRename)
        print("NEW:", change_obj.new_value)
        adapter.apply_patch(change_obj)
    assert adapter.label(BRAIN_SPECIMEN) == "brain sample"
    if not isinstance(adapter, DumperInterface):
        raise ValueError("Adapter does not support dumping")
    adapter.dump(SAVED_TEMPLATES, clean=True)
    adapter2 = get_adapter(f"robottemplate:{SAVED_TEMPLATES}")
    assert adapter2.label(BRAIN_SPECIMEN) == "brain sample"


def test_set_label():
    # do not use fixture, as we will mutate the contents
    adapter = get_adapter(f"robottemplate:{TEMPLATES}")
    if not isinstance(adapter, PatcherInterface):
        raise ValueError("Adapter does not support patching")
    assert adapter.label(BRAIN_SPECIMEN) == "brain specimen"
    assert adapter.set_label(BRAIN_SPECIMEN, "FOO")
    assert adapter.label(BRAIN_SPECIMEN) == "FOO", "failed to update in-memory"
    assert adapter.label(LOW_GRADE_OVARIAN_TUMOR) == "Low grade ovarian tumor"
    assert adapter.set_label(LOW_GRADE_OVARIAN_TUMOR, "BAR")
    if not isinstance(adapter, DumperInterface):
        raise ValueError("Adapter does not support dumping")
    adapter.dump(SAVED_TEMPLATES, clean=True)
    adapter2 = get_adapter(f"robottemplate:{SAVED_TEMPLATES}")
    assert adapter2.label(BRAIN_SPECIMEN) == "FOO", "failed to update on disk"
    assert adapter2.label(LOW_GRADE_OVARIAN_TUMOR) == "BAR", "failed to update on disk"


def test_set_definition():
    # do not use fixture, as we will mutate the contents
    # (also: there appears to be a difference in fixtures between unix and osx?)
    adapter = get_adapter(f"robottemplate:{TEMPLATES}")
    if not isinstance(adapter, PatcherInterface):
        raise ValueError("Adapter does not support patching")
    assert adapter.definition(BRAIN_SPECIMEN) == "A specimen that is derived from brain."
    new_def = "A sample that is derived from brain."
    assert adapter.set_definition(BRAIN_SPECIMEN, new_def)
    assert adapter.definition(BRAIN_SPECIMEN) == new_def, "failed to update in-memory"
    if not isinstance(adapter, DumperInterface):
        raise ValueError("Adapter does not support dumping")
    adapter.dump(SAVED_TEMPLATES, clean=True)
    adapter2 = get_adapter(f"robottemplate:{SAVED_TEMPLATES}")
    assert adapter2.definition(BRAIN_SPECIMEN) == new_def, "failed to update on disk"


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


def test_modify_template():
    template = {"id": "ID", "name": "LABEL", "definition": "A DEFINITION"}
    rows = [{"id": "X:1", "name": "foo"}, {"id": "X:2", "name": "bar", "definition": "A bar"}]
    assert template_modify("X:2", template, rows, {"LABEL": "baz"})
    assert template_slice(template, rows) == [
        {"ID": "X:1", "LABEL": "foo", "A DEFINITION": None},
        {"ID": "X:2", "LABEL": "baz", "A DEFINITION": "A bar"},
    ]
