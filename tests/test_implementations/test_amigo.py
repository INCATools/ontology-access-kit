import unittest

from oaklib import get_adapter
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)


# TODO: use mock tests
class TestAmiGO(unittest.TestCase):
    """
    Tests :ref:`AmiGOImplementation`
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("amigo:NCBITaxon:9606")

    def test_query(self):
        """Tests basic query."""
        adapter = self.adapter
        if not isinstance(adapter, AssociationProviderInterface):
            raise TypeError("adapter is not an AssociationProviderInterface")
        assocs = list(adapter.associations(objects=["GO:0000082"]))
        self.assertGreater(len(assocs), 0)
