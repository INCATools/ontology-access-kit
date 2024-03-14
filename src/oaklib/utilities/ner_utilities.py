"""
Utilities used for annotation and lexmatch processes.
"""

from pathlib import Path
from typing import List, Union


def get_exclusion_token_list(exclude_tokens: Union[str, Path]) -> List[str]:
    """
    Return a list of token to be excluded from NER analysis.

    :param exclude_tokens: Either a file path or the strings to be excluded.
    :return: A list of tokens to exclude.
    """
    token_exclusion_list = []
    if len(exclude_tokens) == 1 and Path(exclude_tokens[0]).exists():
        with open(exclude_tokens[0]) as f:
            token_exclusion_list = f.read().splitlines()
    else:
        token_exclusion_list = list(exclude_tokens)

    return token_exclusion_list
