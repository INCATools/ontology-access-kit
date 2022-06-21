import unittest

from linkml_runtime.dumpers import yaml_dumper

from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations.ols.ols_implementation import OlsImplementation
from oaklib.resource import OntologyResource
from tests import CELLULAR_COMPONENT, CYTOPLASM, DIGIT, VACUOLE


class TestOlsImplementation(unittest.TestCase):
    def setUp(self) -> None:
        oi = OlsImplementation(OntologyResource("go"))
        self.oi = oi

    def test_mappings(self):
        oi = self.oi
        mappings = list(oi.get_sssom_mappings_by_curie(DIGIT))
        for m in mappings:
            print(yaml_dumper.dumps(m))
        assert any(m for m in mappings if m.object_id == "EMAPA:32725")

    def test_ancestors(self):
        oi = self.oi
        ancs = list(oi.ancestors([VACUOLE]))
        # for a in ancs:
        #    print(a)
        assert CYTOPLASM in ancs
        assert CELLULAR_COMPONENT in ancs
        ancs = list(oi.ancestors([VACUOLE], predicates=[IS_A]))
        # for a in ancs:
        #    print(a)
        assert CYTOPLASM not in ancs
        assert CELLULAR_COMPONENT in ancs
