from dataclasses import dataclass
from typing import Any

import pyhornedowl
import rdflib
from pyhornedowl.model import AnnotatedComponent

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class StreamingAxiomWriter(StreamingWriter):
    """
    A writer that emits one axiom at a time in one stream
    """

    syntax: Any = None
    functional_writer: Any = None

    def emit(self, obj: Any, label_fields=None):
        if self.syntax == "ofn" or self.syntax is None:
            self.file.write(str(obj))
            self.file.write("\n")
            return

        ontology = pyhornedowl.PyIndexedOntology()
        if isinstance(obj, AnnotatedComponent):
            ontology.add_axiom(obj.component, set(obj.ann))
        else:
            ontology.add_axiom(obj)

        if self.syntax in {"ttl", "turtle"}:
            rdfxml = ontology.save_to_string("owl")
            g = rdflib.Graph()
            g.parse(data=rdfxml, format="xml")
            rendered = g.serialize(format="ttl")
        elif self.syntax in {"owl", "owx"}:
            rendered = ontology.save_to_string(self.syntax)
        else:
            rendered = str(obj)
        self.file.write(str(rendered))
        if not str(rendered).endswith("\n"):
            self.file.write("\n")
