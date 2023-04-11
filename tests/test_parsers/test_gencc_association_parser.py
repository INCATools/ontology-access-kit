import logging
import unittest

from oaklib.parsers import GENCC
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

G2D_INPUT = INPUT_DIR / "example-g2d.gencc.csv"


class GenCCAssociationParserTest(unittest.TestCase):
    """Tests parsing of hpoa g2p format."""

    def test_parser(self):
        """Tests parsing g2p associations."""
        parser = get_association_parser(GENCC)
        expected = [
            {"subject": "HGNC:10896", "subject_label": "SKI", "object": "MONDO:0008426"},
            {
                "subject": "HGNC:16636",
                "subject_label": "KIF1B",
                "object": "MONDO:0008233",
                "object_label": "pheochromocytoma",
            },
        ]
        with open(G2D_INPUT) as file:
            assocs = list(parser.parse(file))
            found = {}
            for association in assocs:
                logging.info(association)
                for e in expected:
                    if all([getattr(association, k) == e[k] for k, v in e.items()]):
                        found[frozenset(e.items())] = True
            for e in expected:
                self.assertIn(frozenset(e.items()), found, f"Expected {e} not found in {found}")
