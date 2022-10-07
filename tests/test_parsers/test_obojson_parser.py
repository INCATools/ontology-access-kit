import unittest

from linkml_runtime.loaders import json_loader

from oaklib.datamodels.obograph import GraphDocument
from tests import INPUT_DIR

ONT = INPUT_DIR / "go-nucleus.json"


class OboJsonParserTest(unittest.TestCase):
    """Tests parsing OBO JSON directly."""

    def test_parser(self):
        """Tests parsing obojson."""
        gd: GraphDocument = json_loader.load(str(ONT), target_class=GraphDocument)
        g = gd.graphs[0]
        lbls = [n.lbl for n in g.nodes]
        self.assertIn("cytoplasm", lbls)
        self.assertIn("cell periphery", lbls)
