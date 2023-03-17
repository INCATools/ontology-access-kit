import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import GAF
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

INPUT_GAF = INPUT_DIR / "test-uniprot.gaf"


class GafAssociationParserTest(unittest.TestCase):
    """Tests parsing of GAF and GAF-like formats."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = get_association_parser(GAF)
        with open(INPUT_GAF) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="UniProtKB:Q9BPZ7",
                    predicate="is_active_in",
                    object="GO:0005737",
                    property_values=[],
                ),
                assocs,
            )
            self.assertNotIn(
                "UniProtKB:FAKE123",
                [a.subject for a in assocs],
                "by default, negated associations should be filtered",
            )
