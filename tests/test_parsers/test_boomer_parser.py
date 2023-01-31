import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import json_loader

from oaklib.datamodels.obograph import GraphDocument
from oaklib.parsers.boomer_parser import BoomerParser
from tests import INPUT_DIR

EXAMPLE = INPUT_DIR / "boomer-example.md"


class BoomerParserTest(unittest.TestCase):
    """Tests parsing Boomer reports."""

    def test_boomer_parser(self):
        """Tests parsing a simple boomer file."""
        parser = BoomerParser()
        with open(EXAMPLE) as f:
            clusters = list(parser.parse(f))
            for c in clusters:
                print(yaml_dumper.dumps(c))
