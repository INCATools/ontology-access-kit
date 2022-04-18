from dataclasses import dataclass, field
from typing import List

from linkml_runtime.dumpers import yaml_dumper
from oaklib.io.streaming_writer import StreamingWriter
import sssom.sssom_datamodel as sssom_dm
from sssom.sssom_document import MappingSetDocument
from sssom.util import to_mapping_set_dataframe
from sssom.writers import write_table


@dataclass
class StreamingSssomWriter(StreamingWriter):
    """
    pseudo-streaming writer for SSSOM
    """
    mappings : List[sssom_dm.Mapping] = field(default_factory=lambda: [])

    def emit(self, obj: sssom_dm.Mapping):
        self.mappings.append(obj)

    def close(self):
        mset = sssom_dm.MappingSet(mapping_set_id='temp',
                                   mappings=self.mappings,
                                   license='UNSPECIFIED')
        doc = MappingSetDocument(prefix_map={}, mapping_set=mset)
        msdf = to_mapping_set_dataframe(doc)
        write_table(msdf, self.file)
