import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.parsers.boomer_parser import BoomerParser
from tests import INPUT_DIR

EXAMPLE = INPUT_DIR / "boomer-example.md"


class BoomerParserTest(unittest.TestCase):
    """Tests parsing Boomer reports."""

    def setUp(self) -> None:
        self.prefix_map = {
            "A": "http://example.org/A/",
            "B": "http://example.org/B/",
            "C": "http://example.org/C/",
        }

    def test_boomer_parser(self):
        """Tests parsing a simple boomer file."""
        parser = BoomerParser()
        with open(EXAMPLE) as f:
            clusters = list(parser.parse(f))
            for c in clusters:
                logging.info(yaml_dumper.dumps(c))
