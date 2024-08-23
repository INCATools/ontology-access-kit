import logging
import unittest
from copy import deepcopy

import yaml
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.introspection import package_schemaview

import oaklib.datamodels.ontology_metadata as om
from oaklib.datamodels.vocabulary import IS_A
from oaklib.implementations import SqlImplementation
from oaklib.implementations.sparql.sparql_implementation import SparqlImplementation
from oaklib.resource import OntologyResource
from oaklib.utilities.table_filler import (
    ColumnDependency,
    TableFiller,
    TableMetadata,
    parse_table,
    write_table,
)
from tests import IMBO, INPUT_DIR, NUCLEAR_ENVELOPE, NUCLEUS, OUTPUT_DIR

DB = INPUT_DIR / "go-nucleus.db"
FBBT_SUBSET = INPUT_DIR / "fbbt-cl-subset.owl.ttl"
TMP = OUTPUT_DIR / "tmp.tsv"
TMP2 = OUTPUT_DIR / "tmp2.tsv"
SSSOM_YAML = INPUT_DIR / "fill-sssom-table-relations.yaml"
EXAMPLE_SSSOM = INPUT_DIR / "cl-fbbt.sssom.tsv"


EXPECTED = [
    (
        """
        Populating labels from IDs
        """,
        [
            "# curie_map:\n",
            "#   X: http://purl.obolibrary.org/obo/X_\n",
            "#   Y: http://purl.obolibrary.org/obo/Y_\n",
            "#   Z: http://purl.obolibrary.org/obo/Z_\n",
            "# license: UNSPECIFIED\n",
            "# mapping_set_id: temp\n",
        ],
        [
            {"id": NUCLEUS, "label": None},
            {"id": NUCLEAR_ENVELOPE, "label": None},
        ],
        TableMetadata(dependencies=[ColumnDependency("id", "label", "label")]),
        [
            {"id": NUCLEUS, "label": "nucleus"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        True,
    ),
    (
        """
        Populating IDs from labels
        """,
        [
            "# curie_map:\n",
            "#   X: http://purl.obolibrary.org/obo/X_\n",
            "#   Y: http://purl.obolibrary.org/obo/Y_\n",
            "#   Z: http://purl.obolibrary.org/obo/Z_\n",
            "# license: UNSPECIFIED\n",
            "# mapping_set_id: temp\n",
        ],
        [
            {"id": None, "label": "nucleus"},
            {"id": None, "label": "nuclear envelope"},
        ],
        TableMetadata(dependencies=[ColumnDependency("id", "label", "label")]),
        [
            {"id": NUCLEUS, "label": "nucleus"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        True,
    ),
    (
        """
        Missing dependent in results throws error by default
        """,
        [],
        [
            {"id": "FAKE:0001", "label": None},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        TableMetadata(dependencies=[ColumnDependency("id", "label", "label")]),
        [],
        False,
    ),
    (
        """
        Missing pk in results throws error by default
        """,
        [],
        [
            {"id": None, "label": "no such thing"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        TableMetadata(dependencies=[ColumnDependency("id", "label", "label")]),
        [],
        False,
    ),
    (
        """
        Missing dependent must be explicitly allowed
        """,
        [],
        [
            {"id": "FAKE:0001", "label": None},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        TableMetadata(
            dependencies=[ColumnDependency("id", "label", "label", allow_missing_values=True)]
        ),
        [
            {"id": "FAKE:0001", "label": None},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        True,
    ),
    (
        """
        Missing dependent populated by missing value token
        """,
        [],
        [
            {"id": "FAKE:0001", "label": None},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        TableMetadata(
            dependencies=[
                ColumnDependency(
                    "id",
                    "label",
                    "label",
                    allow_missing_values=True,
                    missing_value_token="not a label",  # noqa
                )
            ]
        ),
        [
            {"id": "FAKE:0001", "label": "not a label"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        True,
    ),
    (
        """
        Missing pk must be explicitly allowed
        """,
        [],
        [
            {"id": None, "label": "no such thing"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        TableMetadata(
            dependencies=[ColumnDependency("id", "label", "label", allow_missing_values=True)]
        ),
        [
            {"id": None, "label": "no such thing"},
            {"id": NUCLEAR_ENVELOPE, "label": "nuclear envelope"},
        ],
        True,
    ),
]


class TestTableFiller(unittest.TestCase):
    def setUp(self) -> None:
        oi = SqlImplementation(OntologyResource(slug=f"sqlite:///{str(DB)}"))
        self.oi = oi
        self.table_filler = TableFiller(oi)

    def test_fill_table(self):
        tf = self.table_filler
        for desc, _, input_table, cfg, expected_table, expected_success in EXPECTED:
            logging.info(f"Test: {desc}")
            logging.info(desc)
            output_table = deepcopy(input_table)
            if expected_success:
                tf.fill_table(output_table, cfg)
                # for row in output_table:
                #    logging.info(row)
                self.assertEqual(expected_table, output_table)
            else:
                with self.assertRaises(ValueError):
                    tf.fill_table(output_table, cfg)
        rows = [
            {"id": NUCLEUS, "ancs": None},
        ]
        tm = TableMetadata(
            dependencies=[
                ColumnDependency("id", "ancestors", "ancs", parameters={"predicates": [IS_A]})
            ]
        )

        tf.fill_table(rows, tm)
        ancs = rows[0]["ancs"]
        self.assertIn(NUCLEUS, ancs)
        self.assertIn(IMBO, ancs)

    def test_fill_table_file(self):
        tf = self.table_filler
        for desc, comments, input_table, cfg, expected_table, expected_success in EXPECTED:
            logging.info(f"Test: {desc}")
            with open(TMP, "w", encoding="UTF-8") as input_file:
                write_table(input_table, input_file, comments=comments)
            with open(TMP) as input_file:
                with open(TMP2, "w", encoding="UTF-8") as output_file:
                    if expected_success:
                        tf.fill_table_file(input_file, output_file, cfg)
                        output_file.close()
                        with open(TMP2) as output_file_as_input:
                            output_table = parse_table(output_file_as_input)
                            self.assertEqual(expected_table, output_table)
                    else:
                        with self.assertRaises(ValueError):
                            tf.fill_table_file(input_file, output_file, cfg)

    def test_fill_sssom(self):
        tf = self.table_filler
        tf.ontology_interface = SparqlImplementation(OntologyResource(slug=FBBT_SUBSET))
        with open(EXAMPLE_SSSOM) as file:
            input_table = parse_table(file)
        tm = TableMetadata(dependencies=[])
        with open(SSSOM_YAML) as file:
            for dep in yaml.safe_load(file):
                tm.dependencies.append(ColumnDependency(**dep))
        tm.set_allow_missing_values(True)
        tf.fill_table(input_table, table_metadata=tm)
        labels = {row.get("object_name") for row in input_table}
        self.assertIn("spermatozoon", labels)
        self.assertIn("oocyte", labels)

    def test_infer_metadata_from_row(self):
        tf = self.table_filler
        tm = tf.infer_metadata({"id": "x", "label": "x", "foo": 5})
        self.assertEqual(1, len(tm.dependencies))
        dep = tm.dependencies[0]
        self.assertEqual("id", dep.primary_key)
        self.assertEqual("label", dep.dependent_column)
        self.assertEqual("label", dep.relation)

    def test_infer_metadata_from_denormalized(self):
        tf = self.table_filler
        tm = tf.infer_metadata(
            {
                "id": None,
                "subject_id": None,
                "subject_label": None,
                "object_id": None,
                "object_label": None,
                "description": None,
            }
        )
        self.assertEqual(2, len(tm.dependencies))
        [dep1] = [dep for dep in tm.dependencies if dep.primary_key == "subject_id"]
        [dep2] = [dep for dep in tm.dependencies if dep.primary_key == "object_id"]
        self.assertEqual("subject_id", dep1.primary_key)
        self.assertEqual("subject_label", dep1.dependent_column)
        self.assertEqual("label", dep1.relation)
        self.assertEqual("object_id", dep2.primary_key)
        self.assertEqual("object_label", dep2.dependent_column)
        self.assertEqual("label", dep2.relation)

    def test_infer_metadata_from_linkml(self):
        tf = self.table_filler
        sb = SchemaBuilder()
        foo_id = SlotDefinition("foo_id", identifier=True)
        foo_label = SlotDefinition("foo_label", slot_uri="rdfs:label")
        sb.add_slot(foo_id).add_slot(foo_label)
        sb.add_class("Person", [foo_id.name, foo_label.name])
        schema = sb.schema
        logging.info(yaml_dumper.dumps(schema))
        tm = tf.extract_metadata_from_linkml(schema)
        self.assertEqual(1, len(tm.dependencies))
        dep = tm.dependencies[0]
        self.assertEqual(foo_id.name, dep.primary_key)
        self.assertEqual(foo_label.name, dep.dependent_column)
        self.assertEqual("label", dep.relation)

    def test_infer_metadata_from_ontology_metadata(self):
        tf = self.table_filler
        sv = package_schemaview(om.__name__)
        tm = tf.extract_metadata_from_linkml(sv.schema, class_name="Class")
        self.assertEqual(2, len(tm.dependencies))
        [dep1] = [dep for dep in tm.dependencies if dep.relation == "label"]
        [dep2] = [dep for dep in tm.dependencies if dep.relation == "definition"]
        self.assertEqual("id", dep1.primary_key)
        self.assertEqual("label", dep1.dependent_column)
        self.assertEqual("label", dep1.relation)
        self.assertEqual("id", dep2.primary_key)
        self.assertEqual("definition", dep2.dependent_column)
        self.assertEqual("definition", dep2.relation)
