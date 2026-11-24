"""Adapter for ontology releases published in the ohi.dev catalog."""

import hashlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from oaklib.constants import OAKLIB_MODULE
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation

__all__ = [
    "OhiImplementation",
]

# Formats are tried in this order. Both are Turtle, so rdflib can load either.
OHI_FORMATS = ["owl-turtle", "rdfs-turtle"]


@dataclass
class OhiImplementation(SparqlImplementation):
    """
    Loads an ontology release from the `ohi.dev <https://ohi.dev>`_ catalog.

    The selector is ``ohi:NAMESPACE/NAME``, which loads the latest release, or
    ``ohi:NAMESPACE/NAME@VERSION``, which loads that release. Releases in the catalog
    never change, so a pinned version always gives the same ontology.

    The release's Turtle file is downloaded once into the OAK cache directory, checked
    against the sha256 hash the catalog publishes, and then loaded in memory with rdflib,
    the same way as a local ``.ttl`` file.

    This needs the ``ohi-sdk`` package, which comes with ``pip install oaklib[ohi]``.

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("ohi:obo/ro@2024-04-24")
    >>> print(adapter.label("RO:0002202"))
    develops from
    """

    def __post_init__(self):
        if self.graph is None:
            reference = self.resource.slug
            if not reference:
                raise ValueError(
                    "No ontology given. Use ohi:NAMESPACE/NAME or ohi:NAMESPACE/NAME@VERSION, "
                    "for example ohi:obo/pato"
                )
            path = download_release(reference)
            self.resource.slug = str(path)
            self.resource.local = True
            self.resource.format = "turtle"
        super().__post_init__()


def download_release(reference: str) -> Path:
    """
    Download the Turtle file of an ohi.dev release into the OAK cache.

    :param reference: catalog reference such as ``obo/pato`` or ``obo/pato@2020-02-06``
    :return: path to the local file
    """
    try:
        from ohi import CatalogClient
    except ImportError as e:
        raise ImportError(
            "The ohi: selector needs the ohi-sdk package. "
            "Install it with: pip install 'oaklib[ohi]'"
        ) from e

    client = CatalogClient()
    publication = client.inspect(reference)
    artifacts = {artifact.format.value: artifact for artifact in publication.artifacts}
    artifact = next((artifacts[f] for f in OHI_FORMATS if f in artifacts), None)
    if artifact is None:
        raise ValueError(
            f"Release {publication.namespace}/{publication.name}@{publication.version} "
            f"has no Turtle file (looked for {', '.join(OHI_FORMATS)})"
        )

    directory = OAKLIB_MODULE.join(
        "ohi", publication.namespace, publication.name, publication.version
    )
    path = directory / Path(urlparse(artifact.url).path).name
    if path.exists() and _sha256(path.read_bytes()) == artifact.sha256:
        logging.info(f"Using cached {path}")
        return path

    logging.info(f"Downloading {artifact.url}")
    data = client.get(artifact.url)
    if _sha256(data) != artifact.sha256:
        raise ValueError(f"sha256 of {artifact.url} does not match the catalog")
    # Write to a temporary file first so an interrupted download never leaves a partial file.
    partial = path.with_name(path.name + ".partial")
    partial.write_bytes(data)
    os.replace(partial, path)
    return path


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
