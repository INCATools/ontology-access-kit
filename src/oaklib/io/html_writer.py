from dataclasses import dataclass, field
from typing import List

from linkml_renderer.renderers.html_renderer import HTMLRenderer
from linkml_renderer.style.model import Configuration, RenderRule
from linkml_renderer.style.style_engine import StyleEngine
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class HTMLWriter(StreamingWriter):
    """
    A writer that streams objects as HTML
    """

    uses_schemaview = True
    cached_objects: List[YAMLRoot] = field(default_factory=lambda: [])
    render_rules: List[RenderRule] = None

    def emit_obj(self, obj: YAMLRoot, **kwargs):
        self.cached_objects.append(obj)

    def finish(self):
        renderer = HTMLRenderer()
        config = Configuration(rules=self.render_rules)
        se = StyleEngine(self.schemaview, configuration=config)
        renderer.style_engine = se
        for obj in self.cached_objects:
            self.file.write(renderer.render(obj, schemaview=self.schemaview))
