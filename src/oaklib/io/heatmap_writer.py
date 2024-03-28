from dataclasses import dataclass, field
from typing import Dict, List, Union

from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.datamodels.association import PairwiseCoAssociation
from oaklib.datamodels.similarity import TermPairwiseSimilarity
from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class HeatmapWriter(StreamingWriter):
    """
    A writer that generates heatmap images

    The general approach:

    1. create a data frame with two axis columns and one value column
    2. pivot to a 2D array
    3. use seaborn to generate

    Note that this needs seaborn to be installed

    Currently the only supported data models are:

    - TermPairwiseSimilarity
    """

    items: List[Dict] = field(default_factory=lambda: [])
    value_field: str = field(default_factory=lambda: "phenodigm_score")

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        if isinstance(obj, TermPairwiseSimilarity):
            t1 = obj.subject_id + f" {obj.subject_label}" if obj.subject_label else ""
            t2 = obj.object_id + f" {obj.object_label}" if obj.object_label else ""
            v = getattr(obj, self.value_field)
            self.items.append({"term1": t1, "term2": t2, "score": v})
        if isinstance(obj, PairwiseCoAssociation):
            if label_fields and self.autolabel:
                t1 = f"{obj.object1} {self.ontology_interface.label(obj.object1)}"
                t2 = f"{obj.object2} {self.ontology_interface.label(obj.object2)}"
            else:
                t1 = obj.object1
                t2 = obj.object2
            v = obj.proportion_subjects_in_common
            self.items.append({"term1": t1, "term2": t2, "score": v})
        else:
            raise ValueError(f"Cannot handle: {obj}")

    def finish(self):
        import pandas
        import seaborn

        df = pandas.DataFrame(self.items)
        df = df.pivot(index="term1", columns="term2", values="score")
        ax = seaborn.heatmap(df, annot=True, fmt=".2f")
        ax.get_figure().savefig(self.output, bbox_inches="tight")
