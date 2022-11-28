import unittest

from oaklib.utilities.kgcl_utilities import parse_kgcl_files
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.lexical.yaml"


class TestKgclUtilities(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_parse_kgcl_files(self):
        list(parse_kgcl_files([str(INPUT_DIR / "test-create.kgcl.txt")], None))
