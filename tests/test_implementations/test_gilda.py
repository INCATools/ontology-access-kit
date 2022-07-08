"""Tests for the Gilda annotator."""

import unittest

from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.implementations import GildaImplementation
from tests import CELL_CORTEX


class TestGilda(unittest.TestCase):
    """Tests for the Gilda annotator."""

    def setUp(self) -> None:
        """Set up the test case with a Gilda ontology interface."""
        self.configuration = TextAnnotationConfiguration(matches_whole_text=True)
        self.ontology_interface = GildaImplementation()

    def test_text_annotator(self):
        """Test the annotation works."""
        results = list(
            self.ontology_interface.annotate_text("cell cortex", configuration=self.configuration)
        )
        self.assertTrue(r.object_id == CELL_CORTEX for r in results)
