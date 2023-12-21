import json
import unittest

from oaklib import get_adapter
from oaklib.implementations import UniprotImplementation
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from tests import INPUT_DIR

PROTEIN_PATH = INPUT_DIR / "uniprot-P12345.json"


# TODO: use mock tests
class TestUniprot(unittest.TestCase):
    """
    Tests :ref:`UniprotImplementation`
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("uniprot:")

    def test_query(self):
        """Tests basic query."""
        adapter = self.adapter
        if not isinstance(adapter, AssociationProviderInterface):
            raise TypeError("adapter is not an AssociationProviderInterface")
        assocs = list(adapter.associations(subjects=["UniProtKB:P12345"]))
        self.assertGreater(len(assocs), 0)

    def test_parse_uniprot_json(self):
        adapter = self.adapter
        obj = json.load(open(str(PROTEIN_PATH)))
        if not isinstance(adapter, UniprotImplementation):
            raise AssertionError
        assocs = list(adapter._parse_uniprot_json("UniProtKB:P12345", obj))
        for assoc in assocs:
            print(assoc)
