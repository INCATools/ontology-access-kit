import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview
from oaklib.datamodels import obograph
from oaklib.datamodels.vocabulary import IS_A
from tests import output_path


class TestOboGraphDatamodel(unittest.TestCase):

    def test_create(self):
        """
        Tests the creation of an example instance of the OboGraph datamodel
        """
        nodes = [obograph.Node(id=f'EXAMPLE:{n}', label=f'node {n}') for n in range(1, 100)]
        edges = []
        for i in range(0, len(nodes) - 1):
            edges.append(obograph.Edge(sub=nodes[i].id, pred=IS_A, obj=nodes[i+1].id))
        g = obograph.Graph(id='test',
                           nodes=nodes,
                           edges=edges)
        yaml_dumper.dump(g, output_path('example.obograph.yaml'))

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(obograph.__name__)
        assert 'id' in sv.all_slots()
        assert 'Node' in sv.all_classes()
        assert 'Edge' in sv.all_classes()



