import logging
import tarfile
import tempfile
import time
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve

import requests
from defusedxml.ElementTree import fromstring

from oaklib.utilities.publication_utils.pubdb_wrapper import PubDBWrapper

logger = logging.getLogger(__name__)

ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

RATE_LIMIT_DELAY = 1.0


def extract_all_text(element):
    text = element.text or ""
    for subelement in element:
        text += extract_all_text(subelement)
        text += subelement.tail if subelement.tail else ""
    return text


def extract_text_from_xml(xml_content):
    root = fromstring(xml_content)
    return extract_all_text(root).strip()


@dataclass
class PubmedWrapper(PubDBWrapper):
    """
    A wrapper to provide a search facade over PubMed.
    """

    name: ClassVar[str] = "ncbi"

    cache_path: Optional[str] = None

    session: requests.Session = field(default_factory=lambda: requests.Session())

    api_key: Optional[str] = None

    email: Optional[str] = None

    where: Optional[Dict] = None

    _uses_cache: bool = False

    def objects_by_ids(self, object_ids: List[str]) -> List[Dict]:
        pubmed_ids = sorted([x.replace("PMID:", "") for x in object_ids])
        session = self.session
        logger.info(f"Using session: {session} [cached: {self._uses_cache} for {pubmed_ids}")

        # Parameters for the efetch request
        efetch_params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),  # Combine PubMed IDs into a comma-separated string
            "rettype": "medline",
            "retmode": "text",
        }
        efetch_response = session.get(EFETCH_URL, params=efetch_params)
        if not self._uses_cache or not efetch_response.from_cache:
            # throttle if not using cache or if not cached
            logger.debug(f"Sleeping for {RATE_LIMIT_DELAY} seconds")
            time.sleep(RATE_LIMIT_DELAY)
        if not efetch_response.ok:
            logger.error(f"Failed to fetch data for {pubmed_ids}")
            raise ValueError(
                f"Failed to fetch data for {pubmed_ids} using {session} and {efetch_params}"
            )
        medline_records = efetch_response.text

        # Parsing titles and abstracts from the MEDLINE records
        parsed_data = []
        current_record = {}
        current_field = None

        for line in medline_records.split("\n"):
            if line.startswith("PMID- "):
                current_field = "id"
                current_record[current_field] = "PMID:" + line.replace("PMID- ", "").strip()
            if line.startswith("PMC - "):
                current_field = "pmcid"
                current_record[current_field] = "PMCID:" + line.replace("PMC - ", "").strip()
            elif line.startswith("TI  - "):
                current_field = "title"
                current_record[current_field] = line.replace("TI  - ", "").strip()
            elif line.startswith("PT  - "):
                current_field = "publication_type"
                v = line.replace("PT  - ", "").strip()
                current_record[current_field] = v
                if v == "Retracted Publication":
                    current_record["retracted"] = True
            elif line.startswith("AB  - "):
                current_field = "abstract"
                current_record[current_field] = line.replace("AB  - ", "").strip()
            elif line.startswith("    "):  # Continuation of the previous field
                if current_field and current_field in current_record:
                    current_record[current_field] += " " + line.strip()
            else:
                current_field = None

            if line == "":
                if current_record:
                    parsed_data.append(current_record)
                    current_record = {}
        return parsed_data

    def fetch_pmcid(self, pmid: str) -> Optional[str]:
        pmid = pmid.replace("PMID:", "")
        session = self.session
        params = {"db": "pmc", "linkname": "pubmed_pmc", "id": pmid}
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
        response = session.get(url, params=params)
        root = fromstring(response.content)  # noqa S113

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
                                return extract_text_from_xml(xml_str)
                                # return xml_str
        return None
