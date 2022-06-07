import csv
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Union, Tuple

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.obograph_utils import DEFAULT_PREDICATE_CODE_MAP
from oaklib.utilities.taxon.taxon_constraint_utils import get_term_with_taxon_constraints

predicate_code_map = DEFAULT_PREDICATE_CODE_MAP

def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    #if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingMarkdownWriter(StreamingWriter):
    """
    A writer that streams curies as markdown
    """


    def emit(self, curie, label=None, **kwargs):
        oi = self.ontology_interface
        if label is None:
            label = oi.get_label_by_curie(curie)
        self.file.write(f'## {curie} {label}\n\n')
        defn = oi.get_definition_by_curie(curie)
        if defn:
            self.file.write(f'_{defn}_\n\n')
        self.file.write(f'### Xrefs\n\n')

        for _, x in oi.get_simple_mappings_by_curie(curie):
            self.file.write(f' * {x}\n')
        self.file.write('\n')
        if isinstance(oi, OboGraphInterface):
            self.file.write(f'### Relationships\n\n')
            for k, vs in oi.get_outgoing_relationships_by_curie(curie).items():
                p = predicate_code_map.get(k, None)
                if p is None:
                    p = oi.get_label_by_curie(k)
                    if p is None:
                        p = k
                self.file.write(f'* {p}\n')
                for v in vs:
                    self.file.write(f'    * {v} "{oi.get_label_by_curie(curie)}"\n')
        if 't' in self.display_options and isinstance(oi, OboGraphInterface):
            self.file.write(f'### Taxon Constraints\n\n')
            tc_subj = get_term_with_taxon_constraints(oi, curie)
            for tc in tc_subj.never_in:
                self.file.write(f'* {tc}\n')






        self.file.write('\n')


