"""Tests for the ohi.dev adapter."""

import functools
import hashlib
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pystow

from oaklib.implementations import OhiImplementation
from oaklib.selector import get_adapter, get_resource_from_shorthand
from tests import INPUT_DIR, NUCLEUS

try:
    from ohi import CatalogException

    HAS_OHI = True
except ImportError:
    HAS_OHI = False

ONTOLOGY_PATH = INPUT_DIR / "go-nucleus.owl.ttl"
FILE_URL = "https://api.ohi.dev/files/packages/obo/go-nucleus/1/go-nucleus.owl.ttl"
MODULE = "oaklib.implementations.ohi.ohi_implementation"


def fake_publication(formats=("owl-turtle",), sha256=None):
    """Make a stand-in for ohi.Publication with only the fields the adapter reads."""
    if sha256 is None:
        sha256 = hashlib.sha256(ONTOLOGY_PATH.read_bytes()).hexdigest()
    artifacts = [
        SimpleNamespace(format=SimpleNamespace(value=f), url=FILE_URL, sha256=sha256)
        for f in formats
    ]
    return SimpleNamespace(namespace="obo", name="go-nucleus", version="1", artifacts=artifacts)


@unittest.skipUnless(HAS_OHI, "requires ohi-sdk")
class TestOhiImplementation(unittest.TestCase):
    """Tests against a mocked catalog, using a local test ontology."""

    def setUp(self) -> None:
        cache_dir = tempfile.TemporaryDirectory()
        self.addCleanup(cache_dir.cleanup)
        self.cache_dir = Path(cache_dir.name)
        module_patch = mock.patch(f"{MODULE}.OAKLIB_MODULE", pystow.Module(self.cache_dir))
        module_patch.start()
        self.addCleanup(module_patch.stop)
        client_patch = mock.patch("ohi.CatalogClient")
        self.client = client_patch.start().return_value
        self.addCleanup(client_patch.stop)
        self.client.inspect.return_value = fake_publication()
        self.client.get.return_value = ONTOLOGY_PATH.read_bytes()

    def test_selector(self):
        resource = get_resource_from_shorthand("ohi:obo/pato@2020-02-06")
        self.assertEqual(OhiImplementation, resource.implementation_class)
        self.assertEqual("obo/pato@2020-02-06", resource.slug)

    def test_label(self):
        adapter = get_adapter("ohi:obo/go-nucleus@1")
        self.assertIsInstance(adapter, OhiImplementation)
        self.assertEqual("nucleus", adapter.label(NUCLEUS))
        self.client.inspect.assert_called_once_with("obo/go-nucleus@1")
        expected = self.cache_dir / "ohi" / "obo" / "go-nucleus" / "1" / "go-nucleus.owl.ttl"
        self.assertTrue(expected.exists())

    def test_cached_file_is_reused(self):
        get_adapter("ohi:obo/go-nucleus@1")
        get_adapter("ohi:obo/go-nucleus@1")
        self.client.get.assert_called_once_with(FILE_URL)

    def test_changed_cached_file_is_downloaded_again(self):
        get_adapter("ohi:obo/go-nucleus@1")
        path = self.cache_dir / "ohi" / "obo" / "go-nucleus" / "1" / "go-nucleus.owl.ttl"
        path.write_text("not the file the catalog lists")
        adapter = get_adapter("ohi:obo/go-nucleus@1")
        self.assertEqual(2, self.client.get.call_count)
        self.assertEqual("nucleus", adapter.label(NUCLEUS))

    def test_hash_mismatch(self):
        self.client.inspect.return_value = fake_publication(sha256="0" * 64)
        with self.assertRaises(ValueError):
            get_adapter("ohi:obo/go-nucleus@1")
        self.assertEqual([], list(self.cache_dir.rglob("*.ttl")))

    def test_rdfs_turtle_fallback(self):
        self.client.inspect.return_value = fake_publication(formats=("owl-rdfxml", "rdfs-turtle"))
        adapter = get_adapter("ohi:obo/go-nucleus@1")
        self.assertEqual("nucleus", adapter.label(NUCLEUS))

    def test_no_turtle_file(self):
        self.client.inspect.return_value = fake_publication(formats=("owl-rdfxml",))
        with self.assertRaises(ValueError):
            get_adapter("ohi:obo/go-nucleus@1")
        self.client.get.assert_not_called()

    def test_missing_reference(self):
        with self.assertRaises(ValueError):
            get_adapter("ohi:")
        self.client.inspect.assert_not_called()


def skip_on_remote_error(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except CatalogException as e:
            code = e.error.code.value
            server_error = code == "HTTP_ERROR" and (e.error.status or 0) >= 500
            if code not in ("CONNECTION_ERROR", "TIMEOUT") and not server_error:
                raise
            self.skipTest(f"ohi.dev unavailable: {e}")

    return wrapper


@unittest.skipUnless(HAS_OHI, "requires ohi-sdk")
class TestOhiImplementationRemote(unittest.TestCase):
    """
    Tests against the live ohi.dev catalog.

    These download a small, pinned release, so they are skipped if ohi.dev cannot be reached.
    """

    @skip_on_remote_error
    def test_pinned_release(self):
        adapter = get_adapter("ohi:obo/ro@2024-04-24")
        self.assertEqual("develops from", adapter.label("RO:0002202"))
