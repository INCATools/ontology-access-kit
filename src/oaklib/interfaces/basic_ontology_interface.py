import itertools
import logging
from abc import ABC
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

import curies
from deprecation import deprecated
from prefixmaps.io.parser import load_context
from sssom.parsers import parse_sssom_table, to_mapping_set_document

from oaklib.datamodels.vocabulary import (
    DEFAULT_PREFIX_MAP,
    HAS_ONTOLOGY_ROOT_TERM,
    IS_A,
    IS_DEFINED_BY,
    LABEL_PREDICATE,
    OBSOLETION_RELATIONSHIP_PREDICATES,
    OWL_CLASS,
    OWL_NOTHING,
    OWL_THING,
    PREFIX_PREDICATE,
    URL_PREDICATE,
)
from oaklib.indexes.edge_index import EdgeIndex
from oaklib.interfaces.ontology_interface import OntologyInterface
from oaklib.mappers.ontology_metadata_mapper import OntologyMetadataMapper
from oaklib.types import CATEGORY_CURIE, CURIE, PRED_CURIE, SUBSET_CURIE, URI
from oaklib.utilities.basic_utils import get_curie_prefix, pairs_as_dict
from oaklib.utilities.iterator_utils import chunk
from oaklib.utilities.keyval_cache import KeyValCache

LANGUAGE_TAG = str
NC_NAME = str
PREFIX_MAP = Mapping[NC_NAME, URI]
RELATIONSHIP_MAP = Dict[PRED_CURIE, List[CURIE]]
ALIAS_MAP = Dict[PRED_CURIE, List[str]]
METADATA_MAP = Dict[PRED_CURIE, List[str]]
# ANNOTATED_METADATA_MAP = Dict[PRED_CURIE, List[Tuple[str, METADATA_MAP]]]
RELATIONSHIP = Tuple[CURIE, PRED_CURIE, CURIE]
DATATYPE = CURIE
LITERAL_METADATA_STATEMENT = Tuple[CURIE, PRED_CURIE, Any, DATATYPE, Optional[METADATA_MAP]]
OBJECT_METADATA_STATEMENT = Tuple[CURIE, PRED_CURIE, CURIE, None, Optional[METADATA_MAP]]
METADATA_STATEMENT = Union[LITERAL_METADATA_STATEMENT, OBJECT_METADATA_STATEMENT]
DEFINITION = Tuple[CURIE, str, METADATA_MAP]

MISSING_PREFIX_MAP = dict(
    EFO="http://www.ebi.ac.uk/efo/EFO_",
    SCTID="http://snomed.info/id/",
    ORPHANET="http://www.orpha.net/ORDO/Orphanet_",
)


@lru_cache(1)
def get_default_prefix_map() -> Mapping[str, str]:
    """Construct a default prefix map using a :mod:`prefixmaps.datamodel.Context` object."""
    obo_context = load_context("obo")
    for prefix, uri_prefix in DEFAULT_PREFIX_MAP.items():
        obo_context.add_prefix(prefix, uri_prefix)
    for prefix, uri_prefix in MISSING_PREFIX_MAP.items():
        obo_context.add_prefix(prefix, uri_prefix)
    return obo_context.as_dict()


@dataclass
class BasicOntologyInterface(OntologyInterface, ABC):
    """
    Basic lookup operations on ontologies.

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter('tests/input/go-nucleus.db')
    >>> print(adapter.label("GO:0005634"))
    nucleus

    No Object Model is used - input and payloads are simple scalars, dicts, and lists

    This presents an intentionally highly simplistic, lossy view of an ontology. It
    is intended to fit the "80% of uses" scenario - for more advanced uses, use one of the
    more specialized subclasses.

    For example, BasicOntologyInterface exposes a simple model of synonyms as aliases:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter('tests/input/go-nucleus.db')
    >>> for alias in sorted(adapter.entity_aliases("GO:0005634")):
    ...     print(alias)
    cell nucleus
    horsetail nucleus
    nucleus

    This omits metadata about the synonym, such as the predicate, source, and type.
    For this more granular view, the :ref:`obograph_interface` can be used.

    Basic concepts:

    - An ontology is a collection of entities
    - Entities are typically classes (terms), but they may be other types
    - An entity MUST BE uniquely identifier by a CURIE
    - Each entity SHOULD have a single name
    - Entities may have hierarchical parents and children
    - Entities may have simple relationships to other terms

        - A relationship is a simple triple (in OWL terms, these may represent existential relationships)
        - A CURIE is used for the predicate
    - Entities may have aliases (synonyms)

       - these MAY be typed (scoped)

    - Entities have simple key-value metadata associated with them, where keys are open-ended

    Out of scope:

    - Many OWL axioms including:

        - Disjointness
        - Equivalence (including "logical definitions")
        - Property characteristics

    - All OWL expressions

        - but note that simple SomeValuesFrom expressions are included as relationships

    - Information about specific assignments ("axiom annotations" in OWL terms)

        - this includes attribution for synonyms, definitions, ...

    - A fixed datamodel for metadata, beyond core minimal information

    CURIEs are used as the default means of identifying entities.

    In some cases there may not be a defined CURIE form for an entity, such as an ontology,
    in which case URIs may be used

    """

    strict: bool = False
    """Raise exceptions when entities not found in ID-based lookups"""

    _multilingual: bool = None

    autosave: bool = field(default_factory=lambda: True)
    """For adapters that wrap a transactional source (e.g sqlite), this controls
    whether results should be auto-committed after each operation"""

    exclude_owl_top_and_bottom: bool = field(default_factory=lambda: True)
    """Do not include owl:Thing or owl:Nothing"""

    ontology_metamodel_mapper: Optional[OntologyMetadataMapper] = None
    """An optional mapper that overrides metamodel properties"""

    _converter: Optional[curies.Converter] = None

    auto_relax_axioms: bool = None
    """If True, relax some OWL axioms as per https://robot.obolibrary.org/relax"""

    cache_lookups: bool = False
    """If True, the implementation may choose to cache lookup operations"""

    property_cache: KeyValCache = field(default_factory=lambda: KeyValCache())

    _edge_index: Optional[EdgeIndex] = None
    _entailed_edge_index: Optional[EdgeIndex] = None

    _prefix_map: Optional[PREFIX_MAP] = None

    def prefix_map(self) -> PREFIX_MAP:
        """
        Return a dictionary mapping all prefixes known to the resource to their URI expansion.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for prefix, expansion in adapter.prefix_map().items():
        ...     print(prefix, expansion)
        <BLANKLINE>
        ...
        GO http://purl.obolibrary.org/obo/GO_
        ...

        By default, this returns a combination of the  OBO Foundry prefix map with
        the default OAKlib prefix map (see :data:`oaklib.datamodels.vocabulary.DEFAULT_PREFIX_MAP`).


        :return: prefix map
        """
        if not self._prefix_map:
            self._prefix_map = copy(get_default_prefix_map())
        return self._prefix_map

    @deprecated("Replaced by prefix_map")
    def get_prefix_map(self) -> PREFIX_MAP:
        return self.prefix_map()

    @property
    def converter(self) -> curies.Converter:
        """
        Get a converter for this ontology interface's prefix map.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> converter = adapter.converter
        >>> print(converter.compress("http://purl.obolibrary.org/obo/GO_0005634"))
        GO:0005634

        :return: A converter
        """
        if self._converter is None:
            self._converter = curies.Converter.from_prefix_map(self.prefix_map(), strict=False)
        return self._converter

    def set_metamodel_mappings(self, mappings: Union[str, Path, List[Mapping]]) -> None:
        """
        Sets the ontology metamodel mapper.

        :param mappings: Mappings for predicates such as rdfs:subClassOf
        :return:
        """
        if isinstance(mappings, (str, Path)):
            msdf = parse_sssom_table(mappings)
            msd = to_mapping_set_document(msdf)
            mappings = msd.mapping_set.mappings
        self.ontology_metamodel_mapper = OntologyMetadataMapper(
            mappings, curie_converter=self.converter
        )

    def curie_to_uri(self, curie: CURIE, strict: bool = False) -> Optional[URI]:
        """
        Expands a CURIE to a URI.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> print(adapter.curie_to_uri("GO:0005634"))
        http://purl.obolibrary.org/obo/GO_0005634

        :param curie:
        :param strict: (Default is False) if True, exceptions will be raised if curie cannot be expanded
        :return:
        """
        if ":" not in curie:
            if strict:
                raise ValueError(f"Invalid CURIE: {curie}")
            return None
        rv = self.converter.expand(curie)
        if rv is None and strict:
            prefix_map_text = "\n".join(
                f"  {prefix} -> {uri_prefix}"
                for prefix, uri_prefix in sorted(self.converter.prefix_map.items())
            )
            raise ValueError(
                f"{self.__class__.__name__}.prefix_map() does not support expanding {curie}.\n"
                f"This ontology interface contains {len(self.prefix_map()):,} prefixes:\n{prefix_map_text}"
            )
        return rv

    def uri_to_curie(
        self, uri: URI, strict: bool = True, use_uri_fallback=False
    ) -> Optional[CURIE]:
        """
        Contracts a URI to a CURIE.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> print(adapter.uri_to_curie("http://purl.obolibrary.org/obo/GO_0005634"))
        GO:0005634

        If strict conditions hold, then no URI can map to more than one CURIE
        (i.e one URI base should not start with another).

        :param uri: URI
        :param strict: Boolean [default: True]
        :param use_uri_fallback: if cannot be contracted, use the URI as a CURIE proxy [default: True]
        :return: contracted URI, or original URI if no contraction possible
        """
        if not uri:
            raise ValueError("URI cannot be None")
        rv = self.converter.compress(uri, passthrough=use_uri_fallback)
        if rv is None and strict:
            prefix_map_text = "\n".join(
                f"  {prefix} -> {uri_prefix}"
                for prefix, uri_prefix in sorted(self.converter.prefix_map.items())
            )
            raise ValueError(
                f"{self.__class__.__name__}.prefix_map() does not support compressing {uri}.\n"
                f"This ontology interface contains {len(self.prefix_map()):,} prefixes:\n{prefix_map_text}"
            )
        return rv

    @property
    def edge_index(self) -> EdgeIndex:
        """
        An index of all asserted edges in the ontology.

        .. note::

            not all adapters populate this index.

        :return: index of edges
        """
        if self._edge_index is None:
            self._edge_index = EdgeIndex(lambda: self._all_relationships())
        return self._edge_index

    @property
    def entailed_edge_index(self) -> EdgeIndex:
        """
        An index of all entailed edges in the ontology.

        .. note::

            not all adapters populate this index.

        :return: index of entailed edges
        """
        if self._entailed_edge_index is None:
            self._entailed_edge_index = EdgeIndex(lambda: self._all_entailed_relationships())
        return self._entailed_edge_index

    def _all_entailed_relationships(self):
        raise NotImplementedError("This adapter does not support entailed relationships")

    @property
    def _relationship_index(self) -> Dict[CURIE, List[RELATIONSHIP]]:
        """
        An index of relationships keyed by either subject or object.

        The first time this is called, it will build the index.
        Subsequent calls will return the cached index.

        :return: dictionary mapping subject or object to list of relationships
        """
        if self._relationship_index_cache:
            return self._relationship_index_cache
        logging.info("Building relationship index")
        ix = defaultdict(list)
        for rel in self._all_relationships():
            s, p, o = rel
            ix[s].append(rel)
            ix[o].append(rel)
        self._relationship_index_cache = ix
        return self._relationship_index_cache

    def _rebuild_relationship_index(self):
        self._relationship_index_cache = None
        self._edge_index = None
        _ = self._relationship_index  # force re-index

    def _clear_relationship_index(self):
        self._edge_index = None
        self._relationship_index_cache = None

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        raise NotImplementedError

    @property
    def multilingual(self) -> bool:
        """
        Returns True if this ontology interface supports multilingual annotations.

        This is by default inferred from the content of the ontology, if more than
        one language tag is present. This is the case for the international version
        of the HPO:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> adapter.multilingual
        True

        If no language tags are present, then this will return False:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> adapter.multilingual
        False

        .. note ::

            currently this is only implemented for the SQL backend.

        :return: True if multilingual
        """
        if self._multilingual is None:
            self._multilingual = len([x for x in self.languages()]) > 1
        return self._multilingual

    @multilingual.setter
    def multilingual(self, value: bool):
        self._multilingual = value

    def languages(self) -> Iterable[LANGUAGE_TAG]:
        """
        Returns a list of languages explicitly supported by this ontology interface.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> for lang in sorted(adapter.languages()):
        ...    print(lang)
        cs
        fr
        nl
        tr

        :return: iterator of language tags
        """
        return iter([])

    @property
    def default_language(self) -> Optional[LANGUAGE_TAG]:
        """
        Returns the default language for this ontology interface.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> adapter.default_language
        'en'

        Note that here "default" has a particular meaning: it means that lexical elements
        are MUST NOT be explicitly tagged with this language, and that it MUST be assumed that
        a blank/empty/null language tag means that the default language is intended.

        :return: language tag
        """
        return "en"

    def ontologies(self) -> Iterable[CURIE]:
        """
        Yields all known ontology CURIEs.

        Many OntologyInterfaces will wrap a single ontology, others will wrap multiple.
        Even when a single ontology is wrapped, there may be multiple ontologies included as imports.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.owl.ttl')
        >>> list(adapter.ontologies())
        ['go.owl']

        .. note ::

            The payload for this method may change to return normalized ontology names such as 'go'

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('bioportal:')
        >>> for ont in sorted(adapter.ontologies()):
        ...     print(ont)
        <BLANKLINE>
        ...
        GO
        ...
        UBERON
        ...

        :return: iterator
        """
        raise NotImplementedError(
            f"ontologies() method not implemented for {self.__class__.__name__}"
        )

    @deprecated("Replaced by ontologies()")
    def ontology_curies(self) -> Iterable[CURIE]:
        return self.ontologies()

    @deprecated("Replaced by ontology_curies")
    def all_ontology_curies(self) -> Iterable[CURIE]:
        return self.ontologies()

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        """
        Yields all known entities that are obsolete.

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:cob")
        >>> for entity in adapter.obsoletes():
        ...     print(entity)
        <BLANKLINE>
        ...
        COB:0000014

        In OWL, obsolete entities (aka deprecated entities) are those
        that have an ``owl:deprecated`` annotation with value "True"

        By default, *merged terms* are included. Merged terms are entities
        that are:

        - (a) obsolete
        - (b) have a replacement term
        - (c) have an "obsolescence reason" that is "merged term"

        In OBO Format, merged terms do not get their own stanza, but
        instead show up as ``alt_id`` tags on the replacement term.

        To exclude merged terms, set ``include_merged=False``:

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:cob")
        >>> for entity in adapter.obsoletes(include_merged=False):
        ...     print(entity)
        <BLANKLINE>
        ...
        COB:0000014

        :param include_merged: If True, merged terms will be included
        :return: iterator over CURIEs

        """
        raise NotImplementedError

    def obsoletes_migration_relationships(
        self, entities: Iterable[CURIE]
    ) -> Iterable[RELATIONSHIP]:
        """
        Yields relationships between an obsolete entity and potential replacements.

        Example:
        -------
        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:cob")
        >>> for rel in adapter.obsoletes_migration_relationships(adapter.obsoletes()):
        ...     print(rel)

        Obsoletion relationship predicates may be:

        - IAO:0100001 (term replaced by)
        - oboInOwl:consider
        - rdfs:seeAlso

        :return: iterator

        """
        for entity in entities:
            for prop, vals in self.entity_metadata_map(entity).items():
                if prop in OBSOLETION_RELATIONSHIP_PREDICATES:
                    for val in vals:
                        yield entity, prop, val

    @deprecated("Replaced by obsoletes()")
    def all_obsolete_curies(self) -> Iterable[CURIE]:
        return self.obsoletes()

    def dangling(self, curies: Optional[Iterable[CURIE]] = None) -> Iterable[CURIE]:
        """
        Yields all known entities in provided set that are dangling.

        Example:
        -------
        This example is over an OBO file with one stanza:

        .. code-block:: obo

            [Term]
            id: GO:0012505
            name: endomembrane system
            is_a: GO:0110165 ! cellular anatomical entity
            relationship: has_part GO:0005773 ! vacuole

        The two edges point to entities that do not exist in the file.

        The following code will show these:

        >>> from oaklib import get_adapter
        >>> # Note: pronto adapter refuses to parse ontology files with dangling
        >>> adapter = get_adapter("simpleobo:tests/input/dangling-node-test.obo")
        >>> for entity in sorted(adapter.dangling()):
        ...     print(entity)
        GO:0005773
        GO:0110165

        :param curies: CURIEs to check for dangling; if empty will check all
        :return: iterator over CURIEs

        """
        if curies is None:
            curies = self.entities(filter_obsoletes=False)
            curies = itertools.chain(curies, {rel[2] for rel in self.relationships()})
        for curie_it in chunk(curies):
            chunked_curies = list(curie_it)
            logging.debug(f"Checking {len(chunked_curies)} curies for dangling")
            curie_labels = self.labels(chunked_curies, allow_none=True)
            candidates = [curie for curie, label in curie_labels if label is None]
            exclude = {rel[0] for rel in self.relationships(candidates)}
            logging.debug(f"Candidates {len(candidates)} exclude: {len(exclude)}")
            yield from [curie for curie in candidates if curie not in exclude]

    def ontology_versions(self, ontology: CURIE) -> Iterable[str]:
        """
        Yields all version identifiers for an ontology.

        .. warning ::

            This method is not yet implemented for all OntologyInterface implementations.

        :param ontology:
        :return: iterator
        """
        raise NotImplementedError

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
        """
        Property-values metadata map with metadata about an ontology.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for ont in adapter.ontologies():
        ...     m = adapter.ontology_metadata_map(ont)
        ...     m.get('schema:url')
        ['http://purl.obolibrary.org/obo/go.owl']

        :param ontology:
        :return:
        """
        raise NotImplementedError(
            f"ontology_metadata_map() method not implemented for {self.__class__.__name__}"
        )

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        """
        Yields all known entity CURIEs.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in adapter.entities():
        ...     print(e)
        <BLANKLINE>
        ...
        GO:0005634
        ...

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import OWL_OBJECT_PROPERTY
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in adapter.entities(owl_type=OWL_OBJECT_PROPERTY):
        ...     print(e)
        <BLANKLINE>
        ...
        BFO:0000051
        ...

        :param filter_obsoletes: if True, exclude any obsolete/deprecated element
        :param owl_type: CURIE for RDF metaclass for the object, e.g. owl:Class
        :return: iterator
        """
        raise NotImplementedError(f"{type(self)} does not implement entities()")

    @deprecated("Replaced by entities")
    def all_entity_curies(self, **kwargs) -> Iterable[CURIE]:
        return self.entities(**kwargs)

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CURIE]]:
        """
        Yields all known OWL types for given entities.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e, t in sorted(adapter.owl_types(['GO:0005634', 'BFO:0000050'])):
        ...     print(e, t)
        BFO:0000050 owl:ObjectProperty
        BFO:0000050 owl:TransitiveProperty
        GO:0005634 owl:Class

        The OWL type must either be the instantiated type as the RDFS level, e.g.

        - owl:Class
        - owl:ObjectProperty
        - owl:DatatypeProperty
        - owl:AnnotationProperty
        - owl:NamedIndividual

        Or a vocabulary type for a particular kind of construct, e.g

        - oio:SubsetProperty
        - obo:SynonymTypeProperty

        See `Section 8.3<https://www.w3.org/TR/owl2-primer/#Entity_Declarations>` of the OWL 2 Primer

        :param entities:
        :return: iterator
        """
        raise NotImplementedError

    def owl_type(self, entity: CURIE) -> List[CURIE]:
        """
        Get the OWL type for a given entity.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> adapter.owl_type('GO:0005634')
        ['owl:Class']

        Typically each entity will have a single OWL type, but in some cases
        an entity may have multiple OWL types. This is called "punning",
        see `Section 8.3<https://www.w3.org/TR/owl2-primer/#Entity_Declarations>` of
        the OWL primer

        :param entity:
        :return: CURIE
        """
        return [x[1] for x in self.owl_types([entity]) if x[1] is not None]

    def defined_by(self, entity: CURIE) -> Optional[str]:
        """
        Returns the CURIE of the ontology that defines the given entity.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> adapter.defined_by('GO:0005634')
        'GO'

        :param entity:
        :return:
        """
        for _, x in self.defined_bys([entity]):
            return x

    def defined_bys(self, entities: Iterable[CURIE]) -> Iterable[str]:
        """
        Yields all known isDefinedBys for given entities.

        This is for determining the ontology that defines a given entity, i.e.
        which ontology the entity belongs to.

        Formally, this should be captured by an rdfs:isDefinedBy triple, but
        in practice this may not be explicitly stated. In this case, implementations
        may choose to use heuristic measures, including using the ontology prefix.

        :param entities:
        :return: iterator
        """
        for e in entities:
            if ":" in e:
                yield e, e.split(":")[0]
            else:
                yield e, None

    def roots(
        self,
        predicates: Optional[List[PRED_CURIE]] = None,
        ignore_owl_thing=True,
        filter_obsoletes=True,
        annotated_roots=False,
        id_prefixes: Optional[List[CURIE]] = None,
    ) -> Iterable[CURIE]:
        """
        Yields all entities without a parent.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in sorted(adapter.roots()):
        ...     print(e)
        <BLANKLINE>
        ...
        BFO:0000003
        ...
        OBI:0100026
        ...

        Note that the concept of a "root" in an ontology can be ambiguous:

        - is the (trivial) owl:Thing included (OWL tautology)?
        - are we asking for the root of the is-a graph, or a subset of predicates?
        - do we include parents in imported/merged other ontologies (e.g. BFO)?
        - do we include obsolete nodes (which are typically singletons)?

        Note also that the release OWL versions of many OBO ontologies may exhibit a certain
        level of messiness with multiple roots.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in sorted(adapter.roots(id_prefixes=['GO'])):
        ...     print(e, adapter.label(e))
        GO:0003674 molecular_function
        GO:0005575 cellular_component
        GO:0008150 biological_process

        This method will yield entities that are not the subject of an edge, considering
        only edges with a given set of predicates, optionally ignoring owl:Thing, and
        optionally constraining to a given set of entity CURIE prefixes

        :param predicates: predicates to be considered (default: all)
        :param ignore_owl_thing: do not consider artificial/trivial owl:Thing when calculating (default=True)
        :param filter_obsoletes: do not include obsolete/deprecated nodes in results (default=True)
        :param annotated_roots: use nodes explicitly annotated as root (IAO:0000700)
        :param id_prefixes: limit search to specific prefixes
        :return:
        """
        # this interface-level method should be replaced by specific implementations
        logging.info(
            f"Using naive approach for root detection, may be slow. Predicates={predicates}"
        )
        candidates = []
        if annotated_roots:
            for ontology in self.ontologies():
                meta = self.ontology_metadata_map(ontology)
                candidates += meta.get(HAS_ONTOLOGY_ROOT_TERM, [])
            logging.info(f"  Annotated roots: {candidates}")
            for candidate in candidates:
                yield candidate
            return
        for curie in self.entities(owl_type=OWL_CLASS):
            if id_prefixes is None or get_curie_prefix(curie) in id_prefixes:
                candidates.append(curie)
        logging.info(f"Candidates: {len(candidates)}")
        for subject, pred, object in self.all_relationships():
            if subject == object:
                continue
            if ignore_owl_thing and object == OWL_THING:
                continue
            if not (id_prefixes is None or get_curie_prefix(object) in id_prefixes):
                continue
            # if object not in all_curies:
            #    continue
            if subject in candidates:
                if predicates is None or pred in predicates:
                    candidates.remove(subject)
                    logging.debug(f"Not a root: {subject} [{pred} {object}]")
        if filter_obsoletes:
            exclusion_list = list(self.obsoletes())
        else:
            exclusion_list = []
        exclusion_list += [OWL_THING, OWL_NOTHING]
        for term in candidates:
            if term not in exclusion_list:
                yield term

    def leafs(
        self,
        predicates: Optional[List[PRED_CURIE]] = None,
        ignore_owl_nothing=True,
        filter_obsoletes=True,
    ) -> Iterable[CURIE]:
        """
        Yields all nodes that have no children.

        Note that the concept of a "leaf" in an ontology can be ambiguous:

        - is the (trivial) owl:Nothing included (OWL tautology)?
        - are we asking for the leaf of the is-a graph, or the whole graph?
        - do we include obsolete nodes (which are typically singletons)?

        This method will yield entities that are not the object of an edge, considering
        only edges with a given set of predicates, optionally ignoring owl:Nothing, and
        optionally constraining to a given set of entity CURIE prefixes.

        :param predicates: predicates to be considered (default: all)
        :param ignore_owl_nothing: do not consider artificial/trivial owl:Nothing when calculating (default=True)
        :param filter_obsoletes: do not include obsolete/deprecated nodes in results (default=True)
        :return:
        """
        all_curies = set(list(self.entities(owl_type=OWL_CLASS)))
        candidates = all_curies
        logging.info(f"Candidates: {len(candidates)}")
        for subject, pred, object in self.all_relationships():
            if subject == object:
                continue
            if ignore_owl_nothing and subject == OWL_NOTHING:
                continue
            if object in candidates:
                if predicates is None or pred in predicates:
                    candidates.remove(object)
                    logging.debug(f"Not a leaf: {object} [inv({pred}) {subject}]")
        if filter_obsoletes:
            exclusion_list = list(self.obsoletes())
        else:
            exclusion_list = []
        exclusion_list += [OWL_THING, OWL_NOTHING]
        for term in candidates:
            if term not in exclusion_list:
                yield term

    def singletons(
        self, predicates: Optional[List[PRED_CURIE]] = None, filter_obsoletes=True
    ) -> Iterable[CURIE]:
        """
        Yields entities that have neither parents nor children.

        All singleton nodes, where a singleton has no connections using the specified
        predicate list

        :param predicates:
        :param ignore_owl_nothing:
        :param filter_obsoletes:
        :return:
        """
        # TODO: use a more efficient algorithm
        candidates = list(
            self.roots(predicates=predicates, ignore_owl_thing=True, filter_obsoletes=True)
        )
        logging.info(f"Candidates: {len(candidates)}; filtering using {predicates}")
        for subject, pred, object in self.all_relationships():
            if subject == object:
                continue
            if subject == OWL_NOTHING:
                continue
            if object in candidates:
                if predicates is None or pred in predicates:
                    candidates.remove(object)
                    logging.debug(f"Not a singleton: {object} [inv({pred}) {subject}]")
        if filter_obsoletes:
            exclusion_list = list(self.obsoletes())
        else:
            exclusion_list = []
        exclusion_list += [OWL_THING, OWL_NOTHING]
        for term in candidates:
            if term not in exclusion_list:
                yield term

    def subsets(self) -> Iterable[SUBSET_CURIE]:
        """
        Yields all subsets (slims) defined in the ontology.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in sorted(adapter.subsets()):
        ...     print(e)
        <BLANKLINE>
        ...
        goslim_drosophila
        goslim_flybase_ribbon
        goslim_generic
        ...

        All subsets yielded are contracted to their short form.

        :return: iterator
        """
        raise NotImplementedError

    @deprecated("Replaced by subsets()")
    def subset_curies(self) -> Iterable[SUBSET_CURIE]:
        return self.subsets()

    @deprecated("Replaced by subsets()")
    def all_subset_curies(self) -> Iterable[SUBSET_CURIE]:
        return self.subsets()

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        """
        Yields all entities belonging to the specified subset.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e in sorted(adapter.subset_members('goslim_generic')):
        ...     print(e, adapter.label(e))
        <BLANKLINE>
        ...
        GO:0005634 nucleus
        GO:0005635 nuclear envelope
        GO:0005737 cytoplasm
        GO:0005773 vacuole
        ...

        :return: iterator
        """
        raise NotImplementedError

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        """
        Yields entity-subset pairs for the given set of entities.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/go-nucleus.db')
        >>> for e, subset in sorted(adapter.terms_subsets(['GO:0005634', 'GO:0005635'])):
        ...     print(subset, e, adapter.label(e))
        <BLANKLINE>
        ...
        goslim_yeast GO:0005634 nucleus
        goslim_chembl GO:0005635 nuclear envelope
        goslim_generic GO:0005635 nuclear envelope
        ...

        :return: iterator
        """
        # TODO: replace with adaptor-specific
        logging.info("Using naive method for fetching subsets")
        curies = list(curies)
        for s in self.subsets():
            for t in self.subset_members(s):
                if t in curies:
                    yield t, s

    def terms_categories(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CATEGORY_CURIE]]:
        """
        Yields all categories an entity or entities belongs to.

        .. note ::

            This method is not implemented for all adapters.

        :return: iterator
        """
        raise NotImplementedError

    @deprecated("Replaced by subset_members(subset)")
    def curies_by_subset(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        return self.subset_members(subset)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        fetches the unique label for a CURIE.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.owl")
        >>> adapter.label("GO:0005634")
        'nucleus'

        The CURIE may be for a class, individual, property, or ontology.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.owl")
        >>> adapter.label("BFO:0000050")
        'part of'

        For backends that support internationalization, the lang tag can be used:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> adapter.label('HP:0000118', lang='fr')
        'Anomalie phénotypique'

        If the argument matches the default language, and the literal is not
        explicitly language tagged, it is still returned

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> adapter.label('HP:0000118', lang='en')
        'Phenotypic abnormality'

        :param curie:
        :param lang: [None] language tag
        :return: label
        """
        raise NotImplementedError

    @deprecated("Use label(curie))")
    def get_label_by_curie(self, curie: CURIE) -> Optional[str]:
        return self.label(curie)

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, str]]:
        """
        Yields entity-label pairs for a CURIE or CURIEs.

        The CURIE may be for a class, individual, property, or ontology.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.owl")
        >>> list(sorted(adapter.labels(["GO:0005634", "GO:0005635"])))
        [('GO:0005634', 'nucleus'), ('GO:0005635', 'nuclear envelope')]

        :param curies: identifiers to be queried
        :param allow_none: [True] use None as value if no label found
        :return: iterator over tuples of (curie, label)
        """
        # default implementation: may be overridden for efficiency
        for curie in curies:
            label = self.label(curie)
            if label is None and not allow_none:
                continue
            yield curie, label

    def multilingual_labels(
        self, curies: Iterable[CURIE], allow_none=True, langs: Optional[List[LANGUAGE_TAG]] = None
    ) -> Iterable[Tuple[CURIE, str, LANGUAGE_TAG]]:
        """
        Yields entity-label-language tuples for a CURIE or CURIEs.

        For example, in the HPO international edition:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter('tests/input/hp-international-test.db')
        >>> for tuple in sorted(adapter.multilingual_labels(['HP:0000118'], langs=['en', 'nl'])):
        ...     print(tuple)
        ('HP:0000118', 'Fenotypische abnormaliteit', 'nl')
        ('HP:0000118', 'Phenotypic abnormality', None)

        Note that the english label is not explicitly tagged with a language tag, but is returned
        because it matches the :ref:`default_language`.

        :param curies: identifiers to be queried
        :param allow_none: [True] use None as value if no label found
        :param langs: [None] list of languages to be queried (None means all)
        :return: iterator over tuples of (curie, label, language)
        """
        raise NotImplementedError

    @deprecated("Use labels(...)")
    def get_labels_for_curies(self, **kwargs) -> Iterable[Tuple[CURIE, str]]:
        return self.labels(**kwargs)

    def set_label(self, curie: CURIE, label: str, lang: LANGUAGE_TAG = None) -> bool:
        """
        Sets the value of a label for a CURIE.

        :param curie:
        :param label:
        :param lang:
        :return:
        """
        raise NotImplementedError

    def curies_by_label(self, label: str) -> List[CURIE]:
        """
        Fetches all curies with a given label.

        This SHOULD return maximum one CURIE but there are circumstances where multiple CURIEs
        may share a label

        :param label:
        :return:
        """
        raise NotImplementedError()

    @deprecated("Use curies_by_label(label)")
    def get_curies_by_label(self, label: str) -> List[CURIE]:
        return self.curies_by_label(label)

    def comments(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, Optional[str]]]:
        """
        Yields entity-comment pairs for a CURIE or CURIEs.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> for curie, comment in sorted(adapter.comments(["GO:0016772", "GO:0005634"], allow_none=False)):
        ...     print(f"{curie} {comment[0:31]}[snip]")
        GO:0016772 Note that this term encompasses[snip]

        Note in the above query, no tuples for "GO:0005634" were yielded - this is because
        the test ontology has no comments for this CURIE, and ``allow_none=False``.

        If ``allow_none=True``, then a tuple with a None value in the second position will be yielded.

        The CURIE may be for a class, individual, property, or ontology

        :param curies:
        :param allow_none: [True] if False, only yield entities with comments
        :param lang: [None] language tag
        :return: iterator
        """
        raise NotImplementedError

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        """
        Yields all relationships matching query constraints.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> for s, p, o in sorted(adapter.relationships(subjects=["GO:0005634"])):
        ...     print(f"{p} {o} '{adapter.label(o)}'")
        RO:0002160 NCBITaxon:2759 'Eukaryota'
        rdfs:subClassOf GO:0043231 'intracellular membrane-bounded organelle'

        :param subjects: constrain search to these subjects (i.e outgoing edges)
        :param predicates: constrain search to these predicates
        :param objects: constrain search to these objects (i.e incoming edges)
        :param include_tbox: if true, include class-class relationships (default True)
        :param include_abox: if true, include instance-instance/class relationships (default True)
        :param include_entailed:
        :param exclude_blank: do not include blank nodes/anonymous expressions
        :return:
        """
        if invert:
            for s, p, o in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
                exclude_blank=exclude_blank,
            ):
                yield o, p, s
            return
        if not subjects:
            subjects = list(self.entities())
        logging.info(f"Subjects: {len(subjects)}")
        for subject in subjects:
            for this_predicate, this_objects in self.outgoing_relationship_map(subject).items():
                if predicates and this_predicate not in predicates:
                    continue
                for this_object in this_objects:
                    if objects and this_object not in objects:
                        continue
                    yield subject, this_predicate, this_object

    def relationships_metadata(
        self, relationships: Iterable[RELATIONSHIP], **kwargs
    ) -> Iterator[Tuple[RELATIONSHIP, List[Tuple[PRED_CURIE, Any]]]]:
        """
        given collection of relationships, yield relationships with metadata attached.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:mondo")
        >>> rels = list(adapter.relationships(["MONDO:0009831"]))
        >>> for rel, metadatas in adapter.relationships_metadata(rels):
        ...     for p, v in metadatas:
        ...         print(rel, p, v)
        <BLANKLINE>
        ...
        ('MONDO:0009831', 'rdfs:subClassOf', 'MONDO:0002516') oio:source NCIT:C9005
        ...

        :param relationships: collection of subject-predicate-object tuples
        :param kwargs:
        :return: yields relationships with property-value metadata
        """
        raise NotImplementedError

    def hierarchical_parents(self, curie: CURIE, isa_only: bool = False) -> List[CURIE]:
        """
        Returns all hierarchical parents.

        The definition of hierarchical parent depends on the provider. For example, in OLS,
        this will return part-of parents for GO, as well as is-a

        This only returns Named Entities; i.e. if an RDF source is wrapped, this will NOT return blank nodes

        To get all relationships, see :ref:`outgoing_relationships`

        A fresh map is created each invocation

        :param curie:
        :param isa_only: restrict hierarchical parents to isa only
        :return:
        """
        return self.outgoing_relationship_map(curie).get(IS_A, [])

    def outgoing_relationship_map(self, curie: CURIE) -> RELATIONSHIP_MAP:
        """
        Returns a predicate-objects map with outgoing relationships for a node.

        The return relationship map is keyed by relationship type, where the values
        are the 'parents' or fillers

        OWL formulation:

         - is_a: {P : SubClassOf(C P), class(P)}
         - R: {P : SubClassOf(C ObjectSomeValuesFrom( RP), class(P), property(P)}

        :param curie: the 'child' term
        :return:
        """
        return pairs_as_dict([(p, o) for _, p, o in self.relationships([curie])])

    def outgoing_relationships(
        self, curie: CURIE, predicates: Optional[List[PRED_CURIE]] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        """
        Yields relationships where the input curie in the subject.

        :param curie:
        :param predicates: if None, do not filter
        :return:
        """
        for _, p, o in self.relationships([curie], predicates=predicates):
            yield p, o

    def incoming_relationship_map(self, curie: CURIE) -> RELATIONSHIP_MAP:
        """
        Returns a predicate-subjects map with incoming relationships for a node.

        See :ref:outgoing_relationship_map:

        :param curie:
        :return:
        """
        return pairs_as_dict([(p, s) for s, p, _ in self.relationships(objects=[curie])])

    def incoming_relationships(
        self, curie: CURIE, predicates: Optional[List[PRED_CURIE]] = None
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        """
        Returns relationships where curie in the object

        :param curie:
        :param predicates: if None, do not filter
        :return:
        """
        for s, p, _ in self.relationships(objects=[curie], predicates=predicates):
            yield p, s

    @deprecated("Use relationships()")
    def all_relationships(self) -> Iterable[RELATIONSHIP]:
        """
        Yields all known relationships.

        :return:
        """
        for curie in self.entities():
            for pred, fillers in self.outgoing_relationship_map(curie).items():
                for filler in fillers:
                    yield curie, pred, filler

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        Lookup the text definition of an entity.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> for curie, defn, meta in adapter.definitions(["GO:0005634", "GO:0005737"], include_metadata=True):
        ...     print(f"{curie} {defn[0:30]}[snip] [{meta}]")
        GO:0005634 A membrane-bounded organelle o[snip] [{'oio:hasDbXref': ['GOC:go_curators']}]
        GO:0005737 All of the contents of a cell [snip] [{'oio:hasDbXref': ['ISBN:0198547684']}]

        :param curie: entity identifier to be looked up
        :param lang: language tag
        :return:
        """
        raise NotImplementedError()

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[DEFINITION]:
        """
        Lookup the text definition plus metadata for a list of entities.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.db")
        >>> for curie, defn, meta in adapter.definitions(["GO:0005634", "GO:0005737"], include_metadata=True):
        ...     print(f"{curie} {defn[0:30]}[snip] [{meta}]")
        GO:0005634 A membrane-bounded organelle o[snip] [{'oio:hasDbXref': ['GOC:go_curators']}]
        GO:0005737 All of the contents of a cell [snip] [{'oio:hasDbXref': ['ISBN:0198547684']}]

        :param curies: iterable collection of entity identifiers to be looked up
        :param include_metadata: if true, include metadata
        :param include_missing: if true, include curies with no definition
        :param lang: language tag
        :return: iterator over (id, definition, metadata) tuples
        """
        if include_metadata:
            raise NotImplementedError()
        for curie in curies:
            defn = self.definition(curie)
            if not defn and not include_missing:
                continue
            yield curie, defn, {}

    @deprecated("Use definition()")
    def get_definition_by_curie(self, curie: CURIE) -> Optional[str]:
        return self.definition(curie)

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        """
        Yields mappings for a given subject.

        Here, each mapping is represented as a simple tuple (predicate, object)

        .. note ::

            For a more sophisticated mapping interface, see :ref:`MappingProviderInterface`

        :param curie: entity identifier to be looked up
        :return: iterator over predicate-object tuples
        """
        raise NotImplementedError()

    def simple_mappings(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, PRED_CURIE, CURIE]]:
        """
        Yields simple mappings for a collection of subjects

        :param curies: iterable collection of entity identifiers to be looked up
        :return: iterable subject-predicate-object tuples
        """
        for s in curies:
            for p, o in self.simple_mappings_by_curie(s):
                yield s, p, o

    def entity_aliases(self, curie: CURIE) -> List[str]:
        """
        All aliases/synonyms for a given CURIE

        This lumps together all synonym categories (scopes)

        :param curie:
        :return:
        """
        aliases = set()
        for v in self.entity_alias_map(curie).values():
            aliases.update(set(v))
        return list(aliases)

    @deprecated("Use entity_aliases(curie)")
    def aliases_by_curie(self, curie: CURIE) -> List[str]:
        return self.entity_aliases(curie)

    def alias_relationships(
        self, curie: CURIE, exclude_labels: bool = False
    ) -> Iterator[Tuple[PRED_CURIE, CURIE]]:
        amap = self.entity_alias_map(curie)
        for k, vs in amap.items():
            if exclude_labels and k == LABEL_PREDICATE:
                continue
            for v in vs:
                yield k, v

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        """
        Returns aliases keyed by alias type (scope in OBO terms)

        - The alias map MUST include rdfs:label annotations
        - The alias map MAY include other properties the implementation deems to serve an alias role

        :param curie:
        :return:
        """
        raise NotImplementedError

    @deprecated("Replaced by alias_map(curie)")
    def alias_map_by_curie(self, curie: CURIE) -> ALIAS_MAP:
        return self.entity_alias_map(curie)

    def entity_metadata_map(self, curie: CURIE) -> METADATA_MAP:
        """
        Lookup basic metadata for a given entity.

        Returns a dictionary keyed by property predicate, with a list of zero or more values,
        where each key corresponds to any of a set of open-ended metadata predicates

        This is a simplified version of the metadata model in many ontologies

        :param curie:
        :return:
        """
        raise NotImplementedError

    def entities_metadata_statements(
        self,
        curies: Iterable[CURIE],
        predicates: Optional[List[PRED_CURIE]] = None,
        include_nested_metadata=False,
        **kwargs,
    ) -> Iterator[METADATA_STATEMENT]:
        """
        Retrieve metadata statements (entity annotations) for a collection of entities.

        :param curies:
        :return:
        """
        # Note: this implementation may be inefficient for some backends.
        # It is recommended to override this method in specific implementations.
        for curie in curies:
            for k, vs in self.entity_metadata_map(curie).items():
                if predicates is not None and k not in predicates:
                    continue
                for v in vs:
                    yield curie, k, v, None, None

    def add_missing_property_values(self, curie: CURIE, metadata_map: METADATA_MAP) -> None:
        """
        Add missing property values to a metadata map.

        This is a convenience method for implementations that do not have a complete metadata map.

        :param curie:
        :param metadata_map:
        :return:
        """
        if "id" not in metadata_map:
            metadata_map["id"] = [curie]
        if ":" in curie:
            prefix, _ = curie.split(":", 1)
            if PREFIX_PREDICATE not in metadata_map:
                metadata_map[PREFIX_PREDICATE] = [prefix]
            uri = self.curie_to_uri(curie, False)
            if uri:
                if URL_PREDICATE not in metadata_map:
                    metadata_map[URL_PREDICATE] = [uri]
                if IS_DEFINED_BY not in metadata_map:
                    if uri.startswith("http://purl.obolibrary.org/obo/"):
                        metadata_map[IS_DEFINED_BY] = [
                            f"http://purl.obolibrary.org/obo/{prefix.lower()}.owl"
                        ]
                    else:
                        metadata_map[IS_DEFINED_BY] = [self.curie_to_uri(f"{prefix}:", False)]

    def create_entity(
        self,
        curie: CURIE,
        label: str = None,
        relationships: RELATIONSHIP_MAP = None,
        replace=False,
        **kwargs,
    ) -> CURIE:
        """
        Creates and stores an entity.

        :param curie:
        :param label:
        :param relationships:
        :param replace:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def delete_entity(self, curie: CURIE, label: str = None, **kwargs) -> CURIE:
        """
        Deletes an entity.

        :param curie:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def query(
        self, query: str, syntax: str = None, prefixes: List[str] = None, **kwargs
    ) -> Iterator[Any]:
        """
        Executes a query.

        The behavior of this operation is entirely adapter-dependent, and is
        thus not portable.

        The intention is for SQL backends to support SQL queries, and for
        SPARQL backends to support SPARQL queries.

        :param query:
        :param syntax:
        :param kwargs:
        :return: an iterator over the results, which can be arbitrary objects
        """
        raise NotImplementedError

    def save(self):
        """
        Saves current state.

        :return:
        """
        raise NotImplementedError

    def clone(self, resource: Any) -> None:
        """
        Clones the ontology interface to a new resource.

        :param resource:
        :return:
        """
        raise NotImplementedError

    def precompute_lookups(self) -> None:
        """
        Precompute all main lookup operations.

        An implementation may choose to use this to do lookups in advance. This may be
        faster for some operations that involve repeatedly visiting the same entity.
        :return:
        """
