import pytest
from oaklib import BasicOntologyInterface, get_adapter
from oaklib.interfaces.dumper_interface import DumperInterface

from tests import INPUT_DIR, OUTPUT_DIR

TEMPLATES = INPUT_DIR / "obi-templates"
SAVED_TEMPLATES = OUTPUT_DIR / "obi-templates-modified"

BRAIN_SPECIMEN = "OBI:0002516"
LOW_GRADE_OVARIAN_TUMOR = "OBI:0002217"


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


def test_patcher(adapter):
    adapter.set_label(BRAIN_SPECIMEN, "FOO")
    if not isinstance(adapter, DumperInterface):
        raise ValueError("Adapter does not support dumping")
    adapter.dump(SAVED_TEMPLATES)
    adapter2 = get_adapter(f"robottemplate:{SAVED_TEMPLATES}")
    assert adapter2.label(BRAIN_SPECIMEN) == "FOO"
