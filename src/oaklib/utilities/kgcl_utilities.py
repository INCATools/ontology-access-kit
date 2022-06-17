import uuid

from oaklib.types import CURIE


def generate_change_id() -> CURIE:
    """
    Generates an identifier to be used on a change object
    :return:
    """
    return f"uuid:{uuid.uuid4()}"
