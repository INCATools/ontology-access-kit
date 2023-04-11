import logging
import unittest

from oaklib.datamodels.association import Association
from oaklib.parsers import GENCC, MEDGEN_MIM_D2G
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

D2G_INPUT = INPUT_DIR / "example-d2g.mim2gene.tsv"


class MIM2GeneAssociationParserTest(unittest.TestCase):
    """Tests parsing of medgen file."""

    def test_d2g_parser(self):
        """Tests parsing d2g associations."""
        parser = get_association_parser(MEDGEN_MIM_D2G)
        expected = [
            {"subject": "OMIM:100100", "object": "NCBIGene:1131"},
        ]
        with open(D2G_INPUT) as file:
            assocs = list(parser.parse(file))
            found = {}
            for association in assocs:
                logging.info(association)
                for e in expected:
                    if all([getattr(association, k) == e[k] for k, v in e.items()]):
                        found[frozenset(e.items())] = True
            for e in expected:
                self.assertIn(frozenset(e.items()), found, f"Expected {e} not found in {found}")
