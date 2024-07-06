from dataclasses import dataclass
from typing import Dict, List, Optional

import click
import numpy as np

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.datamodels.association import Association
from oaklib.interfaces.association_provider_interface import AssociationProviderInterface
from oaklib.io.streaming_csv_writer import StreamingCsvWriter
from oaklib.types import CURIE


@dataclass
class MatrixData:
    arr: np.ndarray
    subject_index: Dict[CURIE, int]
    object_index: Dict[CURIE, int]
    subject_index_rev: Optional[Dict[int, CURIE]] = None
    object_index_rev: Optional[Dict[int, CURIE]] = None

    def lookup_subject(self, subject: CURIE) -> List[int]:
        """
        Look up a row in the matrix.

        :param subject:
        :return:
        """
        subject_ix = self.subject_index.get(subject)
        if subject_ix is None:
            return []
        row = self.arr[subject_ix, :]
        return np.where(row > 0)[0].tolist()

    def lookup_object(self, object: CURIE) -> List[int]:
        """
        Look up a column in the matrix.

        :param object:
        :return:
        """
        object_ix = self.object_index.get(object)
        if object_ix is None:
            return []
        column = self.arr[:, object_ix]
        return np.where(column > 0)[0].tolist()

    def object_ic(self, object: CURIE) -> Optional[float]:
        """
        Calculate the information content of an object.

        IC is log2 of the frequency of the object.

        :param object:
        :return:
        """
        object_ix = self.object_index.get(object)
        if object_ix is None:
            return None
        column = self.arr[:, object_ix]
        freq = np.sum(column) / self.arr.shape[0]
        return -np.log2(freq)


def associations_to_matrix(associations: List[Association]) -> MatrixData:
    """
    Convert a list of associations to a matrix.

    >>> from oaklib.datamodels.association import Association
    >>> assoc_pairs = [("G1", ["E1", "E2"]), ("G2", ["E2", "E3"])]
    >>> associations = [Association(subject=subject,
    ...                 object_closure=object_closure) for subject, object_closure in assoc_pairs]
    >>> md = associations_to_matrix(associations)
    >>> md.arr.shape
    (2, 3)
    >>> sorted([md.object_index_rev[i] for i in md.lookup_subject("G1")])
    ['E1', 'E2']
    >>> sorted([md.object_index_rev[i] for i in md.lookup_subject("G2")])
    ['E2', 'E3']
    >>> md.object_ic("E1")
    1.0
    >>> floor(md.object_ic("E2"))
    0
    >>> md.object_ic("E3")
    1.0
    >>> assert md.object_ic("E_MADE_UP") is None

    :param associations:
    :param adapter:
    :param entities_by_term:
    :return:
    """
    subjects = set()
    objects = set()
    for association in associations:
        subjects.add(association.subject)
        objects.update(association.object_closure)
    matrix = np.zeros((len(subjects), len(objects)))
    subject_ix = {term: index for index, term in enumerate(subjects)}
    object_ix = {term: index for index, term in enumerate(objects)}
    subject_ix_rev = {index: term for term, index in subject_ix.items()}
    object_ix_rev = {index: term for term, index in object_ix.items()}
    for association in associations:
        subject = association.subject
        for object in association.object_closure:
            matrix[subject_ix[subject], object_ix[object]] = 1
    md = MatrixData(arr=matrix, subject_index=subject_ix, object_index=object_ix)
    md.subject_index_rev = subject_ix_rev
    md.object_index_rev = object_ix_rev
    return md


def calculate_edge_information(
    child_term: CURIE, parent_term: CURIE, matrix: MatrixData
) -> Optional[float]:
    """
    Calculate edge information.

    :param adapter:
    :param subject:
    :param object:
    :param entities_by_term:
    :return:
    """
    child_ic = matrix.object_ic(child_term)
    parent_ic = matrix.object_ic(parent_term)
    return child_ic - parent_ic if child_ic is not None and parent_ic is not None else None


# make this a click command
@click.command()
@click.option("--ont-adapter-handle", help="The ontology adapter handle.")
@click.option("--assoc-adapter-handle", help="The association adapter handle.")
def calculate_all(ont_adapter_handle: str, assoc_adapter_handle: str):
    """
    Calculate all the edge information.

    :param ont_adapter_handle:
    :param assoc_adapter_handle:
    :return:
    """
    ont_adapter = get_adapter(ont_adapter_handle)
    assoc_adapter = get_adapter(assoc_adapter_handle)
    if not isinstance(ont_adapter, BasicOntologyInterface):
        raise ValueError("Ontology adapter must be a BasicOntologyInterface.")
    if not isinstance(assoc_adapter, AssociationProviderInterface):
        raise ValueError("Association adapter must be an AssociationProviderInterface.")
    assocs = list(assoc_adapter.associations())
    matrix = associations_to_matrix(assocs)
    writer = StreamingCsvWriter(ontology_interface=ont_adapter)
    for s, p, o in ont_adapter.relationships():
        edge_info = calculate_edge_information(s, o, matrix)
        if edge_info is not None:
            writer.emit(
                {"subject": s, "predicate": p, "object": o, "edge_information": edge_info},
                label_fields=["subject", "object"],
            )
    return ont_adapter, matrix
