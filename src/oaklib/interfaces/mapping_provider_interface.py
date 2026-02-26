import logging
from abc import ABC
from typing import Collection, Dict, Iterable, List, Optional, Union

from deprecation import deprecated
from sssom_schema import Mapping

from oaklib.datamodels.mapping_cluster_datamodel import MappingCluster
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE


class MappingProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology interface that provides mappings according to the SSSOM data model.

    Example:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("sqlite:obo:go")
        >>> for mapping in adapter.sssom_mappings("GO:0016772"):
        ...     print(mapping.subject_id, mapping.predicate_id, mapping.object_id)
        <BLANKLINE>
        ...
        GO:0016772 EC:2.7.-.-
        ...

    For more on the SSSOM Data Model, see `<https://w3id.org/sssom/>`_

    .. note ::

        most ontologies only include minimal metadata about mappings at this time, so many fields
        in the sssom mapping datamodel are not populated.

    The core method in this interface is :py:meth:`sssom_mappings`.

    .. note ::

        This interface is for serving pre-calculated mappings.
        See :ref:`sssom_utils` for on-the-fly mapping creation


    Data Model
    -----------

    The central datamodel used here is `SSSOM <http://w3id.org/sssom>`_

    Command Line Use
    ----------------

    .. code::

       runoak -i bioportal: term-mappings UBERON:0002101  -O sssom -o limb-mappings.sssom.tsv
    """

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[Mapping]:
        """
        returns all sssom mappings matching filter conditions.

        To fetch all mappings, simply leave the filter conditions empty:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> for mapping in adapter.sssom_mappings():
        ...     print(mapping.subject_id, mapping.object_id)
        <BLANKLINE>
        ...
        GO:0016772 EC:2.7.-.-
        ...

        To get annotations for a particular term or terms, and to constrain the source of the
        mapping, use the curies and source parameters:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> for mapping in adapter.sssom_mappings(["GO:0005886"], source="Wikipedia"):
        ...     print(mapping.subject_id, mapping.object_id)
        GO:0005886 Wikipedia:Cell_membrane

        Note you can also lookup from the perspective of the mapped entity:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> for mapping in adapter.sssom_mappings(["Wikipedia:Cell_membrane"]):
        ...     print(mapping.subject_id, mapping.object_id)
        GO:0005886 Wikipedia:Cell_membrane

        :param curies: [Optional] entity IDs (in ontology or mapped ontology) to filter by
        :param source: [Optional] only show mappings to source
        :return:
        """
        logging.info("Getting all mappings")
        if curies is not None:
            if isinstance(curies, CURIE):
                it = [curies]
            else:
                it = curies
        else:
            it = self.entities()
        for curies in it:
            logging.debug(f"Getting mappings for {curies}")
            for m in self.get_sssom_mappings_by_curie(curies):
                if source:
                    if m.object_source != source and m.subject_source != source:
                        continue
                yield m

    # TODO: move packages from mapping-walker

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        for mapping in mappings:
            if not mapping.subject_label:
                mapping.subject_label = self.label(mapping.subject_id)
            if not mapping.object_label:
                mapping.object_label = self.label(mapping.object_id)

    def sssom_mappings_by_source(
        self, subject_or_object_source: Optional[str] = None
    ) -> Iterable[Mapping]:
        """
        All SSSOM mappings in the ontology

        The subject_id MUST be a CURIE in the ontology

        :param object_source:
        :return:
        """
        logging.info("Getting all mappings")
        for curie in self.entities():
            logging.debug(f"Getting mappings for {curie}")
            for m in self.get_sssom_mappings_by_curie(curie):
                if subject_or_object_source:
                    if (
                        m.object_source != subject_or_object_source
                        and m.subject_source != subject_or_object_source
                    ):
                        continue
                yield m

    @deprecated("Replaced by sssom_mappings()")
    def all_sssom_mappings(
        self, subject_or_object_source: Optional[str] = None
    ) -> Iterable[Mapping]:
        return self.sssom_mappings_by_source(subject_or_object_source)

    @deprecated("Use sssom_mappings()")
    def get_sssom_mappings_by_curie(self, *args, **kwargs) -> Iterable[Mapping]:
        """
        All SSSOM mappings about a curie

        MUST yield mappings where EITHER subject OR object equals the CURIE

        :param kwargs:
        :return:
        """
        return self.sssom_mappings(*args, **kwargs)

    def get_transitive_mappings_by_curie(self, curie: CURIE) -> Iterable[Mapping]:
        """

        :param curie:
        :return:
        """
        raise NotImplementedError

    def get_mapping_clusters(self) -> Iterable[MappingCluster]:
        raise NotImplementedError

    def normalize(
        self,
        curie: CURIE,
        target_prefixes: List[str],
        source_prefixes: Optional[List[str]] = None,
        strict=False,
    ) -> Optional[CURIE]:
        """
        Normalize a CURIE to a target prefix.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> adapter.normalize("Wikipedia:Cell_membrane", ["GO"])
        'GO:0005886'

        :param curie: the CURIE to normalize
        :param target_prefixes: the prefixes to normalize to
        :param source_prefixes: the prefixes to normalize from
        :param strict: if True, raise an error if there is no single mapping to a target prefix
        :return: the normalized CURIE
        """
        normalized_ids = []
        if source_prefixes is not None:
            source_prefix = curie.split(":")[0]
            if source_prefix not in source_prefixes:
                source_prefixes_lc = {p.lower(): p for p in source_prefixes}
                if source_prefix.lower() not in source_prefixes_lc:
                    return None
                # normalize case
                curie = curie.replace(source_prefix, source_prefixes_lc[source_prefix.lower()])
        target_prefixes_lc_map = {p.lower(): p for p in target_prefixes}
        for m in self.sssom_mappings(curie):
            object_id = m.object_id
            if object_id.lower() == curie.lower():
                object_id = m.subject_id
            object_prefix = object_id.split(":")[0]
            if object_prefix.lower() in target_prefixes_lc_map:
                if object_prefix not in target_prefixes:
                    # case -mismatch; normalize case
                    object_id = object_id.replace(
                        object_prefix, target_prefixes_lc_map[object_prefix.lower()]
                    )
                if not strict:
                    # strict is faster
                    return object_id
                normalized_ids.append(object_id)
        if len(normalized_ids) == 1:
            return normalized_ids[0]
        if strict:
            raise ValueError(f"{curie} no single ID in {target_prefixes}; N={normalized_ids}")
        if normalized_ids:
            return normalized_ids[0]
        curie_lc = curie.lower()
        if curie_lc != curie:
            return self.normalize(curie_lc, target_prefixes, strict=strict)
        return curie

    def normalize_prefix(
        self,
        curie: CURIE,
        prefixes: Optional[Collection[str]] = None,
        prefix_alias_map: Optional[Dict[str, str]] = None,
    ) -> CURIE:
        """
        Normalize a CURIE to a target prefix.

        If a prefix alias map is supplied, this is takes precedence:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> adapter.normalize_prefix("uniprot:P12345", prefix_alias_map={"uniprot": "UniProtKB"})
        'UniProtKB:P12345'

        If not prefix alias map is supplied, then the prefix is mapped to the preferred
        casing determined by the supplied prefixes:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> adapter.normalize_prefix("go:0000001", prefixes=["GO"])
        'GO:0000001'

        :param curie: the CURIE to normalize
        :param prefixes: the prefixes to normalize to
        :param prefix_alias_map: a map of prefix aliases to prefixes
        :return: the normalized CURIE
        """
        prefix = curie.split(":")[0]
        if prefix_alias_map:
            # prefix alias map takes priority
            if prefix in prefix_alias_map:
                return curie.replace(prefix, prefix_alias_map[prefix])
            else:
                return curie
        if not prefixes:
            return curie
        # if not in prefix alias map, use an implicit alias map
        # that maps *any* casing to the preferred case
        if prefix in prefixes:
            return curie
        prefixes_lc = {p.lower(): p for p in prefixes}
        if prefix.lower() not in prefixes_lc:
            return curie
        # normalize case
        return curie.replace(prefix, prefixes_lc[prefix.lower()])

    def create_normalization_map(
        self,
        curies: Optional[Iterable[CURIE]] = None,
        source_prefixes: Optional[Collection[str]] = None,
        target_prefixes: Optional[Collection[str]] = None,
        prefix_alias_map: Optional[Dict[str, str]] = None,
    ) -> Dict[CURIE, CURIE]:
        """
        Create a normalization map for a set of CURIEs.

        This map can then be used to map IDs from one prefix space to another.

        For each curie in curies, find a mapping to a target prefix, and add it to the map.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> nmap = adapter.create_normalization_map(source_prefixes=["GO"], target_prefixes=["Wikipedia"])
        >>> nmap["GO:0005634"]
        'Wikipedia:Cell_nucleus'

        You can also pass in an explicit prefix alias map:

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> nmap = adapter.create_normalization_map(source_prefixes=["GO"], target_prefixes=["WIKIPEDIA"],
        ...     prefix_alias_map={"Wikipedia": "WIKIPEDIA"})
        >>> nmap["GO:0005634"]
        'WIKIPEDIA:Cell_nucleus'

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> nmap = adapter.create_normalization_map(source_prefixes=["go"], target_prefixes=["WIKIPEDIA"],
        ...     prefix_alias_map={"Wikipedia": "WIKIPEDIA", "GO": "go"})
        >>> nmap["go:0005634"]
        'WIKIPEDIA:Cell_nucleus'

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("tests/input/go-nucleus.obo")
        >>> nmap = adapter.create_normalization_map(["go:0005634"], source_prefixes=["go"],
        ...     target_prefixes=["WIKIPEDIA"],
        ...     prefix_alias_map={"Wikipedia": "WIKIPEDIA", "GO": "go"})
        >>> nmap["go:0005634"]
        'WIKIPEDIA:Cell_nucleus'

        :param curies:
        :param subject_prefixes:
        :param object_prefixes:
        :param prefix_alias_map: maps from prefixes used in the adapter to desired prefixes
        :return:
        """
        normalization_map = {}
        # create a reverse map, that maps from the desired prefixes to the prefixes used in the adapter
        if prefix_alias_map is not None:
            reverse_prefix_alias_map = {v: k for k, v in prefix_alias_map.items()}
        else:
            reverse_prefix_alias_map = None
        if curies is None:
            # TODO: use source_prefixes
            curies = list(self.entities())
        else:
            # map input to the form used in this adapter
            curies = [
                self.normalize_prefix(c, source_prefixes, reverse_prefix_alias_map) for c in curies
            ]
        subject_nmap = {
            c: self.normalize_prefix(c, source_prefixes, prefix_alias_map) for c in curies
        }
        # case-neutral form of target prefixes
        target_prefixes_lc = {p.lower(): p for p in target_prefixes}
        for mapping in self.sssom_mappings(curies):
            if mapping.subject_id in subject_nmap:
                other_id = mapping.object_id
                other_prefix = other_id.split(":")[0]
                if other_prefix in target_prefixes or other_prefix.lower() in target_prefixes_lc:
                    normalization_map[mapping.subject_id] = other_id
            elif mapping.object_id in subject_nmap:
                other_id = mapping.subject_id
                other_prefix = other_id.split(":")[0]
                if other_prefix in target_prefixes or other_prefix.lower() in target_prefixes_lc:
                    normalization_map[mapping.object_id] = other_id
        normalization_map = {
            self.normalize_prefix(k, target_prefixes, prefix_alias_map): self.normalize_prefix(
                v, target_prefixes, prefix_alias_map
            )
            for k, v in normalization_map.items()
        }
        return normalization_map
