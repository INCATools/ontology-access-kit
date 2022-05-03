from dataclasses import dataclass, field
from typing import List, Iterator, Tuple, Iterable

from linkml_runtime.dumpers import yaml_dumper
from oaklib.io.streaming_writer import StreamingWriter
import sssom.sssom_datamodel as sssom_dm
from oaklib.types import CURIE
from sssom.sssom_document import MappingSetDocument
from sssom.util import to_mapping_set_dataframe
from sssom.writers import write_table


def mappings_to_pairs(mappings: Iterable[sssom_dm.Mapping]) -> List[Tuple[CURIE, CURIE]]:
    """
    Convert a list of mappings to subject-object pairs

    :param mappings:
    :return:
    """
    return [(m.subject_id, m.object_id) for m in mappings]



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
