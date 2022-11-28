import unittest

from oaklib.datamodels.lexical_index import (
    LexicalTransformation,
    LexicalTransformationPipeline,
    TransformationType,
)
from oaklib.datamodels.mapping_rules_datamodel import Synonymizer
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.simpleobo.simple_obo_implementation import (
    SimpleOboImplementation,
)
from oaklib.resource import OntologyResource
from oaklib.utilities.kgcl_utilities import parse_kgcl_files
from oaklib.utilities.lexical.lexical_indexer import (
    create_lexical_index,
    save_lexical_index,
)
from oaklib.utilities.ontology_builder import OntologyBuilder
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.lexical.yaml"


class TestKgclUtilities(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_parse_kgcl_files(self):
        changes = list(parse_kgcl_files([str(INPUT_DIR / "test-create.kgcl.txt")], None))
