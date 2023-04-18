import logging
import unittest

from oaklib.parsers import MEDGEN_MIM_G2D
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

G2D_INPUT = INPUT_DIR / "example-g2d.mim2gene.tsv"


class MIM2GeneAssociationParserTest(unittest.TestCase):
    """Tests parsing of medgen file."""

    def test_g2d_parser(self):
        """Tests parsing g2d associations."""
        parser = get_association_parser(MEDGEN_MIM_G2D)
        expected = [
            {"object": "OMIM:100100", "subject": "NCBIGene:1131"},
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
