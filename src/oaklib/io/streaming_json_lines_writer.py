from dataclasses import dataclass
from typing import Type, Union

import jsonlines
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class StreamingJsonLinesWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        with jsonlines.Writer(self.file) as writer:
            if isinstance(obj, dict):
                writer.write(obj)
            else:
                writer.write(json_dumper.dumps(obj))

    def emit_dict(self, obj: dict, object_type: Type = None):
        with jsonlines.Writer(self.file) as writer:
            writer.write(obj)
