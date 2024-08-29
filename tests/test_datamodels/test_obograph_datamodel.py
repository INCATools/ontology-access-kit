from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.introspection import package_schemaview

from oaklib.datamodels import obograph
from oaklib.datamodels.vocabulary import IS_A
from tests import output_path
from tests.test_datamodels import AbstractDatamodelTestCase


class TestOboGraphDatamodel(AbstractDatamodelTestCase):
    def test_create(self):
        """
        Tests the creation of an example instance of the OboGraph datamodel
        """
        nodes = [obograph.Node(id=f"EXAMPLE:{n}", lbl=f"node {n}") for n in range(1, 100)]
        edges = []
        for i in range(0, len(nodes) - 1):
            edges.append(obograph.Edge(sub=nodes[i].id, pred=IS_A, obj=nodes[i + 1].id))
        g = obograph.Graph(id="test", nodes=nodes, edges=edges)
        yaml_dumper.dump(g, output_path("example.obograph.yaml"))

    def test_introspect(self):
        """
        Tests ability to introspect the schema and examine the schema elements
        """
        sv = package_schemaview(obograph.__name__)
        assert "id" in sv.all_slots()
        assert "lbl" in sv.all_slots()  # TODO: consider changing
        assert "Node" in sv.all_classes()
        assert "Edge" in sv.all_classes()

    def test_logical_definitions(self):
        """
        Tests the ability to create logical definitions
        """
        g = obograph.Graph(id="test")
        g.logicalDefinitionAxioms.append(
            obograph.LogicalDefinitionAxiom(
                definedClassId="EXAMPLE:1",
                genusIds=["EXAMPLE:2"],
                restrictions=[
                    obograph.ExistentialRestrictionExpression(
                        propertyId="RO:1", fillerId="EXAMPLE:3"
                    ),
                    obograph.ExistentialRestrictionExpression(
                        propertyId="RO:2", fillerId="EXAMPLE:4"
                    ),
                ],
            )
        )
        # allow no restrictions, even though formally permitted
        g.logicalDefinitionAxioms.append(
            obograph.LogicalDefinitionAxiom(
                definedClassId="EXAMPLE:5",
                genusIds=["EXAMPLE:1", "EXAMPLE:2"],
            )
        )
        # allow no genusIds, even though formally permitted
        g.logicalDefinitionAxioms.append(
            obograph.LogicalDefinitionAxiom(
                definedClassId="EXAMPLE:8",
                restrictions=[
                    obograph.ExistentialRestrictionExpression(
                        propertyId="RO:1", fillerId="EXAMPLE:3"
                    ),
                    obograph.ExistentialRestrictionExpression(
                        propertyId="RO:2", fillerId="EXAMPLE:4"
                    ),
                ],
            )
        )
        # domain and range
        # https://github.com/INCATools/ontology-access-kit/issues/413
        g.domainRangeAxioms.append(
            obograph.DomainRangeAxiom(
                predicateId="RO:1",
                domainClassIds=["EXAMPLE:1"],
                rangeClassIds=["EXAMPLE:2"],
            )
        )
        g.domainRangeAxioms.append(
            obograph.DomainRangeAxiom(
                predicateId="RO:1",
                allValuesFromEdges=[
                    obograph.Edge(
                        sub="EXAMPLE:1",
                        pred="RO:1",
                        obj="EXAMPLE:2",
                    ),
                ],
            )
        )
        yaml_dumper.dump(g, output_path("example-ldefs.obograph.yaml"))
        self.attempt_streaming_writers(g.logicalDefinitionAxioms)

    def test_edge_meta(self):
        """
        Tests the ability to create edge metadata

        https://github.com/INCATools/ontology-access-kit/issues/428
        """
        g = obograph.Graph(id="test")
        g.edges.append(
            obograph.Edge(
                sub="EXAMPLE:10",
                pred="RO:1",
                obj="EXAMPLE:11",
                meta=obograph.Meta(
                    basicPropertyValues=[
                        obograph.BasicPropertyValue(pred="oio:is_inferred", val="true")
                    ]
                ),
            )
        )
        yaml_dumper.dump(g, output_path("example-edge-meta.obograph.yaml"))
        self.attempt_streaming_writers(g.logicalDefinitionAxioms)
