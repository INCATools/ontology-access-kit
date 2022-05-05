import csv
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Union, Tuple

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib.io.streaming_writer import StreamingWriter


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
            if 'x' in self.display_options:
                for _, x in oi.get_simple_mappings_by_curie(curie):
                    self.file.write(f' {x}')
            if 'd' in self.display_options:
                defn = oi.get_definition_by_curie(curie)
                if defn:
                    self.file.write(f' "{defn}"')
        self.file.write('\n')


