import unittest

from kgcl_schema.datamodel.kgcl import Change
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.dumpers import yaml_dumper

from oaklib.utilities.kgcl_utilities import (
    parse_kgcl_files,
    substitute_curies_for_labels,
    substitute_labels_for_curies,
    write_kgcl,
)
from tests import INPUT_DIR, OUTPUT_DIR

TEST_ONT = INPUT_DIR / "go-nucleus.obo"
TEST_OUT = OUTPUT_DIR / "go-nucleus.lexical.yaml"

TEST_OUT_KGCL = OUTPUT_DIR / "test-create.kgcl.txt"
TEST_OUT_KGCL_YAML = OUTPUT_DIR / "test-create.kgcl.yaml"


class TestKgclUtilities(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_parse_kgcl_files(self):
        def w(objs):
            for obj in objs:
                print(yaml_dumper.dumps(obj))

        def r(objs):
            for obj in objs:
                print(render(obj))

        objs = list(parse_kgcl_files([str(INPUT_DIR / "test-create.kgcl.txt")], None))
        # w(objs)
        for obj in objs:
            assert isinstance(obj, Change)

        def fake_labeler(curie: str) -> str:
            # return "'" + curie.replace(":", "_") + "'" if curie else curie
            if curie is None:
                return None
            return curie.replace(":", "_")

        def fake_unlabeler(label: str) -> str:
            if label is None:
                return None
            return label.replace("_", ":")

        substitute_curies_for_labels(objs, fake_labeler)
        write_kgcl(objs, str(TEST_OUT_KGCL), "kgcl")
        w(objs)
        r(objs)
        objs = list(parse_kgcl_files([str(TEST_OUT_KGCL)], None))
        w(objs)
        substitute_labels_for_curies(objs, fake_unlabeler)
        w(objs)

    # def test_substitution(self):
