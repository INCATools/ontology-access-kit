import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import G2T
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

INPUT_TSV = INPUT_DIR / "test-pairwise-associations.tsv"


class PairwiseAssociationParserTest(unittest.TestCase):
    """Tests parsing of simple pairwise TSVs."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = get_association_parser(G2T)
        with open(INPUT_TSV) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="UniProtKB:Q9HC35",
                    object="GO:0005737",
                    property_values=[],
                ),
                assocs,
            )
