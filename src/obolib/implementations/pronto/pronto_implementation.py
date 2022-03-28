from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Iterable, Type

from obolib.implementations.pronto.pronto import ProntoProvider
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    METADATA_MAP, SearchConfiguration
from obolib.interfaces.ontology_interface import OntologyInterface
from obolib.interfaces.qc_interface import QualityControlInterface
from obolib.interfaces.rdf_interface import RdfInterface
from obolib.interfaces.relation_graph_interface import RelationGraphInterface
from obolib.resource import OntologyResource
from obolib.types import CURIE
from obolib.vocabulary.vocabulary import LABEL_PREDICATE, IS_A
from pronto import Ontology, LiteralPropertyValue, ResourcePropertyValue


@dataclass
class ProntoImplementation(QualityControlInterface, RdfInterface, RelationGraphInterface):
    """
    Pronto wraps local-file based ontologies in the following formats:

    - obo
    - obojson
    - owl rdf/xml

    To load a local file:

    .. code:: python

        >>> resource = OntologyResource(slug='go.obo', directory='input', local=True)
        >>> oi = ProntoImplementation.create(resource)

    To load from the OBO library:

    .. code:: python

        >>> resource = OntologyResource(local=False, slug='go.obo'))
        >>> oi = ProntoImplementation.create(resource)

    Currently this implementation implements most of the BaseOntologyInterface

    .. code:: python

        rels = oi.get_outgoing_relationships_by_curie('GO:0005773')
        for rel, parents in rels.items():
            print(f'  {rel} ! {oi.get_label_by_curie(rel)}')
                for parent in parents:
                    print(f'    {parent} ! {oi.get_label_by_curie(parent)}')

    """
    engine: Ontology

    @classmethod
    def create(cls, resource: OntologyResource = None) -> "ProntoImplementation":
        ontology = ProntoProvider.create_engine(resource)
        return ProntoImplementation(ontology)

    def store(self, resource: OntologyResource) -> None:
        ProntoProvider.dump(self.engine, resource)

    def _term(self, curie: CURIE):
        if curie in self.engine:
            return self.engine[curie]
        else:
            return None

    def _create(self, curie: CURIE, exist_ok = True):
        if curie in self.engine:
            return self.engine[curie]
        else:
            return self.engine.create_term(curie)

    def _create_pred(self, curie: CURIE, exist_ok = True):
        if curie in self.engine:
            return self.engine[curie]
        else:
            return self.engine.create_relationship(curie)

    def all_entity_curies(self) -> Iterable[CURIE]:
        for t in self.engine.terms():
            yield t.id

    def get_label_by_curie(self, curie: CURIE):
        t = self._term(curie)
        if t:
            return t.name
        else:
            if curie == IS_A:
                return 'subClassOf'
            else:
                return None

    def get_curies_by_label(self, label: str) -> List[CURIE]:
        return [t.id for t in self.engine.terms() if t.name == label]

    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        term = self._term(curie)
        rels = {IS_A: [p.id for p in term.superclasses(distance=1)]}
        for rel_type, parents in term.relationships.items():
            rels[rel_type.id] = [p.id for p in parents]
        return rels

    def basic_search(self, search_term: str, config: SearchConfiguration = SearchConfiguration()) -> Iterable[CURIE]:
        matches = []
        for t in self.engine.terms():
            if search_term in t.name:
                matches.append(t.id)
                continue
            if config.include_aliases:
                for syn in t.synonyms:
                    if search_term in syn.description:
                        matches.append(t.id)
                        continue
        return matches


    def create_entity(self, curie: CURIE, label: str = None, relationships: RELATIONSHIP_MAP = None) -> CURIE:
        ont = self.engine
        t = ont.create_term(curie)
        t.name = label
        for pred, fillers in relationships.items():
            for filler in fillers:
                self.add_relationship(curie, pred, filler)
        return curie

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE):
        t = self._term(curie)
        filler_term = self._create(filler)
        if predicate == IS_A:
            t.superclasses().add(filler_term)
        else:
            predicate_term = self._create_pred(predicate)
            if predicate_term not in t.relationships.keys():
                t.relationships[predicate_term] = []
            t.relationships[predicate_term].add(filler_term)

    def get_definition_by_curie(self, curie: CURIE) -> str:
        """

        :param curie:
        :return:
        """
        return self._term(curie).definition

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        """

        :param curie:
        :return:
        """
        t = self._term(curie)
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [t.name]
        for s in t.synonyms:
            m[s.scope].append(s.description)
        return m

    def metadata_map_by_curie(self, curie: CURIE) -> METADATA_MAP:
        t = self._term(curie)
        m = defaultdict(list)
        for ann in t.annotations:
            p = ann.property
            if isinstance(ann, LiteralPropertyValue):
                m[ann.property].append(ann.literal)
            elif isinstance(ann, ResourcePropertyValue):
                m[ann.property].append(ann.resource)
        return m

    def create_subontology(self, curies: List[CURIE]) -> "ProntoImplementation":
        subontology = Ontology()
        for curie in curies:
            t = self._term(curie)
            subontology.create_term(curie)
            t2 = subontology[curie]
            t2.name = t.name
            # TODO
        typ: Type[OntologyInterface] = type(self)
        return typ(subontology)




