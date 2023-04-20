import logging
from dataclasses import dataclass, field
from typing import List, Optional, Union

from linkml_renderer.renderers.html_renderer import HTMLRenderer
from linkml_renderer.style.model import Configuration, RenderRule
from linkml_renderer.style.style_engine import StyleEngine
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class HTMLWriter(StreamingWriter):
    """
    A writer that streams objects as HTML
    """

    uses_schemaview = True
    cached_objects: List[YAMLRoot] = field(default_factory=lambda: [])
    render_rules: List[RenderRule] = field(default_factory=lambda: [])

    def emit(self, obj: Union[YAMLRoot, dict, CURIE], label_fields: Optional[List[str]] = None):
        """
        Emit an object or CURIE

        :param obj:
        :param label_fields:
        :return:
        """
        if isinstance(obj, CURIE):
            self.emit_curie(obj)
        elif isinstance(obj, dict):
            self.emit_obj(obj)
        elif isinstance(obj, YAMLRoot):
            self.emit_obj(obj)

    def emit_obj(self, obj: YAMLRoot, **kwargs):
        logging.debug(f"Emitting obj {type(obj)}")
        self.cached_objects.append(obj)

    def finish(self):
        renderer = HTMLRenderer()
        config = Configuration(rules=self.render_rules)
        if not self.schemaview:
            raise ValueError("HTMLWriter requires a schemaview")
        se = StyleEngine(self.schemaview, configuration=config)
        renderer.style_engine = se
        for obj in self.cached_objects:
            self.file.write(renderer.render(obj, schemaview=self.schemaview))
