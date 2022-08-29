import csv
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.datamodels.vocabulary import HAS_DBXREF, HAS_DEFINITION_CURIE, IS_A, PART_OF
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.io.streaming_writer import ID_KEY, LABEL_KEY, StreamingWriter
from oaklib.types import CURIE


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    # if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingCsvWriter(StreamingWriter):
    """
    A writer that streams CSV/TSV output
    """

    header_emitted: bool = None
    delimiter: str = "\t"
    writer: csv.DictWriter = None
    keys: List[str] = None

    def emit(self, obj: Union[YAMLRoot, Dict, CURIE], label_fields=None):
        if isinstance(obj, dict):
            obj_as_dict = obj
        elif isinstance(obj, CURIE):
            obj_as_dict = self._get_dict(obj)
        else:
            obj_as_dict = vars(obj)
        self.add_labels(obj_as_dict, label_fields)
        if self.writer is None:
            # TODO: option to delay writing header, as not all keys may be populated in advance
            self.keys = list(obj_as_dict)
            self.writer = csv.DictWriter(self.file, delimiter=self.delimiter, fieldnames=self.keys)
            self.writer.writeheader()
        self.writer.writerow({k: _keyval(v) for k, v in obj_as_dict.items() if k in self.keys})

    def _get_dict(self, curie: CURIE):
        oi = self.ontology_interface
        d = dict(
            id=curie,
            label=oi.label(curie),
            definition=oi.definition(curie),
        )
        for k, vs in oi.entity_alias_map(curie).items():
            d[k] = "|".join(vs)
        for _, x in oi.simple_mappings_by_curie(curie):
            d["mappings"] = x
        for k, vs in oi.entity_metadata_map(curie).items():
            if k not in [HAS_DBXREF, HAS_DEFINITION_CURIE]:
                d[k] = str(vs)
        if isinstance(oi, OboGraphInterface):
            for k, vs in oi.outgoing_relationship_map(curie).items():
                d[k] = "|".join(vs)
                d[f"{k}_label"] = "|".join([str(oi.label(v)) for v in vs])
        if isinstance(oi, SemanticSimilarityInterface):
            d["information_content_via_is_a"] = oi.get_information_content(curie, predicates=[IS_A])
            d["information_content_via_is_a_part_of"] = oi.get_information_content(
                curie, predicates=[IS_A, PART_OF]
            )

        return d

    def emit_curie(self, curie: CURIE, label=None):
        self.emit({ID_KEY: curie, LABEL_KEY: label})
