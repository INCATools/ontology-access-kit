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
from oaklib.utilities.lexical.lexical_indexer import (
    create_lexical_index,
    save_lexical_index,
)
from oaklib.utilities.mapping.boomer_utils import BoomerEngine
from oaklib.utilities.ontology_builder import OntologyBuilder
from tests import INPUT_DIR, OUTPUT_DIR

EXAMPLE = INPUT_DIR / "boomer-example.md"


class TestBoomerUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = BoomerEngine()
        self.engine.load(EXAMPLE)

    def test_filter(self):
        ben = self.engine
        cases = [
            (0.01, None, 7),
            (0.8, None, 0),
            (None, None, 7),
            (None, 0.3, 0),
        ]
        for minc, maxc, expected_n in cases:
            ms = list(ben.mappings(minimum_confidence=minc, maximum_confidence=maxc))
            for m in ms:
                print(m)
            self.assertEqual(expected_n, len(ms))
