import logging
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.introspection import package_schemaview

from oaklib.datamodels import ontology_metadata
from tests import output_path


class TestOntologyMetadataDatamodel(unittest.TestCase):
    def test_create(self):
        c = ontology_metadata.Class(id="EXAMPLE:1", label="foo", has_broad_synonym=["bar"])
        fn = output_path("example.om.yaml")
        yaml_dumper.dump(c, fn)
        yaml_loader.load(fn, target_class=ontology_metadata.Class)

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(ontology_metadata.__name__)
        for c in sv.all_classes():
            logging.info(c)
        assert "id" in sv.all_slots()
        assert "label" in sv.all_slots()
        assert "Class" in sv.all_classes()
