"""
Parse PubMed efetch XML into plain records.

Replaces the PubmedArticle facade previously provided by the unmaintained ``eutils`` package.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import List, Optional
from xml.etree.ElementTree import Element  # noqa S405

__all__ = [
    "PubmedRecord",
    "parse_pubmed_article",
    "parse_pubmed_article_set",
]

logger = logging.getLogger(__name__)

YEAR_PATTERN = re.compile(r"[0-9]{4}")


@dataclass
class PubmedRecord:
    """Fields extracted from a single PubmedArticle element."""

    pmid: str
    title: Optional[str] = None
    abstract: Optional[str] = None
    year: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    mesh_headings: List[str] = field(default_factory=list)
    mesh_qualifiers: List[str] = field(default_factory=list)


def _all_text(element: Optional[Element]) -> Optional[str]:
    """All text under element, including inline markup such as <i>; None if empty."""
    if element is None:
        return None
    text = "".join(element.itertext()).strip()
    return text or None


def _all_texts(element: Element, path: str) -> List[str]:
    return [text for text in (_all_text(e) for e in element.findall(path)) if text]


def _year(citation: Element) -> Optional[str]:
    pub_date = citation.find("Article/Journal/JournalIssue/PubDate")
    if pub_date is None:
        return None
    year = _all_text(pub_date.find("Year"))
    if year:
        return year
    medline_date = _all_text(pub_date.find("MedlineDate"))
    if medline_date:
        match = YEAR_PATTERN.search(medline_date)
        if match:
            return match.group(0)
    return None


def _author(author: Element) -> Optional[str]:
    collective_name = _all_text(author.find("CollectiveName"))
    if collective_name:
        return collective_name
    last_name = _all_text(author.find("LastName"))
    if not last_name:
        return None
    initials = _all_text(author.find("Initials"))
    return f"{last_name} {initials}" if initials else last_name


def parse_pubmed_article(article: Element) -> PubmedRecord:
    """Parse a PubmedArticle element."""
    citation = article.find("MedlineCitation")
    authors = [_author(a) for a in citation.findall("Article/AuthorList/Author")]
    abstract_parts = _all_texts(citation, "Article/Abstract/AbstractText")
    return PubmedRecord(
        pmid=_all_text(citation.find("PMID")),
        title=_all_text(citation.find("Article/ArticleTitle")),
        abstract=" ".join(abstract_parts) or None,
        year=_year(citation),
        authors=[a for a in authors if a],
        mesh_headings=_all_texts(citation, "MeshHeadingList/MeshHeading/DescriptorName"),
        mesh_qualifiers=_all_texts(citation, "MeshHeadingList/MeshHeading/QualifierName"),
    )


def parse_pubmed_article_set(root: Element) -> List[PubmedRecord]:
    """Parse the root of an efetch response for db=pubmed, retmode=xml."""
    if root.tag != "PubmedArticleSet":
        logger.warning(f"Unexpected efetch response <{root.tag}>: {root.findtext('ERROR')}")
        return []
    return [parse_pubmed_article(article) for article in root.findall("PubmedArticle")]
