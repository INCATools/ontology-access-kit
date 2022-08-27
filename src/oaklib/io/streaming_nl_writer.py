from dataclasses import dataclass

from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.datamodels import obograph
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.nlp.natual_language_generation import NaturalLanguageGenerator


@dataclass
class StreamingNaturalLanguageWriter(StreamingWriter):
    """
    A writer that streams basic line by line reporting info
    """

    natural_language_generator: NaturalLanguageGenerator = None

    def emit_curie(self, curie, label=None, **kwargs):
        self._ensure_init()
        self.file.write(self.natural_language_generator.render_entity(curie))
        self.file.write("\n")

    def emit_obj(self, obj: YAMLRoot):
        self._ensure_init()
        if isinstance(obj, obograph.LogicalDefinitionAxiom):
            self.file.write(self.natural_language_generator.render_logical_definition(obj))
            self.file.write("\n")
        else:
            raise NotImplementedError

    def _ensure_init(self):
        if self.natural_language_generator is None:
            self.natural_language_generator = NaturalLanguageGenerator(self.ontology_interface)
