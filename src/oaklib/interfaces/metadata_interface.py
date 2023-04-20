from abc import ABC
from typing import Iterable, Iterator, List, Optional, Tuple

import oaklib.datamodels.ontology_metadata as om
from oaklib.datamodels.vocabulary import HAS_DEFINITION_CURIE
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

ENTITY_AGENT_PAIR = Tuple[CURIE, om.AgentId]


class MetadataInterface(BasicOntologyInterface, ABC):
    def statements_with_annotations(self, curie: CURIE) -> Iterable[om.Axiom]:
        raise NotImplementedError

    def definition_with_annotations(
        self, curie: CURIE
    ) -> Optional[Tuple[str, List[om.Annotation]]]:
        """
        Get the definition of a term, if it exists, along with any annotations.

        :param curie:
        :return:
        """
        for ax in self.statements_with_annotations(curie):
            if ax.annotatedProperty == HAS_DEFINITION_CURIE:
                return ax.annotatedTarget, ax.annotations

    def definitions_with_annotations(
        self, curies: Iterable[CURIE]
    ) -> Iterator[Tuple[str, List[om.Annotation]]]:
        """
        Get the definitions of a set of terms, if they exist, along with any annotations.

        :param curies:
        :return:
        """
        for curie in curies:
            defn_obj = self.definition_with_annotations(curie)
            if defn_obj:
                yield curie, defn_obj[0], defn_obj[1]
            else:
                yield curie, None, None

    def entities_contributors(
        self, curies: Iterable[CURIE], include_creator=True
    ) -> Iterator[ENTITY_AGENT_PAIR]:
        """
        Get the contributors of a set of entities.

        This SHOULD perform AnnotationPropertyNormalization, using all possible annotation properties,
        including:

        - dcterms:contributor
        - IAO:0000117 term editor

        By default, the creator (as defined by :ref:`entities_creators`) is included in the results.

        While there is no consensus on when and how to distinguish creators and contributors, the current
        emerging consensus of the OBO Ontology Metadata group is that these are hard to separate, and that
        it makes no sense to distinguish them in the metadata.

        See: https://github.com/information-artifact-ontology/ontology-metadata/issues/120

        :param curies: collection of entities to be looked up
        :param include_creator: if True, then the creator is included in the results
        :return:
        """
        raise NotImplementedError

    def entities_creators(self, curies: Iterable[CURIE]) -> Iterator[ENTITY_AGENT_PAIR]:
        """
        Get the creators of a set of entities.

        This SHOULD perform AnnotationPropertyNormalization, using all possible annotation properties,
        including:

        - oboInOwl:created_by
        - dcterms:creator

        See :ref:`entities_contributors` for more information on the difference between creators and contributors.

        :param curies: collection of entities to be looked up
        :return:
        """
        raise NotImplementedError
