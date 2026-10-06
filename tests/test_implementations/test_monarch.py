"""Tests for the Monarch API implementation.

The Monarch v3 API is mocked so these tests run offline. The payloads are
trimmed copies of real ``/v3/api/entity/{id}`` responses recorded on 2026-10-06.
"""

import unittest
from unittest.mock import MagicMock

from oaklib.implementations.monarch.monarch_implementation import (
    BASE_URL,
    MonarchImplementation,
)

# Ontology class: ``name`` is set, ``symbol`` is not.
HYPERKALEMIA = {
    "id": "HP:0002153",
    "category": "biolink:PhenotypicFeature",
    "name": "Hyperkalemia",
    "symbol": None,
    "description": (
        "The concentration of potassium(1+) in the blood circulation is above the "
        "upper limit of normal."
    ),
    "xrefs": ["UMLS:C0020461"],
}

# Gene: ``name`` and ``symbol`` are both the gene symbol.
BRCA1 = {
    "id": "HGNC:1100",
    "category": "biolink:Gene",
    "name": "BRCA1",
    "symbol": "BRCA1",
    "full_name": "BRCA1 DNA repair associated",
    "xrefs": [],
}

# Clinical measurement (LOINC): ``name`` is the LOINC long common name.
SERUM_POTASSIUM = {
    "id": "LOINC:2823-3",
    "category": "biolink:ClinicalMeasurement",
    "name": "Potassium [Moles/volume] in Serum or Plasma",
    "symbol": None,
    "description": None,
    "xrefs": [],
}

ENTITIES = {e["id"]: e for e in (HYPERKALEMIA, BRCA1, SERUM_POTASSIUM)}


def _fake_response(status_code: int, payload=None) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = payload if payload is not None else {}
    response.text = ""
    return response


def _fake_get(url: str, **_kwargs) -> MagicMock:
    prefix = f"{BASE_URL}/entity/"
    if url.startswith(prefix):
        curie = url[len(prefix) :]
        if curie in ENTITIES:
            return _fake_response(200, ENTITIES[curie])
        return _fake_response(404)
    raise AssertionError(f"unexpected URL in test: {url}")


class TestMonarchImplementation(unittest.TestCase):
    def setUp(self) -> None:
        session = MagicMock()
        session.get.side_effect = _fake_get
        self.oi = MonarchImplementation(_requests_session=session)

    def test_base_url_is_https(self):
        self.assertTrue(BASE_URL.startswith("https://"))

    def test_label_for_ontology_class(self):
        # ``symbol`` is None for an ontology class; the label comes from ``name``
        self.assertEqual(self.oi.label("HP:0002153"), "Hyperkalemia")

    def test_label_for_clinical_measurement(self):
        self.assertEqual(
            self.oi.label("LOINC:2823-3"), "Potassium [Moles/volume] in Serum or Plasma"
        )

    def test_label_for_gene_is_symbol(self):
        self.assertEqual(self.oi.label("HGNC:1100"), "BRCA1")

    def test_node_carries_definition_and_xrefs(self):
        node = self.oi.node("HP:0002153")
        self.assertEqual(node.id, "HP:0002153")
        self.assertEqual(node.lbl, "Hyperkalemia")
        self.assertIn("above the upper limit of normal", node.meta.definition.val)
        self.assertEqual([x.val for x in node.meta.xrefs], ["UMLS:C0020461"])
        self.assertEqual(
            self.oi.definition("HP:0002153"),
            HYPERKALEMIA["description"],
        )

    def test_unknown_entity(self):
        self.assertIsNone(self.oi.node("LOINC:0000000-9"))
        self.assertIsNone(self.oi.label("LOINC:0000000-9"))


if __name__ == "__main__":
    unittest.main()
