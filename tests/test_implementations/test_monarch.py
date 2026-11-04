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
    "in_taxon": "NCBITaxon:9606",
}

# Clinical measurement (LOINC): ``name`` is the LOINC long common name.
SERUM_POTASSIUM = {
    "id": "LOINC:2823-3",
    "category": "biolink:ClinicalMeasurement",
    "name": "Potassium [Moles/volume] in Serum or Plasma",
    "symbol": None,
    "description": None,
    "xrefs": [],
    "in_taxon": None,
}

# Hypothetical payload with no ``name``: the ``symbol`` fallback is kept for it.
SYMBOL_ONLY = {"id": "HGNC:0", "category": "biolink:Gene", "symbol": "SYMONLY", "xrefs": []}

# CURIE for which the fake API answers HTTP 500.
SERVER_ERROR_CURIE = "HP:0000500"

ENTITIES = {e["id"]: e for e in (HYPERKALEMIA, BRCA1, SERUM_POTASSIUM, SYMBOL_ONLY)}


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
        if curie == SERVER_ERROR_CURIE:
            return _fake_response(500)
        return _fake_response(404)
    if url.startswith(f"{BASE_URL}/association/all"):
        return _fake_response(200, {"items": [], "total": 0})
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

    def test_label_falls_back_to_symbol(self):
        self.assertEqual(self.oi.label("HGNC:0"), "SYMONLY")

    def test_server_error_returns_id_only_node_unless_strict(self):
        with self.assertLogs(
            "oaklib.implementations.monarch.monarch_implementation", level="WARNING"
        ) as logs:
            node = self.oi.node(SERVER_ERROR_CURIE)
        self.assertEqual(node.id, SERVER_ERROR_CURIE)
        self.assertIsNone(node.lbl)
        self.assertTrue(any("500" in line for line in logs.output))
        self.assertIsNone(self.oi.node(SERVER_ERROR_CURIE, strict=True))

    def test_relationships_skip_null_in_taxon(self):
        # Non-gene entities carry the key with a null value; yielding an
        # empty object used to break graph traversal with "Got an empty filler".
        self.assertEqual(list(self.oi.relationships(subjects=["LOINC:2823-3"])), [])
        self.assertEqual(
            list(self.oi.relationships(subjects=["HGNC:1100"])),
            [("HGNC:1100", "RO:0002162", "NCBITaxon:9606")],
        )

    def test_unknown_entity(self):
        self.assertIsNone(self.oi.node("LOINC:0000000-9"))
        self.assertIsNone(self.oi.label("LOINC:0000000-9"))


if __name__ == "__main__":
    unittest.main()
