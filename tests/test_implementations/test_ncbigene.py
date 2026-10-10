import unittest
from unittest.mock import MagicMock, patch
from xml.etree import ElementTree  # noqa S405

from oaklib import get_adapter
from oaklib.implementations import NCBIGeneImplementation
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from tests import CYTOPLASM, INPUT_DIR
from tests.input.mock_ncbi_objects import NCBI_ASSOCIATIONS

GENE_PATH = INPUT_DIR / "ncbigene-1956.xml"


class TestNCBIGene(unittest.TestCase):
    """
    Tests :ref:`NCBIGeneImplementation`
    """

    def setUp(self) -> None:
        self.adapter = get_adapter("NCBIGene:")
        self.mock_assocs = NCBI_ASSOCIATIONS

    def test_query(self):
        """Tests basic query."""
        adapter = MagicMock(spec=AssociationProviderInterface)
        adapter.associations.return_value = iter(self.mock_assocs)

        if not isinstance(adapter, AssociationProviderInterface):
            raise TypeError("adapter is not an AssociationProviderInterface")
        assocs = list(adapter.associations(subjects=["NCBIGene:1956"]))
        self.assertEqual(assocs, self.mock_assocs)
        self.assertGreater(len(assocs), 0)
        adapter.associations.assert_called_once_with(subjects=["NCBIGene:1956"])

    def test_parse_gene_xml(self):
        """Tests parsing gene XML."""
        adapter = self.adapter
        root = ElementTree.parse(str(GENE_PATH)).getroot()  # noqa S314
        if not isinstance(adapter, NCBIGeneImplementation):
            raise AssertionError
        assocs = list(adapter._go_associations_from_xml("NCBIGene:1956", root))
        self.assertGreater(len(assocs), 0)
        self.assertEqual(assocs[0].subject, "NCBIGene:1956")
        found = 0
        for assoc in assocs:
            if assoc.object == CYTOPLASM:
                if set(assoc.publications) == {"PMID:7588596", "PMID:12435727", "PMID:22298428"}:
                    if assoc.evidence_type == "IDA":
                        found += 1
        self.assertEqual(found, 1)

    def test_labels_cache_miss_fetches_esummary(self):
        """Tests that labels() fetches missing labels via esummary, batched and cached."""
        adapter = self.adapter
        response = MagicMock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "result": {
                "12810": {"name": "Coch"},
                "1956": {"name": "EGFR"},
            }
        }
        with patch.object(
            adapter.requests_session, "get", return_value=response
        ) as mock_get:
            labels = list(adapter.labels(["NCBIGene:12810", "NCBIGene:1956"]))
            self.assertEqual(labels, [("NCBIGene:12810", "Coch"), ("NCBIGene:1956", "EGFR")])
            self.assertEqual(mock_get.call_count, 1)
            self.assertEqual(
                mock_get.call_args[0][1],
                {"db": "gene", "id": "12810,1956", "retmode": "json"},
            )
            # second call should be served from the property cache
            labels = list(adapter.labels(["NCBIGene:12810"]))
            self.assertEqual(labels, [("NCBIGene:12810", "Coch")])
            self.assertEqual(mock_get.call_count, 1)
