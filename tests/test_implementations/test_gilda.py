"""Tests for the Gilda annotator."""

import unittest

from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.implementations import GildaImplementation
from tests import CELL_CORTEX

try:
    import gilda  # noqa: F401

    HAS_GILDA = True
except ImportError:
    HAS_GILDA = False


@unittest.skipUnless(HAS_GILDA, "requires Gilda")
class TestGilda(unittest.TestCase):
    """Tests for the Gilda annotator."""

    def setUp(self) -> None:
        """Set up the test case with a Gilda ontology interface."""
        self.ontology_interface = GildaImplementation()

    def test_text_annotator(self):
        """Test the annotation works."""
        results_1 = list(
            self.ontology_interface.annotate_text(
                "cell cortex", configuration=TextAnnotationConfiguration(matches_whole_text=True)
            )
        )
        self.assertTrue(r.object_id == CELL_CORTEX for r in results_1)

        long_text = "this is a long description about the cell cortex"
        results_2 = list(
            self.ontology_interface.annotate_text(
                long_text, configuration=TextAnnotationConfiguration(matches_whole_text=True)
            )
        )
        self.assertEqual(0, len(results_2))

        results_3 = list(
            self.ontology_interface.annotate_text(
                long_text,
                configuration=TextAnnotationConfiguration(matches_whole_text=False),
            )
        )
        self.assertTrue(r.object_id == CELL_CORTEX for r in results_3)
