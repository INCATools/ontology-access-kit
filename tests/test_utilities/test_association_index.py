import unittest

from oaklib.interfaces.association_provider_interface import (
    associations_objects,
    associations_subjects,
)
from oaklib.parsers.parser_base import ColumnReference
from oaklib.parsers.xaf_association_parser import XafAssociationParser
from oaklib.utilities.associations.association_index import AssociationIndex
from tests import INPUT_DIR

GAF = INPUT_DIR / "test-uniprot.gaf"


class AssociationIndexTest(unittest.TestCase):
    """Tests indexing associations in-memory."""

    def test_index(self):
        """Tests in-memory index by loading from GAF."""
        parser = XafAssociationParser(
            subject_column=ColumnReference(1), object_column=ColumnReference(4)
        )
        ix = AssociationIndex()
        ix.create()
        with open(GAF) as file:
            associations = list(parser.parse(file))
            print(associations)
            ix.populate(associations)
            retrieved = list(ix.lookup())
            for r in retrieved:
                print(r)
                self.assertIn(r, associations)
            for a in associations:
                self.assertIn(a, retrieved)
            proteins = list(associations_subjects(associations))
            terms = list(associations_objects(associations))
            for pr in proteins[0:3]:
                retrieved = list(ix.lookup(subjects=[pr]))
                expected = [a for a in associations if a.subject == pr]
                self.assertCountEqual(
                    list(associations_objects(expected)), list(associations_objects(retrieved))
                )
            for t in terms[0:3]:
                retrieved = list(ix.lookup(objects=[t]))
                expected = [a for a in associations if a.object == t]
                self.assertCountEqual(
                    list(associations_objects(expected)), list(associations_objects(retrieved))
                )
