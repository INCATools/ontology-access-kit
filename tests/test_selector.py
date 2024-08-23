import csv
import gzip
import os
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from gilda.grounder import Grounder
    from gilda.term import Term

    have_gilda = True
except ImportError:
    have_gilda = False

from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.implementations.gilda import GildaImplementation
from oaklib.implementations.ontobee.ontobee_implementation import OntobeeImplementation
from oaklib.implementations.pronto.pronto_implementation import ProntoImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.implementations.sqldb.sql_implementation import SqlImplementation
from oaklib.implementations.ubergraph import UbergraphImplementation
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.selector import get_adapter, get_resource_from_shorthand
from tests import INPUT_DIR


@unittest.skipIf(not have_gilda, "Gilda not available")
class TestResource(unittest.TestCase):
    def test_from_descriptor(self):
        # no scheme
        resource = get_resource_from_shorthand("foo.obo")
        assert resource.implementation_class == ProntoImplementation
        self.assertEqual("foo.obo", resource.slug)
        resource = get_resource_from_shorthand("foo.owl")
        # this may change:
        assert resource.implementation_class == SparqlImplementation
        resource = get_resource_from_shorthand("foo.ttl")
        # this may change:
        assert resource.implementation_class == SparqlImplementation
        resource = get_resource_from_shorthand("pronto:foo.owl")
        assert resource.implementation_class == ProntoImplementation
        resource = get_resource_from_shorthand("foo.db")
        assert resource.implementation_class == SqlImplementation
        assert resource.slug.startswith("sqlite")
        # with scheme
        resource = get_resource_from_shorthand("pronto:foo.obo")
        assert resource.implementation_class == ProntoImplementation
        self.assertEqual("foo.obo", resource.slug)
        resource = get_resource_from_shorthand("ubergraph:")
        assert resource.implementation_class == UbergraphImplementation
        self.assertIsNone(resource.slug)
        resource = get_resource_from_shorthand("ontobee:")
        assert resource.implementation_class == OntobeeImplementation
        self.assertIsNone(resource.slug)

    def test_input_specification(self):
        os.chdir(INPUT_DIR.parent.parent)
        adapter = get_adapter(str(INPUT_DIR / "example-g2d-input-specification.yaml"))
        if not isinstance(adapter, AssociationProviderInterface):
            raise ValueError("adapter is not an AssociationProviderInterface")
        # test that normalization of IDs happens
        expected = [("NCBIGene:1131", "MONDO:0007032"), ("NCBIGene:57514", "MONDO:0024506")]
        assocs = []
        for a in adapter.associations():
            print(a)
            assocs.append((a.subject, a.object))
        self.assertCountEqual(expected, assocs)

    @unittest.skipIf(sys.platform == "win32", "Skipping test_gilda_from_descriptor on Windows")
    def test_gilda_from_descriptor(self):
        """Test the Gilda implementation."""
        config = TextAnnotationConfiguration(matches_whole_text=True)

        descriptor = "gilda:"
        adapter_1 = get_adapter(descriptor)
        self.assertIsInstance(adapter_1, GildaImplementation)
        results = list(adapter_1.annotate_text("nucleus", configuration=config))
        self.assertLessEqual(1, len(results))
        results = list(adapter_1.annotate_text("mek", configuration=config))
        self.assertLessEqual(1, len(results))

        terms = [
            Term(
                norm_text="nucleus",
                text="Nucleus",
                db="GO",
                id="0005634",
                entry_name="Nucleus",
                status="name",
                source="GO",
            )
        ]

        with tempfile.TemporaryDirectory() as d:
            path = Path(d).resolve().joinpath("test_terms.tsv.gz")
            dump_terms(terms, path)
            self.assertTrue(path.is_file())

            descriptor = f"gilda:{path.as_posix()}"
            try:
                adapter_2 = get_adapter(descriptor)
            except TypeError as e:
                with gzip.open(path, "rt") as file:
                    content = file.read()
                self.fail(msg=f"Got error {e}\n\nFile content:\n\n{content}")
            self.assertIsInstance(adapter_1, GildaImplementation)
            results = list(adapter_2.annotate_text("nucleus", configuration=config))
            self.assertEqual(1, len(results))

            results = list(adapter_2.annotate_text("mek", configuration=config))
            self.assertEqual(0, len(results))

        grounder = Grounder(terms)
        adapter_3 = get_adapter("gilda:", grounder=grounder)
        self.assertIsInstance(adapter_1, GildaImplementation)
        results = list(adapter_3.annotate_text("nucleus", configuration=config))
        self.assertEqual(1, len(results))

        results = list(adapter_3.annotate_text("mek", configuration=config))
        self.assertEqual(0, len(results))


TERMS_HEADER = [
    "norm_text",
    "text",
    "db",
    "id",
    "entry_name",
    "status",
    "source",
    "organism",
    "source_db",
    "source_id",
]


def dump_terms(terms, fname) -> None:
    """Dump a list of Gilda terms to a tsv.gz file."""
    with gzip.open(fname, "wt", encoding="utf-8") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(TERMS_HEADER)
        writer.writerows(t.to_list() for t in terms)
