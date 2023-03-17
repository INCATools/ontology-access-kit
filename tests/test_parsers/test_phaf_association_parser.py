import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import PHAF
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

PHAF_INPUT = INPUT_DIR / "test.phaf.tsv"


class PhafAssociationParserTest(unittest.TestCase):
    """Tests parsing of PHAF formats."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = get_association_parser(PHAF)
        with open(PHAF_INPUT) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="PomBase:SPCC338.10c",
                    predicate=None,
                    object="FYPO:0000245",
                    property_values=[],
                ),
                assocs,
            )
