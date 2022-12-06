import base64

from oaklib.types import CURIE


def string_as_base64_curie(input: str) -> CURIE:
    """
    Convert a string to a CURIE based on its base64 encoding

    :param input:
    :return:
    """
    return f"base64:{base64.b64encode(input.encode()).decode()}"


def synonym_type_code_from_curie(curie: CURIE) -> str:
    """
    Get the synonym type code from a CURIE

    In many OBO ontologies, the synonym type is encoded as a hash URI, which compacts
    to a curie of form

    - obo:chebi#BRAND_NAME
    - obo:hp#layperson

    In these cases, the code is the part after the hash

    See:

    - https://github.com/information-artifact-ontology/ontology-metadata/issues/122
    - https://github.com/INCATools/ontology-access-kit/issues/385

    :param curie: represents synonym type
    :return: code for the synonym type, or if cannot be determined, the input curie
    """
    if "#" in curie:
        return curie.split("#")[-1]
    else:
        return curie
