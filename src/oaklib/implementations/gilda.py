"""A text annotator based on Gilda."""

from dataclasses import dataclass

from oaklib.interfaces import TextAnnotatorInterface

__all__ = [
    "GildaImplementation",
]


@dataclass
class GildaImplementation(TextAnnotatorInterface):
    """Perform named entity normalization on text strings with Gilda [gyori2021]_.

    .. [gyori2021] Benjamin M Gyori, Charles Tapley Hoyt, Albert Steppi (2021)
        `Gilda: biomedical entity text normalization with machine-learned
        disambiguation as a service <https://doi.org/10.1093/bioadv/vbac034>`_,
        *Bioinformatics Advances*, Volume 2, Issue 1, 2022, vbac034,
    """

    # TODO implement
