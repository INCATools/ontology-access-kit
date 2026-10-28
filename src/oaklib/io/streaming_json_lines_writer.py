import json
from dataclasses import dataclass
from typing import Type, Union

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class StreamingJsonLinesWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        if isinstance(obj, dict):
            self.emit_dict(obj)
        else:
            self.emit_dict(json_dumper.to_dict(obj))

    def emit_dict(self, obj: dict, object_type: Type = None):
        self.file.write(json.dumps(obj, ensure_ascii=False) + "\n")
