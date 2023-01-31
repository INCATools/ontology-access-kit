"""Parser for Boomer output"""
import hashlib
import logging
import math
import re
from dataclasses import dataclass, field
from typing import Iterator, Optional, TextIO

from curies import Converter

from oaklib.datamodels.mapping_cluster_datamodel import MappingCluster, SimpleMapping
from oaklib.datamodels.vocabulary import (
    SKOS_BROAD_MATCH,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
    SKOS_NARROW_MATCH,
)
from oaklib.parsers.parser_base import Parser

re_new_block = re.compile(r"^## (.*)")
re_tag_val = re.compile(r"^(\S+): (.*)")
re_mapping1 = re.compile(r"^- (\[\S+)\s+(\w+)\s+(\S+\))\s+\(most probable\)\s+(\S+)$")
re_mapping2 = re.compile(r"^- (\[\S+)\s+(\w+)\s+(\S+\))\s+(\S+)$")
re_md_link = re.compile(r"^\[(.*)\]\((\S+)\)")

BOOMER_TO_SKOS = {
    "SiblingOf": SKOS_CLOSE_MATCH,
    "EquivalentTo": SKOS_EXACT_MATCH,
    "ProperSubClassOf": SKOS_BROAD_MATCH,
    "ProperSuperClassOf": SKOS_NARROW_MATCH,
}


@dataclass
class BoomerParser(Parser):

    curie_converter: Converter = None

    def parse(self, file: TextIO) -> Iterator[MappingCluster]:
        cluster: Optional[MappingCluster] = None
        for line in file:
            line = line.strip()
            m = re_new_block.match(line)
            if m:
                if cluster:
                    yield cluster
                name = m.group(1)
                cluster_id = self._cluster_id(name)
                # id will be overridden if report is newer
                cluster = MappingCluster(cluster_id, name=name)
                continue
            m = re_tag_val.match(line)
            if m:
                logging.debug(m.groups())
                tag, val = m.groups()
                if tag == "Method":
                    cluster.method = val
                elif tag == "Score":
                    cluster.log_prior_probability = float(val)
                elif tag == "Identifier":
                    cluster.id = val
                elif tag == "Estimated probability":
                    cluster.posterior_probability = float(val)
                elif tag == "Confidence":
                    cluster.confidence = float(val)
                continue
            m = re_mapping1.match(line)
            if not m:
                m = re_mapping2.match(line)
            if m:
                toks = m.groups()
                subject_id, subject_label = self._parse_md_link(toks[0])
                predicate = BOOMER_TO_SKOS[toks[1]]
                object_id, object_label = self._parse_md_link(toks[2])
                prob = float(toks[-1])
                mapping = SimpleMapping(
                    cluster_id=cluster.id,
                    subject_id=subject_id,
                    subject_label=subject_label,
                    predicate_id=predicate,
                    object_id=object_id,
                    object_label=object_label,
                    prior_probability=prob,
                    confidence=cluster.confidence,
                    posterior_probability=cluster.posterior_probability,
                )
                cluster.resolved_mappings.append(mapping)
                continue
        if not cluster:
            logging.warning("No clusters in file")
            return
        yield cluster

    def _parse_md_link(self, link: str):
        m = re_md_link.match(link)
        if not m:
            raise ValueError(f"Cannot parse link {link}")
        name, uri = m.group(1), m.group(2)
        if self.curie_converter:
            id = self.curie_converter.compress(uri)
        else:
            id = uri
        return id, name

    def _cluster_id(self, name: str) -> str:
        # doesn't work... wait for https://github.com/INCATools/boomer/pull/332
        name = name.replace(") [", ")[")
        m = hashlib.sha256(name.encode("utf-8"))
        return m.hexdigest()
