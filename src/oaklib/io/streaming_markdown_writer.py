from dataclasses import dataclass
from typing import Any, Dict, Union

from linkml_runtime import CurieNamespace

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.taxon_constraint_interface import TaxonConstraintInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.utilities.obograph_utils import DEFAULT_PREDICATE_CODE_MAP
from oaklib.utilities.writers.change_handler import ChangeHandler

predicate_code_map = DEFAULT_PREDICATE_CODE_MAP


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    # if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingMarkdownWriter(StreamingWriter):
    """
    A writer that streams curies or changes as markdown
    """

    # TODO: replace with linkml-renderer

    def emit(self, curie_or_change: Union[str, Dict], label=None, **kwargs):
        oi = self.ontology_interface
        other_oi = kwargs.get("other_impl", None)
        if isinstance(curie_or_change, dict):
            # TODO: have a more robust way to determine if this is a change
            change_handler = ChangeHandler(file=self.file, oi=other_oi)
            change_handler.process_changes(curie_or_change)
            return
        if label is None:
            label = oi.label(curie_or_change)
        self.file.write(f"## {curie_or_change} {label}\n\n")
        defn = oi.definition(curie_or_change)
        if defn:
            self.file.write(f"_{defn}_\n\n")
        self.file.write("### Xrefs\n\n")

        for _, x in oi.simple_mappings_by_curie(curie_or_change):
            self.file.write(f" * {x}\n")
        self.file.write("\n")
        if isinstance(oi, OboGraphInterface):
            self.file.write("### Relationships\n\n")
            for k, vs in oi.outgoing_relationship_map(curie_or_change).items():
                p = predicate_code_map.get(k, None)
                if p is None:
                    p = oi.label(k)
                    if p is None:
                        p = k
                self.file.write(f"* {p}\n")
                for v in vs:
                    self.file.write(f'    * {v} "{oi.label(curie_or_change)}"\n')
        if (
            self.display_options
            and "t" in self.display_options
            and isinstance(oi, TaxonConstraintInterface)
        ):
            self.file.write("### Taxon Constraints\n\n")
            tc_subj = oi.get_term_with_taxon_constraints(curie_or_change)
            for tc in tc_subj.never_in:
                self.file.write(f"* {tc}\n")

        self.file.write("\n")
