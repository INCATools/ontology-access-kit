import unittest

from defusedxml.ElementTree import fromstring

from oaklib.implementations.ncbi.pubmed_parser import (
    PubmedRecord,
    parse_pubmed_article_set,
)
from tests import INPUT_DIR

REAL_RECORD = INPUT_DIR / "pubmed-efetch-21873635.xml"
EDGE_CASES = INPUT_DIR / "pubmed-efetch-edge-cases.xml"


def _parse(content: bytes):
    return parse_pubmed_article_set(fromstring(content))


class TestPubmedParser(unittest.TestCase):
    """
    Tests :mod:`oaklib.implementations.ncbi.pubmed_parser`
    """

    def test_real_record(self):
        records = _parse(REAL_RECORD.read_bytes())
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record.pmid, "21873635")
        self.assertEqual(
            record.title,
            "Phylogenetic-based propagation of functional annotations "
            "within the Gene Ontology consortium.",
        )
        self.assertTrue(record.abstract.startswith("The goal of the Gene Ontology (GO) project"))
        self.assertEqual(record.year, "2011")
        self.assertEqual(record.authors, ["Gaudet P", "Livstone MS", "Lewis SE", "Thomas PD"])
        self.assertEqual(
            record.mesh_headings,
            [
                "Databases, Genetic",
                "Genome",
                "Genomics",
                "Molecular Sequence Annotation",
                "Phylogeny",
                "Proteins",
            ],
        )
        self.assertEqual(record.mesh_qualifiers, ["methods", "methods", "chemistry", "genetics"])

    def test_inline_markup_and_structured_abstract(self):
        record = _parse(EDGE_CASES.read_bytes())[0]
        self.assertEqual(record.title, "Role of BRCA1 in DNA repair.")
        self.assertEqual(record.abstract, "First 2 part. Second part.")

    def test_year_from_medline_date(self):
        record = _parse(EDGE_CASES.read_bytes())[0]
        self.assertEqual(record.year, "1998")

    def test_author_variants(self):
        record = _parse(EDGE_CASES.read_bytes())[0]
        self.assertEqual(record.authors, ["Gene Ontology Consortium", "Smith", "Doe J"])

    def test_missing_abstract(self):
        record = _parse(EDGE_CASES.read_bytes())[1]
        self.assertEqual(
            record, PubmedRecord(pmid="1000002", title="No abstract here", year="2020")
        )

    def test_empty_article_set(self):
        self.assertEqual(_parse(b"<PubmedArticleSet></PubmedArticleSet>"), [])

    def test_error_response(self):
        content = b"<eFetchResult><ERROR>ID list is empty! Possibly it has no correct IDs.</ERROR></eFetchResult>"
        with self.assertLogs("oaklib.implementations.ncbi.pubmed_parser", "WARNING") as logs:
            self.assertEqual(_parse(content), [])
        self.assertIn("ID list is empty", logs.output[0])
