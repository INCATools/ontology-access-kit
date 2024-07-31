import contextlib
import tempfile

from linkml.generators import PythonGenerator
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from src.oaklib.utilities.subsets.value_set_expander import ValueSetExpander

SCHEMA_STRING = """
name: label_id_schema
id: http://example.com/label_id_schema
imports:
  - linkml:types
prefixes:
  label_id_schema: http://example.com/label_id_schema/
  linkml: https://w3id.org/linkml/
  ENVO: http://purl.obolibrary.org/obo/ENVO_
default_prefix: label_id_schema
enums:
  TerrestrialBiomeEnum:
    minus:
      - reachable_from:
          source_ontology: obo:envo
          source_nodes:
            - ENVO:00002030
          relationship_types:
            - rdfs:subClassOf
          is_direct: false
    reachable_from:
      source_ontology: obo:envo
      source_nodes:
        - ENVO:00000428
      relationship_types:
        - rdfs:subClassOf
      is_direct: false
slots:
  name:
    range: string
  id:
    range: string
    required: true
  biome:
    range: TerrestrialBiomeEnum
classes:
  NamedThing:
    slots:
      - name
      - id
  Sample:
    is_a: NamedThing
    slots:
      - biome
"""

DATA_STRING = """
name: Sample-1
id: sample_1
biome: tundra biome [ENVO:01000180]
"""


def test_pv_syntax_expander():
    view = SchemaView(SCHEMA_STRING)

    with contextlib.ExitStack() as stack:
        temp_dynamic = stack.enter_context(tempfile.NamedTemporaryFile(mode="w+t", delete=False))
        temp_expanded = stack.enter_context(tempfile.NamedTemporaryFile(mode="w+t", delete=False))

        yaml_dumper.dump(view.schema, temp_dynamic.name)

        expander = ValueSetExpander()

        expander.expand_in_place(
            schema_path=temp_dynamic.name,
            pv_syntax="{label} [{id}]",
            output_path=temp_expanded.name,
        )

        expanded_view = SchemaView(temp_expanded.name)

        generator = PythonGenerator(expanded_view.schema)

        python_code = generator.serialize()

        module_name = "test_module"

        module = compile_python(python_code, module_name)

        Sample = module.Sample

        sample_1 = yaml_loader.loads(source=DATA_STRING, target_class=Sample)

        assert sample_1 is not None
