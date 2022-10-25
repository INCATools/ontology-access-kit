from dataclasses import dataclass, field
from typing import ClassVar, List, Iterable, Dict

from oaklib.implementations.bitwise.bitwise_utils import BITMAP, POS
from oaklib.types import CURIE


@dataclass
class BitwiseOntologyIndex:
    """
    A fast index for an ontology.

    Every entity is mapped to an integer (POS).
    """

    curie_to_int: Dict[CURIE, POS] = None
    """Maps CURIEs to integer indices."""

    int_to_curie: Dict[POS, CURIE] = None
    """Maps integer indices to CURIEs."""

    information_content_map: Dict[POS, float] = None
    """Maps entities to their information content."""

    ancestor_map: Dict[POS, List[POS]] = None
    """Maps an entity by index to its ancestors (represented as index list)."""

    ancestors_map_bitmap: Dict[POS, BITMAP] = None
    """Maps an entity by index to its ancestors (represented as bitmap)."""

    association_map: Dict[POS, List[POS]] = None
    """Maps an entity by index to its associated terms including closure (represented as an index list)."""

    association_map_bitmap: Dict[POS, BITMAP] = None
    """Maps an entity by index to its associated terms including closure (represented as a bitmap)."""

    term_pair_jaccard_index: Dict[tuple[POS, POS], float] = None
    """Term similarity."""

    term_pair_max_information_content: Dict[tuple[POS, POS], float] = None
    """Term max IC."""

    term_pair_best_ancestor: Dict[tuple[POS, POS], List[POS]] = None


