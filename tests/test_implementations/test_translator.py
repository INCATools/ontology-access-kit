import unittest

from oaklib.datamodels.vocabulary import SKOS_CLOSE_MATCH, SKOS_EXACT_MATCH
from oaklib.implementations.translator.translator_implementation import (
    TranslatorImplementation,
)


# TODO: use mock tests
class TestTranslatorImplementation(unittest.TestCase):
    """
    Tests :ref:`TranslatorImplementation`
    """

    def setUp(self) -> None:
        self.impl = TranslatorImplementation()

    @unittest.skip("TODO: use mock tests; service is sometimes unavailable")
    def test_sssom_mappings(self):
        """
        Tests SSSOM mappings from Node Normalizer using a known stable gene
        :return:
        """
        mappings = list(self.impl.sssom_mappings("NCBIGene:1588"))
        cases = [
            ("UniProtKB:P11511", SKOS_CLOSE_MATCH),
            ("HGNC:2594", SKOS_EXACT_MATCH),
        ]
        for mapping in mappings:
            tpl = (mapping.object_id, mapping.predicate_id)
            if tpl in cases:
                cases.remove(tpl)
        self.assertEqual(len(cases), 0, f"Missing cases: {cases}")
