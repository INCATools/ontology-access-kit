import logging
import tarfile
import tempfile
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve

import pystow
import requests
import requests_cache
from defusedxml.ElementTree import fromstring

from oaklib.utilities.publication_utils.pubdb_wrapper import PubDBWrapper

logger = logging.getLogger(__name__)

RATE_LIMIT_DELAY = 1.0


@dataclass
class DOIWrapper(PubDBWrapper):
    """
    A wrapper to provide a search facade over datacite.
    """

    name: ClassVar[str] = "datacite"

    cache_path: Optional[str] = None

    session: requests.Session = field(default_factory=lambda: requests.Session())

    base_url: str = "https://api.crossref.org"

    api_key: Optional[str] = None

    email: Optional[str] = None

    where: Optional[Dict] = None

    _uses_cache: bool = False

    def __post_init__(self):
        cache_path = self.cache_path
        if not cache_path:
            cache_path = pystow.join("oaklib", "session_cache", "ncbi", ensure_exists=True)
        self.set_cache(cache_path)

    def set_cache(self, name: str) -> None:
        self.session = requests_cache.CachedSession(name)
        self._uses_cache = True

    def objects_by_ids(self, dois: List[str]) -> List[Dict]:
        parsed_data = []

        for doi in dois:
            doi = doi.replace("DOI:", "")  # Remove the "DOI:" prefix if present
            url = f"{self.base_url}/works/{doi}"
            response = self.session.get(url)

            if response.status_code == 200:
                data = response.json()

                record = {
                    "id": f"DOI:{data['DOI']}",
                    "title": data["title"][0] if "title" in data else None,
                    "abstract": data.get("abstract", None),
                    "published_online": data.get("published-online", {}).get(
                        "date-parts", [[None]]
                    )[0][0],
                    "published_print": data.get("published-print", {}).get("date-parts", [[None]])[
                        0
                    ][0],
                    "volume": data.get("volume", None),
                    "issue": data.get("issue", None),
                    "page": data.get("page", None),
                    "publisher": data.get("publisher", None),
                    "type": data.get("type", None),
                    "journal": data.get("container-title", [None])[0],
                    "ISSN": data.get("ISSN", [None])[0],
                }

                parsed_data.append(record)
            else:
                logger.error(
                    f"Error fetching data for DOI: {doi}. Status code: {response.status_code}"
                )

        return parsed_data

    def fetch_pmcid(self, pmid: str) -> Optional[str]:
        pmid = pmid.replace("PMID:", "")
        session = self.session
        params = {"db": "pmc", "linkname": "datacite_pmc", "id": pmid}
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
        response = session.get(url, params=params)
        root = fromstring(response.content)

        for link_set in root.findall(".//LinkSet"):
            for link in link_set.findall(".//Link"):
                pmcid = link.find("./Id").text
                if pmcid:
                    return f"PMC:PMC{pmcid}"
        return None

    def fetch_full_text(self, object_id: str) -> Optional[str]:
        session = self.session
        if object_id.startswith("PMID:"):
            pmcid = self.fetch_pmcid(object_id)
        else:
            pmcid = object_id
        # PMC is a banana - get rid of the PMC prefix as well as local prefix
        pmcid = pmcid.replace("PMC:", "")
        pmcid = pmcid.replace("PMC", "")
        url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC{pmcid}"
        response = session.get(url)
        root = fromstring(response.content)

        for record in root.findall(".//record"):
            for link in record.findall(".//link"):
                format_type = link.attrib.get("format")
                download_url = link.attrib.get("href")
                if format_type == "xml":
                    xml_response = requests.get(download_url)  # noqa S113
                    return xml_response.text
                elif format_type == "tgz":
                    # make a named temp file
                    local_file_path = tempfile.NamedTemporaryFile().name
                    parsed_url = urlparse(download_url)
                    if parsed_url.scheme not in ["http", "https", "ftp"]:
                        continue
                    urlretrieve(download_url, local_file_path)  # noqa S310

                    # Open and extract the tar.gz file
                    with tarfile.open(local_file_path, "r:gz") as tar:
                        for member in tar.getmembers():
                            if member.name.endswith(".xml") or member.name.endswith(".nxml"):
                                f = tar.extractfile(member)
                                xml_str = f.read().decode("utf-8")
                                # return extract_text_from_xml(xml_str)
                                return xml_str
        return None
