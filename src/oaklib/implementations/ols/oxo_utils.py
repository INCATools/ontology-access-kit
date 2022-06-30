from typing import Any

from linkml_runtime.loaders import json_loader

import oaklib.datamodels.oxo as oxo


def fix_json_payload(obj: Any) -> None:
    """
    changes payload in place

    - self --> link_to_self

    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        for _, v in obj.items():
            fix_json_payload(v)
        if "self" in obj:
            obj["link_to_self"] = obj["self"]
            del obj["self"]
    elif isinstance(obj, list):
        [fix_json_payload(v) for v in obj]
    else:
        pass


def load_oxo_payload(obj: Any) -> oxo.Container:
    fix_json_payload(obj)
    return json_loader.loads(obj, target_class=oxo.Container)
