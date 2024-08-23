from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

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
    value_field: Optional[str] = None

    def emit(self, obj: Union[YAMLRoot, dict], label_fields=None):
        if isinstance(obj, TermPairwiseSimilarity):
            t1 = obj.subject_id + f" {obj.subject_label}" if obj.subject_label else ""
            t2 = obj.object_id + f" {obj.object_label}" if obj.object_label else ""
            value_field = self.value_field or "phenodigm_score"
            v = getattr(obj, value_field)
            self.items.append({"term1": t1, "term2": t2, "score": v})
        if isinstance(obj, PairwiseCoAssociation):
            if label_fields and self.autolabel:
                t1 = f"{obj.object1} {self.ontology_interface.label(obj.object1)}"
                t2 = f"{obj.object2} {self.ontology_interface.label(obj.object2)}"
            else:
                t1 = obj.object1
                t2 = obj.object2
            value_field = self.value_field or "proportion_subjects_in_common"
            v = getattr(obj, value_field)
            self.items.append({"term1": t1, "term2": t2, "score": v})
        else:
            raise ValueError(f"Cannot handle: {obj}")

    def finish(self):
        import matplotlib.pyplot as plt
        import pandas
        import seaborn as sns

        df = pandas.DataFrame(self.items)
        df = df.pivot(index="term1", columns="term2", values="score")
        # mask = df != 0
        plt.figure(figsize=(24, 20))  # Adjust the dimensions as needed
        value_field = self.value_field or "proportion_subjects_in_common"
        plt.title(f"Heatmap of {value_field}")
        # ax = sns.heatmap(df, annot=mask, fmt=".2f", mask=~mask)  # Annotates only non-zero cells
        ax = sns.heatmap(df, annot=True, fmt=".2f")
        # Rotate x and y labels if necessary
        plt.xticks(rotation=45, ha="right")  # Rotate term2 labels for better fit
        plt.yticks(rotation=0)  # Keep term1 labels horizontal
        # Adjust font size of the labels
        ax.tick_params(axis="both", which="major", labelsize=24)

        # Manually set x-axis labels to ensure correct alignment
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")

        ax.get_figure().savefig(self.output, bbox_inches="tight")
        # plt.savefig(self.output, bbox_inches="tight")
