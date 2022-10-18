"""Tests for OWL to FHIR CodeSystem converter."""
import unittest

from oaklib.converters.owl_to_fhir_codesystem import convert
from tests import INPUT_DIR, OUTPUT_DIR


ONT = INPUT_DIR / "mondo-example.owl"
OUT = OUTPUT_DIR / "mondo-example.json"


class OwlToFhirConversionTest(unittest.TestCase):
    """Tests"""

    def test_convert(self):
        """Tests basic conversion"""
        result = convert(ONT, OUT)
        self.assertTrue(result is True)  # todo
