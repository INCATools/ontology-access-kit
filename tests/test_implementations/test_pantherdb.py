import unittest

import pytest

from oaklib import get_adapter
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.utilities.iterator_utils import chunk


# TODO: use mock tests
@pytest.mark.skip(reason="Network dependency")
class TestPantherDB(unittest.TestCase):
    """
    Tests :ref:`PantherDBImplementation`
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("pantherdb:9606")

    def test_query(self):
        """Tests basic query."""
        adapter = self.adapter
        if not isinstance(adapter, AssociationProviderInterface):
            raise TypeError("adapter is not an AssociationProviderInterface")
        assocs = list(chunk(adapter.associations(subjects=["UniProtKB:P04217"]), 5))
        self.assertGreater(len(assocs), 0)
