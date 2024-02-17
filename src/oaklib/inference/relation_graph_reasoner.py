"""A reasoner that computes entailed edges."""

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, TextIO

from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import (
    DISJOINT_WITH,
    EQUIVALENT_CLASS,
    INVERSE_OF,
    IS_A,
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    OWL_ON_PROPERTY,
    OWL_PROPERTY_CHAIN_AXIOM,
    OWL_RESTRICTION,
    OWL_SOME_VALUES_FROM,
    OWL_TRANSITIVE_PROPERTY,
    RDF_TYPE,
    RDFS_DOMAIN,
    RDFS_RANGE,
    SUBPROPERTY_OF,
)
from oaklib.inference.reasoner import Reasoner
from oaklib.interfaces.owl_interface import OwlInterface
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)

COMMAND = "relation-graph"


@dataclass
class RelationGraphReasoner(Reasoner):
    """
    A reasoner that computes entailed edges.

    The default implementation uses the relation-graph command line tool,
    which must be installed
    """

    ontology_adapter: BasicOntologyInterface
    """The ontology to reason over"""

    path_to_relation_graph: Optional[str] = None
    """If None, the command must be in the PATH"""

    validation_mode: bool = False
    """If True, then validation axioms (e.g domain, range) will be included"""

    _all_predicates: Optional[List[PRED_CURIE]] = None

    _bnode_counter: int = field(default_factory=int)

    _io: Optional[TextIO] = None

    _delete_tempfile: bool = True

    def entailed_edges(self):
        """
        Computes the entailed edges of the ontology.

        :return:
        """
        self._prepare_input()
        full_io = NamedTemporaryFile("w+", encoding="utf-8", delete=False)
        output_file = NamedTemporaryFile("w+", encoding="utf-8", delete=False)
        self._io.seek(0)
        self._insert_prefixes(full_io)
        full_io.write(self._io.read())
        full_io.flush()
        full_io.close()
        cmd = [
            COMMAND,
            "--ontology-file",
            full_io.name,
            "--output-subclasses",
            "true",
            "--output-individuals",
            "true",
            "--mode",
            "tsv",
            "--verbose",
            "true",
            "--output-file",
            output_file.name,
        ]
        logger.info(f"Running command: {' '.join(cmd)}")
        # output_file.close()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.returncode
        logger.info(f"Exit code: {exit_code}")
        logger.info(f"stdout: {str(stdout)}")
        if "LINE:" in str(stdout):
            # TODO: fix relation-graph to fail on parse error
            raise RuntimeError(f"Likely parse err: {str(stdout)}")
        if stderr:
            raise RuntimeError(stderr)
        n = 0
        for line in output_file.readlines():
            s, p, o = line.strip().split("\t")
            yield s, p, o
            n += 1
        if exit_code != 0:
            raise RuntimeError(f"Command failed with exit code {exit_code} // {stdout} // {stderr}")
        logger.info(f"Found {n} entailed edges")
        if self._delete_tempfile:
            Path(output_file.name).unlink()
            Path(full_io.name).unlink()

    def _path_to_executable(self) -> str:
        if self.path_to_relation_graph is None:
            return COMMAND
        return str(self.path_to_relation_graph / COMMAND)

    def is_available(self) -> bool:
        """
        Checks if the reasoner is available on the system.

        :return: True if available, False otherwise
        """
        try:
            subprocess.check_call([self._path_to_executable(), "--version"])
            return True
        except FileNotFoundError:
            return False

    def _insert_prefixes(self, io: TextIO):
        for prefix, expansion in self.ontology_adapter.prefix_map().items():
            io.write(f"@prefix {prefix}: <{expansion}> .\n")

    def _prepare_input(self):
        adapter = self.ontology_adapter
        self._all_predicates = list(adapter.entities(owl_type=OWL_OBJECT_PROPERTY))
        self._io = NamedTemporaryFile("w+", encoding="utf-8")
        # declarations
        for p in self._all_predicates:
            self._emit(p, RDF_TYPE, OWL_OBJECT_PROPERTY)
        for c in adapter.entities(owl_type=OWL_CLASS):
            self._emit(c, RDF_TYPE, OWL_CLASS)
        n = 0
        for rel in adapter.relationships(include_entailed=False):
            self._emit(*rel)
            n += 1
        if isinstance(adapter, OwlInterface):
            for p in adapter.transitive_object_properties():
                self._emit(p, RDF_TYPE, OWL_TRANSITIVE_PROPERTY)
            for p, chain in adapter.simple_subproperty_of_chains():
                rdf_list = self._emit_rdf_list(chain)
                self._emit(p, OWL_PROPERTY_CHAIN_AXIOM, rdf_list)
        else:
            raise NotImplementedError(f"adapter of type {type(adapter)} not supported")
        self._io.flush()
        logger.info(f"Emitted {n} relationships")

    def _emit(self, subject: CURIE, predicate: PRED_CURIE, object: CURIE):
        if predicate in [
            IS_A,
            EQUIVALENT_CLASS,
            RDF_TYPE,
            OWL_PROPERTY_CHAIN_AXIOM,
            SUBPROPERTY_OF,
            INVERSE_OF,
        ]:
            self._emit_triple(subject, predicate, object)
        elif predicate in self._all_predicates:
            bnode = self._get_bnode()
            self._emit_triple(subject, IS_A, bnode)
            self._emit_triple(bnode, RDF_TYPE, OWL_RESTRICTION)
            self._emit_triple(bnode, OWL_ON_PROPERTY, predicate)
            self._emit_triple(bnode, OWL_SOME_VALUES_FROM, object)
        elif predicate in [RDFS_RANGE, RDFS_DOMAIN, DISJOINT_WITH]:
            if self.validation_mode:
                self._emit_triple(subject, predicate, object)
            else:
                logger.debug(f"Skipping {predicate} {object} for {subject} in validation mode")
        else:
            raise NotImplementedError(f"predicate {predicate} not supported")

    def _get_bnode(self):
        self._bnode_counter += 1
        return f"_:bnode{self._bnode_counter}"

    def _emit_rdf_list(self, items: List[CURIE]):
        bnode = self._get_bnode()
        self._emit_triple(bnode, RDF_TYPE, "rdf:List")
        self._emit_triple(bnode, "rdf:first", items[0])
        if len(items) > 1:
            self._emit_triple(bnode, "rdf:rest", self._emit_rdf_list(items[1:]))
        else:
            self._emit_triple(bnode, "rdf:rest", "rdf:nil")
        return bnode

    def _emit_triple(self, subject: CURIE, predicate: PRED_CURIE, object: CURIE):
        self._emit_line(f"{subject} {predicate} {object} .")

    def _emit_line(self, line: str):
        self._io.write(line)
        self._io.write("\n")
