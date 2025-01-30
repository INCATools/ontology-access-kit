from functools import lru_cache
from typing import Optional

from pydantic import BaseModel

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.datamodels.vocabulary import RDFS_LABEL

LICENSE_NAME_TO_URL_PREFIX = {
    "CC0": ("https://creativecommons.org/publicdomain/zero/", "1.0"),
    "CC-BY": ("https://creativecommons.org/licenses/by/", "4.0"),
    "CC-BY-SA": ("https://creativecommons.org/licenses/by-sa/", "4.0"),
    "CC-BY-NC": ("https://creativecommons.org/licenses/by-nc/", "4.0"),
    "CC-BY-NC-SA": ("https://creativecommons.org/licenses/by-nc-sa/", "4.0"),
    "CC-BY-NC-ND": ("https://creativecommons.org/licenses/by-nc-nd/", "4.0"),
    "CC-BY-ND": ("https://creativecommons.org/licenses/by-nd/", "4.0"),
}


def map_license_to_url(license: str) -> str:
    """
    Map a license name to a URL

    Examples:

        >>> map_license_to_url("CC0")
        'https://creativecommons.org/publicdomain/zero/1.0/'
        >>> map_license_to_url("CC-BY")
        'https://creativecommons.org/licenses/by/4.0/'
        >>> map_license_to_url("CC BY")
        'https://creativecommons.org/licenses/by/4.0/'
        >>> map_license_to_url("CC-BY-3.0")
        'https://creativecommons.org/licenses/by/3.0/'

    :param license:
    :return:
    """
    license = normalize_url(license)
    if license.startswith("https://"):
        return license
    license = license.replace(" ", "-")
    toks = license.split("-")
    v = toks[-1]
    # check if v is a version number
    if v[0].isdigit():
        name = "-".join(toks[:-1])
    else:
        name = license
        v = None
    if name in LICENSE_NAME_TO_URL_PREFIX:
        url_prefix, version = LICENSE_NAME_TO_URL_PREFIX[name]
        if v:
            version = v
        return f"{url_prefix}{version}/"
    raise ValueError(f"Could not map license {license} to a URL")


def map_license_url_to_name(url: str) -> str:
    """
    Map a license URL to a name

    Examples:

        >>> map_license_url_to_name('https://creativecommons.org/publicdomain/zero/1.0/')
        'CC0-1.0'
        >>> map_license_url_to_name('https://creativecommons.org/licenses/by/4.0/')
        'CC-BY-4.0'

    :param url:
    :return:
    """
    url = normalize_url(url)
    if url[-1] == "/":
        url = url[:-1]
    toks = url.split("/")
    if toks[-1][0].isdigit():
        version = toks[-1]
        stem = "/".join(toks[:-1]) + "/"
    else:
        version = None
        stem = url
    for name, (this_stem, _this_version) in LICENSE_NAME_TO_URL_PREFIX.items():
        if stem == this_stem:
            return name + "-" + version if version else name
    return url


def normalize_url(url: str, ensure_https=True) -> str:
    if url.startswith("<"):
        url = url[1:-1]
    if ensure_https and url.startswith("http://"):
        url = "https://" + url[len("http://") :]
    return url


@lru_cache
def orcid_adapter() -> BasicOntologyInterface:
    return get_adapter("sqlite:obo:orcid")


class Person(BaseModel):
    orcid: str
    github: Optional[str] = None
    email: Optional[str] = None
    label: Optional[str] = None


def person_by_orcid(id: str, additional_metadata: dict = None) -> Optional[Person]:
    id = normalize_url(id)
    if id[0].isdigit():
        id = f"orcid:{id}"
    if id.startswith("https://orcid.org/"):
        id = f"orcid:{id.split('/')[-1]}"
    if not id.startswith("orcid:"):
        return None
    adapter = orcid_adapter()
    metadata = adapter.entity_metadata_map(id)
    if not metadata:
        metadata = {}

    def _get(k: str) -> Optional[str]:
        v = metadata.get(k, [])
        if v:
            return v[0]
        return None

    d = {
        "orcid": id.replace("orcid:", ""),
        "github": _get("github"),
        "email": _get("email"),
        "label": _get(RDFS_LABEL),
    }
    if additional_metadata:
        x = additional_metadata.get(id)
        if x:
            d.update(x)
    return Person(**d)
