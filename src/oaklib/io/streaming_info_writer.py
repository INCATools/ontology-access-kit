from dataclasses import dataclass
from typing import Any

from linkml_runtime import CurieNamespace

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.obograph_utils import DEFAULT_PREDICATE_CODE_MAP

predicate_code_map = DEFAULT_PREDICATE_CODE_MAP


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    # if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingInfoWriter(StreamingWriter):
    """
    A writer that streams basic line by line reporting info
    """

    def emit_curie(self, curie, label=None, **kwargs):
        oi = self.ontology_interface
        if label is None:
            label = oi.label(curie)
        self.file.write(f"{curie} ! {label}")
        if self.display_options:
            show_all = "all" in self.display_options
            if show_all or "x" in self.display_options:
                for _, x in oi.simple_mappings_by_curie(curie):
                    self.file.write(f" {x}")
            if show_all or "r" in self.display_options and isinstance(oi, OboGraphInterface):
                for k, vs in oi.outgoing_relationship_map(curie).items():
                    p = predicate_code_map.get(k, None)
                    if p is None:
                        p = oi.label(k)
                        if p is None:
                            p = k
                    self.file.write(f" {p}: [")
                    for v in vs:
                        self.file.write(f' {v} "{oi.label(curie)}"')
                    self.file.write("]")
            if show_all or "d" in self.display_options:
                defn = oi.definition(curie)
                if defn:
                    self.file.write(f' "{defn}"')
            if show_all or "db" in self.display_options:
                self.file.write(f" isDefinedBy: {oi.defined_by(curie)}")
            if "ic" in self.display_options and (
                show_all and isinstance(oi, SemanticSimilarityInterface)
            ):
                ic = oi.get_information_content(curie)
                self.file.write(f" IC: {ic}")

        self.file.write("\n")
