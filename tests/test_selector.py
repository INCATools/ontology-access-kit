import os
import unittest

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
