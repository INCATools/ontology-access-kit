import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import HPOA_G2P
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

G2P_INPUT = INPUT_DIR / "test.hpoa_g2p.tsv"


class HpoaG2PAssociationParserTest(unittest.TestCase):
    """Tests parsing of hpoa g2p format."""

    def test_parser(self):
        """Tests parsing g2p associations."""
        parser = get_association_parser(HPOA_G2P)
        with open(G2P_INPUT) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="NCBIGene:8195",
                    subject_label="MKKS",
                    predicate=None,
                    object="HP:0000175",
                    property_values=[],
                ),
                assocs,
            )
