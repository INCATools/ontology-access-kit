import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

from sssom.parsers import parse_sssom_table, to_mapping_set_document
from sssom_schema import Mapping

from oaklib import conf as conf_package
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE, IS_A, LABEL_PREDICATE
from oaklib.mappers.base_mapper import Mapper
from oaklib.types import CURIE, URI


def get_conf_path(name: str):
    conf_path = os.path.dirname(conf_package.__file__)
    return str(Path(conf_path) / f"{name}.sssom.tsv")


def load_default_sssom(name: str) -> List[Mapping]:
    msdf = parse_sssom_table(get_conf_path(name))
    msd = to_mapping_set_document(msdf)
    return msd.mapping_set.mappings


@dataclass
class OntologyMetadataMapper(Mapper):
    """Maps ontology metadata such as labels."""

    def label_curie(self) -> CURIE:
        """Maps rdfs:label."""
        return self.map_curie(LABEL_PREDICATE, unmapped_reflexive=True, single_valued=True)[0]

    def label_uri(self) -> URI:
        """Maps rdfs:label."""
        return self.curie_converter.expand(self.label_curie())

    def definition_curie(self) -> CURIE:
        """Maps text definition property."""
        return self.map_curie(HAS_DEFINITION_CURIE, unmapped_reflexive=True, single_valued=True)[0]

    def definition_uri(self) -> URI:
        """Maps rdfs:label."""
        return self.curie_converter.expand(self.definition_curie())

    def is_a_curie(self) -> CURIE:
        """Maps rdfs:label."""
        return self.map_curie(IS_A, unmapped_reflexive=True, single_valued=True)[0]

    def is_a_uri(self) -> URI:
        """Maps rdfs:label."""
        return self.curie_converter.expand(self.is_a_curie())

    def use_skos_profile(self):
        """Sets the profile to SKOS."""
        self.add_mappings(load_default_sssom("omo-to-skos"))
