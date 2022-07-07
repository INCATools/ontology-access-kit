from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple

from linkml_runtime.utils.metamodelcore import URIorCURIE
from sssom.sssom_document import MappingSetDocument
from sssom.util import to_mapping_set_dataframe
from sssom.writers import write_table
from sssom_schema import Mapping, MappingSet

from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


def create_sssom_mapping(
    subject_id: CURIE, object_id: CURIE, strict=False, **kwargs
) -> Optional[Mapping]:
    """
    Wraps the initialization of an SSSOM Mapping

    if subject or object are not valid CURIEs then return None

    This is useful as some ontologies may include unusual strings as values for properties such as hasDbXref,
    this allows these to be ignored rather than throwing errors

    :param subject_id:
    :param object_id:
    :param strict:
    :param kwargs:
    :return:
    """
    if not URIorCURIE.is_valid(subject_id):
        if strict:
            raise ValueError(f"Subject {subject_id} is not a valid curie")
        return
    elif not URIorCURIE.is_valid(object_id):
        if strict:
            raise ValueError(f"Object {object_id} is not a valid curie")
        return
    else:
        return Mapping(subject_id=subject_id, object_id=object_id, **kwargs)


def mappings_to_pairs(mappings: Iterable[Mapping]) -> List[Tuple[CURIE, CURIE]]:
    """
    Convert a list of mappings to subject-object pairs

    :param mappings:
    :return:
    """
    return list(set([(m.subject_id, m.object_id) for m in mappings]))


@dataclass
class StreamingSssomWriter(StreamingWriter):
    """
    pseudo-streaming writer for SSSOM
    """

    mappings: List[Mapping] = field(default_factory=lambda: [])

    def emit(self, obj: Mapping):
        self.mappings.append(obj)

    def close(self):
        mset = MappingSet(mapping_set_id="temp", mappings=self.mappings, license="UNSPECIFIED")
        doc = MappingSetDocument(prefix_map={}, mapping_set=mset)
        msdf = to_mapping_set_dataframe(doc)
        write_table(msdf, self.file)
