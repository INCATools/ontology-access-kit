import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import HPOA
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

HPOA_INPUT = INPUT_DIR / "test.hpoa.tsv"


class HpoaAssociationParserTest(unittest.TestCase):
    """Tests parsing of hpoa formats."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = get_association_parser(HPOA)
        with open(HPOA_INPUT) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="DECIPHER:1",
                    subject_label="Wolf-Hirschhorn syndrome",
                    predicate=None,
                    object="HP:0000252",
                    property_values=[],
                ),
                assocs,
            )
