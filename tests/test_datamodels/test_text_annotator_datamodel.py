import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview

from oaklib.datamodels import text_annotator
from tests import NUCLEUS, output_path


class TestTextAnnotatorDatamodel(unittest.TestCase):
    def test_create(self):
        """
        Tests the creation of an example instance of the OboGraph datamodel
        """
        ann = text_annotator.TextAnnotation(
            subject_start=1, subject_end=7, match_string="nucleus", object_id=NUCLEUS
        )
        yaml_dumper.dump(ann, output_path("example.text_annotation.yaml"))

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(text_annotator.__name__)
        assert "subject_start" in sv.all_slots()
        assert "TextAnnotation" in sv.all_classes()
