import yaml

from oaklib import get_adapter
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.utilities.subsets.subset_validator import SubsetValidationConfig, validate_subset
from tests import EXAMPLE_ONTOLOGY_DB, INPUT_DIR


def test_validate_subset():
    adapter: SemanticSimilarityInterface = get_adapter(EXAMPLE_ONTOLOGY_DB)
    adapter.load_information_content_scores(str(INPUT_DIR / "go-nucleus-ic.tsv"))
    for subset in adapter.subsets():
        print(f"## Subset: {subset}")
        conf = SubsetValidationConfig(subset_name=subset)
        result = validate_subset(adapter, conf)
        print(yaml.dump(result.model_dump(exclude_unset=True), sort_keys=False))
