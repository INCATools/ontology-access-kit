import logging
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Iterable, Iterator, Union

import pronto
import sssom
from deprecated import deprecated
from linkml_runtime.dumpers import json_dumper
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.interfaces.basic_ontology_interface import RELATIONSHIP_MAP, PRED_CURIE, ALIAS_MAP, \
    METADATA_MAP, PREFIX_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.datamodels.search import SearchConfiguration
from oaklib.interfaces.validator_interface import ValidatorInterface
from oaklib.interfaces.rdf_interface import RdfInterface
from oaklib.interfaces.relation_graph_interface import RelationGraphInterface
from oaklib.resource import OntologyResource
from oaklib.types import CURIE, SUBSET_CURIE
from oaklib.datamodels import obograph
from oaklib.datamodels.obograph import Edge, Graph, GraphDocument
from oaklib.datamodels.vocabulary import LABEL_PREDICATE, IS_A, HAS_DBXREF, SCOPE_TO_SYNONYM_PRED_MAP, SKOS_CLOSE_MATCH
from pronto import Ontology, LiteralPropertyValue, ResourcePropertyValue, Term
from sssom.sssom_datamodel import MatchTypeEnum


@dataclass
class ProntoImplementation(ValidatorInterface, RdfInterface, OboGraphInterface, SearchInterface, MappingProviderInterface):
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
    wrapped_ontology: Ontology = None

    def __post_init__(self):
        if self.wrapped_ontology is None:
            resource = self.resource
            if resource is None:
                ontology = Ontology()
            elif resource.local:
                ontology = Ontology(str(resource.local_path))
            else:
                ontology = Ontology.from_obo_library(resource.slug)
            self.wrapped_ontology = ontology

    @classmethod
    @deprecated('old style')
    def create(cls, resource: OntologyResource = None) -> "ProntoImplementation":
        return ProntoImplementation(resource=resource)

    def store(self, resource: OntologyResource = None) -> None:
        if resource is None:
            resource = self.resource
        ontology = self.wrapped_ontology
        if resource.local:
            with open(str(resource.local_path), 'wb') as f:
                ontology.dump(f, format=resource.format)
        else:
            raise NotImplementedError(f'Cannot dump to {resource}')

    def load_graph(self, graph: Graph, replace: True) -> None:
        if replace:
            ont = self.wrapped_ontology
        else:
            ont = Ontology()
            self.wrapped_ontology = ont
        for n in graph.nodes:
            if n == IS_A:
                pass
            else:
                self.create_entity(n.id, n.lbl)
        for e in graph.edges:
            self.add_relationship(e.sub, e.pred, e.obj)

    @deprecated('Use this when we fix https://github.com/fastobo/fastobo/issues/42')
    def load_graph_using_jsondoc(self, graph: Graph, replace: True) -> None:
        tf = tempfile.NamedTemporaryFile()
        tf_name = '/tmp/tf.json'
        gd = GraphDocument(graphs=[graph])
        json_dumper.dump(gd, to_file=tf_name)
        tf.flush()
        print(f'{tf_name}')
        ont = Ontology(tf_name)
        if replace:
            self.wrapped_ontology = ont
        else:
            raise NotImplementedError


    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_prefix_map(self) -> PREFIX_MAP:
        return {}

    def _entity(self, curie: CURIE):
        for r in self.wrapped_ontology.relationships():
            # see https://owlcollab.github.io/oboformat/doc/obo-syntax.html#4.4.1
            # pronto gives relations shorthand IDs for RO and BFO, as it is providing
            # oboformat as a level of abstraction. We want to map these back to the CURIEs
            if r.id == curie:
                return r
            if curie.startswith('RO:') or curie.startswith('BFO:'):
                if any(x for x in r.xrefs if x.id == curie):
                    return r
        if curie in self.wrapped_ontology:
            return self.wrapped_ontology[curie]
        else:
            return None

    def _create(self, curie: CURIE, exist_ok = True):
        if curie in self.wrapped_ontology:
            return self.wrapped_ontology[curie]
        else:
            return self.wrapped_ontology.create_term(curie)

    def _create_pred(self, curie: CURIE, exist_ok = True):
        if curie in self.wrapped_ontology:
            return self.wrapped_ontology[curie]
        else:
            return self.wrapped_ontology.create_relationship(curie)

    def all_entity_curies(self) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.terms():
            yield t.id
        # note what Pronto calls "relationship" is actually "relationship type"
        for t in self.wrapped_ontology.relationships():
            yield t.id
        for t in self.wrapped_ontology.synonym_types():
            yield t.id

    def all_subset_curies(self) -> Iterable[CURIE]:
        subsets = set()
        for t in self.wrapped_ontology.terms():
            subsets.update(t.subsets)
        for subset in subsets:
            yield subset

    def curies_by_subset(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        for t in self.wrapped_ontology.terms():
            if subset in t.subsets:
                yield t.id

    def get_label_by_curie(self, curie: CURIE) -> str:
        t = self._entity(curie)
        if t:
            return t.name
        else:
            if curie == IS_A:
                return 'subClassOf'
            else:
                return None

    def set_label_for_curie(self, curie: CURIE, label: str) -> bool:
        t = self._entity(curie)
        if t:
            curr = t.name
            if curr != label:
                t.name = label
                return True
            else:
                return False

    def get_curies_by_label(self, label: str) -> List[CURIE]:
        return [t.id for t in self.wrapped_ontology.terms() if t.name == label]

    def _get_pronto_relationship_type_curie(self, rel_type: pronto.Relationship) -> CURIE:
        for x in rel_type.xrefs:
            if x.id.startswith('BFO:') or x.id.startswith('RO:'):
                return x.id
        return rel_type.id


    def get_outgoing_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        # See: https://github.com/althonos/pronto/issues/119
        term = self._entity(curie)
        if isinstance(term, Term):
            # only "Terms" in pronto have relationships
            rels = {IS_A: [p.id for p in term.superclasses(distance=1) if p.id != curie]}
            for rel_type, parents in term.relationships.items():
                pred = self._get_pronto_relationship_type_curie(rel_type)
                rels[pred] = [p.id for p in parents]
        else:
            rels = {}
        return rels

    def get_incoming_relationships_by_curie(self, curie: CURIE, isa_only: bool = False) -> RELATIONSHIP_MAP:
        term = self._entity(curie)
        if isinstance(term, Term):
            # only "Terms" in pronto have relationships
            rels = {IS_A: [p.id for p in term.subclasses(distance=1) if p.id != curie]}
            for xt in self.wrapped_ontology.terms():
                for rel_type, parents in xt.relationships.items():
                    pred = self._get_pronto_relationship_type_curie(rel_type)
                    for p in parents:
                        if curie == p.id:
                            if pred not in rels:
                                rels[pred] = []
                            rels[pred].append(xt.id)
        else:
            rels = {}
        return rels


    def create_entity(self, curie: CURIE, label: str = None, relationships: RELATIONSHIP_MAP = None) -> CURIE:
        ont = self.wrapped_ontology
        t = ont.create_term(curie)
        t.name = label
        if relationships:
            for pred, fillers in relationships.items():
                for filler in fillers:
                    self.add_relationship(curie, pred, filler)
        return curie

    def add_relationship(self, curie: CURIE, predicate: PRED_CURIE, filler: CURIE):
        t = self._entity(curie)
        filler_term = self._create(filler)
        if predicate == IS_A:
            t.superclasses().add(filler_term)
        else:
            predicate_term = self._create_pred(predicate)
            if predicate_term not in t.relationships.keys():
                t.relationships[predicate_term] = []
            t.relationships[predicate_term].add(filler_term)

    def get_definition_by_curie(self, curie: CURIE) -> str:
        return self._entity(curie).definition

    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        t = self._entity(curie)
        if t is None:
            return {}
        m = defaultdict(list)
        m[LABEL_PREDICATE] = [t.name]
        for s in t.synonyms:
            scope = s.scope.upper()
            if scope in SCOPE_TO_SYNONYM_PRED_MAP:
                pred = SCOPE_TO_SYNONYM_PRED_MAP[scope]
            else:
                raise ValueError(f'Unknown scope: {scope}')
            m[pred].append(s.description)
        return m

    def get_simple_mappings_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        m = defaultdict(list)
        t = self._entity(curie)
        if t is None:
            return m
        for s in t.xrefs:
            m[HAS_DBXREF].append(s.id)
        for s in t.annotations:
            # TODO: less hacky
            if s.property.startswith('skos'):
                if isinstance(s, LiteralPropertyValue):
                    v = s.literal
                    m[s.property].append(v)
                elif isinstance(s, ResourcePropertyValue):
                    v = self.uri_to_curie(s.resource)
                else:
                    v = None
                if v:
                    m[s.property].append(v)
        return m

    def metadata_map_by_curie(self, curie: CURIE) -> METADATA_MAP:
        t = self._entity(curie)
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
            t = self._entity(curie)
            subontology.create_term(curie)
            t2 = subontology[curie]
            t2.name = t.name
            # TODO - complete object
        return ProntoImplementation(wrapped_ontology=subontology)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[sssom.Mapping]:
        t = self._entity(curie)
        if t:
            for x in t.xrefs:
                yield sssom.Mapping(subject_id=curie,
                                    predicate_id=SKOS_CLOSE_MATCH,
                                    object_id=x.id,
                                    match_type=MatchTypeEnum.Lexical)
        # TODO: use a cache to avoid re-calculating
        for e in self.all_entity_curies():
            t = self._entity(curie)
            if t:
                for x in t.xrefs:
                    if x.id == curie:
                        yield sssom.Mapping(subject_id=e,
                                            predicate_id=SKOS_CLOSE_MATCH,
                                            object_id=curie,
                                            match_type=MatchTypeEnum.Lexical)



    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(self, curie: CURIE, strict=False) -> obograph.Node:
        t = self._entity(curie)
        if t is None:
            return obograph.Node(id=curie)
        else:
            meta = obograph.Meta()
            if t.definition:
                meta.definition = obograph.DefinitionPropertyValue(val=t.definition)
            if isinstance(t, pronto.Relationship):
                t_id = self._get_pronto_relationship_type_curie(t)
            else:
                t_id = t.id
            if isinstance(t, pronto.Relationship):
                for x in t.xrefs:
                    if x.id.startswith('RO:') or x.id.startswith('BFO:'):
                        t_id = x.id
            #for s in t.synonyms:
            #    meta.synonyms.append(obograph.SynonymPropertyValue(val=s.description,
            #                                                       scope=s.scope.lower(),
            #                                                      xrefs=[x.id for x in s.xrefs]))
            return obograph.Node(id=t_id,
                                 lbl=t.name,
                                 meta=meta)

    def as_obograph(self) -> Graph:
        nodes = [self.node(curie) for curie in self.all_entity_curies()]
        edges = [Edge(sub=r[0], pred=r[1], obj=r[2]) for r in self.all_relationships()]
        return Graph(id='TODO', nodes=nodes, edges=edges)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        if config == None:
            config = SearchConfiguration()
        matches = []
        mfunc = None
        if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
            mfunc = lambda label: str(label).startswith(search_term)
        elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
            import re
            prog = re.compile(search_term)
            mfunc = lambda label: prog.match(label)
        elif config.is_partial:
            mfunc = lambda label: search_term in str(label)
        else:
            mfunc = lambda label: label == search_term
        for t in self.wrapped_ontology.terms():
            if t.name and mfunc(t.name):
                matches.append(t.id)
                logging.info(f'Name match to {t.id}')
                continue
            if SearchProperty(SearchProperty.ALIAS) in config.properties:
                for syn in t.synonyms:
                    if mfunc(syn.description):
                        logging.info(f'Syn match to {t.id}')
                        matches.append(t.id)
                        continue
        return matches

