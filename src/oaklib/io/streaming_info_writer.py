import csv
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Union, Tuple

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.obograph_utils import DEFAULT_PREDICATE_CODE_MAP

predicate_code_map = DEFAULT_PREDICATE_CODE_MAP

def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    #if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingInfoWriter(StreamingWriter):
    """
    A writer that streams basic line by line reporting info
    """

    def emit(self, curie, label=None, **kwargs):
        oi = self.ontology_interface
        if label is None:
            label = oi.get_label_by_curie(curie)
        self.file.write(f'{curie} ! {label}')
        if self.display_options:
            show_all = 'all' in self.display_options
            if show_all or 'x' in self.display_options:
                for _, x in oi.get_simple_mappings_by_curie(curie):
                    self.file.write(f' {x}')
            if show_all or 'r' in self.display_options and isinstance(oi, OboGraphInterface):
                for k, vs in oi.get_outgoing_relationships_by_curie(curie).items():
                    p = predicate_code_map.get(k, None)
                    if p is None:
                        p = oi.get_label_by_curie(k)
                        if p is None:
                            p = k
                    self.file.write(f' {p}: [')
                    for v in vs:
                        self.file.write(f' {v} "{oi.get_label_by_curie(curie)}"')
                    self.file.write(f']')
            if show_all or 'd' in self.display_options:
                defn = oi.get_definition_by_curie(curie)
                if defn:
                    self.file.write(f' "{defn}"')


        self.file.write('\n')


