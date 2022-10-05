import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser
from tests import INPUT_DIR

GAF = INPUT_DIR / "test-uniprot.gaf"


class XafAssociationParserTest(unittest.TestCase):
    """Tests parsing of GAF and GAF-like formats."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = XafAssociationParser(
            subject_column=ColumnReference(1), object_column=ColumnReference(4)
        )
        with open(GAF) as file:
            assocs = list(parser.parse(file))
            for association in assocs:
                logging.info(association)
            self.assertIn(
                Association(
                    subject="Q9BPZ7", predicate=None, object="GO:0005737", property_values=[]
                ),
                assocs,
            )
