"""Exercise the eutils adapter contract without an NCBI request."""

from types import SimpleNamespace
from unittest.mock import Mock

from oaklib.implementations.ncbi.pubmed_implementation import PubMedImplementation


def test_pubmed_eutils_article_contract():
    """Keep label, definition, and metadata working with supported eutils versions."""
    article = SimpleNamespace(
        title="Synthetic publication",
        abstract="Synthetic abstract",
        year="2026",
        authors=["Example Researcher"],
        mesh_qualifiers=[],
        mesh_headings=[],
    )
    client = Mock()
    client.efetch.return_value = [article]
    adapter = PubMedImplementation(entrez_client=client)
    assert adapter.label("PMID:1") == article.title
    assert adapter.definition("PMID:1") == article.abstract
    metadata = adapter.entity_metadata_map("PMID:1")
    assert metadata["year"] == article.year
    assert metadata["authors"] == article.authors
    client.efetch.assert_called_with(db="pubmed", id="1")
