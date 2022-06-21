from dataclasses import dataclass

from funowl import Axiom
from funowl.writers import FunctionalWriter

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class StreamingAxiomWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    syntax: str = None
    functional_writer: FunctionalWriter = None

    def emit(self, obj: Axiom):
        fw = self.functional_writer
        if self.syntax == "ttl":
            self.file.write(str(obj.to_rdf(fw.g)))
            self.file.write("\n")
        elif self.syntax == "ofn":
            self.file.write(str(obj.to_functional(fw)))
            self.file.write("\n")
        else:
            self.file.write(str(obj))
            self.file.write("\n")
