import logging
import unittest

from oaklib.datamodels.association import Association, NegatedAssociation, ParserConfiguration
from oaklib.parsers import GAF
from oaklib.parsers.association_parser_factory import get_association_parser
from tests import INPUT_DIR

INPUT_GAF = INPUT_DIR / "test-uniprot.gaf"


class GafAssociationParserTest(unittest.TestCase):
    """Tests parsing of GAF and GAF-like formats."""

    def test_parser(self):
        """Tests parsing associations."""
        parser = get_association_parser(GAF)
        for preserve_negated_associations in [True, False]:
            config = ParserConfiguration(
                preserve_negated_associations=preserve_negated_associations
            )
            with open(INPUT_GAF) as file:
                assocs = list(parser.parse(file, configuration=config))
                for association in assocs:
                    logging.info(association)
                self.assertIn(
                    Association(
                        subject="UniProtKB:Q9BPZ7",
                        subject_label="MAPKAP1",
                        predicate="is_active_in",
                        object="GO:0005737",
                        property_values=[],
                        evidence_type="IBA",
                        publications=["PMID:21873635"],
                        primary_knowledge_source="infores:GO_Central",
                    ),
                    assocs,
                )
                if preserve_negated_associations:
                    self.assertIn(
                        NegatedAssociation(
                            subject="UniProtKB:FAKE123",
                            subject_label="fake",
                            predicate="located_in",
                            negated=True,
                            object="GO:0005737",
                            property_values=[],
                            evidence_type="IBA",
                            publications=["PMID:21873635"],
                            primary_knowledge_source="infores:GO_Central",
                        ),
                        assocs,
                        "expected to find negated association",
                    )
                else:
                    self.assertNotIn(
                        "UniProtKB:FAKE123",
                        [a.subject for a in assocs],
                        "by default, negated associations should be filtered",
                    )
