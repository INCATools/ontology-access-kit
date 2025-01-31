import unittest

from oaklib import get_adapter

TEST_PMID = "PMID:21873635"


# TODO: use mock tests
class TestPubMed(unittest.TestCase):
    """
    Tests :ref:`PubMedImplementation`
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("pubmed:")

    def test_lookup(self):
        """Tests basic lookup of a PMID."""
        label = self.adapter.label(TEST_PMID)
        desc = self.adapter.definition(TEST_PMID)
        self.assertTrue(label.startswith("Phylogenetic-based propagation"))
        self.assertTrue(desc.startswith("The goal of the Gene Ontology"))
        md = self.adapter.entity_metadata_map(TEST_PMID)
        assert md["year"] == "2011"
