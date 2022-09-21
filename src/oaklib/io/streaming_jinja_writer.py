from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

import pkg_resources
from linkml_runtime import CurieNamespace
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.obograph_utils import DEFAULT_PREDICATE_CODE_MAP
from jinja2 import Template, Environment, FileSystemLoader

predicate_code_map = DEFAULT_PREDICATE_CODE_MAP


@dataclass
class StreamingJinjaWriter(StreamingWriter):
    """
    A writer that streams entries to a Jinja2 template

    The main way this is used via the command line, passing a parameterized
    output object:

        runoak -i sqlite:obo:cl info .all -O jinja//template_path=test.j2

    This will pass through all CL terms to a template, which might look something
    like this:

    .code ::

        ID: {{obj}}
        Name: {{oi.label(obj)}}

        Parents:
        {% for p,o in oi.outgoing_relationships(obj) %}
         - {{p}} {{o}} {{oi.label(o)}}
        {% endfor %}

    """
    template_folder: Union[Path, str] = None
    """Path to folder in which templates are stored. If omitted, this is inferred from template_path"""

    template_name: Union[Path, str] = None
    """Name of a template in the template folder. Do not specify if path is specified"""

    template_path: Union[Path, str] = None
    """Absolute path for a template. If this is specified, then do not specify name or folder"""

    template: Template = None
    """Jinja2 template object. This is instantiated from path/name"""

    def _template(self) -> Template:
        if self.template is None:
            if self.template_path and not self.template_folder:
                p = Path(self.template_path)
                self.template_folder = p.parent
                self.template_name = p.name
            if self.template_folder is None:
                self.template_folder = pkg_resources.resource_filename(__name__, "jinja2_templates")
            loader = FileSystemLoader(self.template_folder)
            env = Environment(loader=loader)
            if "." not in self.template_name:
                self.template_name = f"{self.template_name}.j2"
            self.template = env.get_template(self.template_name)
        return self.template

    def emit_curie(self, curie, label=None, **kwargs):
        oi = self.ontology_interface
        if label is None:
            label = oi.label(curie)
        v = self._template().render(curie=curie, label=label, interface=oi)
        self.file.write(v)

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        oi = self.ontology_interface
        v = self._template().render(obj=obj, oi=oi)
        self.file.write(v)
