from dataclasses import dataclass
from typing import Any, Type, Union

import yaml
from linkml_runtime import CurieNamespace
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    # if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingYamlWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        if self.object_count:
            self.file.write("\n---\n")
        if isinstance(obj, YAMLRoot):
            obj_as_dict = json_dumper.to_dict(obj)
            # self.file.write(yaml_dumper.dumps(obj))
        elif isinstance(obj, dict):
            obj_as_dict = obj
        else:
            raise ValueError(f"Not a dict or YAMLRoot: {obj}")
        self.add_labels(obj_as_dict, label_fields)
        self.file.write(yaml.dump(obj_as_dict))
        self.object_count += 1

    def emit_dict(self, obj: dict, object_type: Type = None):
        self.file.write(yaml.dump(obj))
