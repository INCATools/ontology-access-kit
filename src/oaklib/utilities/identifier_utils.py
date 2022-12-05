import base64

from oaklib.types import CURIE


def string_as_base64_curie(input: str) -> CURIE:
    """
    Convert a string to a CURIE based on its base64 encoding

    :param input:
    :return:
    """
    return f"base64:{base64.b64encode(input.encode()).decode()}"
