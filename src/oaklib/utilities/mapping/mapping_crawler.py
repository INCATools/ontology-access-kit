import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Literal, Optional, Set

import pandas as pd
from pydantic import BaseModel
from sssom_schema import Mapping

from oaklib import BasicOntologyInterface, get_adapter
from oaklib.datamodels.vocabulary import SEMAPV
from oaklib.interfaces import MappingProviderInterface, OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.mapping.sssom_utils import StreamingSssomWriter

DIRECTION = Literal[1, -1]


def curie_prefix(curie: CURIE) -> str:
    return curie.split(":")[0]


class MappingCrawlerConfig(BaseModel):
    # make it strict, ie pydantic should raise errors if unspecified attrs used
    class Config:
        extra = "forbid"

    adapter_configs: Optional[Dict[str, Optional["MappingCrawlerConfig"]]] = None
    adapter_specs: Dict[str, str] = {}
    mapping_predicates: Optional[List[PRED_CURIE]] = None
    mapping_directions: List[DIRECTION] = [1, -1]
    edge_predicates: Optional[List[PRED_CURIE]] = None
    edge_directions: List[DIRECTION] = []
    allowed_prefixes: Optional[List[str]] = None
    prefix_normalization_map: Dict[str, str] = {}
    max_distance: Optional[int] = 10
    max_visits: Optional[int] = 10000
    gap_fill: bool = True
    clique_directory: Optional[str] = None
    stylemap_overrides: Optional[Dict[str, Any]] = None


class MappingClique(BaseModel):
    """
    A set of mappings that are all connected in a graph.
    """

    class Config:
        extra = "forbid"
        arbitrary_types_allowed = True

    mappings: List[Mapping]
    seed: Optional[str] = None
    name: Optional[str] = None
    max_traversal_depth: int = 0

    @property
    def mapping_count(self) -> int:
        return len(self.mappings)

    @property
    def subjects(self) -> List[CURIE]:
        """
        Get the set of subjects in the clique.

        :return:
        """
        return list(set([m.subject_id for m in self.mappings]))

    @property
    def objects(self) -> List[CURIE]:
        """
        Get the set of objects in the clique.

        :return:
        """
        return list(set([m.object_id for m in self.mappings]))

    @property
    def entities(self) -> List[CURIE]:
        """
        Get the set of all entities (subjects and objects) in the clique.
        :return:
        """
        return list(set(self.subjects + self.objects))

    @property
    def entity_labels(self) -> Dict[CURIE, str]:
        lmap = {}
        for m in self.mappings:
            lmap[m.subject_id] = m.subject_label
            lmap[m.object_id] = m.object_label
        return lmap

    @property
    def entity_count(self) -> int:
        return len(self.entities)

    @property
    def predicates(self) -> List[PRED_CURIE]:
        """
        Get the list of unique predicates in the clique.

        :return:
        """
        return list(set([m.predicate_id for m in self.mappings]))

    @property
    def mapping_sources(self) -> List[CURIE]:
        """
        Get the list of unique mapping sources in the clique.

        :return:
        """
        return list(set([m.mapping_source for m in self.mappings]))

    @property
    def entities_by_entity_source(self) -> Dict[str, Set[CURIE]]:
        """
        Get a mapping of entity sources (i.e prefixes) to the entities they contain.

        :return:
        """
        d = defaultdict(set)
        for m in self.mappings:
            d[curie_prefix(m.subject_id)].add(m.subject_id)
            d[curie_prefix(m.object_id)].add(m.object_id)
        return d

    @property
    def incoherency_by_entity_source(self) -> Dict[str, int]:
        """
        Get the incoherency of each entity source.

        An entity source is coherent (incoherency=0) if there is at most one representative for a prefix.
        An entity source is incoherent (incoherency>0) if there are multiple representatives for a prefix,
        i.e. if there are 3 entities with prefixes "A", the incoherency of "A" is 2.

        :return:
        """
        return {k: len(v) - 1 for k, v in self.entities_by_entity_source.items()}

    @property
    def average_incoherency(self) -> float:
        """
        Get the average incoherency of the entity sources.

        :return:
        """
        i_by_s = self.incoherency_by_entity_source
        return sum(i_by_s.values()) / len(i_by_s) if i_by_s else 0

    @property
    def max_incoherency(self) -> int:
        """
        Get the maximum incoherency of the entity sources.

        :return:
        """
        return max(self.incoherency_by_entity_source.values() or [0])

    def as_flat_dict(self) -> Dict[str, Any]:
        d = {}
        for k in [
            "seed",
            "name",
            "mapping_count",
            "entity_count",
            "entities",
            "entity_labels",
            "predicates",
            "mapping_sources",
            "average_incoherency",
            "max_incoherency",
        ]:
            d[k] = getattr(self, k)
        d["sources"] = list(self.entities_by_entity_source.keys())
        for k, v in self.incoherency_by_entity_source.items():
            d[f"incoherency_{k}"] = v
        return d


@dataclass
class MappingCrawler:
    config: MappingCrawlerConfig
    _adapters: Optional[Dict[str, BasicOntologyInterface]] = None

    def crawl_ontology_iter(self, seeds: Optional[List[CURIE]] = None) -> Iterator[MappingClique]:
        adapters = self.adapters()
        if not seeds:
            seeds = set()
            for adapter in adapters.values():
                seeds.update(list(adapter.entities(filter_obsoletes=True)))
        logging.info(f"Seeds: {len(seeds)}")

        def get_label(x) -> Optional[str]:
            for adapter in adapters.values():
                if isinstance(adapter, BasicOntologyInterface):
                    return adapter.label(x)
            return None

        def get_sssom_path(seed: str):
            if self.config.clique_directory:
                base_name = seed.replace(":", "_")
                path = Path(self.config.clique_directory)
                sssom_path = path / "cliques" / f"{base_name}.sssom.tsv"
                sssom_path.parent.mkdir(parents=True, exist_ok=True)
                return sssom_path
            else:
                return None

        clique_by_entity = {}
        aliases = {}
        rows = []
        for seed in seeds:
            if seed in aliases:
                continue

            sssom_path = get_sssom_path(seed)
            # TODO: allow for caching
            # if sssom_path and sssom_path.exists():
            #     continue
            clique = self.crawl([seed])
            clique.seed = seed
            clique.name = get_label(seed)
            clique_by_entity[seed] = clique
            for e in clique.entities:
                aliases[e] = seed
                logging.info(f"Alias {e} -> {seed}")
            yield clique
            if self.config.clique_directory:
                path = Path(self.config.clique_directory)
                path.mkdir(parents=True, exist_ok=True)
                with open(sssom_path, "w") as file:
                    writer = StreamingSssomWriter()
                    # writer.output = str(sssom_path)
                    writer.file = file
                    for m in clique.mappings:
                        writer.emit(m)
                    writer.finish()
                    # writer.close()
                rows.append(clique.as_flat_dict())
        df = pd.DataFrame(rows)
        if self.config.clique_directory:
            df.to_csv(Path(self.config.clique_directory) / "clique_results.csv", index=False)
            df.describe().to_csv(
                Path(self.config.clique_directory) / "clique_summary.csv", index=True
            )

    def adapters(self) -> Dict[str, BasicOntologyInterface]:
        if not self._adapters:
            config = self.config
            adapters = {}
            for k in config.adapter_configs.keys():
                route = config.adapter_specs.get(k)
                if not route:
                    if ":" in k or "/" in k:
                        route = k
                    else:
                        route = f"sqlite:obo:{k.lower()}"
                logging.info(f"Loading adapter for {k} from {route}")
                adapters[k] = get_adapter(route)
            self._adapters = adapters
        return self._adapters

    def crawl(self, seeds: List[CURIE]) -> MappingClique:
        mappings = list(self.crawl_iter(seeds))
        return MappingClique(mappings=mappings)

    def crawl_iter(self, seeds: List[CURIE]) -> Iterator[Mapping]:
        """
        Crawl the graph starting from the seeds, yielding edges as they are discovered.

        :param seeds:
        :return: edge iterator, yielding (subject, predicate, object, direction, source) tuples
        """
        config = self.config
        if not config.adapter_configs:
            raise ValueError("No adapter configs provided")

        adapters = self.adapters()

        # initialize the stack with all seeds at distance 0
        stack = [(s, 0) for s in seeds]
        visited = set()
        mappings = []
        max_dist_traversed = 0

        labels = {}

        def get_label(x) -> Optional[str]:
            if x not in labels:
                for adapter in adapters.values():
                    if isinstance(adapter, BasicOntologyInterface):
                        labels[x] = adapter.label(x)
                        if labels[x]:
                            break
            return labels[x]

        def normalize_id(x: str, this_config: MappingCrawlerConfig = config, reverse=False) -> str:
            m = this_config.prefix_normalization_map
            if reverse:
                m = {v: k for k, v in m.items()}
            for k, v in m.items():
                if ":" not in k:
                    k = k + ":"
                if ":" not in v:
                    v = v + ":"
                if x.startswith(k):
                    x = x.replace(k, v)
            return x

        # main loop; pop a node from the stack, get its neighbors, and add them to the stack
        while stack:
            curie, distance = stack.pop()
            # termination and skipping conditions
            if config.max_distance is not None and distance > config.max_distance:
                continue
            max_dist_traversed = max(max_dist_traversed, distance)
            if curie in visited:
                continue
            visited.add(curie)
            if config.max_visits is not None and len(visited) > config.max_visits:
                break
            # iterate over all adapters, expanding outwards from the current node over mappings and edges
            outgoing = []
            for name, adapter in adapters.items():
                # if there is no specific config, default to the global config
                if config.adapter_configs[name]:
                    override_dict = config.adapter_configs[name].model_dump(exclude_unset=True)
                    curr_dict = config.model_dump(exclude_unset=True)
                    this_config = MappingCrawlerConfig(**{**curr_dict, **override_dict})
                else:
                    this_config = config
                # mappings
                if this_config.mapping_directions and isinstance(adapter, MappingProviderInterface):
                    mapped_curie = normalize_id(curie, this_config, reverse=True)
                    for m in adapter.sssom_mappings(mapped_curie):
                        if (
                            this_config.mapping_predicates
                            and m.predicate_id not in this_config.mapping_predicates
                        ):
                            continue
                        # mappings are returned bi-directionally, so we need to check the direction
                        pred, obj = m.predicate_id, m.object_id
                        if obj == mapped_curie:
                            obj = m.subject_id
                            dirn = -1
                        else:
                            dirn = 1
                        if dirn not in this_config.mapping_directions:
                            continue
                        obj = normalize_id(obj, this_config)
                        outgoing.append((pred, dirn, obj, name, m.mapping_justification))
                # edges
                if this_config.edge_directions and isinstance(adapter, BasicOntologyInterface):
                    if 1 in this_config.edge_directions:
                        for _, p, o in adapter.relationships([curie], this_config.edge_predicates):
                            outgoing.append((p, 1, o, name, SEMAPV.ManualMappingCuration.value))
                    if -1 in this_config.edge_directions:
                        for o, p, _ in adapter.relationships(
                            None, this_config.edge_predicates, [curie]
                        ):
                            outgoing.append((p, -1, o, name, SEMAPV.ManualMappingCuration.value))
            # add outgoing edges to the stack and yield them
            for pred, dirn, obj, src, mj in outgoing:
                allowed_prefixes = config.allowed_prefixes
                if allowed_prefixes and not any(obj.startswith(p + ":") for p in allowed_prefixes):
                    continue
                src_id = f"obo:{src}"
                stack.append((obj, distance + 1))
                if dirn == 1:
                    mapping = Mapping(
                        subject_id=curie,
                        subject_label=get_label(curie),
                        predicate_id=pred,
                        object_id=obj,
                        object_label=get_label(obj),
                        mapping_justification=mj,
                        mapping_source=src_id,
                    )
                else:
                    mapping = Mapping(
                        subject_id=obj,
                        subject_label=get_label(obj),
                        predicate_id=pred,
                        object_id=curie,
                        object_label=get_label(curie),
                        mapping_justification=mj,
                        mapping_source=src_id,
                    )
                mapping.other = f"distance: {distance}, direction: {dirn}"
                yield mapping
                mappings.append(mapping)
        if config.gap_fill:
            all_curies = set()
            for m in mappings:
                all_curies.add(m.subject_id)
                all_curies.add(m.object_id)
            for curie in all_curies:
                for name, adapter in adapters.items():
                    if isinstance(adapter, OboGraphInterface):
                        ancs = list(adapter.ancestors(curie))
                        for curie2 in all_curies:
                            if curie2 != curie and curie2 in ancs:
                                for rel in adapter.relationships(
                                    [curie], None, [curie2], include_entailed=True
                                ):
                                    yield Mapping(
                                        subject_id=curie,
                                        subject_label=get_label(curie),
                                        predicate_id=rel[1],
                                        object_id=curie2,
                                        object_label=get_label(curie2),
                                        mapping_justification=SEMAPV.ManualMappingCuration.value,
                                        mapping_source="obo:" + name,
                                    )
        logging.info(f"Visited {len(visited)} nodes")
        logging.info(f"Yielded {len(mappings)} mappings")
        logging.info(f"Max distance traversed: {max_dist_traversed}")
