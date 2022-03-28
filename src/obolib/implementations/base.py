from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Iterable

from obolib.implementations.pronto.pronto import ProntoProvider
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    METADATA_MAP
from obolib.interfaces.qc_interface import QualityControlInterface
from obolib.interfaces.rdf_interface import RdfInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE
from obolib.vocabulary.vocabulary import LABEL_PREDICATE, IS_A
from pronto import Ontology, LiteralPropertyValue, ResourcePropertyValue


@dataclass
class BaseImpl(QualityControlInterface, RdfInterface):