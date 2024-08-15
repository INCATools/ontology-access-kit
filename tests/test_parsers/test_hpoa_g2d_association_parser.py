import logging
import unittest

from oaklib import get_adapter
from oaklib.conf import CONF_DIR_PATH
from oaklib.parsers import HPOA_G2D
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

G2D_INPUT = INPUT_DIR / "example-hpoa-g2d.tsv"


class HpoaG2DAssociationParserTest(unittest.TestCase):
    """Tests parsing of hpoa g2d format."""

    def test_parser(self):
        """Tests parsing g2p associations."""
        parser = get_association_parser(HPOA_G2D)
        expected = [
            {"subject": "NCBIGene:64170", "subject_label": "CARD9", "object": "OMIM:212050"},
            {"subject": "NCBIGene:2022", "subject_label": "ENG", "object": "Orphanet:231160"},
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

    @unittest.skip("Remote test")
    def test_remote(self):
        adapter = get_adapter(CONF_DIR_PATH / "mondo-hpoa-g2d-input-spec.yaml")
        n = 0
        for association in adapter.associations():
            print(association)
            n += 1
        assert n > 0
