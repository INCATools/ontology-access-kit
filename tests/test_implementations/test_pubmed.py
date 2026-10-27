import unittest
from unittest.mock import MagicMock

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, RDFS_LABEL
from tests import INPUT_DIR

TEST_PMID = "PMID:21873635"
REAL_RECORD = INPUT_DIR / "pubmed-efetch-21873635.xml"
EDGE_CASES = INPUT_DIR / "pubmed-efetch-edge-cases.xml"
EMPTY_SET = b"<PubmedArticleSet></PubmedArticleSet>"


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


class TestPubMedMocked(unittest.TestCase):
    """
    Tests :ref:`PubMedImplementation` against saved efetch responses.
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("pubmed:")
        self.session = MagicMock()
        self.adapter._requests_session = self.session

    def _respond_with(self, content: bytes) -> None:
        response = MagicMock()
        response.content = content
        response.from_cache = True
        response.raise_for_status.return_value = None
        self.session.get.return_value = response

    def test_lookup(self):
        self._respond_with(REAL_RECORD.read_bytes())
        self.assertTrue(self.adapter.label(TEST_PMID).startswith("Phylogenetic-based propagation"))
        self.assertTrue(
            self.adapter.definition(TEST_PMID).startswith("The goal of the Gene Ontology")
        )
        md = self.adapter.entity_metadata_map(TEST_PMID)
        self.assertEqual(md["id"], TEST_PMID)
        self.assertTrue(md[RDFS_LABEL].startswith("Phylogenetic-based propagation"))
        self.assertTrue(md[HAS_DEFINITION_CURIE].startswith("The goal of the Gene Ontology"))
        self.assertEqual(md["year"], "2011")
        self.assertEqual(md["authors"], ["Gaudet P", "Livstone MS", "Lewis SE", "Thomas PD"])
        self.assertIn("Phylogeny", md["mesh_headings"])
        self.assertIn("genetics", md["mesh_qualifiers"])

    def test_unprefixed_id(self):
        self._respond_with(REAL_RECORD.read_bytes())
        self.assertTrue(self.adapter.label("21873635").startswith("Phylogenetic-based"))

    def test_pmid_normalized(self):
        self._respond_with(REAL_RECORD.read_bytes())
        for curie in ["PMID:021873635", "PMID:21873635 "]:
            self.assertTrue(self.adapter.label(curie).startswith("Phylogenetic-based"))
            self.assertEqual(self.session.get.call_args.kwargs["params"]["id"], "21873635")

    def test_foreign_curie(self):
        node = self.adapter.node("DOI:10.1093/bib/bbr042")
        self.assertEqual(node.lbl, "DOI:10.1093/bib/bbr042")
        self.assertEqual(self.adapter.entity_metadata_map("DOI:10.1093/bib/bbr042"), {})
        self.session.get.assert_not_called()

    def test_non_numeric_pmid(self):
        for curie in ["PMID:abc", "PMID:²"]:
            self.assertIsNone(self.adapter.label(curie))
            self.assertIsNone(self.adapter.definition(curie))
            self.assertEqual(self.adapter.entity_metadata_map(curie), {})
        self.session.get.assert_not_called()

    def test_not_found(self):
        self._respond_with(EMPTY_SET)
        self.assertIsNone(self.adapter.label("PMID:99999999999"))
        self.assertIsNone(self.adapter.definition("PMID:99999999999"))
        self.assertEqual(self.adapter.entity_metadata_map("PMID:99999999999"), {})

    def test_no_abstract_and_matching_pmid(self):
        self._respond_with(EDGE_CASES.read_bytes())
        self.assertEqual(self.adapter.label("PMID:1000002"), "No abstract here")
        self.assertIsNone(self.adapter.definition("PMID:1000002"))
        md = self.adapter.entity_metadata_map("PMID:1000002")
        self.assertIsNone(md[HAS_DEFINITION_CURIE])
        self.assertEqual(md["year"], "2020")

    def test_entrez_client_removed(self):
        self.assertFalse(hasattr(self.adapter, "entrez_client"))
