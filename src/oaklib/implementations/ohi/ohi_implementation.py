"""Adapter for ontology releases published in the ohi.dev catalog."""

import hashlib
import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import rdflib

from oaklib.constants import OAKLIB_MODULE
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation

__all__ = [
    "OhiImplementation",
]

OHI_FORMAT = "owl-turtle"

READ_ONLY_MESSAGE = (
    "Releases loaded with ohi: are read-only. Write your changes to a new file instead, "
    "e.g. with the -o option of apply."
)

# How ohi marks a version as one exact release; see the ohi-sdk documentation.
REVISION_SEPARATOR = "-revision-"
NO_REVISION_SUFFIX = "-no-revision"


@dataclass
class OhiImplementation(SparqlImplementation):
    """
    Loads an ontology release from the `ohi.dev <https://ohi.dev>`_ catalog.

    The selector is ``ohi:NAMESPACE/NAME``, which loads the latest release, or
    ``ohi:NAMESPACE/NAME@VERSION``, which loads that release. Releases in the catalog
    never change, so a pinned version always gives the same ontology.

    The release's Turtle file is downloaded once into the OAK cache directory, checked
    against the sha256 hash the catalog publishes, and then loaded in memory with rdflib,
    the same way as a local ``.ttl`` file. The loaded ontology is read-only.

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
            graph = rdflib.Graph()
            graph.parse(str(path), format="turtle")
            self.graph = graph

    def save(self):
        raise NotImplementedError(READ_ONLY_MESSAGE)

    def dump(self, path: str = None, syntax: str = "turtle", **kwargs):
        # apply --overwrite dumps to the resource's own path, which for ohi: is the
        # catalog reference, not a file.
        if path is not None and str(path) == str(self.resource.local_path):
            raise NotImplementedError(READ_ONLY_MESSAGE)
        return super().dump(path, syntax, **kwargs)


def download_release(reference: str) -> Path:
    """
    Download the Turtle file of an ohi.dev release into the OAK cache.

    A reference to one exact release, such as ``obo/pato@2020-02-06-no-revision``, is
    loaded from the cache without contacting ohi.dev when it has been downloaded before.

    :param reference: catalog reference such as ``obo/pato`` or ``obo/pato@2020-02-06``
    :return: path to the local file
    """
    cached = _cached_exact_release(reference)
    if cached is not None:
        logging.info(f"Using cached {cached}")
        return cached

    try:
        from ohi import CatalogClient
    except ImportError as e:
        raise ImportError(
            "The ohi: selector needs the ohi-sdk package. "
            "Install it with: pip install 'oaklib[ohi]'"
        ) from e

    client = CatalogClient()
    publication = client.inspect(reference)
    artifact = next((a for a in publication.artifacts if a.format.value == OHI_FORMAT), None)
    if artifact is None:
        raise ValueError(
            f"Release {publication.namespace}/{publication.name}@{publication.version} "
            f"has no {OHI_FORMAT} file"
        )

    directory = OAKLIB_MODULE.join(
        "ohi", publication.namespace, publication.name, publication.version
    )
    path = directory / Path(urlparse(artifact.url).path).name
    if _file_sha256(path) == artifact.sha256:
        logging.info(f"Using cached {path}")
        if not _hash_path(path).is_file():
            _write_atomic(_hash_path(path), artifact.sha256.encode())
        return path

    logging.info(f"Downloading {artifact.url}")
    data = client.get(artifact.url)
    if hashlib.sha256(data).hexdigest() != artifact.sha256:
        raise ValueError(f"sha256 of {artifact.url} does not match the catalog")
    _write_atomic(path, data)
    # The stored hash lets exact releases load later without asking the catalog.
    _write_atomic(_hash_path(path), artifact.sha256.encode())
    return path


def _cached_exact_release(reference: str) -> Optional[Path]:
    """Return the cached file of a reference to one exact release, if it is intact."""
    namespace, _, rest = reference.partition("/")
    name, _, version = rest.partition("@")
    if version.endswith(NO_REVISION_SUFFIX):
        version = version[: -len(NO_REVISION_SUFFIX)]
    elif REVISION_SEPARATOR not in version:
        # No version, or a version whose latest revision may change.
        return None
    if not (namespace and name and version):
        return None
    directory = OAKLIB_MODULE.join("ohi", namespace, name, version, ensure_exists=False)
    for hash_path in directory.glob("*.sha256"):
        path = hash_path.with_suffix("")
        if _file_sha256(path) == hash_path.read_text().strip():
            return path
    return None


def _hash_path(path: Path) -> Path:
    return path.with_name(path.name + ".sha256")


def _file_sha256(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_atomic(path: Path, data: bytes) -> None:
    # Write to a uniquely named temporary file first, so an interrupted download never
    # leaves a partial file and two processes loading the same release don't collide.
    fd, partial = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".partial")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(partial, path)
    except BaseException:
        Path(partial).unlink(missing_ok=True)
        raise
