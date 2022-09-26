from typing import Tuple, Any, Optional, List

CURIE = str
LABEL = str
URI = str
PRED_CURIE = CURIE
SUBSET_CURIE = CURIE
CATEGORY_CURIE = CURIE
TAXON_CURIE = CURIE

ASSOCIATION_PROPERTY = Tuple[PRED_CURIE, Any, Optional["ASSOCIATION_PROPERTY"]]
"""Generic properties on an association."""

ASSOCIATION = Tuple[CURIE, PRED_CURIE, Any, List[ASSOCIATION_PROPERTY]]
"""Generation association/annotation."""
